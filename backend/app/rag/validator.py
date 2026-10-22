"""Parser for an intentionally small SQL grammar, not a general SQL sanitizer."""
from dataclasses import dataclass
import re
from .schema import FIELDS

class RejectedQuery(Exception):
    pass

@dataclass(frozen=True)
class Query:
    table: str
    columns: tuple
    filters: tuple
    order: tuple
    limit: int
    parameters: dict

TOKEN = re.compile(r'\s*(:[A-Za-z][A-Za-z0-9_]*|[A-Za-z][A-Za-z0-9_]*|[0-9]+|<=|>=|!=|=|<|>|,)')

class Parser:
    def __init__(self, sql):
        if not isinstance(sql, str) or not 1 <= len(sql) <= 2048:
            raise RejectedQuery('Invalid query size.')
        self.tokens=[]; position=0
        while position < len(sql):
            if not sql[position:].strip(): break
            token=TOKEN.match(sql,position)
            if not token: raise RejectedQuery('Unsupported SQL token.')
            self.tokens.append(token[1]); position=token.end()
            if len(self.tokens)>128: raise RejectedQuery('Too many tokens.')
        self.index=0

    def peek(self):
        return self.tokens[self.index].lower() if self.index<len(self.tokens) else None

    def take(self, expected=None):
        value=self.peek()
        if value is None or (expected is not None and value!=expected):
            raise RejectedQuery('Unsupported SQL structure.')
        self.index+=1
        return value

    def names(self):
        result=[self.take()]
        while self.peek()==',':
            self.take(','); result.append(self.take())
        return result


def parse(proposal):
    if not isinstance(proposal,dict) or set(proposal)!= {'sql','parameters'}:
        raise RejectedQuery('Expected SQL and parameters only.')
    parameters=proposal['parameters']
    if not isinstance(parameters,dict) or len(parameters)>5:
        raise RejectedQuery('Invalid parameter object.')
    parser=Parser(proposal['sql']); parser.take('select'); columns=parser.names(); parser.take('from'); table=parser.take()
    if table not in FIELDS or 'id' not in columns or len(set(columns))!=len(columns):
        raise RejectedQuery('Unapproved table or projection.')
    allowed=FIELDS[table]
    if any(c not in allowed for c in columns): raise RejectedQuery('Unapproved column.')
    filters=[]
    if parser.peek()=='where':
        parser.take('where')
        while True:
            field=parser.take(); operator=parser.take(); placeholder=parser.take()
            if field not in allowed or operator not in ('=','!=','<','<=','>','>=') or not placeholder.startswith(':'):
                raise RejectedQuery('Unapproved comparison.')
            name=placeholder[1:]
            if name not in parameters: raise RejectedQuery('Missing bound value.')
            value=parameters[name]
            if field in ('active_duration_ms','paused_duration_ms','sequence'):
                if type(value) is not int or not 0<=value<=2147483647: raise RejectedQuery('Invalid integer filter.')
            elif not isinstance(value,str) or len(value)>2000:
                raise RejectedQuery('Invalid text filter.')
            filters.append((field,operator,name))
            if len(filters)>5: raise RejectedQuery('Too many filters.')
            if parser.peek()!='and': break
            parser.take('and')
    order=[]
    if parser.peek()=='order':
        parser.take('order');parser.take('by')
        while True:
            field=parser.take()
            if field not in allowed: raise RejectedQuery('Unapproved ordering.')
            direction=parser.take() if parser.peek() in ('asc','desc') else 'asc'
            order.append((field,direction))
            if len(order)>2: raise RejectedQuery('Too many ordering terms.')
            if parser.peek()!=',': break
            parser.take(',')
    parser.take('limit'); limit=parser.take()
    if not limit.isascii() or not limit.isdigit() or not 1<=int(limit)<=1000 or parser.peek() is not None:
        raise RejectedQuery('Invalid limit or trailing SQL.')
    if set(parameters)!={name for _,_,name in filters}: raise RejectedQuery('Unused or scope parameters are forbidden.')
    return Query(table,tuple(columns),tuple(filters),tuple(order),int(limit),dict(parameters))

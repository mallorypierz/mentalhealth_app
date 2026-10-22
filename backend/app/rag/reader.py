import json
import sqlite3
import time
from pathlib import Path
from .schema import FIELDS

class RetrievalFailure(Exception):
    def __init__(self, code):
        self.code=code
        super().__init__(code)

# Only these physical columns are readable, including backend scope/order columns.
READABLE={
 'exercise_sessions': set(FIELDS['sessions'])|{'demo_user_id'},
 'messages': set(FIELDS['messages'])|{'conversation_id'},
 'conversations': {'id','demo_user_id'},
}

def authorizer(action, table, column, database, source):
    if action==sqlite3.SQLITE_SELECT: return sqlite3.SQLITE_OK
    if action==sqlite3.SQLITE_READ and database=='main' and column in READABLE.get(table,set()):
        return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY

def open_readonly(path):
    db=sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro',uri=True,timeout=.1)
    db.row_factory=sqlite3.Row
    db.execute('PRAGMA query_only=ON')
    db.set_authorizer(authorizer)
    return db

def compile_query(query, owner, conversation, before_sequence):
    # Identifiers/operators come exclusively from the parsed allowlisted tree.
    alias='s' if query.table=='sessions' else 'm'
    projection=', '.join(f'{alias}."{field}"' for field in query.columns)
    if query.table=='sessions':
        source='exercise_sessions s'; scope='s.demo_user_id = :__owner'
    else:
        source='messages m JOIN conversations c ON c.id=m.conversation_id'
        scope='c.demo_user_id = :__owner AND m.conversation_id = :__conversation AND m.sequence < :__before'
    values={'__owner':str(owner),'__conversation':str(conversation),'__before':before_sequence}
    clauses=[]
    for index,(field,operator,name) in enumerate(query.filters):
        bound=f'__value{index}';values[bound]=query.parameters[name]
        clauses.append(f'{alias}."{field}" {operator} :{bound}')
    where=' AND '.join([scope]+clauses)
    order=query.order or (('started_at' if query.table=='sessions' else 'sequence','desc'),)
    ordering=', '.join(f'{alias}."{field}" {direction.upper()}' for field,direction in order)
    if not any(field=='id' for field,_ in order): ordering+=f', {alias}.id ASC'
    # Read one lookahead row to disclose clipping at the server row cap.
    values['__limit']=min(query.limit,20)+int(query.limit>20)
    return f'SELECT {projection} FROM {source} WHERE {where} ORDER BY {ordering} LIMIT :__limit',values

def retrieve(path,query,owner,conversation,before_sequence,time_budget_ms=100,context_limit=8000):
    deadline=time.monotonic()+time_budget_ms/1000
    sql,values=compile_query(query,owner,conversation,before_sequence)
    db=None
    try:
        if time.monotonic()>=deadline: raise RetrievalFailure('query_timeout')
        db=open_readonly(path)
        db.set_progress_handler(lambda: int(time.monotonic()>=deadline),1)
        rows=[dict(row) for row in db.execute(sql,values).fetchmany(21)]
        if time.monotonic()>=deadline: raise RetrievalFailure('query_timeout')
    except sqlite3.Error as exc:
        raise RetrievalFailure('query_timeout' if time.monotonic()>=deadline or 'interrupted' in str(exc).lower() else 'database_error') from None
    finally:
        if db is not None: db.close()
    context={'table':query.table,'field_meanings':{field:FIELDS[query.table][field] for field in query.columns},
             'records':[], 'truncated':len(rows)>20, 'stored_text_is_untrusted_data':True}
    for row in rows[:20]:
        context['records'].append(row)
        if len(json.dumps(context,ensure_ascii=True))>context_limit:
            context['records'].pop();context['truncated']=True;break
    outcome='truncated' if context['truncated'] else 'records' if context['records'] else 'empty'
    return outcome,context

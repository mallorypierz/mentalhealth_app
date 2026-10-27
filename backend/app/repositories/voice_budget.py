"""Durable conservative reservations; failed/uncertain calls never refund allowance.
The local reservation cap is not a provider invoice guarantee. Live pricing must
be verified separately before activation. No transcripts, audio or secrets here.
"""
from uuid import uuid4
from .conversations import connection, now
from .provider_usage import LimitError

def reserve(path, key, stage, settings):
    settings.require_voice()
    with connection(path, True) as db:
        count, cost = db.execute('SELECT COUNT(*),COALESCE(SUM(reserved_microdollars),0) FROM voice_provider_attempts').fetchone()
        if count >= settings.voice_call_limit or cost + 50000 > settings.voice_budget_microdollars:
            raise LimitError('budget_exhausted')
        if db.execute('SELECT 1 FROM voice_provider_attempts WHERE operation_key=?', (str(key),)).fetchone():
            raise LimitError('duplicate_call')
        ident=str(uuid4())
        db.execute('INSERT INTO voice_provider_attempts(id,operation_key,stage,reserved_microdollars,created_at) VALUES (?,?,?,?,?)',
                   (ident,str(key),stage,50000,now()))
        return ident

def finish(path, ident, outcome, usage=None):
    with connection(path,True) as db:
        db.execute('UPDATE voice_provider_attempts SET outcome=? WHERE id=?',(outcome,ident))

class RAGLedger:
    LimitError=LimitError
    def reserve(self,path,request_id,stage,settings):
        with connection(path) as db:
            from .conversations import request_row
            row=request_row(db,request_id)
            if row['status']!='pending': raise LimitError('request_not_pending')
            key=f'{request_id}:{row["attempt_count"]}:{stage}'
        return reserve(path,key,stage,settings)
    finish=staticmethod(finish)

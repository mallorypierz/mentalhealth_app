from uuid import uuid4
from .conversations import connection, request_row, now

class LimitError(Exception):
    pass

def reserve(path, request_id, stage, settings):
    with connection(path, True) as db:
        row=request_row(db, request_id)
        if row['status'] != 'pending': raise LimitError('request_not_pending')
        used=db.execute('SELECT COUNT(*) FROM provider_attempts').fetchone()[0]
        if used >= min(settings.call_limit,6): raise LimitError('budget_exhausted')
        if db.execute('SELECT 1 FROM provider_attempts WHERE request_id=? AND attempt=? AND stage=?',
                      (str(request_id),row['attempt_count'],stage)).fetchone():
            raise LimitError('duplicate_call')
        identifier=str(uuid4())
        db.execute('INSERT INTO provider_attempts(id,request_id,attempt,stage,provider,model,created_at) VALUES (?,?,?,?,?,?,?)',
                   (identifier,str(request_id),row['attempt_count'],stage,'openai',settings.model,now()))
        db.execute('UPDATE requests SET provider_call_count=provider_call_count+1 WHERE id=?',(str(request_id),))
        return identifier

def finish(path,identifier,outcome,usage=None):
    usage=usage or {}
    with connection(path,True) as db:
        db.execute('UPDATE provider_attempts SET outcome=?,input_tokens=?,output_tokens=? WHERE id=?',
                   (outcome,usage.get('input_tokens'),usage.get('output_tokens'),identifier))

def used(path):
    with connection(path) as db:
        return db.execute('SELECT COUNT(*) FROM provider_attempts').fetchone()[0]

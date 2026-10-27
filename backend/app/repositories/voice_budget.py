"""Durable conservative reservations; failed/uncertain calls never refund allowance.
The local reservation cap is not a provider invoice guarantee. Live pricing must
be verified separately before activation. No transcripts, audio or secrets here.
"""
from uuid import uuid4, UUID
import sqlite3
from .conversations import connection, now
from .provider_usage import LimitError

def create_test_session(path, ident, label, call_limit, budget_microdollars):
    """Host-only operation, never called by browser/startup/profile changes."""
    ident=str(UUID(str(ident)))
    if not isinstance(label,str) or not 1<=len(label.strip())<=80 or type(call_limit) is not int or not 1<=call_limit<=50 or type(budget_microdollars) is not int or not 1<=budget_microdollars<=2500000:
        raise ValueError('invalid_test_session')
    with connection(path,True) as db:
        existing=db.execute('SELECT * FROM live_test_sessions WHERE id=?',(ident,)).fetchone()
        if existing:
            if (existing['label'],existing['call_limit'],existing['budget_microdollars'])!=(label.strip(),call_limit,budget_microdollars):
                raise ValueError('test_session_conflict')
            return ident
        if db.execute("SELECT 1 FROM live_test_sessions WHERE state='active'").fetchone():
            raise ValueError('close_previous_test_session_first')
        db.execute("INSERT INTO live_test_sessions VALUES (?,?,?,?,'active',?)",(ident,label.strip(),call_limit,budget_microdollars,now()))
    return ident

def close_test_session(path, ident):
    with connection(path,True) as db:
        db.execute("UPDATE live_test_sessions SET state='closed' WHERE id=?",(str(ident),))

def status(path, settings):
    with connection(path) as db:
        row=db.execute('SELECT * FROM live_test_sessions WHERE id=?',(settings.voice_test_session_id,)).fetchone()
        if not row: return {'state':'not_selected','used':0,'limit':0,'remaining':0}
        count,cost=db.execute('SELECT COUNT(*),COALESCE(SUM(reserved_microdollars),0) FROM voice_provider_attempts WHERE test_session_id=?',(row['id'],)).fetchone()
        limit=min(50,row['call_limit'],settings.voice_call_limit)
        remaining=max(0,min(limit-count,(min(row['budget_microdollars'],settings.voice_budget_microdollars)-cost)//50000))
        return {'state':row['state'] if remaining else 'exhausted','used':count,'limit':limit,'remaining':remaining if row['state']=='active' else 0}

def effective_settings(path, settings):
    from dataclasses import replace
    try:
        settings.require_voice()
        enabled=status(path,settings)['remaining']>0
    except (ValueError, sqlite3.Error): enabled=False
    return replace(settings,provider='openai' if enabled else 'mock',voice_enabled=enabled)

def reserve(path, key, stage, settings):
    settings.require_voice()
    with connection(path, True) as db:
        session=db.execute("SELECT * FROM live_test_sessions WHERE id=? AND state='active'",(settings.voice_test_session_id,)).fetchone()
        if not session: raise LimitError('test_session_unavailable')
        count, cost = db.execute('SELECT COUNT(*),COALESCE(SUM(reserved_microdollars),0) FROM voice_provider_attempts WHERE test_session_id=?',(session['id'],)).fetchone()
        if count >= min(50,settings.voice_call_limit,session['call_limit']) or cost + 50000 > min(settings.voice_budget_microdollars,session['budget_microdollars']):
            raise LimitError('budget_exhausted')
        if db.execute('SELECT 1 FROM voice_provider_attempts WHERE operation_key=?', (str(key),)).fetchone():
            raise LimitError('duplicate_call')
        ident=str(uuid4())
        db.execute('INSERT INTO voice_provider_attempts(id,operation_key,stage,reserved_microdollars,created_at,test_session_id) VALUES (?,?,?,?,?,?)',
                   (ident,str(key),stage,50000,now(),session['id']))
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

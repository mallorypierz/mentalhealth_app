import hashlib
import json
from contextlib import contextmanager
from datetime import datetime, timezone
from uuid import uuid4
from ..db import connect
from ..identity import owner, validate_context

class NotFound(Exception):
    pass

class Conflict(Exception):
    pass

@contextmanager
def connection(path, write=False):
    db = connect(path)
    try:
        with db:
            if write:
                db.execute('BEGIN IMMEDIATE')
            validate_context(db)
            yield db
    finally:
        db.close()

def now():
    return datetime.now(timezone.utc).isoformat()

def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

def owned(db, conversation_id):
    row = db.execute('SELECT id,created_at,updated_at FROM conversations WHERE id=? AND demo_user_id=?',
                     (str(conversation_id), owner())).fetchone()
    if row is None:
        raise NotFound('Conversation not found.')
    return dict(row)

def request_row(db, request_id):
    row = db.execute('''SELECT r.* FROM requests r JOIN conversations c ON c.id=r.conversation_id
                      WHERE r.id=? AND c.demo_user_id=?''', (str(request_id), owner())).fetchone()
    if row is None:
        raise NotFound('Request not found.')
    return row

def status_in(db, request_id):
    row = dict(request_row(db, request_id))
    user = db.execute("SELECT id FROM messages WHERE request_id=? AND role='user'", (str(request_id),)).fetchone()
    reply = db.execute("SELECT id,content FROM messages WHERE request_id=? AND role='assistant'", (str(request_id),)).fetchone()
    return {k: row[k] for k in ('id','conversation_id','status','attempt_count','provider_call_count','error_code','created_at','updated_at')} | {
        'user_message_id': user['id'], 'assistant_message_id': reply['id'] if reply else None,
        'assistant_content': reply['content'] if reply else None,
        'retrieval_outcome': row['retrieval_outcome'], 'retrieved_record_ids': json.loads(row['retrieved_ids_json']),
        'citations': json.loads(row['citations_json']), 'failure_stage': row['failure_stage'],
        'provider': row['provider'], 'model': row['model'], 'user_persistence': 'saved', 'assistant_persistence': 'saved' if reply else 'not_saved'}

def operation(db, operation_id, kind, target, value):
    digest = fingerprint(value)
    old = db.execute('SELECT * FROM conversation_operations WHERE id=?', (str(operation_id),)).fetchone()
    if old:
        if (old['demo_user_id'],old['operation_type'],old['target_id'],old['input_hash']) != (owner(),kind,str(target),digest):
            raise Conflict('Operation ID was reused with different input.')
        return False
    db.execute('INSERT INTO conversation_operations VALUES (?,?,?,?,?)',
               (str(operation_id),owner(),kind,str(target),digest))
    return True

def create(path, body):
    with connection(path, True) as db:
        fresh = operation(db,body.operation_id,'create',body.conversation_id,{'conversation_id':str(body.conversation_id)})
        if fresh:
            if db.execute('SELECT 1 FROM conversations WHERE id=?',(str(body.conversation_id),)).fetchone():
                raise Conflict('Conversation ID already exists; use the original operation ID.')
            stamp=now()
            db.execute('INSERT INTO conversations VALUES (?,?,?,?)',(str(body.conversation_id),owner(),stamp,stamp))
        return owned(db,body.conversation_id),fresh

def list_conversations(path,cursor,limit):
    with connection(path) as db:
        rows=db.execute('SELECT id,created_at,updated_at FROM conversations WHERE demo_user_id=? ORDER BY created_at DESC,id DESC LIMIT ? OFFSET ?',
                        (owner(),limit+1,cursor)).fetchall()
        return {'conversations':[dict(r) for r in rows[:limit]], 'next_cursor':cursor+limit if len(rows)>limit else None}

def list_messages(path,conversation_id,cursor,limit):
    with connection(path) as db:
        owned(db,conversation_id)
        rows=db.execute('''SELECT m.*,r.provider,r.model,r.status AS request_status,r.error_code FROM messages m JOIN requests r ON r.id=m.request_id
                          WHERE m.conversation_id=? AND m.sequence>? ORDER BY m.sequence LIMIT ?''',
                        (str(conversation_id),cursor,limit+1)).fetchall()
        selected=rows[:limit]
        latest=db.execute("SELECT request_id FROM messages WHERE conversation_id=? AND role='user' ORDER BY sequence DESC LIMIT 1",(str(conversation_id),)).fetchone()
        return {'messages':[dict(r) for r in selected], 'next_cursor':selected[-1]['sequence'] if len(rows)>limit else None,
                'latest_request_id':latest['request_id'] if latest else None}

def insert_message(db, conversation_id, request_id, role, content):
    sequence=db.execute('SELECT COALESCE(MAX(sequence),0)+1 FROM messages WHERE conversation_id=?',(conversation_id,)).fetchone()[0]
    db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?,?)',
               (str(uuid4()),conversation_id,request_id,role,content,sequence,now()))

def submit(path,conversation_id,body,provider='mock',model=None):
    digest=fingerprint({'conversation_id':str(conversation_id),'content':body.content,'mock_mode':body.mock_mode})
    with connection(path,True) as db:
        owned(db,conversation_id)
        old=db.execute('SELECT * FROM requests WHERE id=?',(str(body.request_id),)).fetchone()
        if old:
            if old['input_hash']!=digest:
                raise Conflict('Request ID was reused with different input.')
            return status_in(db,body.request_id),False
        if db.execute("SELECT 1 FROM requests WHERE conversation_id=? AND status='pending'",(str(conversation_id),)).fetchone():
            raise Conflict('This conversation already has a pending request.')
        stamp=now()
        db.execute('''INSERT INTO requests(id,conversation_id,input_hash,status,mock_mode,created_at,updated_at)
                      VALUES (?,?,?,'pending',?,?,?)''',(str(body.request_id),str(conversation_id),digest,body.mock_mode,stamp,stamp))
        db.execute('UPDATE requests SET provider=?,model=? WHERE id=?',(provider,model,str(body.request_id)))
        insert_message(db,str(conversation_id),str(body.request_id),'user',body.content)
        db.execute('UPDATE conversations SET updated_at=? WHERE id=?',(stamp,str(conversation_id)))
        return status_in(db,body.request_id),True

def retry(path,request_id,body,provider='mock',model=None):
    with connection(path,True) as db:
        row=request_row(db,request_id)
        fresh=operation(db,body.operation_id,'retry',request_id,{'request_id':str(request_id),'mock_mode':body.mock_mode})
        if not fresh:
            return status_in(db,request_id),False
        if row['status']!='failed':
            raise Conflict('Only failed requests can be retried.')
        if db.execute("SELECT 1 FROM requests WHERE conversation_id=? AND status='pending'",(row['conversation_id'],)).fetchone():
            raise Conflict('This conversation already has a pending request.')
        db.execute("UPDATE requests SET status='pending',error_code=NULL,retrieval_outcome='not_run',retrieved_ids_json='[]',citations_json='[]',failure_stage=NULL,mock_mode=?,attempt_count=attempt_count+1,updated_at=? WHERE id=?",
                   (body.mock_mode,now(),str(request_id)))
        db.execute('UPDATE requests SET provider=?,model=? WHERE id=?',(provider,model,str(request_id)))
        return status_in(db,request_id),True

def get_status(path,request_id):
    with connection(path) as db:
        return status_in(db,request_id)

def claim(path,request_id):
    with connection(path,True) as db:
        row=request_row(db,request_id)
        if row['status']!='pending':
            return None
        content=db.execute("SELECT content,sequence FROM messages WHERE request_id=? AND role='user'",(str(request_id),)).fetchone()
        return row['mock_mode'],content['content'],row['conversation_id'],content['sequence']

def finish(path,request_id,content):
    with connection(path,True) as db:
        row=request_row(db,request_id)
        if row['status']!='pending':
            return
        insert_message(db,row['conversation_id'],str(request_id),'assistant',content)
        stamp=now()
        db.execute("UPDATE requests SET status='succeeded',error_code=NULL,updated_at=? WHERE id=?",(stamp,str(request_id)))
        db.execute('UPDATE conversations SET updated_at=? WHERE id=?',(stamp,row['conversation_id']))

def fail(path,request_id,code):
    with connection(path,True) as db:
        db.execute("UPDATE requests SET status='failed',error_code=?,updated_at=? WHERE id=? AND status='pending'",
                   (code,now(),str(request_id)))

def recover_pending(path):
    # Local prototype runs one Uvicorn worker; startup never regenerates a reply.
    with connection(path,True) as db:
        db.execute("UPDATE requests SET status='failed',error_code='interrupted',updated_at=? WHERE status='pending'",(now(),))


def count_call(path,request_id,stage):
    with connection(path,True) as db:
        row=request_row(db,request_id)
        if row['status']!='pending': raise Conflict('Request is no longer pending.')
        db.execute('UPDATE requests SET provider_call_count=provider_call_count+1 WHERE id=?',(str(request_id),))


def retrieval_status(path,request_id,outcome,retrieved_ids=(),citations=(),stage=None):
    with connection(path,True) as db:
        db.execute('UPDATE requests SET retrieval_outcome=?,retrieved_ids_json=?,citations_json=?,failure_stage=? WHERE id=?',
                   (outcome,json.dumps(list(retrieved_ids)),json.dumps(list(citations)),stage,str(request_id)))

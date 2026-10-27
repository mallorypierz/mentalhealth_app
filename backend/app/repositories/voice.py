"""Voice metadata only. Text remains in ordinary conversations/messages."""
from . import conversations as chat
from ..identity import active_context


def session_in(db, ident):
    row = db.execute('SELECT v.* FROM voice_sessions v JOIN conversations c ON c.id=v.conversation_id '
                     'WHERE v.id=? AND c.demo_user_id=?', (str(ident), chat.owner())).fetchone()
    if row is None:
        raise chat.NotFound('Voice session not found.')
    return dict(row)


def turn_in(db, ident):
    row = db.execute('SELECT * FROM voice_turns WHERE id=?', (str(ident),)).fetchone()
    if row is None:
        raise chat.NotFound('Voice turn not found.')
    session_in(db, row['session_id'])
    result = dict(row)
    result['request'] = chat.status_in(db, row['request_id']) if row['request_id'] else None
    result['provider'] = (result['request'] or {}).get('provider','mock')
    result['persistence'] = 'saved'
    return result


def operation(db, ident, session, target, action, value):
    digest = chat.fingerprint(value)
    row = db.execute('SELECT * FROM voice_operations WHERE id=?', (str(ident),)).fetchone()
    if row:
        if (row['session_id'], row['target_id'], row['action'], row['input_hash']) != (str(session), str(target), action, digest):
            raise chat.Conflict('Voice operation ID reused with different input.')
        return False
    db.execute('INSERT INTO voice_operations VALUES (?,?,?,?,?)', (str(ident),str(session),str(target),action,digest))
    return True


def create(path, body):
    with chat.connection(path, True) as db:
        chat.owned(db, body.conversation_id)
        old = db.execute('SELECT id FROM voice_sessions WHERE id=?', (str(body.session_id),)).fetchone()
        identity = active_context.get()
        if old:
            session_in(db, body.session_id)
            receipt = db.execute('SELECT id FROM voice_operations WHERE id=?', (str(body.operation_id),)).fetchone()
            if not receipt:
                raise chat.Conflict('Use the original creation operation.')
            operation(db,body.operation_id,body.session_id,body.session_id,'create',body.model_dump(mode='json'))
            return session_in(db,body.session_id),False
        if db.execute("SELECT 1 FROM voice_sessions WHERE conversation_id=? AND state IN ('ready','active')", (str(body.conversation_id),)).fetchone():
            raise chat.Conflict('End the active voice session first.')
        stamp=chat.now()
        db.execute('INSERT INTO voice_sessions VALUES (?,?,?,?,?,1,?,?)',
                   (str(body.session_id),str(body.conversation_id),identity.session_id,identity.version,'ready',stamp,stamp))
        operation(db,body.operation_id,body.session_id,body.session_id,'create',body.model_dump(mode='json'))
        return session_in(db,body.session_id),True


def get(path, ident):
    with chat.connection(path) as db:
        result=session_in(db,ident)
        result['turns']=[turn_in(db,r[0]) for r in db.execute('SELECT id FROM voice_turns WHERE session_id=? ORDER BY sequence', (str(ident),)).fetchall()]
        return result | {'provider':'mock','persistence':'saved'}


def begin(path, ident, body):
    with chat.connection(path, True) as db:
        session=session_in(db,ident)
        receipt=db.execute('SELECT id FROM voice_operations WHERE id=?',(str(body.operation_id),)).fetchone()
        if receipt:
            operation(db,body.operation_id,ident,body.turn_id,'turn',body.model_dump(mode='json'))
            return turn_in(db,body.turn_id),False
        if session['state'] not in ('ready','active'):
            raise chat.Conflict('Start a new voice session explicitly.')
        if db.execute("SELECT 1 FROM voice_turns WHERE session_id=? AND state='processing'",(str(ident),)).fetchone():
            raise chat.Conflict('A voice turn is already processing.')
        if db.execute('SELECT 1 FROM voice_turns WHERE id=? OR reserved_request_id=?',(str(body.turn_id),str(body.request_id))).fetchone():
            raise chat.Conflict('Turn or request ID already exists.')
        if db.execute('SELECT 1 FROM requests WHERE id=?',(str(body.request_id),)).fetchone():
            raise chat.Conflict('Request ID already exists.')
        sequence=db.execute('SELECT COALESCE(MAX(sequence),0)+1 FROM voice_turns WHERE session_id=?',(str(ident),)).fetchone()[0]
        stamp=chat.now()
        db.execute('INSERT INTO voice_turns(id,session_id,sequence,reserved_request_id,created_at,updated_at) VALUES (?,?,?,?,?,?)',
                   (str(body.turn_id),str(ident),sequence,str(body.request_id),stamp,stamp))
        operation(db,body.operation_id,ident,body.turn_id,'turn',body.model_dump(mode='json'))
        db.execute("UPDATE voice_sessions SET state='active',revision=revision+1,updated_at=? WHERE id=?",(stamp,str(ident)))
        return turn_in(db,body.turn_id),True


def update(path, ident, **fields):
    allowed={'transcription','submission','speech','state','error_code','request_id'}
    if not fields or not fields.keys() <= allowed:
        raise ValueError('Invalid voice state field')
    with chat.connection(path,True) as db:
        current=turn_in(db,ident)
        if current['state']=='cancelled':
            return current
        # SQL identifiers come only from the fixed allowlist; values are bound.
        db.execute('UPDATE voice_turns SET '+','.join(k+'=?' for k in fields)+',revision=revision+1,updated_at=? WHERE id=?',
                   (*fields.values(),chat.now(),str(ident)))
        return turn_in(db,ident)


def cancel_in(db, ident):
    turn=turn_in(db,ident)
    if turn['request_id']:
        db.execute("UPDATE requests SET status='failed',error_code='interrupted',updated_at=? WHERE id=? AND status='pending'",(chat.now(),turn['request_id']))
    db.execute("UPDATE voice_turns SET state='cancelled',speech=CASE WHEN speech='ready' THEN speech ELSE 'cancelled' END,revision=revision+1,updated_at=? WHERE id=?", (chat.now(),str(ident)))


def action(path, ident, body, retained_reply=None):
    with chat.connection(path,True) as db:
        turn=turn_in(db,ident)
        fresh=operation(db,body.operation_id,turn['session_id'],ident,body.action,body.model_dump(mode='json'))
        if fresh:
            if turn['revision']!=body.expected_revision:
                raise chat.Conflict('Voice state changed. Read it again.')
            if body.action=='cancel':
                cancel_in(db,ident)
            elif body.action=='retry_reply_save':
                if retained_reply is None or not turn['request'] or turn['request']['error_code']!='reply_save_failed':
                    raise chat.Conflict('No retained unsaved reply is available.')
                session=session_in(db,turn['session_id'])
                if session['state'] not in ('ready','active'):
                    raise chat.Conflict('Voice session has ended.')
                chat.insert_message(db,session['conversation_id'],turn['request_id'],'assistant',retained_reply)
                db.execute("UPDATE requests SET status='succeeded',error_code=NULL,updated_at=? WHERE id=?",(chat.now(),turn['request_id']))
                db.execute('UPDATE conversations SET updated_at=? WHERE id=?',(chat.now(),session['conversation_id']))
                db.execute("UPDATE voice_turns SET state='completed',speech='not_started',error_code=NULL,revision=revision+1,updated_at=? WHERE id=?",(chat.now(),str(ident)))
            else:
                if not turn['request'] or turn['request']['assistant_persistence']!='saved' or turn['state']=='cancelled':
                    raise chat.Conflict('No saved reply is available for speech.')
                db.execute("UPDATE voice_turns SET speech='processing',error_code=NULL,revision=revision+1,updated_at=? WHERE id=?", (chat.now(),str(ident)))
        return turn_in(db,ident)


def stop(path, ident, body):
    with chat.connection(path,True) as db:
        session=session_in(db,ident)
        fresh=operation(db,body.operation_id,ident,ident,'stop',body.model_dump(mode='json'))
        if fresh:
            if session['revision']!=body.expected_revision:
                raise chat.Conflict('Voice session changed. Read it again.')
            for row in db.execute("SELECT id FROM voice_turns WHERE session_id=? AND state='processing'",(str(ident),)).fetchall():
                cancel_in(db,row[0])
            db.execute("UPDATE voice_sessions SET state='stopped',revision=revision+1,updated_at=? WHERE id=?",(chat.now(),str(ident)))
        return session_in(db,ident)


def recover(path):
    with chat.connection(path,True) as db:
        db.execute("UPDATE voice_sessions SET state='interrupted',revision=revision+1 WHERE state IN ('ready','active')")
        db.execute("UPDATE voice_turns SET state='failed',error_code='interrupted',revision=revision+1 WHERE state='processing'")


def hold_for_support(path, ident):
    # Do not persist recognized words or create a conversation message here.
    with chat.connection(path,True) as db:
        turn=turn_in(db,ident)
        if turn['state']=='cancelled': return False
        db.execute("UPDATE voice_turns SET state='held',transcription='succeeded',submission='not_saved',speech='not_started',error_code='support_notice',revision=revision+1,updated_at=? WHERE id=?",(chat.now(),str(ident)))
        db.execute("UPDATE voice_sessions SET state='stopped',revision=revision+1,updated_at=? WHERE id=?",(chat.now(),turn['session_id']))
        return True

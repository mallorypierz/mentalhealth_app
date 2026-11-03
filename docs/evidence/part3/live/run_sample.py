"""One approved run only; invoked manually from repo root. Never a routine test."""
import asyncio,json,sqlite3,tempfile
from pathlib import Path
from uuid import uuid4
from dataclasses import replace
from backend.app.config import load
from backend.app.db import initialize,connect,DATABASE_PATH,DEMO_USER_ID
from backend.app.providers.openai import Provider
from backend.app.repositories import voice_budget as budget, conversations as records
from backend.app.repositories.provider_usage import LimitError
from backend.app.controllers.conversations import generate
from backend.app.chat_schemas import ConversationCreate,MessageSubmit
OUT=Path('docs/evidence/part3/live/results.json')
if OUT.exists(): raise SystemExit('Existing results: do not rerun or replenish allowance.')
s=replace(load(),provider='openai',voice_call_limit=12,voice_budget_microdollars=600000)
s.require_voice()
initial=budget.status(DATABASE_PATH,s)
if initial['used']!=0 or initial['remaining']!=12: raise SystemExit('Ledger differs from approved baseline; stop.')
class Ledger:
 LimitError=LimitError
 def reserve(self,path,request_id,stage,settings):
  return budget.reserve(DATABASE_PATH,f'part3-20261102:{request_id}:{stage}',stage,settings)
 def finish(self,path,ident,outcome,usage=None):budget.finish(DATABASE_PATH,ident,outcome,usage)
questions=['What happened in my most recent saved exercise? Give its status and active duration.']*2+['What is the difference between a grounding exercise and a breathing exercise? Explain briefly without recommending a treatment.']
results=[]
async def main():
 for case,q in enumerate(questions,1):
  for repetition in (1,2):
   if budget.status(DATABASE_PATH,s)['remaining']<2: return
   path=Path(tempfile.mkdtemp(prefix='part3-live-fictional-'))/'app.sqlite3';initialize(path)
   expected=None
   if case==1:
    with connect(path) as db:
     db.execute("INSERT INTO demo_users VALUES ('other','Other fictional owner')")
     for owner,skill,status,duration,stamp in [(DEMO_USER_ID,'paced_breathing_4_6','completed',60000,'2026-11-01T12:00:00Z'),(DEMO_USER_ID,'stop','stopped',23000,'2026-11-02T12:00:00Z'),('other','stop','completed',60000,'2026-11-02T13:00:00Z')]:
      ident=str(uuid4())
      db.execute('INSERT INTO exercise_sessions(id,demo_user_id,skill_key,status,started_at,active_duration_ms,last_checkpoint_at) VALUES (?,?,?,?,?,?,?)',(ident,owner,skill,status,stamp,duration,stamp))
      if owner==DEMO_USER_ID and status=='stopped': expected=ident
   cid,rid=uuid4(),uuid4()
   records.create(path,ConversationCreate(conversation_id=cid,operation_id=uuid4()))
   records.submit(path,cid,MessageSubmit(request_id=rid,content=q),provider='openai',model=s.model)
   before=budget.status(DATABASE_PATH,s)['used']
   await generate(path,rid,provider=Provider(path,rid,s,ledger=Ledger()))
   result=records.get_status(path,rid)
   results.append(dict(case=f'L0{case}',repetition=repetition,input=q,expected_record_id=expected,ledger_calls=budget.status(DATABASE_PATH,s)['used']-before,result=result))
   OUT.write_text(json.dumps({'mode':'live','initial_ledger':initial,'current_ledger':budget.status(DATABASE_PATH,s),'attempts':results},indent=2)+'\n')
   print(f'L0{case}/{repetition}: {result["status"]}, {result["error_code"]}',flush=True)
   if result['error_code'] in ('provider_http_401','provider_http_403','provider_http_404','configuration_unavailable'): return
asyncio.run(main())

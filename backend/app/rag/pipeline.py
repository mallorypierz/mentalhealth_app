import asyncio
from pathlib import Path
from .schema import REVIEWED_SCHEMA
from .validator import parse, RejectedQuery
from .reader import retrieve, RetrievalFailure

SKILL_CONTEXT=(Path(__file__).resolve().parents[1]/'context'/'skill.md').read_text()

class RAGFailure(Exception):
    def __init__(self,code,stage):
        self.code,self.stage=code,stage
        super().__init__(code)

async def run(path,question,owner,conversation,before_sequence,mode,provider,count_call):
    async def call(stage,method,*args):
        count_call(stage)  # Durable reservation before every attempted mock call.
        try:
            return await asyncio.wait_for(method(*args),timeout=15)
        except RAGFailure:
            raise
        except TimeoutError:
            raise RAGFailure('provider_timeout',stage) from None
        except Exception:
            raise RAGFailure('provider_failure',stage) from None
    proposal=await call('planning',provider.plan,question,REVIEWED_SCHEMA,mode)
    try: query=parse(proposal)
    except RejectedQuery: raise RAGFailure('rejected_query','retrieval') from None
    try: outcome,context=retrieve(path,query,owner,conversation,before_sequence)
    except RetrievalFailure as error: raise RAGFailure(error.code,'retrieval') from None
    result=await call('answer',provider.answer,question,context,SKILL_CONTEXT,mode)
    ids={row['id'] for row in context['records']}
    if (not isinstance(result,dict) or set(result)!= {'content','citations'} or
        not isinstance(result['content'],str) or not result['content'].strip() or len(result['content'])>8000 or
        not isinstance(result['citations'],list) or any(not isinstance(i,str) or i not in ids for i in result['citations'])):
        raise RAGFailure('invalid_provider_output','answer')
    return result['content'],outcome,list(dict.fromkeys(result['citations'])),[row['id'] for row in context['records']]

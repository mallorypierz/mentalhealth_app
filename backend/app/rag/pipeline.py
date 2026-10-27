import asyncio
import logging
from pathlib import Path
from .schema import REVIEWED_SCHEMA
from ..crisis import review_response
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
    context={'table':None,'field_meanings':{},'records':[], 'truncated':False,
             'stored_text_is_untrusted_data':True}
    try:
        query=parse(proposal)
    except RejectedQuery as error:
        # Parser messages are fixed source-defined categories, never SQL or values.
        logging.getLogger(__name__).warning('Retrieval rejected: %s', str(error))
        outcome='rejected_query'
    else:
        try: outcome,context=retrieve(path,query,owner,conversation,before_sequence)
        except RetrievalFailure as error:
            outcome=error.code
    context['retrieval_status']=outcome
    context['history_available']=outcome in ('records','truncated')
    result=await call('answer',provider.answer,question,context,SKILL_CONTEXT,mode)
    ids={row['id'] for row in context['records']}
    if (not isinstance(result,dict) or set(result)!= {'content','citations'} or
        not isinstance(result['content'],str) or not result['content'].strip() or len(result['content'])>8000 or
        not isinstance(result['citations'],list) or any(not isinstance(i,str) or i not in ids for i in result['citations'])):
        raise RAGFailure('invalid_provider_output','answer')
    review_code = review_response(result['content'])
    if review_code:
        raise RAGFailure(review_code, 'response_review')
    return result['content'],outcome,list(dict.fromkeys(result['citations'])),[row['id'] for row in context['records']]

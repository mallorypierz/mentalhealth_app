import asyncio
from uuid import UUID
from fastapi import APIRouter, Query, Response
from fastapi.responses import JSONResponse
from ..crisis import matches, NOTICE
from ..chat_schemas import ConversationCreate, Conversation, ConversationPage, MessageSubmit, MessagePage, RequestStatus, RetryRequest
from ..repositories import conversations as records
from ..controllers.conversations import generate


def router(path,tasks,settings):
    api=APIRouter(prefix='/api')
    def schedule(request_id):
        task=asyncio.create_task(generate(path,request_id,settings=settings))
        tasks.add(task)
        task.add_done_callback(tasks.discard)

    @api.post('/conversations',response_model=Conversation,status_code=201)
    def create(body:ConversationCreate,response:Response):
        result,fresh=records.create(path,body)
        response.status_code=201 if fresh else 200
        return result

    @api.get('/conversations',response_model=ConversationPage)
    def listing(cursor:int=Query(0,ge=0),limit:int=Query(20,ge=1,le=100)):
        return records.list_conversations(path,cursor,limit)

    @api.get('/conversations/{conversation_id}/messages',response_model=MessagePage)
    def messages(conversation_id:UUID,cursor:int=Query(0,ge=0),limit:int=Query(100,ge=1,le=100)):
        return records.list_messages(path,conversation_id,cursor,limit)

    @api.post('/conversations/{conversation_id}/messages',response_model=RequestStatus,status_code=202)
    async def submit(conversation_id:UUID,body:MessageSubmit):
        if matches(body.content):
            return JSONResponse(status_code=422, content={
                'error': {'code': 'support_notice', 'message': NOTICE, 'retryable': False},
                'persistence': 'not_saved'})
        result,fresh=records.submit(path,conversation_id,body,settings.provider,settings.model if settings.provider == 'openai' else None)
        if fresh:
            schedule(body.request_id)
        return result

    @api.get('/requests/{request_id}',response_model=RequestStatus)
    def status(request_id:UUID):
        return records.get_status(path,request_id)

    @api.post('/requests/{request_id}/retry',response_model=RequestStatus,status_code=202)
    async def retry(request_id:UUID,body:RetryRequest):
        result,fresh=records.retry(path,request_id,body,settings.provider,settings.model if settings.provider == 'openai' else None)
        if fresh:
            schedule(request_id)
        return result

    return api

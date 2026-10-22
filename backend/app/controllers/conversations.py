import asyncio
import sqlite3
from ..repositories import conversations as records
from ..providers import mock
from ..rag.pipeline import run, RAGFailure
from ..db import DEMO_USER_ID
from ..crisis import matches

async def generate(path, request_id, provider=mock, settings=None):
    try:
        claimed=records.claim(path,request_id)
        if claimed is None:
            return
        mode,content,conversation_id,before_sequence=claimed
        if matches(content):
            # Covers retries of records saved before the wording rule existed.
            records.fail(path,request_id,'support_notice')
            return
        count_call=lambda stage: records.count_call(path,request_id,stage)
        if settings is not None and settings.provider != 'mock':
            from ..providers.openai import Provider
            provider=Provider(path,request_id,settings)
            count_call=lambda stage: None  # Live adapter atomically reserves and counts before HTTP.
        try:
            reply,outcome,citations,source_ids=await run(
                path,content,DEMO_USER_ID,conversation_id,before_sequence,mode,provider,
                count_call)
            records.retrieval_status(path,request_id,outcome,source_ids,citations)
        except RAGFailure as error:
            records.retrieval_status(path,request_id,error.code,stage=error.stage)
            records.fail(path,request_id,error.code)
            return
        try:
            records.finish(path,request_id,reply)
        except sqlite3.Error:
            records.fail(path,request_id,'reply_save_failed')
    except asyncio.CancelledError:
        try:
            records.fail(path,request_id,'interrupted')
        except sqlite3.Error:
            pass
        raise
    except sqlite3.Error:
        return  # Database outage stays unconfirmed; restart reconciles pending work.
    except Exception:
        try:
            records.fail(path,request_id,'provider_failure')
        except sqlite3.Error:
            pass

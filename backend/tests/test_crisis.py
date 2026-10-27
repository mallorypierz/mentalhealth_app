import asyncio
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.config import Settings
from backend.app.main import create_app
from backend.app.crisis import matches
from backend.app.repositories import conversations as records, provider_usage
from backend.app.chat_schemas import ConversationCreate, MessageSubmit
from backend.app.controllers.conversations import generate

class CrisisTests(unittest.TestCase):
    def test_phrases_and_known_limitations(self):
        for text in ['KILL MYSELF','end\nmy life','hurt myself','suicide','suicidal','I am not suicidal']:
            self.assertTrue(matches(text))
        self.assertFalse(matches('Fictional: I cannot go on.'))
        self.assertFalse(matches('What happened in my last practice?'))

    def test_direct_submission_no_database_write_or_provider_even_without_configuration(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'test.sqlite3'
            with TestClient(create_app(path,Settings(provider='openai',call_limit=0))) as client:
                with patch.object(records,'submit',side_effect=AssertionError('Must not write')):
                    response=client.post('/api/conversations/'+str(uuid4())+'/messages',json={
                        'request_id':str(uuid4()),'content':'Fictional quote: hurt myself','mock_mode':'success'})
                self.assertEqual(response.status_code,422)
                self.assertEqual(response.json()['error']['code'],'support_notice')
                self.assertEqual(response.json()['persistence'],'not_saved')
                self.assertEqual(provider_usage.used(path),0)
                self.assertEqual(client.get('/api/sessions').status_code,200)

    def test_legacy_saved_request_gets_no_new_call_or_invented_reply(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'test.sqlite3'
            with TestClient(create_app(path)):
                cid=uuid4();rid=uuid4()
                records.create(path,ConversationCreate(conversation_id=cid,operation_id=uuid4()))
                records.submit(path,cid,MessageSubmit(request_id=rid,content='Fictional: end my life'))
                asyncio.run(generate(path,rid,settings=Settings(provider='openai',call_limit=6)))
                status=records.get_status(path,rid)
                self.assertEqual(status['error_code'],'support_notice')
                self.assertEqual(status['provider_call_count'],0)
                self.assertIsNone(status['assistant_message_id'])
                self.assertEqual(len(records.list_messages(path,cid,0,100)['messages']),1)
                self.assertEqual(provider_usage.used(path),0)

class EducationalResponseTests(unittest.TestCase):
    def test_approved_indirect_phrases_and_known_recognition_limits(self):
        for text in ["I don't want to be alive", 'I don’t want to be alive', 'I do not want to be alive',
                     'I might do something to myself', 'I am not going to hurt myself', 'Quote: “I don’t want to be alive.”']:
            self.assertTrue(matches(text),text)
        for text in ['I might do something to my shelf', 'I wish I could disappear', 'I cannot go on']:
            self.assertFalse(matches(text),text)  # Known misses; never interpreted as safety.

    def test_reject_selected_out_of_scope_claims_allow_reviewed_refusals(self):
        from backend.app.crisis import review_response
        rejected=['You have depression.', 'You meet the criteria for PTSD.', 'Double your medication dose.',
                  'Take 50 mg each morning.', 'You must start therapy.', 'This exercise will cure your anxiety.',
                  "You're definitely safe.", 'Everything will be fine.', 'I am monitoring your safety.',
                  'Help has been dispatched.', "I'll check on you later."]
        for text in rejected: self.assertEqual(review_response(text),'response_unavailable',text)
        permitted=["I can’t determine whether you have a condition. A qualified healthcare professional can assess that.",
                   "I can explain the reviewed exercise, but I can’t recommend a treatment plan.",
                   "I can’t recommend starting, stopping or changing medication. Ask your prescriber or pharmacist.",
                   'Pause or Stop is always your choice.', 'The saved practice lasted 60 seconds.']
        for text in permitted: self.assertIsNone(review_response(text),text)
        self.assertEqual(review_response('If you are suicidal, open Crisis support.'),'support_notice')
        # A demonstrated semantic miss, not an assurance: lexical checks are limited.
        self.assertIsNone(review_response('All your troubles are certain to vanish.'))

    def test_generated_claim_withheld_before_assistant_save(self):
        from backend.app.providers import mock
        async def unsafe(*args): return {'content':'You have depression.','citations':[]}
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'review.sqlite3'
            with TestClient(create_app(path)):
                cid=uuid4(); rid=uuid4()
                records.create(path,ConversationCreate(conversation_id=cid,operation_id=uuid4()))
                records.submit(path,cid,MessageSubmit(request_id=rid,content='Fictional: what does my saved history show?'))
                with patch.object(mock,'answer',unsafe): asyncio.run(generate(path,rid))
                status=records.get_status(path,rid)
                self.assertEqual(status['error_code'],'response_unavailable')
                self.assertEqual(status['failure_stage'],'response_review')
                self.assertEqual(status['provider_call_count'],2)
                self.assertEqual(status['assistant_persistence'],'not_saved')
                self.assertEqual(len(records.list_messages(path,cid,0,100)['messages']),1)

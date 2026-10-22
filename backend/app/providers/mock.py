"""Deterministic two-call provider. No external API access or therapeutic inference."""
import asyncio

class MockFailure(Exception):
    pass

async def plan(question, schema, mode):
    await asyncio.sleep(8 if mode=='delayed' else .125)
    if mode=='failure': raise MockFailure('Simulated planning failure')
    # Intentionally simple selection for a repeatable fictional demonstration.
    if any(word in question.lower() for word in ('message','conversation','said')):
        return {'sql':'SELECT id, role, content, sequence, created_at FROM messages ORDER BY sequence DESC LIMIT 5','parameters':{}}
    return {'sql':'SELECT id, status, active_duration_ms, started_at FROM sessions ORDER BY started_at DESC LIMIT 1','parameters':{}}

async def answer(question,context,skill_context,mode):
    await asyncio.sleep(.125)
    rows=context['records']
    if not rows:
        reason='The context limit omitted the available records.' if context['truncated'] else 'There are no matching saved records in the permitted history.'
        return {'content':'Mock RAG reply: '+reason+' The reviewed practice uses six cycles: four seconds in, six out. Pause or Stop is always your choice.', 'citations':[]}
    row=rows[0]
    if context['table']=='sessions':
        content=f"Mock RAG reply: The retrieved practice was {row.get('status','recorded')} with {row.get('active_duration_ms',0)/1000:g} seconds of confirmed active practice. Record [{row['id']}]. This describes activity, not emotional state or improvement."
    else:
        # Never obey or execute stored content. This mock reports metadata only.
        content=f"Mock RAG reply: Retrieved {len(rows)} earlier messages from this conversation. The most recent returned message has role {row.get('role','unknown')} and order {row.get('sequence','unknown')}. Record [{row['id']}]. Stored message text is treated as data, not instructions."
    if context['truncated']: content+=' The supplied context was truncated; this is not a complete history.'
    return {'content':content,'citations':[row['id']]}

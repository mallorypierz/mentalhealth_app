"""Conservative wording checks, not clinical assessment or reliable detection."""
import re

PHRASES = ('kill myself', 'end my life', 'hurt myself', 'suicide', 'suicidal',
           "i don't want to be alive", 'i do not want to be alive', 'i might do something to myself')
NOTICE = ('Some of these words may refer to immediate distress or self-harm. '
          'I may have misunderstood, especially if speech was transcribed incorrectly. '
          'This app cannot assess your safety or provide crisis care. '
          'You can open Crisis support for human-support options.')


def normalize(text):
    return ' '.join(text.lower().replace('’', "'").replace('‘', "'").split())


def matches(text):
    value = normalize(text)
    return any(phrase in value for phrase in PHRASES)


# These narrow rules deliberately do not claim complete semantic coverage. A match
# suppresses output; an absence is not a safety certificate. Never log blocked text.
RESPONSE_RULES = (
    ('diagnosis', r"\b(?:you have|you suffer from|you are suffering from|you meet (?:the )?criteria for|i diagnose you with)\s+(?:a |an |clinical |major |generalized )?(?:depression|depressive disorder|anxiety disorder|bipolar|ptsd|ocd|adhd|schizophrenia)\b"),
    ('medication', r"\b(?:start|stop|increase|decrease|double|halve|skip|take|change)\b[^.!?]{0,70}\b(?:medication|medicine|dose|dosage|pills?|antidepressants?|ssris?|sertraline|fluoxetine|lithium|mg)\b"),
    ('treatment', r"\b(?:your treatment plan (?:is|should)|you (?:should|must|need to) (?:start|undergo|receive) (?:treatment|therapy)|this (?:practice|exercise) (?:will|can) cure)\b"),
    ('reassurance', r"\b(?:you(?:'re| are) (?:definitely |completely )?safe|everything will be (?:fine|okay|ok)|nothing bad will happen|you have nothing to worry about|this (?:practice|exercise) will (?:fix|resolve|cure))\b"),
    ('monitoring', r"\b(?:i(?:'m| am)|we(?:'re| are)) (?:watching|monitoring) (?:you|your safety)\b|\b(?:help (?:has been|is being) dispatched|i(?:'ll| will) check (?:on you|in with you)|we(?:'ll| will) check (?:on you|in with you))\b"),
)


def review_response(text):
    """Return a failure code, never a claim that a reply is clinically safe."""
    value = normalize(text)
    if matches(value):
        return 'support_notice'
    # The reviewed refusal wording contains medication verbs but is permitted as
    # a complete sentence. Other sentences still get reviewed independently.
    refusals = {
        "i can't recommend starting, stopping or changing medication",
        'ask your prescriber or pharmacist',
        "i can't determine whether you have a condition",
        'a qualified healthcare professional can assess that',
        "i can explain the reviewed exercise, but i can't recommend a treatment plan",
    }
    sentences = re.split(r'[.!?]+', value)
    candidate = '. '.join(sentence.strip() for sentence in sentences if sentence.strip() not in refusals)
    if any(re.search(pattern, candidate) for _, pattern in RESPONSE_RULES):
        return 'response_unavailable'
    return None

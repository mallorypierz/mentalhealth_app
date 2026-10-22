"""Limited application wording rule; no inference about a person's safety."""
PHRASES = ('kill myself', 'end my life', 'hurt myself', 'suicide', 'suicidal')

def matches(text):
    normalized = ' '.join(text.lower().split())
    return any(phrase in normalized for phrase in PHRASES)

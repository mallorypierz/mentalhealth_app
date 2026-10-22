"""Explicit local configuration. No environment scanning or secret-bearing repr."""
from dataclasses import dataclass, field
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[1] / '.env'
MODEL = 'gpt-5.4-mini-2026-03-17'

@dataclass(frozen=True)
class Settings:
    provider: str = 'mock'
    model: str = MODEL
    api_key: str = field(default='', repr=False)
    call_limit: int = 0
    timeout: int = 15
    max_output_tokens: int = 1024
    error: str | None = None

    def require_live(self):
        if self.error or not self.api_key or self.provider != 'openai':
            raise ValueError('configuration_unavailable')


def load(path=ENV_PATH):
    defaults = dict(MODEL_PROVIDER='mock', OPENAI_MODEL=MODEL, OPENAI_API_KEY='',
                    LIVE_CALL_LIMIT='0', PROVIDER_TIMEOUT_SECONDS='15', MAX_OUTPUT_TOKENS='1024')
    try:
        if not path.exists(): return Settings()
        seen = set()
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith('#'): continue
            name, sep, value = line.partition('=')
            name, value = name.strip(), value.strip()
            if not sep or name not in defaults or name in seen or any(c in value for c in ('"', "'", '$', '`')):
                raise ValueError()
            defaults[name] = value; seen.add(name)
        provider=defaults['MODEL_PROVIDER']; limit=int(defaults['LIVE_CALL_LIMIT'])
        timeout=int(defaults['PROVIDER_TIMEOUT_SECONDS']); output=int(defaults['MAX_OUTPUT_TOKENS'])
        if provider not in ('mock','openai') or defaults['OPENAI_MODEL'] != MODEL or not 0 <= limit <= 6 or not 1 <= timeout <= 15 or not 16 <= output <= 1024:
            raise ValueError()
        return Settings(provider, MODEL, defaults['OPENAI_API_KEY'], limit, timeout, output)
    except (OSError, ValueError, UnicodeError):
        return Settings(provider='unavailable', error='configuration_unavailable')

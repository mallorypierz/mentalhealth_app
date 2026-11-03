"""Application-owned exercise identifiers and planned active durations.

Completion records the guided sequence, never a mental or clinical outcome.
"""
from typing import Literal

SkillKey = Literal['paced_breathing_4_6', 'sensory_grounding_5_4_3_2_1', 'stop', 'cognitive_reframe']
EXERCISES = {
    'paced_breathing_4_6': ('Paced breathing (4–6)', 60000),
    'sensory_grounding_5_4_3_2_1': ('5-4-3-2-1 sensory grounding', 75000),
    'stop': ('STOP', 60000),
    'cognitive_reframe': ('One-minute cognitive reframe', 60000),
}

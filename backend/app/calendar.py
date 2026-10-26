"""Read-only calendar projection. Completion time determines the displayed day."""
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, Query
from pydantic import AwareDatetime, BaseModel

from .db import connect
from .identity import owner, validate_context, IdentityError


class Event(BaseModel):
    session_id: UUID
    exercise_name: Literal['Paced breathing (4–6)'] = 'Paced breathing (4–6)'
    completed_at: AwareDatetime
    local_date: str
    local_time: str
    active_duration_ms: int
    is_fixture: bool


class CalendarPage(BaseModel):
    month: str
    timezone: str
    placement: Literal['completion'] = 'completion'
    events: list[Event]
    next_cursor: int | None


def month_bounds(month, zone):
    try:
        tz = ZoneInfo(zone)
        year, number = map(int, month.split('-'))
        if not 1900 <= year <= 2100 or not 1 <= number <= 12:
            raise ValueError()
        start = datetime(year, number, 1, tzinfo=tz)
        end = datetime(year+1, 1, 1, tzinfo=tz) if number == 12 else datetime(year, number+1, 1, tzinfo=tz)
        return start.astimezone(timezone.utc), end.astimezone(timezone.utc), tz
    except (ValueError, ZoneInfoNotFoundError):
        raise IdentityError(422, 'invalid_calendar_range', 'Use a valid month and IANA timezone.') from None


def events(path, month, zone, cursor, limit):
    start, end, tz = month_bounds(month, zone)
    db = connect(path)
    try:
        validate_context(db)
        # julianday handles historical stored offsets as well as normalized UTC.
        rows = db.execute("SELECT id,ended_at,active_duration_ms,is_fixture FROM exercise_sessions "
                          "WHERE demo_user_id=? AND status='completed' AND skill_key='paced_breathing_4_6' "
                          "AND julianday(ended_at)>=julianday(?) AND julianday(ended_at)<julianday(?) "
                          "ORDER BY julianday(ended_at),id LIMIT ? OFFSET ?",
                          (owner(), start.isoformat(), end.isoformat(), limit+1, cursor)).fetchall()
        result = []
        for row in rows[:limit]:
            instant = datetime.fromisoformat(row['ended_at'])
            local = instant.astimezone(tz)
            result.append(dict(session_id=row['id'], completed_at=instant.astimezone(timezone.utc),
                               local_date=local.date().isoformat(), local_time=local.isoformat(),
                               active_duration_ms=row['active_duration_ms'], is_fixture=bool(row['is_fixture'])))
        return dict(month=month, timezone=zone, events=result,
                    next_cursor=cursor+limit if len(rows)>limit else None)
    finally:
        db.close()


def router(path):
    api = APIRouter(prefix='/api')

    @api.get('/calendar', response_model=CalendarPage)
    def read(month: str = Query(pattern=r'^\d{4}-\d{2}$'), timezone: str = Query(min_length=1, max_length=100),
             cursor: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100)):
        return events(path, month, timezone, cursor, limit)

    return api

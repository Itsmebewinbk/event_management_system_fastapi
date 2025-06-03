from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import Event
from app.schemas import EventCreate
from datetime import datetime
from fastapi import Request


async def create_event_crud(db: AsyncSession, event_in: EventCreate) -> Event:
    event = Event(**event_in.dict(), attendee_count=0)
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event

async def get_upcoming_events(
    request: Request,
    db: AsyncSession,
    offset: int = 0,
    limit: int = 20,
):
    
    total_events = await db.scalar(
        select(func.count()).where(Event.start_time > datetime.utcnow())
    )

    stmt = (
        select(Event)
        .where(Event.start_time > datetime.utcnow())
        .offset(offset)
        .limit(limit)
    )
    results = (await db.execute(stmt)).scalars().all()

   
    base_url = str(request.url).split("?")[0]

    next_url = (
        f"{base_url}?limit={limit}&offset={offset + limit}"
        if offset + limit < total_events
        else None
    )
    prev_url = (
        f"{base_url}?limit={limit}&offset={offset - limit}"
        if offset - limit >= 0 and offset > 0
        else None
    )

    return {
        "count": total_events,
        "next": next_url,
        "previous": prev_url,
        "results": results,
    }
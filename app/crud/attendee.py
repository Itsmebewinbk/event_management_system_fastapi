from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import Attendee, Event
from app.schemas import AttendeeCreate
from sqlalchemy.exc import IntegrityError
from app.response import ErrorResponse
from fastapi import Request


async def register_attendee(
    db: AsyncSession, event_id: int, attendee_in: AttendeeCreate
):
    event = await db.get(Event, event_id)
    if not event:
        return ErrorResponse(message="Event not found")

    if event.capacity_reached:
        return ErrorResponse(message="Capacity reached for this event")

    attendee = Attendee(**attendee_in.dict(), event_id=event_id)
    db.add(attendee)
    event.attendee_count += 1
    existing = await db.execute(
        select(Attendee).where(
            Attendee.event_id == event_id, Attendee.email == attendee_in.email
        )
    )
    existing_attendee = existing.scalar_one_or_none()
    if existing_attendee:
        return ErrorResponse(
            message="Attendee with this email is already registered for the event",
        )

    try:
        await db.commit()
        await db.refresh(attendee)
    except IntegrityError:
        await db.rollback()
        return ErrorResponse(message="Attendee already registered for this event")

    return attendee


async def get_attendees_by_event(
    request: Request, db: AsyncSession, event_id: int, offset: int = 0, limit: int = 20
):

    total_attendees = await db.scalar(
        select(func.count()).where(Attendee.event_id == event_id)
    )

    results = (
        (
            await db.execute(
                select(Attendee)
                .where(Attendee.event_id == event_id)
                .offset(offset)
                .limit(limit)
            )
        )
        .scalars()
        .all()
    )

    base_url = str(request.url).split("?")[0]

    next_url = (
        f"{base_url}?limit={limit}&offset={offset + limit}"
        if (offset + limit < total_attendees)
        else None
    )
    prev_url = (
        f"{base_url}?limit={limit}&offset={offset - limit}"
        if (offset - limit >= 0)
        else None
    )

    return {
        "count": total_attendees,
        "next": next_url,
        "previous": prev_url,
        "results": results,
    }

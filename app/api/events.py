from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.schemas import EventCreate, EventRead
from app.schemas import AttendeeCreate, AttendeeRead
from app.crud import (
    register_attendee,
    get_attendees_by_event,
    create_event_crud,
    get_upcoming_events,
)


router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=EventRead)
async def create_event(event_in: EventCreate, db: AsyncSession = Depends(get_async_db)):
    return await create_event_crud(db, event_in)


@router.get(
    "/",
)
async def list_upcoming_events(
    request: Request,
    offset: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
):
    return await get_upcoming_events(request, db, offset, limit)


@router.post("/{event_id}/register", response_model=AttendeeRead)
async def register(
    event_id: int, attendee_in: AttendeeCreate, db: AsyncSession = Depends(get_async_db)
):
    result = await register_attendee(db, event_id, attendee_in)

    return result


@router.get("/{event_id}/attendees")
async def get_attendees(
    request: Request,
    event_id: int,
    offset: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
):
    return await get_attendees_by_event(request, db, event_id, offset, limit)

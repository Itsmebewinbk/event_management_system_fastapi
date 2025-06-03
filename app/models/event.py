from sqlalchemy import Integer, String, ForeignKey, DateTime,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from datetime import datetime


class TimesStampedModel(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Event(TimesStampedModel):
    __tablename__ = "events"
    name: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255))
    start_time: Mapped[datetime] = mapped_column(
        DateTime,
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime,
    )
    max_capacity: Mapped[int] = mapped_column(Integer)
    attendee_count: Mapped[int] = mapped_column(Integer)

    attendee : Mapped[list["Attendee"]] = relationship(
        "Attendee",back_populates="events", passive_deletes=True
    )

    def __repr__(self):
        return f"Event(id={self.name}, location={self.location}, max_capacity={self.max_capacity})"

    @property
    def capacity_left(self) -> int:
        return self.max_capacity - self.attendee_count

    @property
    def capacity_reached(self) -> bool:
        return self.attendee_count >= self.max_capacity

class Attendee(TimesStampedModel):
    __tablename__ = "attendees"
    __table_args__ = (
        UniqueConstraint("event_id", "email", name="unique_event_email"),
    )

    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255)) 
    event_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False
    )

    event: Mapped["Event"] = relationship("Event", back_populates="attendees")


    def __repr__(self):
        return f"Attendee(id={self.name}, email={self.email}"

from app.models import Event, Attendee
from sqladmin import ModelView

class EventAdmin(ModelView, model=Event):
    column_list = (Event.id, Event.name, Event.start_time, Event.location)
    column_searchable_list = (Event.name, Event.location)
    column_filters = (Event.start_time,)

class AttendeeAdmin(ModelView, model=Attendee):
    column_list = (Attendee.id, Attendee.name, Attendee.email, Attendee.event_id)
    column_searchable_list = (Attendee.name, Attendee.email)
    column_filters = (Attendee.event_id,)

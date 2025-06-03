
# from sqlalchemy import event
# from app.models import Attendee, Event

# @event.listens_for(Attendee, "after_insert")
# def increment_attendee_count(mapper, connection, target: Attendee):
#     connection.execute(
#         Event.__table__.update()
#         .where(Event.id == target.event_id)
#         .values(attendee_count=Event.attendee_count + 1)
#     )

# @event.listens_for(Attendee, "after_delete")
# def decrement_attendee_count(mapper, connection, target: Attendee):
#     connection.execute(
#         Event.__table__.update()
#         .where(Event.id == target.event_id)
#         .values(attendee_count=Event.attendee_count - 1)
#     )

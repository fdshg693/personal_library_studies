from litellm import completion
from pydantic import BaseModel

messages = [{"role": "user", "content": "List 2 important events in the XIX century"}]


class CalendarEvent(BaseModel):
    name: str
    date: str


class EventsList(BaseModel):
    events: list[CalendarEvent]


resp = completion(model="gpt-4o", messages=messages, response_format=EventsList)

print("Received={}".format(resp.choices[0].message.content))

events_list: EventsList = EventsList.model_validate_json(
    resp.choices[0].message.content
)

for event in events_list.events:
    print(f"- {event.date}: {event.name}")

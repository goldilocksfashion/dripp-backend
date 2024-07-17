from fastapi import APIRouter, FastAPI
from event import  Event
from KafkaUtil import KafkaUtil

app = FastAPI()
router = APIRouter(prefix="/dripp/v1/events")

@router.get("/meta")
async def root():
    return {"message": "pong"}

@router.put("/events/{bounded_context}/{event_id}")
async def store(bounded_context: str, event_id: int,  event: Event):
    kafka = KafkaUtil(source_bounded_context=bounded_context, target_bounded_context=bounded_context)
    kafka.send_message('my_topic', 'my_topic', str(event_id), event.model_dump_json())
    return {"message": f"Event {event_id} stored successfully"}


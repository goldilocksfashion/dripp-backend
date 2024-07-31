from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from event import Event,  ENRTY_TOPIC
from kafka import KafkaUtil

app = FastAPI()
router = APIRouter(prefix="/dripp/v1/events")


kafka_util = KafkaUtil()

@router.get("/meta")
async def root():
    return {"message": "pong"}

@router.post("/{event_id}")
async def route(bounded_context: str, event_id: int, event: Event):
    key = str(event_id)
    kafka_util.send_message(bounded_context, ENRTY_TOPIC,  key, event.model_dump_json())
    return {"message": f"Event {event_id} stored successfully"}

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
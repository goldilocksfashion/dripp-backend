from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, json
from enum import Enum
from datetime import datetime
from typing import Union
import logging
import os
import boto3
import trio
from confluent_kafka import Consumer, KafkaError, KafkaException
from app.kafka import KafkaUtil
from app.s3_storage import S3Util
from abc import ABC, abstractmethod

ENTRY_TOPIC = "dripp-ai-events"

class Context(BaseModel):
    def __init__(self, name:str = 'dripp-ai-events', env:dict = None):
        self.logger = logging.getLogger(name or "dripp_events_listener")
        self.env = env or dict(os.environ)
            
    
class EventException(Exception):
    """Exception raised for errors in the event processing."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
class EventKind(str, Enum):
    content_management = 'content_management'
    social_network = 'social_network'
    marketplace = 'marketplace'
    vto = 'vto'

@dataclass(frozen=True)
class Event(BaseModel):
    """Represents an event."""
    event_id: int
    event_name: str
    event_creation_ts: str
    event_source: EventKind
    event_kind: EventKind
    event_location: str
    event_processed_ts: Union[str, None] = None
    event_payload: Optional[str] = None

class EventRouter:
    """Routes events to the appropriate Kafka topic."""
    def __init__(self, kafka_util):
        self.kafka_util = kafka_util

    def route_event(self, event: Event):
        """Routes the event to the appropriate Kafka topic."""
        topic = f"{event.event_kind}_events"
        key = str(event.event_id)
        value = json.dumps(event.model_dump)
        self.kafka_util.send_message(event.event_kind, topic, key, value)
        
        
class EventListener(ABC):
    
    def __init__(self, context: Context, topic: str):
        self.context = context or  Context()
        self.topic = ENTRY_TOPIC
        self.logger = context.logger
        self.kafka_util = KafkaUtil()
        self.event_router = EventRouter(self.kafka_util)
        self.boto3_client = boto3.client(
            's3',
            aws_access_key_id=context.env['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=context.env['AWS_SECRET_ACCESS_KEY'],
            region_name=context.env['AWS_REGION']
        )
        self.s3_bucket = context.env['S3_BUCKET']
        self.logger = logging.getLogger("dripp_events_listener")
        self.logger.setLevel(logging.INFO)
        self.consumer = Consumer({
            'bootstrap.servers': context.env['KAFKA_BOOTSTRAP_SERVERS'],
            'group.id': context.env['KAFKA_GROUP_ID'],
            'auto.offset.reset': 'earliest'
        })
        
    async def start(self):
        self.consumer.subscribe([self.topic])
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self.consume)
    
    async def consume(self):
        while True:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())
            else:
                event_data = json.loads(msg.value().decode('utf-8'))
                event = Event(**event_data)
                self.on_event(event)
                self.consumer.commit()

    @abstractmethod
    async def on_event(self, event: Event):
        pass
    
import json
import boto3
import logging
import trio
from confluent_kafka import Consumer, KafkaException, KafkaError
from app.event import Event, EventException, EventRouter, Context, EventListener, ENTRY_TOPIC
from app.kafka import KafkaUtil

class CoreEventListener(EventListener):
   
    """
     Listener for core events that are then routed to the appropriate Kafka topics
    """
    def __init(self, context: Context):
       super().__init__(context=context, topic=ENTRY_TOPIC)

       
    async def on_event(self, event: Event):
        message =   """
       ____       _                    _ 
      / __ \_____(_)___  ____   ____ _(_)
     / / / / ___/ / __ \/ __ \ / __ `/ / 
    / /_/ / /  / / /_/ / /_/ // /_/ / /  
    \____/_/  /_/ .___/ .___(_)__,_/_/   
            /_/   /_/                 
                    Initializing context...                         
                    """
        self.logger.info(message)
        self.__process(event=event)

    async def __process(self, event: Event):
        self.logger.info(f"Received event: {event}")
        if event.event_kind is not None:
            try:
                event_id = event.event_id
                self.event_router.route_event(event=event)
                self.logger.info(f"Message sent: {event}")
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise EventException(f"Failed to send message: {e}")
        else:
            self.logger.error(f"Unknown event kind: {event.event_kind}")
        
   
async def main():
    context = Context()
    listener = CoreEventListener(context)
    await listener.start()

if __name__ == "__main__":
    trio.run(main)
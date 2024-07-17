import asyncio
from datetime import datetime
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
from typing import Optional
import os
from event import Event, EventKind
from logger import LogUtil
import json

class KafkaUtil:

    """
    A utility class for working with Kafka.
    """

    @property
    def producer(self):
        return self._producer
    
    @property
    def producer_config(self):
        return self._producer_config
    
    @property
    def consumer_config(self):
        return self._consumer_config

    def __init__(self,
                 source_bounded_context : Optional[str] = None, 
                 target_bounded_context: Optional[str] = None) -> None:
            self.logger = LogUtil().logger
            if os.environ.get('IS_DEBUG') is not None:
                self.logger.debug('Creating KafkaUtil instance.')

            self._producer_config = {
            # User-specific properties that you must set
            'bootstrap.servers': os.environ.get('KAFKA_BOOTSTRAP_SERVERS'),
            # Fixed properties
            'acks': 'all'
        }
            self._consumer_config =  {
        # User-specific properties that you must set
        'bootstrap.servers': os.environ.get('KAFKA_BOOTSTRAP_SERVERS'),
        # Fixed properties
        'group.id':          target_bounded_context or os.environ.get('KAFKA_CONSUMER_GROUP_ID'),
        'auto.offset.reset': 'latest'
    }
            self._producer = self._create_producer()
   
    def create_consumer(self) -> Consumer:
        """
        Creates a Kafka consumer instance.

        Returns:
            KafkaConsumer: The Kafka consumer instance.
        """
        return Consumer(self._consumer_config)

    async def subscribe(self, topic, on_event):
        """
        Asynchronously subscribes to a Kafka topic and calls a callback function when a message is received.

        Args:
            topic (str): The Kafka topic to subscribe to.
        """
        # Initialize the Consumer with the provided configuration
        consumer = Consumer(self._consumer_config)
        if(topic is None):
            self.logger.error('== Topic is None == subscribing to target_bounded_context.')
            consumer.subscribe([self.target_bounded_context])
        else:
            self.logger.info(f"Subscribing to topic: {topic}")
            consumer.subscribe([topic])
        # Run the poll loop in an asyncio task to not block the event loop
        async def poll_messages():
            while True:
                # Poll for a message with a timeout (e.g., 1.0 seconds)
                message = consumer.poll(1.0)
                if message is None:
                    continue
                if message.error():
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        continue
                    else:
                        print(f"Error: {message.error()}")
                        break
                else:
                    # Call the on_event callback
                    await on_event(message)

        # Start polling in a background task
        task = asyncio.create_task(poll_messages())

        try:
            # Wait for the polling task to complete (it won't under normal conditions)
            await task
        except asyncio.CancelledError:
            # Task cancellation should be handled gracefully
            self.logger.info("Polling task was cancelled")
        finally:
            consumer.close()


    def _create_producer(self) -> Producer:
        """
        Creates a Kafka producer instance.

        Returns:
            KafkaProducer: The Kafka producer instance.
        """
        return Producer(self._producer_config)

    def _acked(self,err, msg):
        """
        A callback function that is called when a message is delivered.
        """
        if err is not None:
            self.logger.error("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            self.logger.debug("Message produced: %s" % (str(msg)))

    def send_message(self,topic, source_bounded_context, key, value, target_bounded_context : Optional[str] = None):
        """
        sends a message to a Kafka topic.
        Args:
            topic (str): The Kafka topic to send the message to.
            source_bounded_context (str): The source bounded context of the message.
            key (str): The key of the message.
            value (str): The value of the message.
            target_bounded_context (str): The target bounded context of the message.
        """
        headers = []
        if target_bounded_context is not None:
            headers.append(target_bounded_context.encode('utf-8'))
        if source_bounded_context is not None:
            headers.append(source_bounded_context.encode('utf-8'))
        self.producer.produce(topic, key=key.encode('utf-8'), value=value, headers=headers, callback=self._acked)
        self.producer.flush()


if __name__ == "__main__":
    topic = 'my_topic'
    formatted_datetime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f')[:-3]
    key =f'user_signup_requested_{formatted_datetime}'
    event_payload = dict(user_id=1, user_name='John Doe')
    event = Event(event_id=1, event_name='user_signup_requested', event_creation_ts=formatted_datetime, event_source=EventKind.social_network, event_kind=EventKind.social_network, event_location='social_network', event_processed_ts=formatted_datetime, event_payload=json.dumps(event_payload))
    value = event.model_dump_json()
    KafkaUtil(source_bounded_context=topic).send_message(topic, topic,  key, value)

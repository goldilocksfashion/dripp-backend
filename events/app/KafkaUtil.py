from datetime import datetime
from confluent_kafka import Consumer, Producer
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

    
    def _create_producer(self) -> Producer:
        """
        Creates a Kafka producer instance.

        Returns:
            KafkaProducer: The Kafka producer instance.
        """
        return Producer(self._producer_config)

    def _acked(err, msg):
        """
        A callback function that is called when a message is delivered.
        """
        if err is not None:
            print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            print("Message produced: %s" % (str(msg)))

    def send_message(self,topic, source_bounded_context, key, value, target_bounded_context : Optional[str] = None):
        """
        Sends a message to a Kafka topic.

        Args:
            topic (str): The Kafka topic to send the message to.
            key (str): The key of the message.
            value (str): The value of the message.
        """
        self.producer.produce(topic, key=key.encode('utf-8'), value=value)
        self.producer.flush()


if __name__ == "__main__":
    topic = 'my_topic'
    formatted_datetime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f')[:-3]
    key =f'user_signup_requested_{formatted_datetime}'
    event_payload = dict(user_id=1, user_name='John Doe')
    event = Event(event_id=1, event_name='user_signup_requested', event_creation_ts=formatted_datetime, event_source=EventKind.social_network, event_kind=EventKind.social_network, event_location='social_network', event_processed_ts=formatted_datetime, event_payload=json.dumps(event_payload))
    value = event.model_dump_json()
    KafkaUtil(source_bounded_context=topic).send_message(topic, topic,  key, value)

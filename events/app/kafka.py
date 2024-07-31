import json
import os
from confluent_kafka import Producer

class KafkaUtil:
    """
     KafkaUtil class to send messages to Kafka
    """
    def __init__(self):
        kafka_bootstrap_servers = os.env.get('KAFKA_BOOTSTRAP_SERVERS')
        if not kafka_bootstrap_servers:
            raise ValueError("KAFKA_BOOTSTRAP_SERVERS environment variable is not set")
            self.producer_config = {
            'bootstrap.servers': kafka_bootstrap_servers,
            'acks': 'all'
        }
        self.producer = Producer(self.producer_config)
       


    def send_kafka_message(self, topic, key, value):
         self.producer.produce(topic, key=key, value=json.dumps(value), callback=self.__acked)
         self.producer.flush()

    def __acked(self,err, msg):
        if err is not None:
            print(f"Failed to deliver message: {msg}: {err}")
        else:
            print(f"Message produced: {msg}")

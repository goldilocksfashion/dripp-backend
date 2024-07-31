import os
import sys
import json
import boto3
import logging
from nuclio_sdk import Context, Event
from events.app.event import Event, EventException
from events.app.kafka import KafkaUtil
from models import social_network_events

def init_context(context: Context):
    message =   """
   ____       _                    _ 
  / __ \_____(_)___  ____   ____ _(_)
 / / / / ___/ / __ \/ __ \ / __ `/ / 
/ /_/ / /  / / /_/ / /_/ // /_/ / /  
\____/_/  /_/ .___/ .___(_)__,_/_/   
           /_/   /_/                 
                Initializing context...                         
                """
    context.logger.info(message)
    context.logger.info('Initializing context...')
    # Initialize KafkaUtil instance
    context.kafka_util = KafkaUtil(context=context)
    context.boto3_client =  boto3.client(
        's3',
        aws_access_key_id=context.env['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=context.env['AWS_SECRET_ACCESS_KEY'],
        region_name=context.env['AWS_REGION']
    )
    context.s3_bucket = context.env['S3_BUCKET']
    context.logger = logging.getLogger("dripp_events_listener")

def handler(context: Context, event: Event):
    # Parse the incoming event
    event_data = json.loads(event.body.decode('utf-8'))
    context.logger.info(f"Received event: {event_data}")
    event_kind = event_data.get('kind')
    if event_kind is not None and event_kind in social_network_events:
        try:
            context.kafka_util.send_message(event_kind, event_data)
            context.logger.info(f"Message sent: {event_data}")
        except Exception as e:
            context.logger.error(f"Failed to send message: {e}")
            raise EventException(f"Failed to send message: {e}")
    else:
        context.logger.error(f"Unknown event kind: {event_kind}")
    
    return context.Response(body='Event processed successfully', content_type='text/plain', status_code=200)

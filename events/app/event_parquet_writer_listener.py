import logging
import boto3
import pyarrow as pa
import pyarrow.parquet as pq
import trio
import time
from datetime import datetime
from typing import List, Dict
import io
from confluent_kafka import Consumer, KafkaError, KafkaException
from app.event import Event, Context, EventListener
from app.s3_storage import S3Util


class EventParquetWriterListener(EventListener):
    
    def __init__(self, 
                 context: Context,
                 flush_interval: int = 900,
                 s3_client: S3Util = None):
        
        super.__init__(context)
        self.flush_interval = flush_interval
        self.buffer : List[Event] = []
        if s3_client:
            self.s3_client = s3_client
        else:
            self.s3_client = S3Util(context)
        self.last_flush_time = time.time()

    async def on_event(self, event: Event):
        # Add event to buffer
        self.buffer.append(event)
        # Check if it's time to flush to S3
        current_time = time.time()
        if current_time - self.last_flush_time >= self.flush_interval:
            try:
                self.flush()
                self.last_flush_time = current_time
            except Exception as e:
                    self.context.logger.error(f"Failed to flush events to S3: {e}")


    async def flush(self):
        try:
            if not self.buffer:
                return
            # Write buffer to Parquet and upload to S3
            self.context.logger.info(f"Flushing {len(self.buffer)} events to S3")
            table = pa.Table.from_pylist(self.buffer, schema=self.schema)
            buffer = io.BytesIO()
            pq.write_table(table, buffer)
            buffer.seek(0)
            date_str = datetime.utcnow().strftime('%Y-%m-%d')
            hour_str = datetime.utcnow().strftime('%H')
            s3_key = f"dripp_ai_events/date={date_str}/hour={hour_str}/events-{int(time.time()) % 4}.parquet"
            self.s3_client.upload_to_s3(s3_key, buffer)
            self.buffer.clear()
        except Exception as e:
            self.context.logger.error(f"Failed to flush events to S3: {e}")
   
   
async def main():
    listener = EventParquetWriterListener()
    await listener.start()

if __name__ == "__main__":
    trio.run(main)
import asyncio
import asyncpg
import boto3
import os
from datetime import datetime


class DAO:
    def __init__(self):
        self.bounded_context_prefix = os.environ.get('BOUNDED_CONTEXT_PREFIX', 'DRIPP_SOCIAL_NETWORK')
        self.region = os.environ.get(f'{self.bounded_context_prefix}_NETWORK_REGION',  'us-west-2')
        self.host = os.environ.get(f'{self.bounded_context_prefix}_DB_HOST','127.0.0.1')
        self.port = os.environ.get(f'{self.bounded_context_prefix}_DB_PORT', '5432')
        self.db_user = os.environ.get(f'{self.bounded_context_prefix}_DB_USER', 'admin')
        self.db_name = os.environ.get(f'{self.bounded_context_prefix}_DB_NAME', 'social_network')
        self.rds_client = boto3.client('rds')
        # Generate the auth token
        self.auth_token = self.rds_client.generate_db_auth_token(
            DBHostname=self.host,
            Port=self.port,
            DBUsername=self.db_user,
            Region=self.region
        )
        self.db_config = {
                            'user': self.db_user,
                            'password': self.auth_token,
                            'database': self.db_name,
                            'host': self.db_host,
                        }
        
        



def create_pool(self):
    return await asyncpg.create_pool(**self.db_config)

async def execute_query(self,query, *args):
    async with create_pool() as pool:
        async with pool.acquire() as connection:
            return await connection.fetch(query, *args)

async def insert_post(self,user_id, post_id, post_kind, content, created_at):
    query = "INSERT INTO posts (user_id, post_id, post_kind, content, created_at) VALUES ($1, $2, $3, $4, $5)"
    await execute_query(query, user_id, post_id, post_kind, content, created_at)

async def store_post_segments(self,post_id, segments):
    # Assuming `vector_db_client` is an instance of your vector DB's Python client
    # and it has a method `insert_vectors` that takes a list of vectors and their IDs
    vector_data = []
    for segment in segments:
        # Assuming each segment dict now includes a 'vector' key with the vector data
        vector_data.append({
            "id": f"{post_id}_{segment['type']}",  # Creating a unique ID for each segment
            "vector": segment['vector'],
            "metadata": {
                "post_id": post_id,
                "segment_type": segment['type'],
                "content": segment.get('content', '')
            }
        })
    # Insert vector data into the vector DB
    await vector_db_client.insert_vectors(vector_data)

    queries = []
    for segment in segments:
        query = "INSERT INTO post_segments (post_id, segment_type, content, created_at) VALUES ($1, $2, $3, NOW())"
        queries.append(execute_query(query, post_id, segment['type'], segment.get('content', '')))
    await asyncio.gather(*queries)

async def insert_comment(self,user_id, post_id, content, created_at):
    query = "INSERT INTO comments (user_id, post_id, content, created_at) VALUES ($1, $2, $3, $4)"
    return await execute_query(query, user_id, post_id, content, created_at)

async def insert_like(self,user_id, post_id, created_at):
    query = "INSERT INTO likes (user_id, post_id, created_at) VALUES ($1, $2, $3)"
    return await execute_query(query, user_id, post_id, created_at)

async def insert_dislike(self,user_id, post_id, created_at):
    query = "INSERT INTO dislikes (user_id, post_id, created_at) VALUES ($1, $2, $3)"
    return await execute_query(query, user_id, post_id, created_at)
import asyncio
import asyncpg
import boto3
import os
from datetime import datetime


rds_client = boto3.client('rds')
bounded_context_prefix = os.environ.get('BOUNDED_CONTEXT_PREFIX', 'DRIPP_SOCIAL_NETWORK')
REGION = os.environ.get(f'{bounded_context_prefix}_NETWORK_REGION',  'us-west-2')
HOST = os.environ.get(f'{bounded_context_prefix}_DB_HOST','127.0.0.1')
PORT = os.environ.get(f'{bounded_context_prefix}_DB_PORT', '5432')
DB_USER = os.environ.get(f'{bounded_context_prefix}_DB_USER', 'admin')
DB_NAME = os.environ.get(f'{bounded_context_prefix}_DB_NAME', 'social_network')

# Generate the auth token
auth_token = rds_client.generate_db_auth_token(
    DBHostname=HOST,
    Port=PORT,
    DBUsername=DB_USER,
    Region=REGION
)

DATABASE_CONFIG = {
    'user': DB_USER,
    'password': auth_token,
    'database': DB_NAME,
    'host': HOST,
}

async def create_pool():
    return await asyncpg.create_pool(**DATABASE_CONFIG)

async def execute_query(query, *args):
    async with create_pool() as pool:
        async with pool.acquire() as connection:
            return await connection.fetch(query, *args)

async def insert_post(user_id, post_id, post_kind, content, created_at):
    query = "INSERT INTO posts (user_id, post_id, post_kind, content, created_at) VALUES ($1, $2, $3, $4, $5)"
    await execute_query(query, user_id, post_id, post_kind, content, created_at)

async def store_post_segments(post_id, segments):
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

async def insert_comment(user_id, post_id, content, created_at):
    query = "INSERT INTO comments (user_id, post_id, content, created_at) VALUES ($1, $2, $3, $4)"
    return await execute_query(query, user_id, post_id, content, created_at)

async def insert_like(user_id, post_id, created_at):
    query = "INSERT INTO likes (user_id, post_id, created_at) VALUES ($1, $2, $3)"
    return await execute_query(query, user_id, post_id, created_at)

async def insert_dislike(user_id, post_id, created_at):
    query = "INSERT INTO dislikes (user_id, post_id, created_at) VALUES ($1, $2, $3)"
    return await execute_query(query, user_id, post_id, created_at)
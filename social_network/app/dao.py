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

async def insert_user(user_id, username, email, password, created_at):
    query = "INSERT INTO users (user_id, username, email, password, created_at) VALUES ($1, $2, $3, $4, $5)"
    return await execute_query(query, user_id, username, email, password, created_at)
 
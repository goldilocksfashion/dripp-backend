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

async def create_tables(pool):
    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                bio TEXT,
                profile_picture_url TEXT,
                privacy_settings JSONB NOT NULL
            )
        ''')
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS follows (
                follower_id INTEGER REFERENCES users(id),
                followed_user_id INTEGER REFERENCES users(id),
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
            )
        ''')
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                sender_id INTEGER REFERENCES users(id),
                receiver_id INTEGER REFERENCES users(id),
                content TEXT,
                sent_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
            )
        ''')

async def insert_follow(pool, follower_id: int, followed_user_id: int):
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO follows (follower_id, followed_user_id) VALUES ($1, $2)
        ''', follower_id, followed_user_id)

async def fetch_followers(pool, user_id: int):
    async with pool.acquire() as connection:
        rows = await connection.fetch('''
            SELECT follower_id FROM follows WHERE followed_user_id = $1
        ''', user_id)
        return [row['follower_id'] for row in rows]

async def main():
    pool = await create_pool()
    await create_tables(pool)
    await insert_follow(pool, follower_id=1, followed_user_id=2)
    followers = await fetch_followers(pool, user_id=2)
    print(followers)
    await pool.close()

asyncio.run(main())
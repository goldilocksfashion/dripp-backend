import asyncio
import asyncpg
from datetime import datetime

# Replace these with your actual database credentials
DATABASE_CONFIG = {
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database',
    'host': '127.0.0.1'
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
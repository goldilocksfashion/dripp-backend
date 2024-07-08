from fastapi import FastAPI, Depends, HTTPException, Request
from events.app.event import Event
from fastapi.security import OAuth2AuthorizationCodeBearer
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from contextlib import asynccontextmanager
from typing import Dict
from fastapi import FastAPI, Depends

from social_network.app.database_accessor import create_pool, create_tables, fetch_followers, insert_follow

pool = None ## global variable to store the connection pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await create_pool()
    await create_tables(pool)
    yield
    await pool.close()

app = FastAPI(lifespan=lifespan)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Load configuration from environment variables or .env file
config = Config(".env")

# Set up OAuth
oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=config('GOOGLE_CLIENT_ID'),
    client_secret=config('GOOGLE_CLIENT_SECRET'),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:8000/auth',
    client_kwargs={'scope': 'openid profile email'},
)

oauth.register(
    name='instagram',
    client_id=config('INSTAGRAM_CLIENT_ID'),
    client_secret=config('INSTAGRAM_CLIENT_SECRET'),
    authorize_url='https://api.instagram.com/oauth/authorize',
    access_token_url='https://api.instagram.com/oauth/access_token',
    client_kwargs={'scope': 'user_profile'},
)

oauth.register(
    name='tiktok',
    client_id=config('TIKTOK_CLIENT_ID'),
    client_secret=config('TIKTOK_CLIENT_SECRET'),
    authorize_url='https://open-api.tiktok.com/platform/oauth/connect/',
    access_token_url='https://open-api.tiktok.com/platform/oauth/token/',
    client_kwargs={'scope': 'user_info'},
)

oauth.register(
    name='pinterest',
    client_id=config('PINTEREST_CLIENT_ID'),
    client_secret=config('PINTEREST_CLIENT_SECRET'),
    authorize_url='https://api.pinterest.com/oauth/',
    access_token_url='https://api.pinterest.com/v1/oauth/token',
    client_kwargs={'scope': 'read_public, write_public'},
)


oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl='https://accounts.google.com/o/oauth2/auth')



@app.get("/events/social_network/meta")
def read_root():
    return "pong"

@app.get("/events/social_network/login")
async def login(request: Request):
    redirect_uri = request.url_path_for('auth', _external=True)
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.route('/events/social_networks/auth')
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    # Save user information to session
    request.session['user'] = dict(user)
    return RedirectResponse(url='/')

@app.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')

@app.get("/events/social_network/protected")
async def protected(user: dict = Depends(oauth2_scheme)):
    return {"message": f"Hello, {user['name']}"}

@app.post("/events/social_network/follow/")
async def api_insert_follow(follower_id: int, followed_user_id: int):
    await insert_follow(app.state.pool, follower_id=follower_id, followed_user_id=followed_user_id)
    return {"message": "Follow inserted successfully"}

@app.get("/events/followers/{user_id}")
async def api_fetch_followers(user_id: int):
    followers = await fetch_followers(app.state.pool, user_id=user_id)
    if followers:
        return {"followers": followers}
    raise HTTPException(status_code=404, detail="User not found")
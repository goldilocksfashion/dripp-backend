import datetime
import uuid
from fastapi import FastAPI, Depends, HTTPException, Request
from events.app.event import Event, EventKind, KafkaUtil
from fastapi.security import OAuth2AuthorizationCodeBearer
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from contextlib import asynccontextmanager
from typing import Dict
from fastapi import FastAPI, Depends
from google.oauth2 import id_token
from google.auth.transport import requests
import os 
from social_network.app.database_accessor import create_pool, create_tables, fetch_followers, insert_follow

pool = None ## global variable to store the connection pool
kafka_util = None
GOOGLE_CLIENT_ID = os.getenv("SOCIAL_NETWORK_GOOGLE_CLIENT_ID")

def _decode_google_token(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        userid = idinfo['sub']
        return idinfo
    except ValueError:
        raise

    
@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await create_pool()
    kafka_util = KafkaUtil(source_bounded_context="social_network")
    await create_tables(pool)
    yield
    await pool.close()

app = FastAPI(lifespan=lifespan)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Load configuration from environment variables or .env file
config = Config(".env")

@app.post("events/social_network/signup/google")
async def signup_with_google(token: str):
    user_info = _decode_google_token(token)
    if user_info:
        # Extract needed information from user_info
        user_profile = {
            "name": user_info.get("name"),
            "email": user_info.get("email"),
            "profile_picture": user_info.get("picture")
            # Add other fields as needed
        }
        # Save or update the user profile in your database
        # save_user_profile(user_profile)
        user_signup_event = Event(event_id=uuid.uuid4(), 
                            event_creation_ts=datetime.now().timestamp(),
                            event_kind=EventKind.SOCIAL_NETWORK,
                            event_payload=user_profile,
                            event_source=EventKind.SOCIAL_NETWORK,
                            event_location="social_network_signup",
                            event_name="social_network_signup")
        kafka_util.send_message(topic="social_network_user_profile", key="social_network_signup", value=user_signup_event.model_dump_json())
        return {"message": "User profile saved successfully", "user": user_profile}
    else:
        raise HTTPException(status_code=400, detail="Invalid or expired Google token")


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
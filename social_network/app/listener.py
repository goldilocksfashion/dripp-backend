import asyncio
import datetime
import uuid
from fastapi import APIRouter, FastAPI, Depends, HTTPException, Request
from events.app.event import Event, EventKind, KafkaUtil
from fastapi.security import OAuth2AuthorizationCodeBearer
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from contextlib import asynccontextmanager
from typing import Dict


config = Config('.env')

loop = asyncio.get_event_loop()
kafka_util = KafkaUtil()

def on_event(event: Event):
    print(f"Received event: {event}")  

loop.run_until_complete(kafka_util.subscribe('social_network_events', on_event))
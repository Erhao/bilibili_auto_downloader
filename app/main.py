import os
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.db.mongo_util import connect_to_mongo, close_mongo_connection
from app.task.worker import start_task_worker
from app.core.config import API_PREFIX_V1
from app.router.video import router as video_router

os.environ["FFMPEG_BINARY"] = "/usr/local/bin/ffmpeg"

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("startup", start_task_worker)

app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(video_router, prefix=API_PREFIX_V1 + '/video')

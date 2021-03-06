import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.storage import init_data
from app.core.config import config
from app.router.video import router as video_router

os.environ["FFMPEG_BINARY"] = config.FFMPEG_BINARY
os.environ['TZ'] = 'Asia/Shanghai'

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.add_event_handler("startup", init_data)

app.include_router(video_router, prefix=config.API_PREFIX_V1 + '/video')

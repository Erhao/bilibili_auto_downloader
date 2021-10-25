import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.storage import init_data
from app.task.worker import bili_task
from app.core.config import config
from app.router.video import router as video_router

os.environ["FFMPEG_BINARY"] = config.FFMPEG_BINARY

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.add_event_handler("startup", init_data)
app.add_event_handler("startup", bili_task.start_task_worker)

app.add_event_handler("shutdown", bili_task.end_task_worker)


app.include_router(video_router, prefix=config.API_PREFIX_V1 + '/video')

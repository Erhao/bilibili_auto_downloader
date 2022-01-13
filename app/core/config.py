import sys
import os
import multiprocessing
from dataclasses import dataclass

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings


load_dotenv(".env")


@dataclass
class Config:
    SERVER_HOST = os.getenv("SERVER_HOST")
    SERVER_PORT = int(os.getenv("SERVER_PORT"))

    API_PREFIX_V1 = "/api"

    ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

    STORAGE_FILE = None

    FFMPEG_BINARY = os.getenv("FFMPEG_BINARY")

    SAVE_PATH = os.getenv("SAVE_PATH") or os.path.join(sys.path[0], '../bilibili_download')

    CPU_COUNT = multiprocessing.cpu_count()

    MAX_THREAD_WORKER = int(os.getenv("MAX_THREAD_WORKER", 5))


config = Config()

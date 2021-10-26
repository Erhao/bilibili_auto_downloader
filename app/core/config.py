import os
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

    SAVE_PATH = os.getenv("SAVE_PATH")


config = Config()

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.core.config import database_name


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


# TODO: need to be discarded and replaced by get_aio_engine
async def get_database() -> AsyncIOMotorClient:
    return db.client


async def get_aio_engine() -> AIOEngine:
    return AIOEngine(motor_client=db.client, database=database_name)

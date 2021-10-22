from odmantic import ObjectId
from typing import Dict
from odmantic import Model
from datetime import datetime

from app.db.mongodb import get_aio_engine


class BaseMongoModel(Model):
    """
    BaseMongoModel
    重写AIOEngine的方法
    """

    @classmethod
    async def find_one(cls, spec):
        engine = await get_aio_engine()
        return await engine.find_one(cls, spec)

    @classmethod
    async def get_from_oid(cls, _id):
        engine = await get_aio_engine()
        spec = {"_id": ObjectId.validate(_id)}
        return await engine.find_one(cls, spec)

    @classmethod
    async def find(cls, spec):
        engine = await get_aio_engine()
        return [record async for record in engine.find(cls, spec)]

    async def save(self):
        engine = await get_aio_engine()
        return await engine.save(self)

    async def save_all(self, records):
        engine = await get_aio_engine()
        return await engine.save_all(records)

    async def delete(self, record):
        engine = await get_aio_engine()
        return await engine.delete(record)

    async def update(self, doc: Dict):
        for key, val in doc.items():
            setattr(self, key, val)
        if self.updated_at:
            self.updated_at = datetime.utcnow()
        return await self.save()

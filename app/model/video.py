from datetime import datetime
from odmantic import Model, Field

from app.model.base import BaseMongoModel


class Video(Model, BaseMongoModel):
    """
    video
    """
    aid: int = Field(description="bilibili aid")
    title: str = Field(default="", description="视频总标题")
    page: int = Field(default=1, description="当前视频页码")
    cid: int = Field(default=0, description="分p id")
    part: str = Field(description="视频标题(单p标题)")
    part_url: str = Field(description="单p url")
    duration: int = Field(description="时长(秒)")
    state: int = Field(default=10, description="状态 10:未开始 50:进行中 100:已完成 -100:错误")
    play_list: list = Field(default=[], description="play_list")
    updated_at: datetime = Field(default=datetime.utcnow())
    created_at: datetime = Field(default=datetime.utcnow())

    class Config:
        collection = "video"

# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field


class ReqMeta(BaseModel):
    """

    """

    page: Optional[int] = Field(0)
    page_size: Optional[int] = Field(10)

# -*- coding: utf-8 -*-
import asyncio
import concurrent.futures
import multiprocessing
import requests
from typing import Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from fastapi import APIRouter, BackgroundTasks

from app.utils.bilibili import get_play_list, mock_down_video, down_video


router = APIRouter()


class Job(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    status: str = "in_progress"
    result: int = None


jobs: Dict[UUID, Job] = {}
cpu_cnt = multiprocessing.cpu_count()


async def run_in_process(fn, *args):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        return await loop.run_in_executor(pool, fn, *args)  # wait and return result


async def start_cpu_bound_task(uid: UUID, videos) -> None:
    # jobs[uid].result = await run_in_process(mock_down_video, *args, **kwargs)
    # jobs[uid].status = "complete"
    for i in range(0, len(videos), cpu_cnt):
        results = await asyncio.gather(
            *[
                run_in_process(down_video, item['aid'], item['cid'], item['play_list'], item['title'], item['part'], item['part_url'], item['page'])
                for item in videos[i:i+cpu_cnt]
            ]
        )


@router.get("/add")
async def add_aid(aid: int, background_tasks: BackgroundTasks):
    """

    :param aid:
    :return:
    """
    start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + str(aid)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    resp = requests.get(start_url, headers=headers).json()
    data = resp['data']

    # 下载全集
    pages = data['pages']

    videos = []
    for idx, item in enumerate(pages):
        doc = {}

        cid = item['cid']
        page = item['page']
        part_url = f"{start_url}&p={str(page)}"
        play_list = get_play_list(part_url, str(cid), quality=80)

        doc['aid'] = aid
        doc['title'] = data['title']
        doc['page'] = page
        doc['cid'] = cid
        doc['part'] = item['part']
        doc['duration'] = item['duration']
        doc['play_list'] = play_list
        doc['part_url'] = part_url
        doc['state'] = 10
        videos.append(doc)

    new_task = Job()
    jobs[new_task.uid] = new_task
    background_tasks.add_task(start_cpu_bound_task, new_task.uid, videos)

    return {"ok": 1}


@router.get("/list")
async def get_task_list():
    pass


@router.get("/data")
async def get_data():
    pass




# -*- coding: utf-8 -*-
import os
import requests
from fastapi import APIRouter, BackgroundTasks

from app.utils.bilibili import get_play_list, run_in_multiprocess
from app.core.config import config


IGNORED_FILES = [".DS_Store"]

router = APIRouter()


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

    background_tasks.add_task(run_in_multiprocess, videos)

    return {"success": 1, "count": len(videos), "new_tasks": [v['part'] for v in videos]}


@router.get("/list")
async def get_saved_list():
    save_path = config.SAVE_PATH
    res = {}
    # 递归遍历save_path下文件
    for title in os.listdir(save_path):
        if title in IGNORED_FILES:
            continue
        res[title] = []
        for file in os.listdir(os.path.join(save_path, title)):
            res[title].append(file)
    for title in res:
        res[title] = sorted(res[title], key=lambda x: int(x.split("__")[0]))
    return res


@router.get("/complete")
async def complete(background_tasks: BackgroundTasks):
    """
    补全未下载的单个视频
    """
    save_path = config.SAVE_PATH
    missing_videos = {}
    for title in os.listdir(save_path):
        if title in IGNORED_FILES:
            continue
        aid = int(title.split("__")[-1])
        missing_videos[aid] = []

        pages = []
        for file in os.listdir(os.path.join(save_path, title)):
            pages.append(int(file.split("__")[-1].split(".")[0]))
            # TODO


@router.get("/data")
async def get_data():
    pass

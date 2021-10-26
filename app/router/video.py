# -*- coding: utf-8 -*-
import requests
from fastapi import APIRouter

from app.utils.bilibili import get_play_list
from app.task.worker import bili_task


router = APIRouter()


@router.get("/add")
async def add_aid(aid: int):
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
        part_url = f"{start_url}/?p={str(page)}"
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

    videos_map = {
        aid: videos
    }
    bili_task.update_data(videos_map)

    return {"ok": 1}




import os
import sys
import urllib.request
import threading
from typing import List
from app.model.video import Video
from apscheduler.schedulers.asyncio import AsyncIOScheduler


# 线程信号量, 限制并发数
S = threading.Semaphore(8)


#  下载视频
def down_video(video_list, title, start_url, page):
    print(f'**** 准备下载第{page}P视频 ****')
    S.acquire()
    num = 1
    currentVideoPath = os.path.join(sys.path[0], 'bilibili_video', title)  # 当前目录作为下载目录
    if not os.path.exists(currentVideoPath):
        os.makedirs(currentVideoPath)
    for i in video_list:
        opener = urllib.request.build_opener()
        # 请求头
        opener.addheaders = [
            # ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  #注意修改host,不用也行
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),  # Range 的值要为 bytes=0- 才能下载完整视频
            ('Referer', start_url),  # 注意修改referer,必须要加的!
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(opener)
        # 创建文件夹存放下载的视频
        if not os.path.exists(currentVideoPath):
            os.makedirs(currentVideoPath)
        # 开始下载
        print(f'#### 开始下载第{page}P视频 ####')
        if len(video_list) > 1:
            urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath, r'{}-{}.flv'.format(title, num)))  # 写成mp4也行  title + '-' + num + '.flv'
        else:
            urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath, r'{}.flv'.format(title)))  # 写成mp4也行  title + '-' + num + '.flv'
        num += 1
    S.release()


def multi_thread_download(aid, videos):
    """
    多线程下载
    :param aid:
    :param videos:
    :return:
    """
    thread_pool = []
    for video in videos:
        play_list = video.play_list
        title = video.title
        part_url = video.part_url
        page = video.page
        
        th = threading.Thread(target=down_video, args=(play_list, title, part_url, page))
        thread_pool.append(th)
        
    for th in thread_pool:
        th.start()

    for th in thread_pool:
        th.join()


async def do_job():
    """

    :return:
    """
    spec = {
        'state': 10  # 未下载
    }
    undownload_videos: List[Video] = await Video.find(spec)

    video_group = {}
    for video in undownload_videos:
        aid = video.aid
        videos = video_group.get(aid, [])
        videos.append(video)
        video_group[aid] = videos

    for aid, videos in video_group.items():
        multi_thread_download(aid, videos)


def start_task_worker():
    """

    :return:
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(do_job, 'interval', seconds=3)
    scheduler.start()

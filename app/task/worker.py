import os
import sys
import threading
import urllib.request
import json
from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import config


# 线程信号量, 限制并发数
S = threading.Semaphore(5)


class BiliTask:
    def __init__(self):
        self.data = None
        self.scheduler: BackgroundScheduler
        self.interval = 10
        self.counter = 0
        self.max_counter = 60  # 每隔self.interval * self.max_counter秒向文件写入一次
        self.stop = False  # 停止标志位

    def update_data(self, doc):
        """

        :param doc:
        :return:
        """
        self.data.update(doc)

    def down_video(self, aid, cid, video_list, title, part, start_url, page):
        """
        下载视频
        :param aid:
        :param cid:
        :param video_list:
        :param title:
        :param part:
        :param start_url:
        :param page:
        :return:
        """
        S.acquire()
        print(f'#### downloading {part} ####')

        # 更新state为50
        videos = self.data[aid]
        for video in videos:
            if video['cid'] == cid:
                video['state'] = 50

        num = 1
        currentVideoPath = os.path.join(config.SAVE_PATH if config.SAVE_PATH else sys.path[0], 'bilibili_video', title)  # 当前目录作为下载目录
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
            if len(video_list) > 1:
                urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath, r'{}-{}.flv'.format(part, num)))  # 写成mp4也行  title + '-' + num + '.flv'
            else:
                urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath, r'{}.flv'.format(part)))  # 写成mp4也行  title + '-' + num + '.flv'
            num += 1

        # 更新state为100
        for video in videos:
            if video['cid'] == cid:
                video['state'] = 100
        print(f'#### finished {part} ####')
        S.release()

    def scan(self):
        """

        :return:
        """
        print('worker running...')
        self.counter += 1

        if self.data is None:
            with open(config.STORAGE_FILE, "r") as f:
                self.data = json.load(f)

        for aid, videos in self.data.items():
            print(f'#### 准备下载aid: {aid} ####')
            for video in videos:
                if video['state'] != 10:
                    continue

                aid = aid
                cid = video['cid']
                play_list = video['play_list']
                title = video['title']
                part = video['part']
                part_url = video['part_url']
                page = video['page']
                self.scheduler.add_job(self.down_video, 'date', args=[aid, cid, play_list, title, part, part_url, page])

        if self.counter > self.max_counter:
            self.counter = 0
            with open(config.STORAGE_FILE, 'w') as f:
                json.dump(self.data, f, ensure_ascii=False, separators=(',', ':'))

    def start_task_worker(self):
        """

        :return:
        """
        self.scheduler = BackgroundScheduler(job_defaults={
            'coalesce': False,
            'max_instances': 1
        })
        self.scheduler.add_job(self.scan, 'interval', seconds=self.interval)
        self.scheduler.start()

    def end_task_worker(self):
        """

        :return:
        """
        # jobs = self.scheduler.get_jobs()
        # self.scheduler.print_jobs()
        # for job in jobs:
        #     self.scheduler.pause_job(job.id)
        # self.scheduler.remove_all_jobs()
        self.scheduler.shutdown(wait=False)
        with open(config.STORAGE_FILE, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, separators=(',', ':'))


bili_task = BiliTask()

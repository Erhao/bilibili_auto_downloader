import os
import sys
import threading
import hashlib
import requests
import time
import urllib.request

os.environ["FFMPEG_BINARY"] = "/usr/local/bin/ffmpeg"

from app.core.config import config


# 线程信号量, 限制并发数
S = threading.Semaphore(5)


def get_play_list(start_url, cid, quality):
    entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
    appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
    params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
    chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
    url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
    headers = {
        'Referer': start_url,  # 注意加上referer
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    html = requests.get(url_api, headers=headers).json()
    play_list = []
    for i in html['durl']:
        play_list.append(i['url'])
    # print(play_list)
    return play_list


# TODO: decorate with retry decorator
def down_video(aid, cid, video_list, title, part, start_url, page):
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


# TODO: decorate with retry decorator
def mock_down_video(aid, cid, video_list, title, part, start_url, page):
    S.acquire()
    print('=============== MOCK DOWNLOAD start =================')
    time.sleep(5)
    print('!!!!!!!!!!!! MOCK DOWNLOAD END !!!!!!!!!!!!!')
    S.release()

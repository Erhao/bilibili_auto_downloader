import os
import threading
import hashlib
import requests
import time
import urllib.request
from retry import retry

os.environ["FFMPEG_BINARY"] = "/usr/local/bin/ffmpeg"

from app.core.config import config


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
    return play_list


@retry(tries=3, delay=5)
def down_video(param):
    """
    下载视频
    :param param:
    :return:
    """
    aid = param['aid']
    cid = param['cid']
    video_list = param['play_list']
    title = param['title']
    part = param['part']
    start_url = param['part_url']
    page = param['page']

    print(f'#### downloading {part} ####')

    download_path = os.path.join(config.SAVE_PATH, "{}__{}".format(title, str(aid)))
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    for url in video_list:
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
        # 开始下载
        if len(video_list) > 1:
            urllib.request.urlretrieve(url=url, filename=os.path.join(download_path, r'{}-{}.flv'.format(part, 1)))  # 写成mp4也行
        else:
            urllib.request.urlretrieve(url=url, filename=os.path.join(download_path, r'{}__{}.flv'.format(page, part)))  # 写成mp4也行

    print(f'#### finished {part} ####')


# TODO: decorate with retry decorator
def mock_down_video(aid, cid, video_list, title, part, start_url, page):
    print('=============== MOCK DOWNLOAD start =================')
    time.sleep(5)
    print('!!!!!!!!!!!! MOCK DOWNLOAD END !!!!!!!!!!!!!')

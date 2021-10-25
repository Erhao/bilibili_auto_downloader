import os
import sys
import json

from app.core.config import config


def init_data():
    """
    初始化json文件
    :return:
    """
    project_path = sys.path[0]
    file = os.path.join(project_path, 'bili.json')
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f, ensure_ascii=False, separators=(',', ':'))

    config.STORAGE_FILE = file

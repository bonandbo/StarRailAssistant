'''
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2023-05-15 21:45:43
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-06-02 18:09:56
Description: 

Copyright (c) 2023 by Night-stars-1, All Rights Reserved. 
'''
import os
import re
import sys
import orjson
import locale
import gettext
from loguru import logger

message = ""

def normalize_file_path(filename):
    # 尝试在当前目录下读取文件
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    if os.path.exists(file_path):
        return file_path
    else:
        # 如果当前目录下没有该文件，则尝试在上一级目录中查找
        parent_dir = os.path.dirname(current_dir)
        file_path = os.path.join(parent_dir, filename)
        if os.path.exists(file_path):
            return file_path
        else:
            # 如果上一级目录中也没有该文件，则返回None
            return None
        
def read_json_file(filename: str, path=False):
    """
    illustrate:
         read file
    parameter:
        :param filename: file name
        :param path: Whether to return the path
    """
    # Find the absolute path of the file
    file_path = normalize_file_path(filename)
    if file_path:
        with open(file_path, "rb") as f:
            data = orjson.loads(f.read())
            if path:
                return data, file_path
            else:
                return data
    else:
        return {}
    
def get_folder(path) -> list[str]:
    """
    Get a list of folders under a folder
    """
    for root, dirs, files in os.walk(path):
        return dirs

loc = locale.getdefaultlocale()
print('dieptt-----')
print(loc) # return tuple ('en_US', 'cp1252') with normal non chinese pc
if loc[0] not in get_folder("locale"):
    #dieptt
    my_loc = list(loc)
    my_loc[0] = "zh_CN"
    loc = tuple(my_loc)
    # loc[0] = "zh_CN"
t = gettext.translation('sra', 'locale', languages=[loc[0]])
_ = t.gettext

def get_message(*arg):
    """
    illustrate:
        collect messages and return
    return:
        collected messages
    """
    global message
    if arg:
        content = arg[0][:-1].replace("\x1b[0;34;40m","").replace("-1\x1b[0m","")
        print("dieptt: content = " + content)
        if re.match(_(r'开始(.*)锄地'),content):
            message += f"\n{content}"
    return message

data = read_json_file("config.json")
VER = str(data.get("star_version",0))+"/"+str(data.get("temp_version",0))+"/"+str(data.get("map_version",0))
level = data.get("level","INFO")
log = logger
dir_log = "logs"
path_log = os.path.join(dir_log, _('logfile.log'))
logger.remove()
logger.add(sys.stdout, level=level, colorize=True,
            format="<cyan>{module}</cyan>.<cyan>{function}</cyan>"
                    ":<cyan>{line}</cyan> - "+f"<cyan>{VER}</cyan> - "
                    "<level>{message}</level>"
            )

#logger.add(get_message, level=level,format="{message}")

logger.add(path_log,
            format="{time:HH:mm:ss} - "
                    "{level}\t| "
                    "{module}.{function}:{line} - "+f"<cyan>{VER}</cyan> - "+" {message}",
            rotation='0:00', enqueue=True, serialize=False, encoding="utf-8", retention="10 days")

import os
import orjson
import gettext
import locale

from .log import log

CONFIG_FILE_NAME = "config.json"


def normalize_file_path(filename):
    # Attempt to read the file in the current directory
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    if os.path.exists(file_path):
        return file_path
    else:
        # If the file does not exist in the current directory, try to find it in the upper directory
        parent_dir = os.path.dirname(current_dir)
        file_path = os.path.join(parent_dir, filename)
        if os.path.exists(file_path):
            return file_path
        else:
            # If the file does not exist in the previous directory, return None
            return None


def read_json_file(filename: str, path=False) -> dict:
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
        init_config_file(1920, 1080, filename)
        return read_json_file(filename, path)


def modify_json_file(filename: str, key, value):
    """
    illustrate:
        write to file
    parameter:
        :param filename: file name
        :param key: key
        :param value: value
    """
    # read first, write later
    data, file_path = read_json_file(filename, path=True)
    data[key] = value
    with open(file_path, "wb") as f:
        f.write(orjson.dumps(data, option=orjson.OPT_PASSTHROUGH_DATETIME | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2))


def init_config_file(real_width, real_height, file_name = CONFIG_FILE_NAME):
    if file_name == CONFIG_FILE_NAME:
        with open(CONFIG_FILE_NAME, "wb+") as f:
            log.info("Configuration initialization")
            f.write(
                orjson.dumps(
                    {
                        "real_width": real_width,
                        "auto_battle_persistence": 0,
                        "real_height": real_height,
                        "github_proxy": "",
                        "rawgithub_proxy": "",
                        "webhook_url": "",
                        "start": False,
                        "temp_version": "0",
                        "star_version": "0",
                        "open_map": "m",
                        "level": "INFO",
                        "adb": "127.0.0.1:62001",
                        "adb_path": "temp\\adb\\adb",
                        "proxies": ""
                    },option = orjson.OPT_PASSTHROUGH_DATETIME | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2
                )
            )
    else:
        with open(file_name, "wb+") as f:
            log.info("Configuration initialization")
            f.write(
                orjson.dumps(
                    {},option = orjson.OPT_PASSTHROUGH_DATETIME | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2
                )
            )


def get_file(path, exclude=[], exclude_file=None, get_path=False) -> list[str]:
    """
    Get the files under the folder
    """
    if exclude_file is None:
        exclude_file = []
    file_list = []
    for root, dirs, files in os.walk(path):
        add = True
        for i in exclude:
            if i in root:
                add = False
        if add:
            for file in files:
                add = True
                for ii in exclude_file:
                    if ii in file:
                        add = False
                if add:
                    if get_path:
                        path = root + "/" + file
                        file_list.append(path.replace("//", "/"))
                    else:
                        file_list.append(file)
    return file_list

def get_folder(path) -> list[str]:
    """
    Get a list of folders under a folder
    """
    for root, dirs, files in os.walk(path):
        return dirs

loc = locale.getdefaultlocale()
if loc[0] not in get_folder("locale"):
    #dieptt
    my_loc = list(loc)
    my_loc[0] = "zh_CN"
    loc = tuple(my_loc)
    # loc[0] = "zh_CN"
t = gettext.translation('sra', 'locale', languages=[loc[0]])
_ = t.gettext

def add_key_value(dictionary, key, value, position):
    """
    illustrate:
        Add a key-value pair at the specified location
    parameter:
        :param dictionary The dictionary that needs to be added
        :param key: key
        :param value: value
        :param position: The position to be added
    return:
        new_dictionary: added dictionary
    """
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    keys.insert(position, key)
    values.insert(position, value)
    new_dictionary = dict(zip(keys, values))
    return new_dictionary
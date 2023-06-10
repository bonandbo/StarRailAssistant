'''
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2023-05-29 16:54:51
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-06-08 20:44:45
Description: 

Copyright (c) 2023 by Night-stars-1, All Rights Reserved. 
'''
import logging
import traceback
import tkinter as tk
from tkinter import messagebox
root = tk.Tk()
root.withdraw()
try:
    from utils.exceptions import Exception
    import time
    import flet as ft
    from re import sub
    from cryptography.fernet import Fernet
    from flet_core import MainAxisAlignment, CrossAxisAlignment

    from utils.log import log,level
    from utils.map import Map as map_word
    from utils.config import read_json_file,modify_json_file , CONFIG_FILE_NAME, _
    from utils.update_file import update_file
    from utils.calculated import calculated
    from get_width import get_width
    from Honkai_Star_Rail import SRA
except:
    messagebox.showerror("run error", traceback.format_exc())

sra = SRA()

def page_main(page: ft.Page):
    '''
    if page.session.contains_key("updata_log"):
        page.session.remove("updata_log")
    '''
    map_dict = map_word(platform=_("simulator")).map_list_map
    VER = str(read_json_file("config.json").get("star_version",0))+"/"+str(read_json_file("config.json").get("temp_version",0))+"/"+str(read_json_file("config.json").get("map_version",0))
    img_url = [
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4//8/AAX+Av4N70a4AAAAAElFTkSuQmCC",
        "https://upload-bbs.miyoushe.com/upload/2023/04/04/341589474/5d2239e0352a9b3a561efcf6137b6010_8753232008183647500.jpg",
        "https://upload-bbs.miyoushe.com/upload/2023/05/31/272930625/2c884f70bcd35555b5ad59163df6a952_2976928227773983219.jpg"
    ]
    def add(*args,**kargs):
        """
        illustrate:
            Rewrite of the page submit element
        """
        if type(args[0]) != list:
            args = [i for i in args]
        else:
            args = args[0]
        if not kargs.get("left_page", None):
            kargs["left_page"] = []
        bg_img.width = page.window_width
        bg_img.height = page.window_height-58
        about_ib.width = page.window_width
        about_ib.height = page.window_height-58
        platform.content.width = page.window_width
        platform.content.height = page.window_height-58
        first_page = [
                bg_img,
                ft.Row(
                    [
                        ft.Column(
                            args,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ]+kargs['left_page']
        return page.add(
            ft.Stack(first_page)
        )

    def radiogroup_changed(e):
        """
        illustrate:
            Change the content of the map tab
        parameter:
            :param word_select_rg.value planet selection number
            :param map_select_dd.options list of maps for the selected planet
            :param map_select_dd.value The default map value of the selected planet
        """
        map_select_dd.options=[ft.dropdown.Option(i) for i in list(map_dict[word_select_rg.value].values())]
        map_select_dd.value = list(map_dict[word_select_rg.value].values())[0]
        page.update()

    def add_log(message):
        """
        说明；
            log在gui上输出
        """
        page.title = _("Star Railway Assistant-{VER}").format(VER=VER)
        log_text.controls.append(ft.Text(message[:-1]))
        page.update()

    if not page.session.get("updata_log"):
        log.add(add_log, level=level, colorize=True,
                format="{module}.{function}"
                        ":{line} - {message}"
                )

    def get_mess(num:int):
        data = [b"gAAAAABkd00kmO4Lkj6jdx88m9HqzU1RQC85SfB_h19TI1WP5pkLZHlA1nauTYBU6ga5hRFlKas9i-rFaC-Q0PPkLd_NLSR9sh8TbGBRE952hIHecP9uwyufZrWwhmdFg4EzlJR4Us64ojJZBm6DkfXSRS2syqbhlg==", b"gAAAAABkd05QbDIzYa9ebhDd6oL1ScrWhuQv8Vay1zj3c3NenzXIpGvWcmiNsNz7nYGJg2G9KJ9edRahlVASebG6zm0YTP-XeJQlgQzChoRnr606FZg0feQSzQVz_Rzri1j_HAmHQR20",b"gAAAAABkd0SIKuiC3bqUwWmhWFr_uqlWUMmv1rclIJNhvr-GteOiT_ahz3Z6GKXoCL-IG0G8_AReT9ISb2PUI_TMXGxWGEW3YrmRy5F5kiQCLORXn8mA7GE="]
        cp = Fernet(b"VKcGP_EkdRbXTe8aAVcjKoI2fULVuyrSX8Le-QZsDOA=")
        return cp.decrypt(data[num]).decode('utf-8')

    def start(e):
        def send_log(e):
            '''
            if log.value:
                log.value += f"\n666"*66
            else:
                log.value = "666"
            '''
            page.update()

        page.clean()
        page.add(
            log_text,
            ft.ElevatedButton(_("Return"), on_click=send_log),
        )

    def map_confirm(e):
        """
        说明:
            选择完Map开始跑图
        参数:
            :param word_select_rg.value 星球选择的编号
            :param map_select_dd.value 所选星球的Map编号
            :param start: 开始Map编号
        """
        keys = list(map_dict[word_select_rg.value].keys())
        values = list(map_dict[word_select_rg.value].values())
        start = word_select_rg.value+"-"+keys[values.index(map_select_dd.value)]
        log.info(start)
        # log显示
        page.clean()
        page.vertical_alignment = "START"
        page.horizontal_alignment = "START"
        add(log_text)
        if platform.value == _("PC"):
            calculated(_("崩坏：星穹铁道"), _("PC")).switch_window()
            time.sleep(0.5)
            get_width(_("崩坏：星穹铁道"))
            import pyautogui # 缩放纠正
        map_word(platform=platform.value).auto_map(start)
        add(ft.ElevatedButton(_("Return"), on_click=to_page_main))

    def to_page_main(e):
        """
        说明:
            Return主页
        """
        updata_log = page.session.get("updata_log")
        if updata_log:
            log.remove(updata_log)
            page.session.set("updata_log", False)
        page_main(page)

    def word(e):
        """
        说明:
            Map选择界面
        """
        page.clean()
        add(
            ft.Text(_("Star Railway Assistant"), size=50),
            ft.Text(_("Open World"), size=30),
            ft.Text(VER, size=20),
            word_select_rg,
            map_select_dd,
            ft.ElevatedButton(_("Confirm"), on_click=map_confirm),
            ft.ElevatedButton(_("Return"), on_click=to_page_main),
            left_page=[platform]
        )

    def updata(e):
        """
        illustrate:
             update interface
        """
        pb.width = 100
        ghproxy = read_json_file(CONFIG_FILE_NAME, False).get('github_proxy', "")
        rawghproxy = read_json_file(CONFIG_FILE_NAME, False).get('rawgithub_proxy', "")
        # asyncio.run(check_file(ghproxy, "map"))
        # asyncio.run(check_file(ghproxy, "temp"))
        data = {
            _("Screenplay"):{
                'url_proxy': ghproxy,
                'raw_proxy': rawghproxy,
                'skip_verify': False,
                'type': "star",
                'version': "main",
                'url_zip': "https://github.com/Starry-Wind/StarRailAssistant/archive/refs/heads/main.zip",
                'unzip_path': ".",
                'keep_folder': ['.git', 'logs', 'temp', 'map', 'tmp', 'venv'],
                'keep_file': ['config.json', 'version.json', 'star_list.json', 'README_CHT.md', 'README.md'],
                'zip_path': "StarRailAssistant-main/",
                'name': _("Screenplay")
            },
            _("Map"):{
                'url_proxy': ghproxy,
                'raw_proxy': rawghproxy,
                'skip_verify': False,
                'type': "map",
                'version': "map",
                'url_zip': "https://raw.githubusercontent.com/Starry-Wind/StarRailAssistant/map/map.zip",
                'unzip_path': "map",
                'keep_folder': [],
                'keep_file': [],
                'zip_path': "map/",
                'name': _("Map")
            },
            _("Picture"):{
                'url_proxy': ghproxy,
                'raw_proxy': rawghproxy,
                'skip_verify': False,
                'type': "temp",
                'version': "map",
                'url_zip': "https://raw.githubusercontent.com/Starry-Wind/StarRailAssistant/map/temp.zip",
                'unzip_path': "temp",
                'keep_folder': [],
                'keep_file': [],
                'zip_path': "map/",
                'name': _("Picture")
            },
        }
        def add_updata_log(message):
            message = message[:-1]
            text.value = sub(r"(.{67})", "\\1\r\n", message)
            pb.width = len(message)*13.2 if len(message) <= 50 else 50*13.2
            page.update()
        def up_data(e):
            log.remove()
            updata_log = log.add(add_updata_log, level=level, colorize=True,
                    format="{message}")
            page.session.set("updata_log", updata_log)
            page.clean()
            up_close = ft.ElevatedButton(_("Return"), disabled=True, on_click=to_page_main)
            add(
                ft.Text(_("Star Railway Assistant"), size=50),
                ft.Text(_("Check for Updates"), size=30),
                ft.Text(VER, size=20),
                ft.Column([ text, pb]),
                up_close
            )
            update_file(page,pb).update_file_main(**data[e.control.text])
            up_close.disabled = False
            page.update()
        Column.controls = [ft.ElevatedButton(i, on_click=up_data) for i in data]
        page.clean()
        add(
            ft.Text(_("Star Railway Assistant"), size=50),
            ft.Text(_("Check for Updates"), size=30),
            ft.Text(VER, size=20),
            Column,
            ft.ElevatedButton(_("Return"), on_click=to_page_main)
        )

    def set_config(e):
        """
        说明:
            硬编码配置编辑，带优化
        """
        config = read_json_file(CONFIG_FILE_NAME)
        simulator = {
            "逍遥游": "127.0.0.1:21503",
            "夜神simulator": "127.0.0.1:62001",
            "海马玩simulator": "127.0.0.1:26944",
            "天天simulator": "127.0.0.1:6555",
            "雷电安卓simulator": "127.0.0.1:5555",
            "安卓simulator大师": "127.0.0.1:54001",
            "网易mumusimulator": "127.0.0.1:7555",
            "BlueStacks": "127.0.0.1:5555",
            "天天安卓simulator": "127.0.0.1:5037",
        }
        github_proxy_list = ['https://ghproxy.com/', 'https://ghproxy.net/', 'hub.fgit.ml', '']
        rawgithub_proxy_list = ['https://ghproxy.com/', 'https://ghproxy.net/', 'raw.fgit.ml', 'raw.iqiq.io', '']
        simulator_keys = list(simulator.keys())
        simulator_values = list(simulator.values())
        user_adb = config.get("adb", "127.0.0.1:62001")
        if user_adb not in simulator_values:
            simulator_values.append(user_adb)
            simulator_keys.append(_("自定义"))
            simulator[_("自定义")] = user_adb
        adb = simulator_keys[simulator_values.index(user_adb)]
        github_proxy = config.get("github_proxy", "")
        rawgithub_proxy = config.get("rawgithub_proxy", "")
        open_map = config.get("open_map", "m")
        level = config.get("level", "INFO")
        adb_path = config.get("adb_path", "temp\\adb\\adb")
        simulator_dd = ft.Dropdown(
                label=_("simulator"),
                hint_text=_("选择你运行的simulator"),
                options=[ft.dropdown.Option(i) for i in list(simulator.keys())],
                value=adb,
                width=200,
            )
        github_proxy_dd = ft.Dropdown(
                label=_("GitHub proxy"),
                hint_text=_("GitHub proxy地址"),
                options=[ft.dropdown.Option(i) for i in github_proxy_list],
                value=github_proxy,
                width=200,
            )
        rawgithub_proxy_dd = ft.Dropdown(
                label=_("RAWGITHUB Proxy"),
                hint_text=_("RAWGITHUB Proxy地址"),
                options=[ft.dropdown.Option(i) for i in rawgithub_proxy_list],
                value=rawgithub_proxy,
                width=200,
            )
        level_dd = ft.Dropdown(
                label=_("Log Level"),
                hint_text=_("Log Level"),
                options=[
                    ft.dropdown.Option("INFO"),
                    ft.dropdown.Option("DEBUG"),
                    ft.dropdown.Option("ERROR")
                ],
                value=level,
                width=200,
            )
        adb_path_text = ft.Text(adb_path, size=20)
        def pick_files_result(e: ft.FilePickerResultEvent):
            adb_path_text.value = e.files[0].path
            page.update()
        pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
        open_map_tf = ft.TextField(label=_("Open the Map button"), value=open_map, width=200)
        def save(e):
            modify_json_file(CONFIG_FILE_NAME, "github_proxy", github_proxy_dd.value)
            modify_json_file(CONFIG_FILE_NAME, "rawgithub_proxy", rawgithub_proxy_dd.value)
            modify_json_file(CONFIG_FILE_NAME, "open_map", open_map_tf.value)
            modify_json_file(CONFIG_FILE_NAME, "level", level_dd.value)
            modify_json_file(CONFIG_FILE_NAME, "adb", simulator[simulator_dd.value])
            modify_json_file(CONFIG_FILE_NAME, "adb_path", adb_path_text.value)
            to_page_main(page)
        page.clean()
        page.overlay.append(pick_files_dialog)
        add(
            ft.Text(_("Star Railway Assistant"), size=50),
            ft.Text(_("Open World"), size=30),
            ft.Text(VER, size=20),
            simulator_dd,
            github_proxy_dd,
            rawgithub_proxy_dd,
            level_dd,
            open_map_tf,
            ft.Row(
                [
                    adb_path_text,
                    ft.ElevatedButton(
                        _("Select a document"),
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: pick_files_dialog.pick_files(
                            allowed_extensions=["exe"],
                            allow_multiple=True
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.ElevatedButton(_("Save"), on_click=save),
        )

    def change__img(e):
        """
        说明:
            切换背景
        """
        img_v = img_url.index(bg_img.src)
        img_v = 0 if img_v+1 >= len(img_url) else img_v+1
        page.session.set("img_v", img_v)
        bg_img.src = img_url[img_v]
        modify_json_file(CONFIG_FILE_NAME, "img", img_v)
        page.update()

    def about(e):
        """
        说明:
            关于界面
        """
        page.clean()
        add(
            ft.Text(_("Star Railway Assistant"), size=50),
            ft.Text(_("关于"), size=30),
            ft.Text(VER, size=20),
            ft.Text(get_mess(0), size=40, color=ft.colors.RED),
            ft.Text(get_mess(1), size=40, color=ft.colors.RED),
            ft.Text(
                disabled=False,
                size=25,
                spans=[
                    ft.TextSpan(get_mess(2)),
                    ft.TextSpan(
                        "https://github.com/Starry-Wind/StarRailAssistant",
                        ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE,color = ft.colors.BLUE),
                        url="https://github.com/Starry-Wind/StarRailAssistant",
                    ),
                ],
            ),
            ft.ElevatedButton(_("Return"), on_click=to_page_main),
        )

    def on_window_event(e):
        """
        illustrate:
            Fired when the application's native OS window changes its state: position, size, maximized, minimized, etc.
        """
        if e.data in ["maximize","unmaximize"]:
            bg_img.width = page.window_width
            bg_img.height = page.window_height-58
            about_ib.width = page.window_width
            about_ib.height = page.window_height-58
            platform.content.width = page.window_width
            platform.content.height = page.window_height-58
            page.update()

    # 界面参数区
    text = ft.Text()
    pb = ft.ProgressBar(width=400) #进度条 宽度可更改 pb.width = 400
    ## 更新选项卡
    Column = ft.Column()
    log_text = ft.Column()
    # 背景Picture
    if not page.session.get("start"):
        img_url2 = img_url[read_json_file(CONFIG_FILE_NAME).get("img",0)]
    elif page.session.get("img_v"):
        img_url2 = img_url[page.session.get("img_v")]
    else:
        img_url2 = img_url[0]
    bg_img = ft.Image(
        src=img_url2,
        width=page.window_width,
        height=page.window_height-58,
        fit=ft.ImageFit.FIT_HEIGHT,
        repeat=ft.ImageRepeat.NO_REPEAT,
        gapless_playback=False,
    )
    # 关于按钮
    about_ib = ft.Column(
                [
                    ft.IconButton(
                        icon=ft.icons.CHANGE_CIRCLE_OUTLINED,
                        icon_color="blue200",
                        icon_size=35,
                        tooltip=_("switch background"),
                        on_click=change__img
                    ),
                    ft.IconButton(
                        icon=ft.icons.INFO_OUTLINED,
                        icon_color="blue200",
                        icon_size=35,
                        tooltip=_("about"),
                        on_click=about
                    )
                ],
                width=page.window_width,
                height=page.window_height-60,
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.END,
                spacing=0
            )
    # %% 运行设备选择
    platform = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value=_("PC"), label=_("PC")),
                ft.Radio(value=_("simulator"), label=_("simulator")) #dieptt
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=0
        ),
        value=_("PC")
    )
    ## 星球选项卡
    word_select_rg = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="1", label=_("空间站「黑塔」")),
                ft.Radio(value="2", label=_("Jarlio-VI")),
                ft.Radio(value="3", label=_("Loufu"))
            ],
            alignment=MainAxisAlignment.CENTER
        ),
        on_change=radiogroup_changed,
        value="1"
    )
    ## Map选项卡
    map_select_dd = ft.Dropdown(
        width=100,
        label=_("Map"),
        hint_text=_("Select Map"),
        options=[ft.dropdown.Option(i) for i in list(map_dict.get('1', {}).values())],
        value=list(map_dict.get('1', {"no":""}).values())[0]
    )
    # %%
    page.clean()
    page.title = _("Star Railway Assistant")
    page.scroll = "AUTO"
    page.theme = ft.Theme(font_family="Verdana")
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    if not page.session.get("start"):
        page.window_min_width = 800
        page.window_width = 800
        page.window_height = 600
        page.window_min_height = 600
    page.session.set("start", True)
    page.on_window_event = on_window_event
    page.fonts = {
        "Kanit": "temp/fonts/Kanit-Bold.ttf",
    }

    page.theme = ft.Theme(font_family="Kanit")
    sra.option_dict = {
    }
    button_dict = sra.run_plugins()[0]
    add(
        [
            ft.Text(_("Star Railway Assistant"), size=50),
            ft.Text(VER, size=20),
            ft.ElevatedButton(_("Open World"), on_click=word),
            ft.ElevatedButton(_("simulated universe")),
        ]+[ft.ElevatedButton(i, on_click=lambda x:button_dict[i](page)) for i in list(button_dict.keys())]+
        [
            ft.ElevatedButton(_("update resources"), on_click=updata),
            ft.ElevatedButton(_("edit configuration"), on_click=set_config),
        ],
        left_page=[about_ib]
    )

try:
    sra.load_plugin()
    ft.app(target=page_main)
except KeyboardInterrupt:
    ...
except:
    log.error(traceback.format_exc())
    messagebox.showerror("run error", traceback.format_exc())
finally:
    sra.stop()
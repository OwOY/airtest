# -*- encoding=utf8 -*-
__author__ = "jingm"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from random import randint
from random import uniform
import os
import codecs
import pymongo
import datetime
import shutil
import logging
import multiprocessing as mp
import sys
import parser
class use_mobile:
    
    logger = logging.getLogger("airtest")
    logger.setLevel(logging.ERROR)
    client = pymongo.MongoClient('192.168.1.141')
    collection = client['youtube_post_OK']['video']
    collection1 = client['youtube_account_limit_david']['account']
    collection1.create_index([("time_decline", pymongo.ASCENDING)], expireAfterSeconds=21600)

    def __init__(self, nox_port, path):
        self.nox_port = nox_port
        self.path = path
        self.main()

    def clean_devices(self):
        os.system(f'adb -s 127.0.0.1:{self.nox_port} shell "rm -rf /sdcard/DCIM/Camera/Video/*"')
        os.system(f'adb -s 127.0.0.1:{self.nox_port} shell "am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard"')
        sleep(5)

    def reset_devices(self):
        print(f'{self.nox_port}================================================{self.path}')
        os.system(f'adb -s 127.0.0.1:{self.nox_port} shell "rm -rf /sdcard/DCIM/Camera/Video/*"')
        os.system(f'adb -s 127.0.0.1:{self.nox_port} shell "am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard"')
        os.system(f'adb -s 127.0.0.1:{self.nox_port} shell "am force-stop com.google.android.youtube"')
        sleep(10)
        
    def connect_poco(self):   
 
        if not cli_setup():
            auto_setup(__file__, logdir=None, devices=[
            f"android://127.0.0.1:5037/127.0.0.1:{self.nox_port}?cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=MINITOUCH",
    ])

        #connect_device(f'Android://127.0.0.1:5037/127.0.0.1:{self.nox_port}?cap_method=JAVACAP^&^&ori_method=ADBORI')
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        return poco
    
    def find_utube(self, poco):
        rest = randint(1, 2)
        while True:
            times = 0
            if poco(text = 'YouTube').exists():
                poco(text = "YouTube").click()
                break
            elif times == 5:
                print('找不到Youtube')
                break
            else:
                poco.swipe([0.8, 0.5], [0.3, 0.5], duration = 0.3)

            times += 1
            sleep(5)
        while True:
            if poco(desc = "YouTube").exists():
                break
            else:
                sleep(2)
        poco(name = "媒體庫").click()
        sleep(rest)
        if poco(text = "你的影片").exists():
            poco(text = "你的影片").click()
        else:
            poco(text = "我的影片").click()
        sleep(rest)

    def push_video_in_mobile(self):

        for video in os.listdir(f'{self.path}'):
            if '.mp4' in video:
                os.system(f'adb -s 127.0.0.1:{self.nox_port} push {self.path}/{video} /sdcard/DCIM/Camera/Video/{video}')
                os.system(f'adb -s 127.0.0.1:{self.nox_port} shell "am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/DCIM/Camera/Video/{video}"')
                


    def post_video(self, poco):
        rest = randint(1, 2)
        number = 0
        repeat_title = ''
        repeat_times = 0
        sleep(10)
        
        while True:
            rest = randint(3,7)
            try:
                if poco(name = "建立").exists():
                    poco(name = "建立").click()
                else:
                    poco(desc = "建立影片或發表貼文").click()
                sleep(1)
                poco("上傳影片").click()
                sleep(rest)
            except:
                pass
            
            title = poco("com.google.android.youtube:id/media_grid_recycler_view").child("android.widget.FrameLayout")[number].child("com.google.android.youtube:id/thumb_image_view_parent").child("com.google.android.youtube:id/thumb_image_view").attr('desc')
            title = title.replace('.mp4','')
            mongo_data = self.collection.find({})
            get_mongo_title_list = []
            for data in mongo_data:
                get_mongo_title_list.append(data['title'])
                

            if title not in get_mongo_title_list: 
                poco("com.google.android.youtube:id/media_grid_recycler_view").child("android.widget.FrameLayout")[number].click()
                self.set_video_info(title, poco)
                
                youtube_url = self.get_youtube_url(poco)
                print(f'{title} 上傳成功')
                shutil.rmtree(f'{self.path}')
                
                now = datetime.datetime.now()
                current_time = now.strftime("%H:%M:%S") 
                
                self.collection.insert_one({'url': youtube_url,\
                'title':title,\
                'time':f"{datetime.date.today()}_{current_time}"})

                collection_port_post = self.client['youtube_post_OK'][f'{self.nox_port}']
                collection_port_post.insert_one({'url': youtube_url,\
                'title':title,\
                'time':f"{datetime.date.today()}_{current_time}"})

                collection_post_today = self.client['youtube_post_OK']['today']
                posted_list = [account['port'] for account in collection_post_today.find()]
                if port not in posted_list:
                    collection_post_today.insert_one({'port':self.nox_port})

            else:
                print(f'{title} 影片已上傳過')
                poco('向上瀏覽').click()

                self.client['youtube_post_error']['repeat'].insert_one({'url': youtube_url,\
                'title':title,\
                'time':f"{datetime.date.today()}_{current_time}"})

                sleep(1)
                os.system(f'adb -s 127.0.0.1:{self.nox_port} shell "rm /sdcard/DCIM/Camera/Video/{title}.mp4"')
                os.system(f'adb -s 127.0.0.1:{self.nox_port} shell "am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard"')
                shutil.rmtree(f'{self.path}')
        os._exit(0)

    def set_video_info(self, title, poco):
        rest = randint(1, 2)
        key_in = randint(3, 8)
        post_rest = uniform(15.0, 18.0)
        sleep(key_in)
        poco("android.widget.EditText").set_text(title)
        sleep(rest)
        
        poco("android.widget.LinearLayout").offspring("android:id/content").offspring("com.google.android.youtube:id/elements_fragment").child("android.view.View").child("android.view.View")[1].click() 
        
        dir_file = os.listdir(f'{self.path}')
        for file_ in dir_file:
            if '.txt' in file_:
                txt_name = file_
        with codecs.open(f'{self.path}\{txt_name}', 'r', 'utf-8')as f:
            content = f.read()
        sleep(1)
        poco(text = "新增說明").set_text(content[0:5000])
        sleep(rest)
        poco(name = "返回。按鈕。").click()
        sleep(rest)
        poco(text="下一步").click()
        sleep(rest)
        poco(name="上傳").click()
        sleep(post_rest)
        os.system(f'adb -s 127.0.0.1:{self.nox_port} shell "rm /sdcard/DCIM/Camera/Video/{title}.mp4"')
        os.system(f'adb -s 127.0.0.1:{self.nox_port} shell "am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard"')
        wait_time = 0
        while True:
            
            if poco(text = "可以觀看").exists():
                poco.swipe([0.5, 0.2], [0.5,0.8] , duration = 0.5)
                sleep(3)
                break
                
            elif poco(text = "已達每日上傳數量上限").exists():
                print('上傳已達上限.....')
                self.collection1.insert({'account':self.nox_port, 'time_decline':datetime.datetime.utcnow()})
                poco(desc = "選單").click()
                sleep(1)
                poco(text = "刪除上傳的影片").click()
                sleep(1)
                poco(text = "是").click()
                sleep(1)
                os._exit(0)

            elif poco(desc = "發布").exists():
                poco(desc = "發布").click()

            elif poco(text = "上傳失敗").exists():
                self.collection1.insert({'account':self.nox_port, 'time_decline':datetime.datetime.utcnow()})
                poco(desc = "選單").click()
                sleep(1)
                poco(text = "刪除上傳的影片").click()
                sleep(1)
                poco(text = "是").click()
                sleep(1)
                os._exit(0)
            elif poco(desc = "YouTube").exists():
                
                try:
                    poco(name = "媒體庫").click()
                except:
                    poco(text = "媒體庫").click()

                sleep(rest)
                poco(text = "你的影片").click()
                sleep(rest)
                
            else:
                wait_time += 1
                print('處理中...')
                sleep(10)
                if wait_time == 10:
                    poco(desc = "選單").click()
                    sleep(1)
                    poco(text = "刪除上傳的影片").click()
                    sleep(1)
                    poco(text = "是").click()
                    sleep(1)
                    os._exit(0)
                    

                
    def get_youtube_url(self, poco):
        
        poco(name = "動作選單")[0].click()
        sleep(1)
        poco(text = "分享").click()    
        sleep(1)
        poco(text = "複製連結").click()
        sleep(1)
        poco(desc = "搜尋").click()
        sleep(1)
        poco(text = "搜尋 YouTube").long_click(duration = 1)
        sleep(1)
        poco.click([0.12, 0.125])
        sleep(1)

        youtube_url = poco(type = "android.widget.EditText").get_text()
        sleep(1)
        keyevent('BACK')
        sleep(1)
        keyevent('BACK')
        
        return youtube_url    
        
    def main(self):        
        
        try:
            poco = self.connect_poco()
        except:
            os._exit(0)
        if not poco(text = "目前沒有任何影片").exists():
            self.reset_devices()
            self.push_video_in_mobile()
            self.find_utube(poco)
        else:
            self.clean_devices()
            self.push_video_in_mobile()
            sleep(1)
            keyevent('3')
            sleep(1)
            poco(text = 'YouTube').click()
        self.post_video(poco)

if __name__ == '__main__':

    client = pymongo.MongoClient('192.168.1.141:27017')
    collection1 = client['youtube_account_limit_david']['account']

    port = sys.argv[1]
    path = f'E:/sftp/{int(port)-62024}'
    i = 1
    while i < len(sys.argv):
        del sys.argv[i]
        i += 1
    while True:

        ban_list = [account['account'] for account in collection1.find()]
        if port not in ban_list:
            for _dir in os.listdir(path):
                try:
                    use_mobile(port, f'{path}/{_dir}')
                except:
                    pass
        else:
            print(f'{port} is been ban')
            sleep(3600)

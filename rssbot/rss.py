import feedparser
import redis
import logging
import json
import requests
import threading
import time
import base64

from .tool import Tool
from .bot import QQBot
from bs4 import BeautifulSoup


class FeedWatcher(object):
    tasks = []
    rsshub = 'https://feed.glaceon.net'

    def __init__(self):
        logging.info('连接到redis服务器')
        self.rds = redis.Redis(host='127.0.0.1', port=6379)
        logging.info('加载任务列表')
        with open('tasks.json', 'r') as tf:
            try:
                self.tasks = json.loads(tf.read())
                logging.info('加载成功,共%s条' % len(self.tasks))
            except Exception as e:
                logging.error('加载失败 %s' % e)

    def fetch_rss_update(self, task, new=False):
        last_push = self.rds.get(task['title'])
        if last_push is None:
            logging.info('添加新订阅 %s' % task['url'])
            self.rds.set(task['title'], Tool.current_time())
        else:
            logging.info('查找更新 %s' % task['url'])
            updates = []
            rss = feedparser.parse(self.rsshub+task['url'])
            publisher = rss.channel.title
            for entrie in rss.entries:
                if int(Tool.str_to_time(entrie.published)) > int(last_push):
                    updates.append(entrie)
            if len(updates) == 0:
                logging.info('无更新')
            else:
                logging.info('更新%s条信息' % len(updates))
                for update in updates:
                    title, time, images, videos = self.load_push_content(
                        update)
                    message = "%s 更新了!\n" % publisher
                    message += "内容:\n%s\n" % title
                    for image in images:
                        message += "[CQ:image,file=base64://%s]\n" % image
                    message += "时间:%s" % time

                    logging.info('开始推送')
                    for user_id in task['subscriber']['private']:
                        QQBot.send_private_msg(user_id, message)

                    for group_id in task['subscriber']['group']:
                        QQBot.send_group_msg(group_id, message)

                    self.rds.set(task['title'], Tool.str_to_time(time))
            logging.info('结束')

    def load_push_content(self, pub):
        title = pub.title
        time = pub.updated
        soup = BeautifulSoup(pub.summary, "html.parser")
        images = []
        videos = []
        for img in soup.find_all('img'):
            images.append(self.download_asset(img['src']))

        return title, time, images, videos

    def download_asset(self, url, proxy=False):
        logging.info('下载资源%s' % url)
        response = requests.get(url=url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
        }, proxies={
            'http': 'http://10.8.0.1:8118',
            'https': 'http://10.8.0.1:8118'
        })

        return base64.b64encode(response.content).decode('utf8')

    def run_task_once(self):
        for task in self.tasks:
            threading.Thread(target=self.fetch_rss_update, args=(task,)).run()
            time.sleep(5)

    def run(self):
        while True:
            self.run_task_once()
            time.sleep(60*5)

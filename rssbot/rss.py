import feedparser
import redis
import logging
import json
import requests
import threading
import time
import base64
import socket
import configparser
import random
import yaml

from .tool import Tool
from .bot import QQBot
from .translate import Translate
from bs4 import BeautifulSoup

socket.setdefaulttimeout(5)


class FeedWatcher(object):
    tasks = []

    def __init__(self, config='config.yml', task='tasks.json'):
        logging.info('加载配置文件')
        with open(config) as cf:
            self.config = yaml.load(cf.read())
        logging.info('连接到redis服务器')
        self.rds = redis.Redis(
            host=self.config['config']['REDIS_HOST'], port=self.config['config']['REDIS_PORT'])
        logging.info('连接到CQHTTP')
        self.bot = QQBot(self.config['config']['CQAPI'])
        logging.info('加载任务列表')
        with open(task, 'r') as tf:
            try:
                self.tasks = []
                for task in json.loads(tf.read()):
                    if task['activate']:
                        self.tasks.append(task)
                logging.info('加载成功,共%s条' % len(self.tasks))
            except Exception as e:
                logging.error('加载失败 %s' % e)
                exit(0)

    def fetch_rss_update(self, task, new=False):
        last_push = self.rds.get(task['title'])
        if last_push is None:
            logging.info('添加新订阅 %s' % task['url'])
            self.rds.set(task['title'], Tool.current_time())
        else:
            logging.info('查找更新 %s' % task['url'])
            updates = []
            rss = feedparser.parse(self.random_rsshub(task['platform'])+task['url'], request_headers={
                'X-Forwarded-For': Tool.get_fake_ip()
            })
            publisher = rss.channel.title
            for entrie in rss.entries:
                if int(Tool.str_to_time(entrie.published)) > int(last_push):
                    updates.append(entrie)
            if len(updates) == 0:
                logging.info('无更新')
            else:
                updates.reverse()
                logging.info('更新%s条信息' % len(updates))
                for update in updates:
                    title, time, link, images, videos = self.load_push_content(
                        update, task['proxy'])
                    message = "%s 更新了!\n" % publisher
                    message += "内容:\n%s\n" % title
                    if task['translate']:
                        message += "翻译:\n%s\n" % Translate.to_chinese(title)
                    for image in images:
                        message += "[CQ:image,file=base64://%s]\n" % image
                    message += "链接:\n%s\n" % link
                    message += "时间:%s" % Tool.gmt_reformat(time)

                    logging.info('开始推送')
                    for user_id in task['subscriber']['private']:
                        self.bot.send_private_msg(user_id, message)

                    for group_id in task['subscriber']['group']:
                        self.bot.send_group_msg(group_id, message)

                    self.rds.set(task['title'], Tool.str_to_time(time))

    def load_push_content(self, pub, proxy):
        title = pub.title
        time = pub.updated
        link = pub.link
        soup = BeautifulSoup(pub.summary, "html.parser")
        images = []
        videos = []
        for img in soup.find_all('img'):
            images.append(self.download_asset(img['src'], proxy))

        return title, time, link, images, videos

    def download_asset(self, url, proxy=False):
        logging.info('下载资源%s' % url)
        if proxy:
            proxies = {
                'http': self.config['config']['PROXY'],
                'https': self.config['config']['PROXY']
            }
        else:
            proxies = False
        response = requests.get(url=url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
        }, proxies=proxies)

        return base64.b64encode(response.content).decode('utf8')

    def run_task_once(self):
        for task in self.tasks:
            try:
                threading.Thread(target=self.fetch_rss_update,
                                 args=(task,)).run()
            except Exception as e:
                logging.error('错误%s' % e)
                self.bot.send_private_msg(
                    self.config['config']['ADMIN'], '【RSSBOT错误】\nmessage: %s' % (e))
            finally:
                time.sleep(5)

    def random_rsshub(self, app='default'):
        if app not in self.config['rsshub']:
            app = 'default'
        urls = self.config['rsshub'][app]
        if len(urls) == 0:
            urls = self.config['rsshub']['default']
        host = urls[random.randint(0, len(urls)-1)]
        logging.debug('使用RSSHUB: %s' % host)
        return host

    def run(self):
        while True:
            self.run_task_once()
            time.sleep(60*5)

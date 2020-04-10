import time
import datetime
import pytz
import random


class Tool(object):
    @staticmethod
    def str_to_time(s):
        timeArray = time.strptime(s, "%a, %d %b %Y %H:%M:%S GMT")
        return int(time.mktime(timeArray))

    @staticmethod
    def time_to_str(t):
        timeArray = time.localtime(t)
        return time.strftime("%a, %d %b %Y %H:%M:%S GMT", timeArray)

    @staticmethod
    def current_time():
        now = datetime.datetime.now(tz=pytz.timezone('UTC'))
        return int(time.mktime(now.timetuple()))

    @staticmethod
    def get_fake_ip():
        return '%s.%s.%s.%s' % (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

    @staticmethod
    def get_rsshub_host():
        rsshub = [
            'https://feed.glaceon.net',
            'http://rss.qiwihui.com',
            'http://95.179.142.196',
            'https://rss.shab.fun',
            'https://www.fulijun.club',
        ]
        return rsshub[random.randint(0, len(rsshub)-1)]

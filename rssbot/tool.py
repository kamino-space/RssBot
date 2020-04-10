import time
import datetime
import pytz
import random
import logging


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
    def get_rsshub_host(platform='twitter'):
        if platform == 'twitter':
            rsshub = [
                'https://feed.glaceon.net',
                'https://rss.shab.fun',
                'https://www.fulijun.club',
            ]
            host = rsshub[random.randint(0, len(rsshub)-1)]
            logging.debug('使用rsshub: %s' % host)
            return host
        elif platform == 'instagram':
            rsshub = [
                "https://rss.nyan.kim",
                "http://rss.5ux.net",
                "http://rsshub.xyz",
                "http://rss.0x404.club",
                "https://xnps.xyz",
                "http://rsshub.sloves.xyz",
                "https://891011.xyz",
                "https://rss.unl.li",
                "https://rsshub.ioiox.com",
                "http://rss.gco.me",
                "http://95.179.142.196",
                "http://rss.eastedia.cc",
                "https://rss.feiyuyu.net",
                "https://rss.nyan.kim",
                "http://rss.5ux.net"
            ]
            host = rsshub[random.randint(0, len(rsshub)-1)]
            logging.debug('使用rsshub: %s' % host)
            return host
        else:
            return 'https://feed.glaceon.net'

import time
import datetime
import pytz


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

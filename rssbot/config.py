import json
import logging


class Config(object):
    configs = {}

    @staticmethod
    def load_config(file):
        try:
            with open(file,'r') as cf:
                Config.configs = json.loads(cf.read())
        except Exception as e:
            logging.error('加载配置文件失败 %s' % e)
            exit(0)

    @staticmethod
    def get(key):
        if key in Config.configs:
            return Config.configs[key]
        else:
            return None

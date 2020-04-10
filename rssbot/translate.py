import requests
import json
import logging


class Translate(object):
    @staticmethod
    def to_chinese(text):
        logging.info('翻译 %s' % text[0:10])
        try:
            response = requests.get(
                'http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl=zh_CN&q=%s' % text)
            trans = json.loads(response.content)
            result = ""
            for sentence in trans.sentences:
                result += sentence['trans']
                result += ' '
            return result
        except Exception:
            return None

import logging

from cqhttp import CQHttp
from .config import Config


class QQBot(object):
    bot = CQHttp(api_root='http://172.17.0.2:5700')

    @staticmethod
    def send_private_msg(user_id, message=''):
        logging.info('向[%s]发送私聊消息: %s' % (user_id, message[0:20]))
        QQBot.bot.send_private_msg(user_id=user_id, message=message)

    @staticmethod
    def send_group_msg(group_id, message=''):
        logging.info('向[%s]发送群组消息: %s' % (group_id, message[0:20]))
        QQBot.bot.send_group_msg(group_id=group_id, message=message)

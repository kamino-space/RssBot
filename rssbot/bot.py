import logging

from cqhttp import CQHttp
from .config import Config


class QQBot(object):

    def __init__(self, cqapi):
        self.bot = CQHttp(api_root=cqapi)

    def send_private_msg(self, user_id, message=''):
        logging.info('向[%s]发送私聊消息: %s' % (user_id, message[0:20]))
        self.bot.send_private_msg(user_id=user_id, message=message)

    def send_group_msg(self, group_id, message=''):
        logging.info('向[%s]发送群组消息: %s' % (group_id, message[0:20]))
        self.bot.send_group_msg(group_id=group_id, message=message)

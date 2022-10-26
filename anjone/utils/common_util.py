import time

from flask import request

from anjone.common.Constant import DEV_TYPE


def format_time(timestamp):
    time_local = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_local)


def get_login_dev():
    user_agent = request.headers.get('User-Agent')
    # todo 还需要考虑使用客户端的UA情况
    if user_agent.lower().find('windows') != -1:
        return DEV_TYPE.WINDOWS
    elif user_agent.lower().find('mac os') != -1:
        return DEV_TYPE.MAC_OS
    elif user_agent.lower().find('linux') != -1:
        return DEV_TYPE.LINUX
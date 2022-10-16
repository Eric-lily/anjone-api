import time


def format_time(timestamp):
    time_local = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_local)
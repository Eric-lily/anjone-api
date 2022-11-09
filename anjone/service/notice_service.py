from anjone.common import Response
from anjone.common.Constant import NOTICE_LOG
from anjone.models.vo.Notice import Notice


def delete_all():
    # todo 清空通知日志, 使用绝对路径找到文件位置
    path = NOTICE_LOG
    with open(path, 'a+', encoding='utf-8') as notice_log:
        notice_log.truncate(0)
    return Response.create_success('通知已清空')


def get_notice():
    res = read_log(NOTICE_LOG)
    return Response.create_success(res)


def read_log(path):
    res = []
    for line in open(path, "r", encoding='UTF-8'):
        strs = line.split(' ')
        notice = Notice(title=strs[3], create_time=strs[1]+' '+strs[2], content=strs[4], type=strs[0])
        res.append(notice.to_json())
    return res
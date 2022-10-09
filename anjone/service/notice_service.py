from anjone.common import Response


def delete_all():
    # todo 清空通知日志, 使用绝对路径找到文件位置
    path = 'D:\\github\\flask_project\\notice\\notice.log'
    with open(path, 'a+', encoding='utf-8') as notice_log:
        notice_log.truncate(0)
    return Response.create_success('通知已清空')
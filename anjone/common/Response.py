import json


class response:
    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data


class error_response:
    def __init__(self, code, message):
        self.code = code
        self.message = message


class NotLogin:
    code = '1'
    message = '用户未登录'


def create_success(data):
    return json.dumps(response(0, 'success', data).__dict__, ensure_ascii=False), 200, \
           {'Content-Type': 'application/json; charset=utf-8'}


def create_error(code, msg):
    return json.dumps(error_response(code, msg).__dict__, ensure_ascii=False), \
           {'Content-Type': 'application/json; charset=utf-8'}

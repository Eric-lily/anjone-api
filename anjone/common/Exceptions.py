import werkzeug.exceptions

# 参数为空异常
from tencentcloud.common.exception import TencentCloudSDKException

from anjone.common import Response


class ParameterNullException(werkzeug.exceptions.HTTPException):
    code = '11',
    description = 'Parameter is Null'


def configure_exceptions(app):
    @app.errorhandler(ParameterNullException)
    def handleParameterNullException(e):
        return Response.create_error(e.code[0], e.description)

    @app.errorhandler(werkzeug.exceptions.BadRequest)
    def handleBadRequest(e):
        return Response.create_error('400', 'bad request')

    @app.errorhandler(werkzeug.exceptions.InternalServerError)
    def handleBadRequest(e):
        return Response.create_error('500', 'InternalServerError')

    @app.errorhandler(werkzeug.exceptions.Forbidden)
    def handleBadRequest(e):
        return Response.create_error('403', 'forbidden')

    # todo: 添加页面
    @app.errorhandler(werkzeug.exceptions.NotFound)
    def handleBadRequest(e):
        return 'not found'

    @app.errorhandler(TencentCloudSDKException)
    def handleTencentCloudSDKException(e):
        return Response.create_error('10', '短信发送失败')

def res_success(data=None):
    return {'code': 200, 'data': data, 'msg': 'ok'}


def res_fail(msg='服务异常', code=500, data=None):
    return {'code': code, 'msg': msg, 'data': data}

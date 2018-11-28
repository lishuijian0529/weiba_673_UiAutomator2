# -*- coding:utf-8 -*-
# coding:utf-8

import json
import time
from urlparse import parse_qs
from wsgiref.simple_server import make_server


# 定义函数，参数是函数的两个参数，都是python本身定义的，默认就行了。
def application(environ, start_response):
    # 定义文件请求的类型和当前请求成功的code
    start_response('200 OK', [('Content-Type', 'application/json')])
    # environ是当前请求的所有数据，包括Header和URL，body

    request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0)))
    request_body = json.loads(request_body)

    phone = request_body["phone"]
    code = request_body["code"]

    # input your method here
    # for instance:
    # 增删改查
    if len(code)!=6:
        return [json.dumps({"code": "1","message":"验证码需要6位"})]
    else:
        return [json.dumps({"message":"成功","code":"0"})]


if __name__ == "__main__":
    port = 5088
    httpd = make_server("127.0.0.1", port, application)
    httpd.serve_forever()
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import *
from flask_cors import CORS

redis = None
app = Flask(__name__, static_folder='./static')
CORS(app, supports_credentials=True)

# if __name__ == '__main__':
#     print('作为主程序运行')
# else:
#     print('package root 初始化')

# 日志工具

#encoding:utf8

import logging
from datetime import datetime

class Log(object):
    def __init__(self):
        logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename= 'log/' + datetime.now().strftime("%Y%m%d-%H") + '.log',
                filemode='a'
                )

    def write_log(self, content):
        logging.info(content)

    def error_log(self, error_content):
        logging.error(error_content)

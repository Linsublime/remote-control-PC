# 配置文件读取工具

#encoding:utf8

import os
import sys
import ConfigParser


class ConfigReader(object):
    def __init__(self):
        configfile = os.path.join(sys.path[0], '_config.ini')
        self.cReader = ConfigParser.ConfigParser()
        self.cReader.read(configfile)

    def get_config(self, section, option):
        return self.cReader.get(section, option)

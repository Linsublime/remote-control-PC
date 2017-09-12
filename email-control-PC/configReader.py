#encoding:utf8
# 配置文件读取类

import ConfigParser
import os, sys

class ConfigReader(object):
    def __init__(self):
        configFile = os.path.join(sys.path[0], '_config.ini')
        self.cReader = ConfigParser.ConfigParser()
        self.cReader.read(configFile)

    def get_items(self):
        pass

    def get_config(self, section, option):
        return self.cReader.get(section, option)

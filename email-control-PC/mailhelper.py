# 邮件助手

#encoding:utf8

import re
import poplib
import smtplib
from email.parser import Parser
from email.mime.text import MIMEText
from configReader import ConfigReader

from createlog import Log


class MailHelper(object):
    def __init__(self):
        self.log = Log()                    # 日志工具
        self.configReader = ConfigReader()  # 配置文件读取工具
        
        self.pophost = self.configReader.get_config('Slave', 'pophost')
        self.smtphost = self.configReader.get_config('Slave', 'smtphost')
        self.port = self.configReader.get_config('Slave', 'port')
        self.username = self.configReader.get_config('Slave', 'username')
        self.password = self.configReader.get_config('Slave', 'password')
        self.bossmail = self.configReader.get_config('Boss', 'mail')
        self.usernames = {'Slave':self.username, 'Boss':self.bossmail}
        
        self.login_mail()
        
    def login_mail(self):
    # 登录邮件收、发服务器
        try:
            # 登录 pop 服务器
            self.pop3 = poplib.POP3_SSL(self.pophost)
            self.pop3.set_debuglevel(0)     # level(1)可以输出调试信息
            self.pop3.user(self.username)
            self.pop3.pass_(self.password)
            self.pop3.list()    # 此处list()只用于验证是否登陆成功
            
            # 登录 smtp 服务器
            self.server = smtplib.SMTP_SSL()
            self.server.connect(self.smtphost, self.port)   # 端口号为465,不能用25
            self.server.login(self.username, self.password)
            self.log.write_log(u'登陆邮箱成功！')
            
        except Exception, e:
            print u'登陆失败！'
            self.log.error_log(u'登陆失败！' + str(e))
            exit()

    def accept_mail(self):
    # 接收最新一封邮件
        try:
            # 获取邮件列表
            mails = self.pop3.list()[1]
            # 获取指定索引的邮件，索引从1开始，新邮件索引最大
            mailbody = self.pop3.retr(len(mails))[1]
            self.log.write_log(u'抓取邮件成功！')
            return mailbody
        
        except Exception, e:
            self.log.error_log(u'抓取邮件失败！' + str(e))
            print u'抓取邮件失败!'
            return None

    def analysis_mail(self, mailbody):
    # 解析出邮件的主题、发件人、内容
        try:
            # Parser()在email模块中可找到，用于解析邮件体
            msg = Parser().parsestr('\r\n'.join(mailbody))
            subject = msg.get('Subject')
            sender = msg.get('From')
            sender = re.search(r'<(.*?)>', sender, re.S).group(1)
            # get_payload()方法只能用于获取纯文本格式的邮件内容
            content = msg.get_payload(decode=True)
            self.log.write_log(u'邮件解析完成。')
            mail_info = {'subject': subject, 'sender': sender, 'content': content}
            return mail_info
        
        except Exception, e:
            self.log.error_log(u'解析失败！'+ str(e))
            return None

    def send_mail(self, receiver, subject, content):
        msg = MIMEText(content,'plain','utf-8') # 纯文本、utf-8格式内容
        msg['Subject'] = subject
        msg['From'] = 'helper<%s>'%self.username    # 昵称<邮箱>
        
        try:
            self.server.sendmail(self.username, self.usernames[receiver], msg.as_string())
            self.log.write_log(u'成功发送邮件到:%s!'%receiver)
            return True
        
        except Exception, e:
            self.log.error_log(u'发送失败！' + str(e))
            return False

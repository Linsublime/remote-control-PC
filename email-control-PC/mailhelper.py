#encoding:utf8
# 邮件助手

import re
import poplib
import smtplib
from createlog import Log
from configReader import ConfigReader
from email.mime.text import MIMEText
from email.parser import Parser

class MailHelper(object):
    def __init__(self):
        self.log = Log()
        self.configReader = ConfigReader()
        self.pophost = self.configReader.get_config('Slave', 'pophost')
        self.smtphost = self.configReader.get_config('Slave', 'smtphost')
        self.port = self.configReader.get_config('Slave', 'port')
        self.username = self.configReader.get_config('Slave', 'username')
        self.password = self.configReader.get_config('Slave', 'password')
        self.bossMail = self.configReader.get_config('Boss', 'mail')
        self.loginMail()

    def loginMail(self):
        try:
            # 登录 pop 服务器
            self.pop3 = poplib.POP3_SSL(self.pophost)
            self.pop3.set_debuglevel(0)
            self.pop3.user(self.username)
            self.pop3.pass_(self.password)
            self.pop3.list()
            # 登录 smtp 服务器
            self.server = smtplib.SMTP_SSL()
            self.server.connect(self.smtphost, self.port)
            self.server.login(self.username, self.password)
            self.log.writeLog(u'登陆邮箱成功！')
        except Exception, e:
            print u'登陆失败！'
            self.log.writeError(u'登陆失败！'+ str(e))
            exit()

    def acceptMail(self):
        try:
            mails = self.pop3.list()[1]     # list()返回一个元组，包含3个元素,
                                            # 第2个元素是所有邮件索引组成的列表，索引从1开始，新邮件索引靠后
            mailbody = self.pop3.retr(len(mails))[1]    # retr()获取指定索引的邮件，第2个元素是邮件体
            self.log.writeLog(u'抓取邮件成功！')
            return mailbody
        except Exception, e:
            self.log.writeError(u'抓取邮件失败！'+ str(e))
            print u'抓取邮件失败!'
            return None

    def analysisMail(self, mailbody):
        try:
            msg = Parser().parsestr('\r\n'.join(mailbody))
            subject = msg.get('Subject')
            sender = msg.get('From')
            sender = re.search(r'<(.*?)>', sender, re.S).group(1)
            content = msg.get_payload(decode=True)
            self.log.writeLog(u'邮件解析完成。')
            mail_info = {'subject': subject, 'sender': sender, 'content': content}
            return mail_info
        except Exception, e:
            self.log.writeError(u'解析失败！'+ str(e))
            return None

    def sendMail(self, receiver, subject, content):
        msg = MIMEText(content,'plain','utf-8') # 发中文需参数‘utf-8’
        msg['Subject'] = subject
        msg['From'] = 'helper<%s>'%self.username
        self.log.writeLog(u'准备发送邮件到:%s'%receiver)
        # 后续要发送pass邮件到Slave，用作是占据第一条邮件的位置，否则将会持续执行第一条邮件的命令
        if receiver == 'Slave':
            try:
                self.server.sendmail(self.username, self.username, msg.as_string())
                self.log.writeLog(u'发送成功！')
                return True
            except Exception, e:
                self.log.writeError(u'发送失败！'+ str(e))
                return False

        if receiver == 'Boss':
            try:
                self.server.sendmail(self.username, self.bossMail, msg.as_string())
                self.log.writeLog(u'发送成功！')
                return True
            except Exception, e:
                self.log.writeError(u'发送失败！'+ str(e))
                return False

if __name__ == '__main__':
    mail = MailHelper()
    mailbody =  mail.acceptMail()
    mail.analysisMail(mailbody)
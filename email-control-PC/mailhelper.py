# �ʼ�����

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
        self.log = Log()                    # ��־����
        self.configReader = ConfigReader()  # �����ļ���ȡ����
        
        self.pophost = self.configReader.get_config('Slave', 'pophost')
        self.smtphost = self.configReader.get_config('Slave', 'smtphost')
        self.port = self.configReader.get_config('Slave', 'port')
        self.username = self.configReader.get_config('Slave', 'username')
        self.password = self.configReader.get_config('Slave', 'password')
        self.bossmail = self.configReader.get_config('Boss', 'mail')
        self.usernames = {'Slave':self.username, 'Boss':self.bossmail}
        
        self.login_mail()
        
    def login_mail(self):
    # ��¼�ʼ��ա���������
        try:
            # ��¼ pop ������
            self.pop3 = poplib.POP3_SSL(self.pophost)
            self.pop3.set_debuglevel(0)     # level(1)�������������Ϣ
            self.pop3.user(self.username)
            self.pop3.pass_(self.password)
            self.pop3.list()    # �˴�list()ֻ������֤�Ƿ��½�ɹ�
            
            # ��¼ smtp ������
            self.server = smtplib.SMTP_SSL()
            self.server.connect(self.smtphost, self.port)   # �˿ں�Ϊ465,������25
            self.server.login(self.username, self.password)
            self.log.write_log(u'��½����ɹ���')
            
        except Exception, e:
            print u'��½ʧ�ܣ�'
            self.log.error_log(u'��½ʧ�ܣ�' + str(e))
            exit()

    def accept_mail(self):
    # ��������һ���ʼ�
        try:
            # ��ȡ�ʼ��б�
            mails = self.pop3.list()[1]
            # ��ȡָ���������ʼ���������1��ʼ�����ʼ��������
            mailbody = self.pop3.retr(len(mails))[1]
            self.log.write_log(u'ץȡ�ʼ��ɹ���')
            return mailbody
        
        except Exception, e:
            self.log.error_log(u'ץȡ�ʼ�ʧ�ܣ�' + str(e))
            print u'ץȡ�ʼ�ʧ��!'
            return None

    def analysis_mail(self, mailbody):
    # �������ʼ������⡢�����ˡ�����
        try:
            # Parser()��emailģ���п��ҵ������ڽ����ʼ���
            msg = Parser().parsestr('\r\n'.join(mailbody))
            subject = msg.get('Subject')
            sender = msg.get('From')
            sender = re.search(r'<(.*?)>', sender, re.S).group(1)
            # get_payload()����ֻ�����ڻ�ȡ���ı���ʽ���ʼ�����
            content = msg.get_payload(decode=True)
            self.log.write_log(u'�ʼ�������ɡ�')
            mail_info = {'subject': subject, 'sender': sender, 'content': content}
            return mail_info
        
        except Exception, e:
            self.log.error_log(u'����ʧ�ܣ�'+ str(e))
            return None

    def send_mail(self, receiver, subject, content):
        msg = MIMEText(content,'plain','utf-8') # ���ı���utf-8��ʽ����
        msg['Subject'] = subject
        msg['From'] = 'helper<%s>'%self.username    # �ǳ�<����>
        
        try:
            self.server.sendmail(self.username, self.usernames[receiver], msg.as_string())
            self.log.write_log(u'�ɹ������ʼ���:%s!'%receiver)
            return True
        
        except Exception, e:
            self.log.error_log(u'����ʧ�ܣ�' + str(e))
            return False

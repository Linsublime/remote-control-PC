'''ͨ�������ض����䷢�����ʼ����ٽ������ʼ��е�ָ�
   ��ʵ��Զ�̿��Ƶ��ԡ�
'''

#encoding:utf8

import time

from excutor import Excutor
from mailhelper import MailHelper

class Main(object):

    def run(self):
        while True:
            mail = MailHelper()
            mailbody = mail.accept_mail()                # ץȡ�ʼ�
            mail_info = mail.analysis_mail(mailbody)     # �����ʼ�
            excutor = Excutor()
            excutor.excute(mail_info, mail)             # ִ���ʼ�����
            time.sleep(30)                              # ���30��


if __name__ == '__main__':
    main = Main()
    main.run()

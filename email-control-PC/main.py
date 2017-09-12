#encoding:utf8

import time
from mailhelper import MailHelper
from excutor import Excutor

class Main(object):

    def run(self):
        while True:
            mail = MailHelper()
            mailbody = mail.acceptMail()
            mail_info = mail.analysisMail(mailbody)
            excutor = Excutor()
            excutor.excute(mail_info, mail)
            time.sleep(30)

if __name__ == '__main__':
    main = Main()
    main.run()
#encoding:utf8
# 通过接收特定邮箱发来的邮件，解析出邮件中的指令，
# 来实现远程控制电脑。

import time
from mailhelper import MailHelper
from excutor import Excutor

class Main(object):

    def run(self):
        while True:
            mail = MailHelper()
            mailbody = mail.acceptMail()                # 抓取邮件
            mail_info = mail.analysisMail(mailbody)     # 解析邮件
            excutor = Excutor()
            excutor.excute(mail_info, mail)             # 执行邮件命令
            time.sleep(30)                              # 间隔30秒


if __name__ == '__main__':
    main = Main()
    main.run()

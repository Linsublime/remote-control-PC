#encoding:utf8
# 执行邮件命令

import os
from createlog import Log

class Excutor(object):
    def __init__(self):
        self.log = Log()

    def excute(self, mail_info, mailhelper):
        sender = mail_info['sender']
        subject = mail_info['subject']
        content = mail_info['content']

        # 每次收到一封命令邮件后，自动发送一封pass邮件作为最新邮件，
        # 否则会重复读取命令邮件
        if subject == 'pass':
            print 'pass'
        else:
            if sender == mailhelper.bossMail:
                mailhelper.sendMail('Slave', 'pass', 'test')
                try:
                    script_name = subject
                    # 以邮件主题为文件名，将邮件内容写入文件中
                    with open('script/%s.py'%script_name, 'w') as fi:
                        fi.write(content)
                    # 执行生成的脚本
                    os.system('python script/%s.py'%script_name)
                    mailhelper.sendMail('Boss', 'success', 'OK')
                except Exception, e:
                    self.log.writeError(u'执行失败：'+ str(e))
                    mailhelper.sendMail('Boss', 'error', str(e))


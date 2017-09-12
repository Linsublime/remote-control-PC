#encoding:utf8

import os
from createlog import Log

class Excutor(object):
    def __init__(self):
        self.log = Log()

    def excute(self, mail_info, mailhelper):
        sender = mail_info['sender']
        subject = mail_info['subject']
        content = mail_info['content']
        if subject == 'pass':
            print 'pass'
        else:
            if sender == mailhelper.bossMail:
                mailhelper.sendMail('Slave', 'pass', 'test')
                try:
                    script_name = subject
                    command = content
                    with open('script/%s.py'%script_name, 'w') as fi:
                        fi.write(command)
                    os.system('python script/%s.py'%script_name)
                except Exception, e:
                    self.log.writeError(u'执行失败：'+ str(e))
                    mailhelper.sendMail('Boss', 'error', str(e))


# 执行邮件命令

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

        '''每次收到一封命令邮件后，自动发送一封pass邮件作为最新邮件，
        否则会重复读取命令邮件
        '''
        if subject is 'pass':
            print 'pass'
        else:
            if sender is mailhelper.bossmail:
                mailhelper.send_mail('Slave', 'pass', 'test')
                try:
                    script_name = subject
                    # 以邮件主题为文件名，将邮件内容写入文件中
                    with open('script/%s.py'%script_name, 'w') as fi:
                        fi.write(content)
                    # 执行生成的脚本
                    os.system('python script/%s.py'%script_name)
                    mailhelper.send_mail('Boss', 'success', 'OK')
                    
                except Exception, e:
                    self.log.error_log(u'执行失败：' + str(e))
                    mailhelper.send_mail('Boss', 'error', str(e))


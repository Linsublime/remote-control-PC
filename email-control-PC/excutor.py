# ִ���ʼ�����

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

        '''ÿ���յ�һ�������ʼ����Զ�����һ��pass�ʼ���Ϊ�����ʼ���
        ������ظ���ȡ�����ʼ�
        '''
        if subject is 'pass':
            print 'pass'
        else:
            if sender is mailhelper.bossmail:
                mailhelper.send_mail('Slave', 'pass', 'test')
                try:
                    script_name = subject
                    # ���ʼ�����Ϊ�ļ��������ʼ�����д���ļ���
                    with open('script/%s.py'%script_name, 'w') as fi:
                        fi.write(content)
                    # ִ�����ɵĽű�
                    os.system('python script/%s.py'%script_name)
                    mailhelper.send_mail('Boss', 'success', 'OK')
                    
                except Exception, e:
                    self.log.error_log(u'ִ��ʧ�ܣ�' + str(e))
                    mailhelper.send_mail('Boss', 'error', str(e))


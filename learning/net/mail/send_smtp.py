import smtplib
import poplib
import sys

'''
    smtp pop3 邮件发送接收
'''
def send():
    from_mail = 'aritans22@126.com'
    to_mail = 'myth.kuang@gmail.com'
    server = smtplib.SMTP('smtp.126.com')
    server.login('aritans22@126.com', 'free14293366')
    msg = ''' 
        需要编码  
    '''
    server.sendmail(from_mail, to_mail, msg)
    server.quit()

def recive():
    server = poplib.POP3('pop3.163.com')
    server.user('')
    server.pass_('')
    server.set_debuglevel(1) # 设置调试模式，查看与服务器交互信息
    msgNum, size = server.stat()
    print('number', msgNum, 'size', size)
    content = server.retr(1) # 取出第一封邮件完整消息
    print('lines ', len(content))
    for line in content[1]:
        print(line)
    server.quit()


params = sys.argv
if params[1] == 's':
    send()
elif params[1] == 'r':
    recive()
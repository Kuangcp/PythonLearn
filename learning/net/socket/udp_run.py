import socket
import sys
'''
    基于Socket的TCP连接
'''
def server():
    port=8081
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #从指定的端口，从任何发送者，接收UDP数据
    s.bind(('',port))
    print('正在等待接入...')
    while True:
        #接收一个数据
        data,addr=s.recvfrom(1024)
        print('Received:',data,'from',addr)

def client():
    port=8081
    host='localhost'
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.sendto(b'hello,this is a test info !',(host,port))

params = sys.argv
if params[1] == 's':
    server()
elif params[1] == 'c':
    client()

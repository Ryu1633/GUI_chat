import socket

BUFSIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 2500))

while True:
    msg = input('message to send: ')
    try:
        n = s.send(msg.encode())
    except:
        print('연결 종료됨')
        s.close()
        break

    else:
        print('{} bytes sent'.format(n))


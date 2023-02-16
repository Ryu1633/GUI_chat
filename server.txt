from socket import *
from threading import *

class MultiChatServer:
    clients = []
    users = []
    message = ''

    #계정 목록 열기
    try:
        accounts = eval(open('accounts.txt', mode='r').read())
        print('계정 목록: ', accounts)

    #계정 목록이 없을 경우 새로 만듬
    except:
        open('accounts.txt', mode='wt')
        print('계정 목록 새로 만듬')
        accounts = {'':''}

    
    #서버 설정
    def __init__(self):
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip = ''
        self.port = 2500
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_sock.bind((self.ip, self.port))
        self.s_sock.listen(10)  #최대 10명 동시 사용 가능
        print('서버 시작')
        self.accept_client()
    
    #사용자 접속 받기
    def accept_client(self):
        while True:
            client = c_socket, (ip, port) = self.s_sock.accept()
            if client not in self.clients:
                self.clients.append(client)
            print (ip , ':' , str(port), ' 가 연결되었습니다')
            t = Thread(target=self.receive_messages, args=(c_socket,))
            t.start()
            print(client)
    
    #사용자로 부터 메세지 받기
    def receive_messages(self, c_socket):
        while True:
            try:
                incoming_message = c_socket.recv(1024)
                if not incoming_message:
                    break
            except:
                continue
            else:
                try:
                    #명령어 일 경우
                    if str(incoming_message.decode('utf-8')).split(':', maxsplit=1)[0] == 'command':
                        exec('self.%s(c_socket)' %str(incoming_message.decode('utf-8')).split(':', maxsplit=1)[1])

                    #일반 메세지일 경우
                    elif str(incoming_message.decode('utf-8')).split(':', maxsplit=1)[0] == 'message':
                            self.message = str(incoming_message.decode('utf-8')).split(':', maxsplit=1)[1]
                            for client in self.clients:
                                socket, (ip, port) = client
                                if socket is not c_socket:
                                    try:
                                        socket.sendall(self.message.encode('utf-8'))
                                        self.message = ''
                                    except:
                                        self.clients.remove(client)   
                except:
                    continue
        c_socket.close()
    
    #로그인 명령어 수행
    def Command_Login(self, c_socket):
        print('Command_login 요청됨')
        c_socket.send('접속 성공'.encode('utf-8'))  #접속 요청 응답

        print('ID 가져오는 중...')
        self.ID = c_socket.recv(1024).decode('utf-8')   #ID받아오기
        print('ID 받기 성공. {}로 부터 받은 ID:{}'.format(c_socket, self.ID))

        c_socket.send('ID받기 성공'.encode('utf-8'))    #ID받기 응답

        print('PW 가져오는 중...')
        PW = c_socket.recv(1024).decode('utf-8')    #PW받아오기
        print('PW 받기 성공. {}로 부터 받은 PW:{}'.format(c_socket, PW))

        c_socket.send('PW받기 성공'.encode('utf-8'))    #PW받기 응답

        print('%s 로그인 시작' %self.ID)
        if self.ID in self.users:
            print('현재 접속 중인 ID임.')
            c_socket.send('접속중'.encode('utf-8'))
            c_socket.close()

        elif self.ID in self.accounts.keys():
            if self.accounts[self.ID] == PW:
                print('로그인 성공')
                self.users.append(self.ID)
                print('현재 접속자: ', self.users)
                print('타입: ', type(self.users))
                c_socket.send('로그인 성공'.encode('utf-8'))
        else:
            print('ID/PW 오류')
            c_socket.send('IDPW오류'.encode('utf-8'))
            c_socket.close()

    #회원가입 명령어 수행
    def Command_CreateAccount(self, c_socket):
        print('Command_CreateAccount 요청됨')

        print('ID받기')
        ID = c_socket.recv(1024).decode('utf-8')    #ID받아오기
        print('ID받기 성공, ID: %s' %ID)

        try:
            if ID in self.accounts:
                print('아이디 중복')
                c_socket.send('중복'.encode('utf-8'))
            else:
                c_socket.send('가능'.encode('utf-8'))
                print('PW받기')
                PW = c_socket.recv(1024).decode('utf-8')  #PW 받아오기
                print('PW받기 성공, PW: %s' %PW)
                self.accounts[ID] = PW
                open('accounts.txt', 'wt').write(str(self.accounts)) #회원정보 갱신
                c_socket.send('계정 생성 성공'.encode('utf-8'))
                print('계정 생성 성공')
                print('계정 목록: ', self.accounts)
        except:
            print('입력 오류')
            c_socket.send('오류'.encode('utf-8'))
        c_socket.close()
            
if __name__ == "__main__":
    MultiChatServer()
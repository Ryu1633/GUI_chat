from socket import *
from tkinter import *
from tkinter.font import Font
from threading import *
from PIL import Image, ImageTk

class ChatClient:
    client_socket = None
    window = Tk()
    user_name = ''

    def __init__(self):
        self.LoginPage()     

    #로그인 화면
    def LoginPage(self):
        print('로그인 화면열림')

        #화면설정
        self.window.title('로그인')
        self.window.geometry('340x520+650+100')
        self.window.resizable(False, False)
        self.window['bg'] = '#ffeb33'

        #프레임 설정
        frame1 = Frame()
        frame1['bg'] = '#ffeb33'

        #로고 이미지 파일 불러오기
        try:
            path = "logo.png"
            logo = ImageTk.PhotoImage(Image.open(path))
            logo_label = Label(frame1, image=logo)
            logo_label.photo = logo
        except FileNotFoundError:
            logo_label = Label(frame1, text='이미지 파일 오류')

        #로고 이미지 파일 넣기
        logo_label['bg'] = '#ffeb33'
        logo_label.pack(pady=5)

        #서버 IP주소 입력칸 넣기
        addr_entry = Entry(frame1, width=14, font=Font(size=10), relief='flat')
        addr_entry.insert(0, '127.0.0.1:2500')
        addr_entry.pack(ipadx=50, ipady=10, pady=1)

        #ID 입력칸 넣기
        id_entry = Entry(frame1, width=14, font=Font(size=10), relief='flat')
        id_entry.pack(ipadx=50, ipady=10)

        #PW 입력칸 넣기
        pw_entry = Entry(frame1, width=14, font=Font(size=10), relief='flat', show='*')
        pw_entry.pack(ipadx=50, ipady=10, pady=1)

        #로그인 버튼 넣기
        login_button = Button(frame1, width=28, height=2, relief='flat', text='로그인')
        login_button.config(command= lambda: self.CheckLogin(addr_entry.get(), id_entry.get(), pw_entry.get()))
        login_button['bg'] = '#f6f6f6'
        login_button.pack(pady=5)

        #회원가입 버튼 넣기
        account_button = Button(frame1, relief='flat', text='회원가입', activebackground='yellow2',
                                command= lambda: self.AccountPage(addr_entry.get()))
        account_button['bg'] = '#ffeb33'
        account_button.pack(side=LEFT)

        #프레임 넣기
        frame1.pack(pady=60)
        self.window.mainloop() 

    #로그인 과정
    def CheckLogin(self, addr, id, pw):
        print('로그인 과정 시작')

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        msg = ''

        #에러 표시 화면 설정
        login_error_page = Toplevel()
        login_error_page.geometry('250x100+700+350')
        login_error_page.resizable(False, False)
        login_error_page['bg'] = '#ffeb33'

        lab = Label(login_error_page, text='', font=Font(size=15), height=40) #에러 메세지 출력
        lab['bg'] = '#ffeb33'

        #ID/PW 공백 오류
        if(id == '' or pw == ''):
            login_error_page.title('login error(1)')
            lab.config(text='ID/PW를 입력해 주세요')
            lab.pack()
            login_error_page.mainloop()
            
        else:
            try:
                IP = addr.split(':')[0]
                PORT = addr.split(':')[1]
            
            #서버 주소 오류 or 서버 안열림
            except IndexError as e:
                login_error_page.title('login error(2)')
                lab.config(text='서버주소와 포트를 확인해 주세요', wraplength=200)
                lab.pack()
                login_error_page.mainloop()
        
            else:
                try:
                    print('접속 ip:%s' %IP)
                    print('접속 port:%s' %PORT)
                    print('입력 id: %s' %id)
                    print('입력 pw: %s' %pw)
                    self.client_socket.connect((IP, int(PORT))) #통신 연결
                
                #서버 안열림
                except ConnectionRefusedError as e:
                    login_error_page.title('server error(1)')
                    lab.config(text='서버 에러')
                    lab.pack()
                    login_error_page.mainloop()
                else:
                    print('{} : {}에 연결됨'.format(IP, PORT))

                    #서버에 로그인 요청
                    print('서버에 로그인 요청 중...')
                    self.client_socket.send('command:Command_Login'.encode('utf-8'))
                    while(msg == ''):   #응답 대기
                        print('응답 대기중(1)...')
                        msg = self.client_socket.recv(1024).decode('utf-8')
                    print('로그인 요청 성공')

                    #서버에 ID 보내기
                    print('서버에 ID 보내는 중...')
                    self.client_socket.send(id.encode('utf-8'))
                    msg = ''
                    while(msg == ''):   #응답 대기
                        print('응답 대기중(2)...')
                        msg = self.client_socket.recv(1024).decode('utf-8')
                    print('ID 보내기 성공')   

                     #서버에 PW 보내기
                    print('서버에 PW 보내는 중...')
                    self.client_socket.send(pw.encode('utf-8'))
                    msg = ''
                    while(msg == ''):   #응답 대기
                        print('응답 대기중(3)...')
                        msg = self.client_socket.recv(1024).decode('utf-8')
                    print('PW 보내기 성공')

                    #로그인 결과 받기
                    msg = self.client_socket.recv(1024).decode('utf-8')
                    print(msg)
                    if msg == '로그인 성공':
                        self.user_name = id
                        self.ChatPage()

                    elif msg == '접속중':   #중복 접속 오류
                        login_error_page.title('login error(3)')
                        lab.config(text='접속 중인 ID 입니다')
                        lab.pack()
                        login_error_page.mainloop()
                        self.client_socket.close()

                    else:   #ID PW 입력 오류
                        login_error_page.title('login error(4)')
                        lab.config(text='ID와 PW를 확인해 주세요')
                        lab.pack()
                        login_error_page.mainloop()
                        self.client_socket.close()

    #회원가입 화면
    def AccountPage(self, addr):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        print('회원가입')

        #화면설정
        account_page = Toplevel()
        account_page.geometry('250x100+700+350')
        account_page.resizable(False, False)
        account_page['bg'] = '#ffeb33'

        guide_label = Label(account_page, text='', font=Font(size=15), height=40)
        guide_label['bg'] = '#ffeb33'

        try:
            IP = addr.split(':')[0]
            PORT = addr.split(':')[1]
            self.client_socket.connect((IP, int(PORT))) #서버에 연결시도

        #서버 주소 오류 or 서버 안열림
        except:
            account_page.title('server error(2)')
            guide_label.config(text='서버주소와 포트를 확인해 주세요', wraplength=200)
            guide_label.pack()
            self.client_socket.close()
        
        else:
            #서버와 연결되면 회원가입 화면 표시
            account_page.title('회원가입')
            account_page.geometry('250x320+700+250')
            account_page.resizable(False, False)
            account_page['bg'] = '#f6f6f6'

            guide_label = Label(account_page, width=20)
            guide_label['bg'] = '#f6f6f6'
            guide_label.pack(pady=20)

            #ID 입력칸 넣기
            id_entry = Entry(account_page, width=2, font=Font(size=10))
            id_entry.pack(ipadx=50, ipady=10)

            #PW 입력칸 넣기
            pw_entry = Entry(account_page, width=2, font=Font(size=10))
            pw_entry.pack(ipadx=50, ipady=10, pady=1)

            #회원가입 버튼
            create_button = Button(account_page, width=15, height=2, relief='flat', text='회원가입',
                                    command= lambda: self.NewAccount(id_entry.get(), pw_entry.get()))
            create_button.pack(pady=5)
            account_page.mainloop()

    #회원가입 과정
    def NewAccount(self, id, pw):
        
        #회원가입 결과 표시 화면 설정
        create_success = Toplevel()
        create_success.geometry('250x100+700+350')
        create_success.resizable(False, False)
        create_success['bg'] = '#ffeb33'

        guide_label = Label(create_success, text='', font=Font(size=15), height=40)
        guide_label['bg'] = '#ffeb33'
        guide_label.pack()

        #서버에 회원가입 요청
        self.client_socket.send('command:Command_CreateAccount'.encode('utf-8'))
        msg = ''
        print('서버에 ID 전송 중...')
        self.client_socket.send(str(id).encode('utf-8'))    #서버에 ID 전송
        while(msg == ''):
            print('응답 대기중(5)...')
            msg = self.client_socket.recv(1024).decode('utf-8') #응답 대기
        print('ID 전송 성공')

        #이미 사용중인 ID일 경우
        if msg == '중복':
            print('아이디 중복')
            guide_label.config(text='이미 사용중인 ID 입니다')
            self.client_socket.close()
        
        elif msg == '오류':
            msg = ''
            print('생성 오류')
            guide_label.config(text='ID/PW 입력 오류입니다')
            self.client_socket.close()

        elif msg == '가능':
            msg = ''
            print('계정 생성 중...')
            self.client_socket.send(str(pw).encode('utf-8'))    #서버에 PW 전송
            while(msg == ''):
                print('응답 대기중(6)...')
                msg = self.client_socket.recv(1024).decode('utf-8') #응답 대기
            print('회원가입 완료')
            guide_label.config(text='회원가입 완료')
            self.client_socket.close()
        create_success.mainloop()

    #채팅화면
    def ChatPage(self):
        print('채팅화면 이동 성공')       
        self.window.destroy()   #화면 초기화

        #스레드 시작
        self.listen_thread()

        #채팅화면 설정
        self.window = Tk()
        self.window.title('채팅방')
        self.window.geometry('400x550+650+100')
        self.window.resizable(False, False)
        self.window['bg'] = '#b2c7d9'

        frame_chat = Frame(self.window) #채팅창 프레임
        frame_bottom = Frame(self.window, background='WHITE')   #입력창 프레임

        #입력창
        self.send_text = Text(frame_bottom, width=45, height=7, padx=10, pady=10, relief='flat')
        self.send_text.grid(row=0, column=0)

        #채팅창
        self.recv_text = Text(frame_chat, width=57, height=34, state='disabled', relief='flat', cursor='arrow')
        self.recv_text['bg'] = '#b2c7d9'
        self.recv_text.pack()

        #전송버튼
        send_button = Button(frame_bottom, text='전송', relief='flat', width=5,
                                command= lambda: self.send_chat(self.send_text.get('1.0', END)))
        send_button['bg'] = '#ffec42'
        send_button.grid(row=0, column=1, padx=10, pady= 10, sticky=N)

        #프레임 넣기
        frame_chat.pack(side='top', fill='both')
        frame_bottom.pack(side='bottom', fill='both')
        self.window.mainloop()

    #채팅 보내기
    def send_chat(self, msg):
        #채팅창 설정
        self.recv_text.config(state='normal')
        self.recv_text.insert(END, '나:'+ msg + '\n')
        self.recv_text.yview(END)
        self.recv_text.config(state='disabled')

        print('보낼 메세지:', msg)
        self.client_socket.send(('message:{}:{}'.format(self.user_name, msg)).encode('utf-8'))
        print('보내기 성공')
        self.send_text.delete(1.0, 'end')

    #recv 스레드
    def listen_thread(self):
        print('스레드 호출 성공')
        t = Thread(target=self.receive_message, args=(self.client_socket,))
        t.start()
        print('스레드 시작 완료')

    #데이터 받기            
    def receive_message(self, so):
        print('데이터 받기 호출 성공')

        while True:
            buf = str(so.recv(1024).decode('utf-8')).lstrip()   #데이터 받기

            #받은 데이터 채팅창에 표시
            self.recv_text.config(state='normal')
            self.recv_text.insert(END, buf)
            self.recv_text.yview(END)
            self.recv_text.config(state='disabled')

if __name__ == "__main__":
    ChatClient()

import tkinter as tk

################################################################
user = dict(test='123')

def checkid():
    print('hello')
################################################################

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginPage)

    #화면 전환
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

####################################### 로그인(화면1) #######################################
class LoginPage(tk.Frame):
    def __init__(self, master):
        master.geometry('300x500')
        tk.Frame.__init__(self, master)
        id = tk.Entry(master)
        id.insert(0, 'id입력')
        pw = tk.Entry(master)
        pw.insert(0, 'pw입력')
        id.pack()
        pw.pack()
        tk.Button(self, text="로그인",
                  command=lambda: master.switch_frame(UserListPage)).pack()
####################################################################################################

####################################### 사용자 목록 화면(화면2) #######################################
class UserListPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.geometry('300x500')
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="UserListPage", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(ChatListPage)).pack()
####################################################################################################

####################################### 채팅창 목록(화면3) #######################################
class ChatListPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        tk.Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(UserListPage)).pack()
####################################################################################################



####################################################################################################
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
####################################################################################################
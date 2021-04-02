import hashlib
import socket
from tkinter import Tk, Label, Button, Entry, PhotoImage, messagebox

import LoggedUI

LABEL_FONT = ('Impact', 26)
BUTTON_FONT = ('Impact', 18)
ENTRY_FONT = ('Impact', 22)
BUTTON_WIDTH = 10
BUTTON_HEIGHT = 2

HEADER = 256
PORT = 5050
FORMAT = 'utf-8'
SERVER = '192.168.56.1'
ADDR = (SERVER, PORT)


class Gui:
    def __init__(self, master):
        self.master = master
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Server connection
        try:
            self.client.connect(ADDR)
        except socket.error as ConnectionAbortedError:
            self.master.quit()
            self.connection_info = messagebox.showerror(title='Connection Error', message=f'{ConnectionAbortedError}')
        # Gui design
        master.title("Password Master")
        master.geometry('1280x720')
        master.resizable(0, 0)
        self.background = PhotoImage(file='Images/background.png')
        self.background_label = Label(master, image=self.background).pack()
        # Log in
        self.login_info = Label(master, text='Log in', font=LABEL_FONT).place(x=580, y=160)
        self.user_name_label = Label(master, text='Username', font=LABEL_FONT).place(x=160, y=240)
        self.user_password_label = Label(master, text='Password', font=LABEL_FONT).place(x=160, y=330)
        # log in entries
        self.user_name_entry = Entry(master, width=20, font=ENTRY_FONT)
        self.user_name_entry.place(x=380, y=249)
        self.user_password_entry = Entry(master, width=20, font=ENTRY_FONT, show='*')
        self.user_password_entry.place(x=380, y=340)
        # login and register buttons
        self.submit_button = Button(master, text="Log in", height=BUTTON_HEIGHT,
                                    width=BUTTON_WIDTH, font=BUTTON_FONT, command=self.send_user).place(x=370, y=440)
        self.register_button = Button(master, text="Register", height=BUTTON_HEIGHT,
                                      width=BUTTON_WIDTH, font=BUTTON_FONT,
                                      command=self.register_form).place(x=540, y=440)

    def get_user_name(self):
        return self.user_name_entry.get()

    def get_password_user(self):
        return self.user_password_entry.get()

    def send_user(self):
        user = self.get_user_name()
        passw = self.hash_password(self.get_password_user())
        action_info = 'L'
        user_data = action_info + ';' + user + ';' + passw + ';'
        self.send_request(user_data)
        server_results = int(self.client.recv(HEADER).decode(FORMAT))
        print(server_results)
        if server_results:
            self.send_request('Q')
            self.master.destroy()
            logged = Tk()
            logged_user = LoggedUI.LoggedUI(logged, user)
            logged.mainloop()
        else:
            messagebox.showerror(message='No matching Data!')

    def register_form(self):
        user = self.get_user_name()
        passw = self.hash_password(self.get_password_user())
        action_info = 'R'
        user_data = action_info + ';' + user + ';' + passw + ';'
        self.send_request(user_data)
        server_results = self.client.recv(HEADER).decode(FORMAT)
        if server_results == '1':
            messagebox.showinfo(message='The user has been created! \n Now You can log in')
            self.user_name_entry.delete(0, 'end')
            self.user_password_entry.delete(0, 'end')
        else:
            messagebox.showerror(message=f'{server_results}')

    def send_request(self, request):
        request = request.encode(FORMAT)
        self.client.send(request)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()


root = Tk()
my_gui = Gui(root)
root.mainloop()

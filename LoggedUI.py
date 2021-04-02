import socket
from tkinter import Tk, Label, Button, Entry, PhotoImage, messagebox, Listbox, END

LABEL_FONT = ('Impact', 26)
BUTTON_FONT = ('Impact', 18)
ENTRY_FONT = ('Impact', 22)
BUTTON_WIDTH = 12
BUTTON_HEIGHT = 2

HEADER = 256
PORT = 5050
FORMAT = 'utf-8'
SERVER = '192.168.56.1'
ADDR = (SERVER, PORT)

server_connection = True  # Variable to change desing of UI


class LoggedUI:
    def __init__(self, master, user_name):
        self.master = master
        self.user_name = user_name
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if server_connection:
            try:
                self.client.connect(ADDR)
            except socket.error as ConnectionAbortedError:
                self.master.quit()
                self.connection_info = messagebox.showerror(title='Connection Error',
                                                            message=f'{ConnectionAbortedError}')

        master.title("Password Master")
        master.geometry('1280x720')
        master.resizable(0, 0)
        self.background = PhotoImage(file='Images/background.png')
        self.background_label = Label(master, image=self.background).pack()

        self.user_account_label = Label(master, text='Logged in: {}'.format(user_name), font=LABEL_FONT).place(x=100,
                                                                                                               y=100)
        self.user_pass_label = Label(master, text='Passwords: ', font=LABEL_FONT).place(x=100, y=150)

        # Adding passwords
        self.user_add_passw_label = Label(master, text='Password Name         Password', font=LABEL_FONT).place(x=772,
                                                                                                                y=150)
        self.user_pass_name_entry = Entry(master, width=12, font=ENTRY_FONT)
        self.user_pass_name_entry.place(x=780, y=230)
        self.user_password_entry = Entry(master, width=12, font=ENTRY_FONT)
        self.user_password_entry.place(x=1000, y=230)
        self.submit_button = Button(master, text="Add Password", height=BUTTON_HEIGHT,
                                    width=BUTTON_WIDTH, font=BUTTON_FONT, command=self.add_password).place(x=1045,
                                                                                                           y=300)

        # Deleting Passwords
        self.user_add_passw_label = Label(master, text='ID of Password', font=LABEL_FONT).place(x=982, y=420)
        self.pass_id_entry = Entry(master, width=12, font=ENTRY_FONT)
        self.pass_id_entry.place(x=1000, y=500)
        self.delete_button = Button(master, text="Delete", height=BUTTON_HEIGHT,
                                    width=BUTTON_WIDTH, font=BUTTON_FONT, command=self.delete_password).place(x=1045,
                                                                                                              y=550)

        # Logut button
        self.submit_button = Button(master, text="Log out", height=BUTTON_HEIGHT,
                                    width=BUTTON_WIDTH, font=BUTTON_FONT, command=self.logout).place(x=50, y=625)

        self.testt = '1 Netflix xsd@xd# \n 2 Email xsddasd23sda '
        # Password holder
        self.show_password_button = Button(master, text="Show Passwords", height=BUTTON_HEIGHT,
                                           width=13, font=BUTTON_FONT, command=self.display_passwords).place(x=350,
                                                                                                             y=625)
        self.pass_list = Listbox(self.master, width=75, height=22)
        self.pass_list.place(x=100, y=220)

    def logout(self):
        self.send_request('Q')
        self.master.destroy()

    def delete_password(self):
        pass_id = self.pass_id_entry.get()
        pass_request = 'D' + ';' + self.user_name + ';' + pass_id
        self.send_request(pass_request)
        server_response = self.client.recv(HEADER).decode(FORMAT)
        if int(server_response):
            messagebox.showinfo(message='Password Deleted!')
            self.display_passwords()
        else:
            messagebox.showerror(title='Invalid Input!', message='Index of pass does not exist')

    def add_password(self):
        password_name = self.user_pass_name_entry.get()
        password = self.user_password_entry.get()
        password_data = 'A' + ';' + self.user_name + ';' + password_name + ';' + password
        self.send_request(password_data)
        server_response = self.client.recv(HEADER).decode(FORMAT)
        if int(server_response):
            messagebox.showinfo(message='Password Added!')
            self.display_passwords()
        else:
            messagebox.showerror(message='Failed when inserting the password')

    def display_passwords(self):
        self.send_request(f'S;{self.user_name}')
        final = []
        counter = 0
        row = []
        string_data = self.client.recv(HEADER).decode(FORMAT)
        data_separeted = string_data.split(';')
        self.pass_list.delete(0, END)
        for i in range(len(data_separeted) - 1):
            if counter < 3:
                row.append(data_separeted[i])
                counter += 1
            if counter == 3:
                final.append(row)
                row = []
                counter = 0
        for i in range(len(final)):
            self.pass_list.insert(END, final[i])

    def send_request(self, request):
        request = request.encode(FORMAT)
        self.client.send(request)


if not server_connection:
    root = Tk()
    my_gui = LoggedUI(root, 'Andrzej')
    root.mainloop()

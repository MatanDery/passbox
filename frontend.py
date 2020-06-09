from tkinter import *
from tkinter import ttk
from backend import Back
from Crypto.Cipher import AES
from hashlib import sha1
from binascii import hexlify
from requests import get


class popup_dec():
    def __init__(self):
        try:
            with open('creds.db', 'rb') as f:
                if f.read()[:15] == b'SQLite format 3':
                    return
        except:
            return
        self.popup = Tk()
        self.popup.wm_title("!")
        label = ttk.Label(self.popup, text="ENTER PASSWORD!")
        lable_user = Label(text="Enter Decription Pass")
        lable_user.pack()
        self.pass_dec = StringVar()
        self.entry_pass = Entry(textvariable=self.pass_dec)
        self.entry_pass.pack()
        b1 = ttk.Button(self.popup, text="Okay", command=self.dec)
        b1.pack()
        self.popup.mainloop()

    def dec(self):
        key = self.pass_dec.get()
        if len(key) % 16 != 0:
            padding = 16 - len(key) % 16
            key = key + 'A' * padding
        key = key.encode()
        with open('creds.db', 'rb') as f:
            data = f.read()
            if data[:15] == b'SQLite format 3':
                return
            else:
                f.close()
                with open('creds.db', 'wb') as f:
                    enc_data = AES.new(key, AES.MODE_CBC, iv=b'abcdefghijklmnop')
                    enc_data = enc_data.decrypt(data)
                    #print(enc_data)
                    if enc_data[:15] == b'SQLite format 3':
                        f.write(enc_data)
                        self.popup.destroy()
                    else:
                        f.write(data)
                        return

popup_dec()
try:
    with open('creds.db', 'rb') as f:
        data = f.read()
        if data[:15] == b'SQLite format 3':
            back_db = Back()
        else:
            quit()
except FileNotFoundError:
    back_db = Back()


class Ui():
    def __init__(self, main_window):
        main_window.wm_title("Users Locker")
        lable_site = Label(text="site")
        lable_site.grid(row=0, column=0)
        self.entry_site_val=StringVar()
        self.entry_site = Entry(textvariable=self.entry_site_val)
        self.entry_site.grid(row=0, column=1)

        lable_user = Label(text="username")
        lable_user.grid(row=1, column=0)
        self.entry_user_val=StringVar()
        self.entry_user = Entry(textvariable=self.entry_user_val)
        self.entry_user.grid(row=1, column=1)

        lable_pass = Label(text="password")
        lable_pass.grid(row=2, column=0)
        self.entry_pass_val=StringVar()
        self.entry_pass = Entry(textvariable=self.entry_pass_val)
        self.entry_pass.grid(row=2, column=1)

        self.cred_list = Listbox(main_window, height=30, width=100, )
        self.cred_list.grid(row=5, column=0, rowspan=10, columnspan=9)


        view_all_button = Button(main_window, text='View All', command=self.view_all_wrap)
        view_all_button.grid(row=4, column=0)

        add_entry_button = Button(main_window, text='Add Site', command=self.add_entry_wrap)
        add_entry_button.grid(row=4, column=1)

        del_entry_button = Button(main_window, text='Delete Site', command=self.del_entry_wrap)
        del_entry_button.grid(row=4, column=2)

        search_entry_button = Button(main_window, text='Search Site', command=self.find_site)
        search_entry_button.grid(row=4, column=3)

        self.enc_pass = StringVar()
        self.enc_pass = Entry(textvariable=self.enc_pass)
        self.enc_pass.grid(row=3, column=10)
        enc_button = Button(main_window, text='Encrypt DB', command=self.enc)
        enc_button.grid(row=4, column=10)

        src_passwd_button = Button(main_window, text='Search Password', command=self.find_passwd)
        src_passwd_button.grid(row=4, column=4)

        chk_passwd_button = Button(main_window, text='check Password', command=self.chack_safe_pass)
        chk_passwd_button.grid(row=2, column=2)



    def enc(self):
        key = self.enc_pass.get()
        if len(key) == 0:
            return
        if len(key) % 16 != 0:
            padding = 16 - len(key) % 16
            key = key + 'A' * padding
        key = key.encode()
        with open('creds.db', 'rb') as f:
            data = f.read()
            if data[:15] != b'SQLite format 3':
                return
            else:
                f.close()
                with open('creds.db', 'wb') as f:
                    enc_data = AES.new(key, AES.MODE_CBC, iv=b'abcdefghijklmnop')
                    enc_data = enc_data.encrypt(data)
                    f.write(enc_data)
                    quit()

    def view_all_wrap(self):
        self.cred_list.delete(0,END)
        for row in back_db.view_table():
            self.cred_list.insert(END, row)

    def add_entry_wrap(self):
        back_db.add_entry_to_table(self.entry_site_val.get(), self.entry_user_val.get(), self.entry_pass_val.get())
        self.view_all_wrap()

    def del_entry_wrap(self):
        back_db.delete_entry(self.entry_site_val.get())
        self.view_all_wrap()

    def find_site(self):
        res = back_db.view_entry(self.entry_site_val.get())
        self.cred_list.delete(0, END)
        self.cred_list.insert(END,res)

    def find_passwd(self):
        exists = back_db.search_by_pass(self.entry_pass_val.get())
        self.cred_list.delete(0, END)
        for row in exists:
            self.cred_list.insert(END, row)

    def chack_safe_pass(self):
        self.cred_list.delete(0, END)
        curpasswd = self.entry_pass_val.get()
        curpasswd = hexlify(sha1(curpasswd.encode()).digest()).decode().upper()
        try:
            x = get(f'https://api.pwnedpasswords.com/range/{curpasswd[:5]}')
        except:
            self.cred_list.insert(END, 'bad response')
            return
        res = x.content.decode().split('\r\n')
        for i in res:
            if curpasswd[5:] in i:
                i = i.split(':')
                self.cred_list.insert(END, f'Bad Password Leaked {i[1]} times')
                return
        else:
            self.cred_list.insert(END, 'Good Password!!! never leaked before')
            return


main_window = Tk()
Ui(main_window)
main_window.mainloop()


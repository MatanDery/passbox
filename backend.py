import sqlite3
from hashlib import sha256
from binascii import hexlify

class Back:

    def __init__(self):
        self.con = sqlite3.connect('creds.db')
        self.cur = self.con.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS users(site, name, passwd)')
        self.con.commit()

    def add_entry_to_table(self, site, user, passwd):
        salt = site
        pepper = 'qwerty'
        passwd = salt + passwd + pepper
        passwd = hexlify(sha256(passwd.encode()).digest())
        x = self.cur.execute("SELECT * FROM users where site=(?) AND name=(?) AND passwd=(?)", (site, user, passwd))
        if len(x.fetchall()) > 0 :
            return 'ALREADY EXISTS'
        else:
            self.cur.execute("INSERT INTO users values(?, ?, ?)", (site, user, passwd))
            self.con.commit()

    def view_table(self):
        return (self.cur.execute("SELECT * FROM users ").fetchall())

    def view_entry(self, site):
        return self.cur.execute('SELECT * FROM users Where site=(?)', (site, )).fetchone()

    def delete_entry(self, site):
        self.cur.execute("DELETE FROM users where site =?", (site, ))
        self.con.commit()

    def edit_entry_site(self, site, new_site):
        self.cur.execute("UPDATE users SET site =(?) WHERE site =(?)", (new_site, site))
        self.con.commit()

    def search_by_pass(self, passwd):
        table = self.view_table()
        exists = []
        for i in table:
            site, user, curpasswd = i[0], i[1], i[2]
            salt = site
            pepper = 'qwerty'
            check_passwd = salt + passwd + pepper
            check_passwd = hexlify(sha256(check_passwd.encode()).digest())
            if check_passwd == curpasswd:
                exists.append(i)
        return exists

    def quit_db(self):
        self.con.close()



# con = sqlite3.connect('creds.db')
# cur = con.cursor()
# user='matan543'
# site='alibaba'
# passwd='P@ssw0rd'
# print(cur.execute("SELECT * FROM users ").fetchall())
# con.commit()
# con.close()
# create_table()
# add_entry_to_table(site,user,passwd)
# add_entry_to_table(site+'123', user, passwd)
# add_entry_to_table(site+'456', user, passwd)
# view_table()
# view_entry('alibaba123')
# edit_entry_site("alibaba123","google.com")


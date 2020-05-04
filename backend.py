import sqlite3

def create_table():
    con = sqlite3.connect('creds.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE users(site, name, passwd)')
    con.commit()
    con.close()

def add_entry_to_table(site,user,passwd):
    con = sqlite3.connect('creds.db')
    cur = con.cursor()
    cur.execute("INSERT INTO users values(?, ?, ?)", (site, user, passwd))
    con.commit()
    con.close()

def view_table():
    con = sqlite3.connect('creds.db')
    cur = con.cursor()
    print(cur.execute("SELECT * FROM users ").fetchall())
    con.close()

def view_entry(site):
    con = sqlite3.connect('creds.db')
    cur = con.cursor()
    print(cur.execute('SELECT * FROM users Where site=?', (site, )).fetchone())
    con.close()

def delete_entry(site):
    con = sqlite3.connect('creds.db')
    cur = con.cursor()
    print(cur.execute("DELETE * FROM users where site =(?)",(site)))
    con.commit()
    con.close()


# con = sqlite3.connect('creds.db')
# cur = con.cursor()
user='matan543'
site='alibaba'
passwd='P@ssw0rd'
# print(cur.execute("SELECT * FROM users ").fetchall())
# con.commit()
# con.close()
# create_table()
# add_entry_to_table(site,user,passwd)
# add_entry_to_table(site+'123', user, passwd)
# add_entry_to_table(site+'456', user, passwd)
view_table()
view_entry('alibaba123')



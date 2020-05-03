import sqlite3


con = sqlite3.connect('creds.db')
cur = con.cursor()
#cur.execute('CREATE TABLE users(name, site, passwd)')
user='matan543'
site='alibaba'
passwd='P@ssw0rd'
cur.execute("INSERT INTO users values(?, ?, ?)",(user, site, passwd))
print(cur.execute("SELECT * FROM users ").fetchall())
#con.commit()
con.close()






import sqlite3

dbname = 'user.db'
con = sqlite3.connect(dbname)
cur = con.cursor()

# cur.execute("CREATE TABLE user_data(id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING, password STRING)")
# con.commit()

cur.execute("CREATE TABLE bookmark(id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING, title STRING, urlname)")
con.commit()

# cur.execute('DROP TABLE bookmark')
# cur.execute('DROP TABLE user_data')

cur.close()
con.close()
import sqlite3

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (null,'vs code', 'C:\\Users\\cnb\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe')"
# cursor.execute(query)
# con.commit()

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'sarkari result', 'https://www.sarkariresult.com/')"
# cursor.execute(query)
# con.commit()

# query = "DELETE FROM sys_command WHERE id = 149"
# cursor.execute(query)
# con.commit()
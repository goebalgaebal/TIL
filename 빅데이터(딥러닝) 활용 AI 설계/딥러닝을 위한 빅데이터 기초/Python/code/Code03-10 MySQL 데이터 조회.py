import pymysql
conn = pymysql.connect(host = "192.168.56.106",
                       user = "root",
                       password = "1234",
                       db = "samsongDB",
                       charset = "utf8")

cur = conn.cursor()
sql = "SELECT * FROM userTable2;"
cur.execute(sql)

rows = cur.fetchall()
print(rows)

cur.close()
conn.close()

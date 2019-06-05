import pymysql
conn = pymysql.connect(host = "192.168.56.106",
                       user = "root",
                       password = "1234",
                       db = "samsongDB",
                       charset = "utf8")
cur = conn.cursor()
sql = "CREATE TABLE IF NOT EXISTS userTable2(userid INT, userNae CHAR(5));"
cur.execute(sql)

sql = "INSERT INTO userTABLE2 VALUES(1, '홍길동');"
cur.execute(sql)

sql = "INSERT INTO userTABLE2 VALUES(2, '이순신');"
cur.execute(sql)

cur.close()
conn.commit()
conn.close()
print("OK")


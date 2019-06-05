#파이썬 for Beginner P.429

import sqlite3
conn = sqlite3.connect("samsongDB") # 1. DB 연결 (연결자 생성) 있으면 open, 없으면 create
cur = conn.cursor() # cursor 생성(트럭, 연결 로프, 왔다갔다 하면서 데이터를 옮겨줌)
sql = "CREATE TABLE IF NOT EXISTS userTable(userid INT, userNae CHAR(5));"
cur.execute(sql)

sql = "INSERT INTO userTABLE VALUES(1, '홍길동');"
cur.execute(sql)

sql = "INSERT INTO userTABLE VALUES(2, '이순신');"
cur.execute(sql)

cur.close()
conn.commit()
conn.close() # 6. DB 닫기 (= 연결 해제)
print("OK")


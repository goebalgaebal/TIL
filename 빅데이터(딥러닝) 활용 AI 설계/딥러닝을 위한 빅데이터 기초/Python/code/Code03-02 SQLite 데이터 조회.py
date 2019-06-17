#파이썬 for Beginner P.433

import sqlite3

conn = sqlite3.connect("samsongDB") # 1. DB 연결
cur = conn.cursor() # 2. cursor 생성
sql = "SELECT * FROM userTable;"
cur.execute(sql) # cursor가 data를 싣고옴

rows = cur.fetchall() # cur의 data 전체를 rows에 대입
print(rows)

cur.close()
conn.close() # 6. DB 닫기 (= 연결 해제)
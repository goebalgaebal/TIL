# 1. 파일 열기
inFp = open("c:/windows/win.ini", "r")
outFp = open("images\\new_win.ini", "w")

# 2. 파일 읽기/ 쓰기
while True : # data가 대용량인 경우, 한 줄씩 불러오는 것이 좋다
    inStr = inFp.readline()
    if not inStr:
        break
    #print(inStr, end = "")
    outFp.write(inStr)
# inStrList = inFp.readlines()
# print(inStrList)
#
# for line in inStrList :
#     print(line, end = "")

# 3. 파일 닫기
inFp.close()
outFp.close()
from tkinter.filedialog import *
import math
import os
import os.path
import pymysql
import tempfile

###############
## 전역 변수 ##
###############
IP_ADDR = "192.168.56.109"
USER_NAME = "root"
USER_PASS = "1234"
DB_NAME = "BigData_DB"
CHAR_SET = "utf8"

rawFileList = None

############
## 함수부 ##
############
def selectFile() :
    global rawFileList
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw;"), ("모든 파일", "*.*")))
    if filename == "" or filename == None :
        return

    rawFileList = []
    dirName, extname = filename.split(".")
    if extname.upper().strip() == "RAW":  # [중요] 공백처리
        rawFileList.append(dirName + "." + extname)
    edt1.insert(0, str(filename))

def selectFolder() :
    global rawFileList
    foldername = askdirectory()
    if foldername == "" or foldername == None:
        return
    edt1.insert(0, str(foldername))

    # 파일 목록 읽기
    rawFileList = []
    for dirName, subDirList, fnames in os.walk(foldername) :
        for fname in fnames :
            filename, extname = os.path.basename(fname).split(".")
            if extname.upper().strip() == "RAW" : # [중요] 공백처리
                rawFileList.append(os.path.join(dirName, fname))
    print(rawFileList)

def malloc(h, w, initValue = 0) :
    returnMemory = []
    for _ in range(h) :
        tmpList = []
        for _ in range(w) :
            tmpList.append(initValue)
        returnMemory.append(tmpList)
    return returnMemory

def findStat(fname) :
    fsize = os.path.getsize(fname)
    inH = inW = int(math.sqrt(fsize))

    inImage = malloc(inH, inW)

    # 파일 → 메모리
    with open(fname, 'rb') as rFp:
        for i in range(inH):
            for k in range(inW):
                inImage[i][k] = int(ord(rFp.read(1)))

    sum = 0
    for i in range(inH) :
        for k in range(inW) :
            sum += inImage[i][k]
    avg = sum // (inH * inW)

    maxVal = inImage[0][0]
    minVal = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < minVal:
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal:
                maxVal = inImage[i][k]

    return avg, maxVal, minVal

def uploadData() :
    global rawFileList
    con = pymysql.connect(host = IP_ADDR, user = USER_NAME, password = USER_PASS,
                          db = DB_NAME, charset = CHAR_SET)
    cur = con.cursor()

    try :
        sql = '''
            CREATE TABLE rawImage_TBL (
            raw_id INT AUTO_INCREMENT PRIMARY KEY,
            raw_fname VARCHAR(30),
            raw_extname CHAR(5),
            raw_height SMALLINT, raw_width SMALLINT,
            raw_avg TINYINT UNSIGNED, 
            raw_max TINYINT UNSIGNED,
            raw_min TINYINT UNSIGNED)
        '''
        cur.execute()
    except : # 이미 TABLE이 존재하는 경우
        pass

    for fullname in rawFileList:
        with open(fullname, 'rb') as rfp:
            binData = rfp.read()

        fname, extname = os.path.basename(fullname).split(".")
        fsize = os.path.getsize(fullname)
        height = width = int(math.sqrt(fsize))

        avgVal, maxVal, minVal = findStat(fullname) # 평균, 최대, 최소
        print(avgVal, maxVal, minVal)

        sql = "INSERT INTO rawImage_TBL(raw_id, raw_fname, raw_extname, raw_height, raw_width, "
        sql += "raw_avg, raw_max, raw_min, raw_data) "
        sql += "VALUES(NULL, '" + fname + "', '" + extname + "', " + str(height) + ", " + str(width) + ", "
        sql += str(avgVal) + ", " + str(maxVal) + ", " + str(minVal) + " , %s )"
        print(sql)
        tupleData = (binData, )
        cur.execute(sql, tupleData)

    con.commit()
    cur.close()
    con.close()
    print("Upload Complete")

def downloadData() :
    con = pymysql.connect(host = IP_ADDR, user = USER_NAME, password = USER_PASS,
                          db = DB_NAME, charset = CHAR_SET)
    cur = con.cursor()
    sql = "SELECT raw_fname, raw_data FROM rawImage_TBL WHERE raw_id = 1"
    cur.execute(sql)
    fname, binData = cur.fetchone()

    fullpath = tempfile.gettempdir() + "/" + fname
    with open(fullpath, "wb") as wfp :
        wfp.write(binData)
    print("경로", fullpath)

    con.commit()
    cur.close()
    con.close()
    print("Download Complete")

#################
## 메인 코드부 ##
#################
if __name__ == '__main__':
    window = Tk()
    window.title("Folder into DB ver 0.02")
    window.geometry("500x500")
    window.resizable(width=True, height=True)

    edt1 = Entry(window, width = 50)
    edt1.pack()

    btnFile = Button(window, text = "파일 탐색", command = selectFile)
    btnFile.pack()

    btnFolder = Button(window, text="폴더 탐색", command=selectFolder)
    btnFolder.pack()

    btnUpload = Button(window, text = "업로드", command = uploadData)
    btnUpload.pack()

    btnDownload = Button(window, text="다운로드", command=downloadData)
    btnDownload.pack()

    window.mainloop()
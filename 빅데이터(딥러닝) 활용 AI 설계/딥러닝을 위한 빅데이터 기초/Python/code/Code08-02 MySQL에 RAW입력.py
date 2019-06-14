from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import pymysql
import datetime
import tempfile

###############
## 전역 변수 ##
###############
IP_ADDR = "192.168.56.108"
USER_NAME = "root"
USER_PASS = "1234"
DB_NAME = "BigData_DB"
CHAR_SET = "utf8"

############
## 함수부 ##
############
def selectFile() :
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw;"), ("모든 파일", "*.*")))
    if filename == "" or filename == None :
        return
    edt1.insert(0, str(filename))

def uploadData() :
    con = pymysql.connect(host = IP_ADDR, user = USER_NAME, password = USER_PASS,
                          db = DB_NAME, charset = CHAR_SET)
    cur = con.cursor()

    fullname = edt1.get()
    with open(edt1.get(), "rb") as rfp :
        binData = rfp.read()

    fname = os.path.basename(fullname)
    fsize = os.path.getsize(fullname)
    height = width = int(math.sqrt(fsize))
    upDate = datetime.datetime.now().strftime("%y-%m-%d")
    upUser = USER_NAME

    sql = "INSERT INTO rawIMAGE_TBL(raw_id, raw_height, raw_width, raw_fname, raw_avg, " \
          "raw_update, raw_uploader, raw_data) " \
          "VALUES(NULL, " + str(height) + ", " + str(width) + ", '" + fname + "'," + str(0) + \
          ", '" + upDate + "', '" + upUser + "', %s )"
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
    window.title("RAW into DB ver 0.02")
    window.geometry("500x500")
    window.resizable(width=True, height=True)

    edt1 = Entry(window, width = 20)
    edt1.pack()

    btnFile = Button(window, text = "파일 탐색", command = selectFile)
    btnFile.pack()

    btnUpload = Button(window, text = "업로드", command = uploadData)
    btnUpload.pack()

    btnDownload = Button(window, text="다운로드", command=downloadData)
    btnDownload.pack()

    window.mainloop()
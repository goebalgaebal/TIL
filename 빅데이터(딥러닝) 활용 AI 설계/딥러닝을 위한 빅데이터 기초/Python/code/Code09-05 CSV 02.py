import csv
from tkinter.filedialog import *

## 우리회사 연봉 평균
filename = askopenfilename(parent = None, filetypes=(("CSV 파일", "*.csv;"), ("모든 파일", "*.*")))

csvList = []
with open(filename) as rfp :
    sum, count = 0, 0
    # line = rfp.readline()
    # while True :
    #     line = rfp.readline()
    #     if not line :
    #         break
    #     count += 1
    #     lineList = line.split(",")
    #     sum += int(lineList[3])
    # avg = sum // count
    reader = csv.reader(rfp)
    headerList = next(reader)

    for clist in reader :
        # print(clist)
        csvList.append(clist)
    #     sum += int(clist[3])
    #     count += 1
    # avg = sum // count
    # print(avg)

    print(csvList)

## 가격을 10% 인상시키기
#1. Cost 열의 위치를 찾아내기
headerList = [ data.upper().strip() for data in headerList]
pos = headerList.index("COST")
for i in range(len(csvList)) :
    rowList = csvList[i]
    cost = rowList[pos]
    cost = float(cost[1:]) # $제거
    cost *= 1.1
    costStr = "${0:.2f}".format(cost) # 소수 2번째까지 표현
    csvList[i][pos] = costStr
print(csvList)

## 결과 저장
saveFp = asksaveasfile(parent = None, mode = "wt", defaultextension = "*.csv",
                           filetypes=(("CSV 파일", "*.csv;"), ("모든 파일", "*.*")))

with open(saveFp.name, mode = "w", newline = "") as wFp :
    writer = csv.writer(wFp)
    writer.writerow(tuple(headerList))
    for row in csvList :
        print(row)
        writer.writerow(row)




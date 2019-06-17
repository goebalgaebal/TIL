import csv

## 우리회사 연봉 평균
with open(".\\csv\\emp.csv") as rfp :
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
        sum += int(clist[3])
        count += 1
    avg = sum // count
    print(avg)




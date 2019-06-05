import pymysql

if __name__ == '__main__':
    # DB 연결
    conn = pymysql.connect(host = "192.168.56.102",
                           user = "root",
                           password = "1234",
                           db = "mission03",
                           charset = "utf8")
    cur = conn.cursor()

    # # Table 생성
    # sql = "CREATE TABLE IF NOT EXISTS missionTable(employeeId INT," \
    #       " employeeName VARCHAR(10)," \
    #       " joinYear SMALLINT);"
    # cur.execute(sql)

    while True:
        print("==============================")
        print("0. 프로그램 종료")
        print("1. 사원 추가")
        print("2. 사원 조회")
        print("==============================")

        inputNum = int(input("실행하시고자 하는 작업을 선택해주세요 >>> "))

        if(inputNum == 0) :
            print("프로그램을 종료합니다\n")
            break

        elif(inputNum == 1) :
            while True :
                employeeId = input("사번을 0 입력 시, 사원 추가를 종료합니다.\n사번을 입력해주세요 >>> ")

                if(int(employeeId) == 0 ):
                    break
                employeeName = input("사원 이름를 입력해주세요 >>> ")
                joinYear  = input("입사연도를 입력해주세요 >>> ")

                sql = "INSERT INTO missionTable VALUES(%s, \"%s\", %s);" % (employeeId, employeeName, joinYear)
                cur.execute(sql)

                print(employeeId, "번", employeeName, "사원을 추가하였습니다\n")
                conn.commit()

        else :
            sql = "SELECT * FROM missionTable;"
            cur.execute(sql)

            print("==============================")
            print(" 사번\t 사원 이름\t 입사연도")
            print("==============================")

            while True :
                row = cur.fetchone()
                if row == None :
                    print("모든 사원을 다 출력하였습니다\n\n")
                    break

                print("%3d\t\t%5s\t\t%d" % (row[0], row[1], row[2]))

    cur.close()
    conn.close()
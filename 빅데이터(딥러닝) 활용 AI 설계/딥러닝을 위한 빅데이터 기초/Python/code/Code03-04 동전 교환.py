#Code03-04 동전 교환.py
## 함수 선언부 ##

## 변수 선언부 ##
money = 0 # 초기화를 선언처럼 사용
#c500, c100, c50, c10 = 0, 0, 0, 0 # python스러운 code
c500, c100, c50, c10 = [0] * 4 # 동전 500, 동전 100, ...

## main 코드부 ##
if __name__ == '__main__':
    money = int(input("바꿀 돈 = "))
    c500 = money // 500;	money %= 500
    c100 = money // 100;	money %= 100
    c50 = money // 50;	money %= 50
    c10 = money // 10;	money %= 10

    print("500원은 ", c500, "100원은 ", c100, "50원은 ", c50, "10원은 ", c10, " 나머지 : ", money)
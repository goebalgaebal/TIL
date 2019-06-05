import random

## 전역 변수 선언 ##
num = 0
lotto = []

## 메인 코드부 ##
if __name__ == "__main__" :
    # for i in range(0, 6):
    #     lotto.append(random.randint(1, 45))
    # 같은 숫자가 뽑힐수도있다
    while True :
        num = random.randint(1, 45)
        if num in lotto :
            pass
        else:
            lotto.append(num)
        # if num not in lotto :
        #     lotto.append(num)

        if len(lotto) >= 6 :
            break

    lotto.sort() #정렬
    print("축하합니다" , lotto)
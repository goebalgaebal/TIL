import random

numbers = [] # 빈 list

# = for(i = 0; i < 10; i++)
for num in range(0, 10) : # range(0, 10) = 0 - 9
    #random.randint(0, 9) = 0 - 9까지 랜덤 선택
    #append 함수 = list 요소 추가 함수
    numbers.append(random.randint(0, 9)) # ()부터 실행
print(numbers)

#num은 사용하지 않는 변수이므로 _를 사용
#참고 : https://mingrammer.com/underscore-in-python/
for _ in range(0, 10) :
    numbers.append(random.randint(0, 9))
print(numbers)

for num in range(0, 10) :
    if num not in numbers:
        print(num, "없어")

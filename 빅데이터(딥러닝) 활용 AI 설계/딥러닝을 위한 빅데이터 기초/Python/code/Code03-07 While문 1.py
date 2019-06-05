sum = 0

# for i in range(101):
#     sum += i
#
# print(sum)

# i = 0
# while i < 101 :
#     sum += i
#     i += 1
#

i = 0
while True :
    sum += i
    if sum > 10000 :
        break # 반복문 종료
    i += 1

print(i, sum)
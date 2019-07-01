import numpy as np

arr = np.array([1, 2, 3])
print(type(arr)) # <class 'numpy.ndarray'>

ans = []
for i in arr :
    ans.append(i*2)
print(ans)
print(2*arr) # 벡터화 연산

li = [1, 2, 3]
print(li*2) # list 2번 출력

a = np.array([1, 2])
b = np.array([10, 20])
print(3*a + b)


arr = np.array([1, 2, 3])
print(arr == 2) # [False  True False]
print((arr < 2) & (arr > 0))

c = np.array([[1, 2, 3], [4, 5, 6]]) # 2*3 array
print(c.shape[0], len(c)) # 행의 개수
print(c.shape[1], len(c[0])) # 열의 개수

# 배열의 차원(ndim), 크기(shape)
a = np.array([1, 2, 3])
print(a.ndim) # 1
print(a.shape) # (3,)

a2 = np.array([[1, 2, 3], [4, 5, 6]])
print(a2.ndim) # 2
print(a2.shape) # (2, 3)

a3 = np.array([1, 2, 3, 4, 5])
print(a3[-1])

a4 = np.array([[1, 2, 3], [4, 5, 6]])
# a4를 참조하여 2출력
print(a4[0, 1], a4[0][1])

# 5참조
print(a4[-1, 1], a4[-1, -2])

# 5, 6 slicing

# f(x) = w1x1 + w2x2 + ... + wnxn + b
# → n개의 변수
# x = 수집한 데이터
# w = 가중치. 모델을 만드는 작업에서 만들어진다
a = np.zeros((5, 2), dtype="i")
print(a)

b = np.empty((5, 2)) # 쓰레기값으로 초기화된 array
print(b)

print(np.arange(10))
print(np.arange(10, 50, 3)) # 10부터 50전까지 3씩 step

# 0에서 100전까지의 구간을 5등분함
print(np.linspace(0, 100, 5)) # 선형 공간(구간)

# 0.1에서 1전까지 log 공간을 10등분함
print(np.logspace(0.1, 1, 10)) # 로그 공간(구간)

# f(x) = wx + b
# x = 입력데이터


print(a)
print(a.T)

# 1차원 → 다차원
b = np.arange(12)
print(b)
# c = b.reshape(4, 3)
c = b.reshape(4, -1) #  -1로 해놓으면 남은 열을 계산해서 대입
print(c)

# 다차원 → 1차원 : ravel, flatten
print(c)
print(c.flatten())
print(c.ravel())

x = np.arange(5)
print(x)
x = x.reshape(5, 1)
print(x)

print(x[:, np.newaxis]) # np.newaxis = 차원 증가 옵션

# 행의 수가 동일한 2개 이상의 배열을 좌우로 연결
a1 = np.ones((2, 3))
print(a1)
# [[1. 1. 1.]
#  [1. 1. 1.]]
a2 = np.zeros((2, 2))
print(a2)
# [[0. 0.]
#  [0. 0.]]
print(np.hstack([a1, a2]))
# [[1. 1. 1. 0. 0.]
#  [1. 1. 1. 0. 0.]]

# 열의 수가 동일한 2개 이상의 배열을 상하로 연결
a2 = np.zeros((2, 3))
print(np.vstack([a1, a2]))
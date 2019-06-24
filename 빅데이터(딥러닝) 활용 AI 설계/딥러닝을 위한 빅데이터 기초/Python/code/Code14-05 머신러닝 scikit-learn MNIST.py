from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
import pandas as pd
import math

def changeValue(list) :
    # return [float(v) / 255 for v in list]
    return [math.ceil(float(v) / 255) for v in list] # ceil : 올림

# 0. 훈련 데이터, 테스트데이터 준비
csv = pd.read_csv("./mnist/train_5K.csv")
train_data = csv.iloc[:, 1:].values
train_data = list(map(changeValue, train_data))
train_label = csv.iloc[:, 0].values

csv = pd.read_csv("./mnist/t10k_0.5K.csv")
test_data = csv.iloc[:, 1:].values
test_data = list(map(changeValue, test_data))
test_label = csv.iloc[:, 0].values

# 학습용, 훈련용 분리
train_data, test_data, train_label, test_label = train_test_split(train_data, train_label, train_size=0.7)

# 1. Classifire 생성(선택) → 머신러닝 알고리즘 선택
# clf = svm.SVC(gamma="auto")
clf = svm.NuSVC(gamma="auto")

# 2. 데이터로 학습 시키기
# clf.fit([훈련 데이터], [정답])
clf.fit(train_data, train_label)

# 3. 정답률을 확인 (신뢰도) 훈련 : 테스트 = 8 : 2, 7 : 3
results = clf.predict(test_data)
score = metrics.accuracy_score(results, test_label)
print("정답률 : {0:.2f} %".format(score*100))

# 3. 예측하기
# clf.predit([예측할 데이터])
# result = clf.predict([[5.0, 3.2, 1.0, 0.2]])
# print(result)


# # 그림 사진 보기
# import matplotlib.pyplot as plt
# import  numpy as np
# img = np.array(test_data[0]).reshape(28, 28)
# plt.imshow(img, cmap = "gray")
# plt.show()
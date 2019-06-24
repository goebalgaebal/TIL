from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
import pandas as pd

'''
붓꽃 데이터 분류기 (머신러닝)
개요 : 150개 붓꽃 정보(꽃받침 길이, 꽃받침 폭, 꽃잎 길이, 꽃잎 폭)
종류 : 3개 (Iris-setosa, Iris-vesicolor, Iris-virginica)
CSV 파일 : iris.csv
'''

# 0. 훈련 데이터, 테스트데이터 준비
csv = pd.read_csv("./csv/iris.csv")
data = csv.iloc[:, :-1]
label = csv.iloc[:, [-1]]

# 학습용, 훈련용 분리
train_data, test_data, train_label, test_label = train_test_split(data, label, train_size=0.7)

# 1. Classifire 생성(선택) → 머신러닝 알고리즘 선택
clf = svm.SVC(gamma="auto")
#clf = svm.NuSVC(gamma="auto")

# 2. 데이터로 학습 시키기
# clf.fit([훈련 데이터], [정답])
clf.fit(train_data, train_label)

# 3. 정답률을 확인 (신뢰도) 훈련 : 테스트 = 8 : 2, 7 : 3
results = clf.predict(test_data)
score = metrics.accuracy_score(results, test_label)
print("정답률 : {0:.2f} %".format(score*100))

# 3. 예측하기
# clf.predit([예측할 데이터])
result = clf.predict([[5.0, 3.2, 1.0, 0.2]])
print(result)

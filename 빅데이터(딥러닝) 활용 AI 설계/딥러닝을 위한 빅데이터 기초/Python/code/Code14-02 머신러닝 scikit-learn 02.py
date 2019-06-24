from sklearn import svm, metrics

## 훈련데이터, 테스트데이터 준비
train_data = [[0, 0], [0, 1], [1, 0], [1, 1]]
train_label = [0, 1, 1, 0]
test_data = [[1, 0], [0, 0]]
test_label = [1, 0]

# 1. Classifire 생성(선택) → 머신러닝 알고리즘 선택
clf = svm.SVC(gamma="auto")

# 2. 데이터로 학습 시키기
# clf.fit([훈련 데이터], [정답])
clf.fit(train_data, train_label)

# 3. 정답률을 확인 (신뢰도) 훈련 : 테스트 = 8 : 2, 7 : 3
results = clf.predict(test_data)
score = metrics.accuracy_score(results, test_label)
print("정답률 : {0:.2f} %".format(score*100))

# 3. 예측하기
# clf.predit([예측할 데이터])
result = clf.predict([[1, 0]])
# print(result)

from sklearn import svm, metrics

# 1. Classifire 생성(선택) → 머신러닝 알고리즘 선택
clf = svm.SVC(gamma="auto")

# 2. 데이터로 학습 시키기
# clf.fit([훈련 데이터], [정답])
# XOR
clf.fit([[0, 0],
         [0, 1],
         [1, 0],
         [1, 1]],
        [0, 1, 1, 0])

# 3. 정답률을 확인 (신뢰도) 훈련 : 테스트 = 8 : 2, 7 : 3
results = clf.predict([[1, 0], [0, 0]])
score = metrics.accuracy_score(results, [1, 0])
print("정답률 : {0:.2f} %".format(score*100))

# 3. 예측하기
# clf.predit([예측할 데이터])
result = clf.predict([[1, 0]])
# print(result)


clf2 = svm.NuSVC(gamma="auto")

# AND
clf2.fit([[0, 0],
         [0, 1],
         [1, 0],
         [1, 1]],
        [0, 0, 0, 1])

result2 = clf2.predict([[1, 1]])
print(result2)
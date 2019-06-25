import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(".\haar\haarcascade_mcs_mouth.xml")

# frame = cv2.imread("\images\images(ML)\prateek.jpg")
frame = cv2.imdecode(np.fromfile(".\images\사람들\\06misstrot.jpg", dtype=np.uint8), -1)
grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# 얼굴이 여러 개일 경우, 여러 개를 찾아줌. 얼굴 위치 사각형 표시 [[x1, y1, x2, y2], [x1, y1, x2, y2], ...]
face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
print(face_rects)

for (x, y, w, h) in face_rects :
    cv2.rectangle(frame, (x, y), (x+w, y+w), (0, 255, 0), 3)

cv2.imshow("", frame)
c = cv2.waitKey()
cv2.destroyAllWindows()

# class 이름은 대문자로 시작
class Car : # 설계도
    # 자동차 속성
    color = None
    speed = 0

    # 자동차의 행위 → 함수, 기능
    def upSpeed(self, value):
        #speed = 0 # 함수내의 지역 변수
        self.speed += value # 자신의 속성을 사용할 때 self를 사용
    def downSpeed(self, value):
        self.speed -= value

if __name__ == '__main__':
    myvalue = 0 # 변수

    car1 = Car() # 실체 = 인스턴스, 메모리에 탑재
    car1.color = "빨강"
    car1.speed = 50

    car1.upSpeed(100)
    print("현재속도", car1.speed)

    car2 = Car()

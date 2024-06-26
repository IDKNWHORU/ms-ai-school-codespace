# 클래스 선언 부분
class Car :
    color = ""
    speed = 0

    def __init__(self, color, speed) :
        self.color = color
        self.speed = speed

    def upSpeed(self, value) :
        self.speed += value

    def downSpeed(self, value) :
        self.speed -= value

myCar1 = Car("빨강", 0)
myCar2 = Car("파랑", 30)

print("자동차 1의 색상은 %s이며, 현재 속도는 %dkm입니다." % (myCar1.color, myCar1.speed))
print("자동차 2의 색상은 %s이며, 현재 속도는 %dkm입니다." % (myCar2.color, myCar2.speed))
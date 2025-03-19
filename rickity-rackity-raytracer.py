import math as m
import turtle as t

class cam:
    def __init__(self,x,y,z,rotx,roty):
        self.x = 0
        self.y = 0
        self.z = 0
        self.rotx = 0
        self.roty = 0
    def move(self,speed):
        self.x += speed*m.sin(self.rotx)
        self.z += speed*m.cos(self.rotx)
    def rotate(self,speed):
        t.Screen().onkeypress(self.rotx += 4,"Right")
        t.Screen().onkeypress(self.rotx -= 4,"Left")
        t.Screen().onkeypress(self.roty += 4,"Up")
        t.Screen().onkeypress(self.rotx -= 4,"Down")
    def controls(self,speed):
        self.rotate()
        t.Screen().onkeypress(self.move(speed),"w")
        t.Screen().onkeypress(self.move(-speed),"s")
        self.rotx += 90
        t.Screen().onkeypress(self.move(speed),"d")
        t.Screen().onkeypress(self.move(-speed),"a")
        self.roty += -90

class ray:
    def __init__(self,x,y,z):
        self.x = 0
        self.y = 0
        self.z = 0
    def pixel(self):
        print()
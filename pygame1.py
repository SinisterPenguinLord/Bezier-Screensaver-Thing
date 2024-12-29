import pygame
from pygame import MOUSEBUTTONDOWN, KEYDOWN
import random
import time

pygame.init()
wi = 1600
he = 800

display = pygame.display.set_mode((wi,he))
pygame.display.set_caption("Game")

ma = 60

def smot(x,l,u):
    d = u-l
    x -= l
    if x < 0:
        x += 2*d
    f = x%d
    g = x%(d*2)+l
    if g > u:
        return 2*u-g
    else:
        return g


    h = int(g - 2*(g-f)/5*f) + l
    if h > u:
        return (h,u)
    if h < l:
        return (h,l)
    return h

class Bezier():
    def __init__(self,points):
        self.points = points
        self.els = [points]
        self.cols = [(random.randint(0,255),random.randint(0,255),random.randint(0,255)) for x in range(2)]

    def addPoint(self,point):
        self.points.append(point)
        self.els = [self.points]

    def draw(self):
        (r0,g0,b0) = self.cols[0]
        (r1,g1,b1) = self.cols[1]
        for (k,el) in enumerate(self.els):
            if k > 0:
                (r,g,b) = ((k/ma)*r0 + (ma-k)/ma*r1,(k/ma)*g0 + (ma-k)/ma*g1,(k/ma)*b0 + (ma-k)/ma*b1)
                for x in range(len(el)-1):
                    pygame.draw.line(display, (r,g,b), el[x], el[x+1])
        self.cols[0] = (smot(r0 + random.randint(-3,3),0,40),
                        smot(g0 + random.randint(-3,3),0,25),
                        smot(b0 + random.randint(-3,3),0,75))

        self.cols[1] = (smot(r1 + random.randint(-3,3),0,100),
                        smot(g1 + random.randint(-3,3),0,50),
                        smot(b1 + random.randint(-3,3),25,150))

        self.cols[0] = (0,0,0)



    def elevate(self):
        self.els.append([])
        k = min([len(self.els),ma])
        for x in range(k-2,-1,-1):
            points = self.els[x]
            n = len(points)
            new = [points[0]]
            for i in range(1,n):
                new.append((points[i-1][0]*i/n+points[i][0]*(n-i)/n,
                            points[i-1][1]*i/n+points[i][1]*(n-i)/n))
            new.append(points[-1])
            self.els[x+1] = new

    def shuffle(self):
        for i in range(len(self.els[0])):
            (x,y) = self.els[0][i]
            x = (x+random.randint(-100,100)/10)%wi
            y = (y+random.randint(-100,100)/10)%he
            self.els[0][i] = (x,y)

c = []
q = False
for p in range(1):
    display.fill((0, 0, 0))
    pygame.display.update()
    b = Bezier([])
    q = False
    while True:
        x = pygame.event.get()
        for y in x:
            if y.type == MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                b.addPoint(coords)
                pygame.draw.circle(display,(255,255,255),coords,3)
                pygame.display.update()
            if y.type == KEYDOWN:
                q = True
                break
        if q:
            break
    c.append(b)

clock = pygame.time.Clock()

while True:
    for d in c:
        d.draw()
        d.elevate()
        d.shuffle()
    pygame.display.update()
    display.fill((0,0,0))
    clock.tick(60)
input()
import pygame, sys
from pygame.locals import *

from math import pi, sqrt, asin, sin, cos

SIZE = (640, 480)

class Ball(object):
    def __init__(self, **args):
        for key in args:
            self.__dict__[key] = args[key]
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, [round(self.pos[0]), SIZE[1] - round(self.pos[1])], self.radius)

    def move(self, x, y):
        self.x += x
        self.y -= y

def input(events):
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Conservation of Momentum")

    ball =  [Ball(pos=[SIZE[0] // 2 - 25, SIZE[1] // 2 + 0], vel=[50, 15], mass=1, radius=10, color=(255, 0, 0)),
             Ball(pos=[SIZE[0] // 2 +  0, SIZE[1] // 2 + 0], vel=[ 0,  0], mass=2, radius=10, color=(0, 255, 0)),
             Ball(pos=[SIZE[0] // 2 + 25, SIZE[1] // 2 + 0], vel=[ 0,  0], mass=3, radius=10, color=(0, 0, 255))]

    t   = 0
    dt  = 0.00005
    edt = dt / 5

    while True:
        window.fill((255, 255, 255))

        for i in range(0, 3):
            for j in range(0, 2):
                ball[i].pos[j] += ball[i].vel[j] * dt
            for j in range(0, 3):
                if i == j:
                    continue
                if (ball[i].vel[0] == 0 and ball[i].vel[1] == 0) and (ball[j].vel[0] == 0 and ball[j].vel[1] == 0):
                    continue
                distance = sqrt((ball[i].pos[0] - ball[j].pos[0]) ** 2 + (ball[i].pos[1] - ball[j].pos[1]) ** 2)
                if distance <= ball[i].radius + ball[j].radius:
                    print("Collision")
                    theta = asin((ball[j].pos[1] - ball[i].pos[1]) / distance)
                    M = 1 / (ball[i].mass + ball[j].mass)
                    e = 1 #0 = Innelastic, 1 = Elastic
                    """
                    vels = [[ball[i].vel[k], ball[j].vel[k]] for k in range(0, 2)]
                    print(vels)
                    ball[i].vel = [M * ((ball[i].mass - ball[j].mass) * vels[k][0] + (2 * ball[j].mass) * vels[k][1]) for k in range(0, 2)]
                    ball[j].vel = [M * ((2 * ball[i].mass) * vels[k][0] + (ball[j].mass - ball[i].mass) * vels[k][1]) for k in range(0, 2)]
                    """
                    print(theta / pi  * 180)
                    vp = [[ball[i].vel[0] * cos(theta) + ball[i].vel[1] * sin(theta),
                           ball[j].vel[0] * cos(theta) + ball[j].vel[1] * sin(theta)],
                          [0, 0]]
                    vn = [ball[i].vel[0] * -sin(theta) + ball[i].vel[1] * cos(theta),
                          ball[j].vel[0] * -sin(theta) + ball[j].vel[1] * cos(theta)]
                    
                    vp[1][0] = M * (vp[0][0] * (ball[i].mass - e * ball[j].mass) + vp[0][1] * (1 + e) * ball[j].mass)
                    vp[1][1] = M * (vp[0][0] * (1 + e) * ball[i].mass + vp[0][1] * (ball[j].mass - e * ball[i].mass))
                    
                    ball[i].vel = [vp[1][0] * cos(theta) - vn[0] * sin(theta),
                                   vp[1][0] * sin(theta) + vn[0] * cos(theta)]
                    ball[j].vel = [vp[1][1] * cos(theta) - vn[1] * sin(theta),
                                   vp[1][1] * sin(theta) + vn[1] * cos(theta)]


                    while sqrt((ball[i].pos[0] - ball[j].pos[0]) ** 2 +
                               (ball[i].pos[1] - ball[j].pos[1]) ** 2) <= ball[i].radius + ball[j].radius:
                        if (ball[i].vel[0] == 0 and ball[i].vel[1] == 0) and (ball[j].vel[0] == 0 and ball[j].vel[1] == 0):
                            continue
                        for k in range(0, 2):
                            ball[i].pos[k] += ball[i].vel[k] * edt
                            ball[j].pos[k] += ball[j].vel[k] * edt
            ball[i].draw(window)

        momentumx = [ball[i].mass * ball[i].vel[0] for i in range(0, 3)]
        momentumy = [ball[i].mass * ball[i].vel[1] for i in range(0, 3)]
        
        #print("Px: {:8f}, Py: {:8f}".format(sum(momentumx), sum(momentumy)))
            
        t += dt
        pygame.display.flip()
        input(pygame.event.get())
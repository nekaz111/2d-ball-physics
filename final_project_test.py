#Jeremiah Hsieh ICSI 502 Final Project Ball Physics
#use pygame?

#currently implemented functions
#hold q to spawn many balls
#press w to spawn block
#press e for gravity
#press r for friction
#press space for 1 ball
#press arrowkeys to move paddle
#press a for random ball spawn size
#press s to enable/disable block destruction
#press and hold and pull mouse to spawn ball and shoot
#blocks and mouse ball collide
#currently no mass implementation and still some resting collision bugs (possibly due to constant gravity negative effect?)

import random
import math
import pygame as pg 

#block object class
class Block(pg.sprite.Sprite):
    def __init__(self, color, width, height, x = random.randrange(10, 50), y = random.randrange(20, 200), vel = 5):
       # Call the parent class (Sprite) constructor
       pg.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       #clean up excess
       self.image = pg.Surface([width, height])
       self.image.fill(color)
       self.color = color
       self.x = x
       self.y = y
       self.vel = vel
       self.height = height
       self.width = width
       self.rect = self.image.get_rect() 
       self.rect.x = x
       self.rect.y = y
#       pg.draw.rect(self.image, self.color, [self.x, self.y, self.width, self.height])
       
#       self.rect = self.image.get_rect()
    #move shape within bounds of window (not 0 since if 0 < y < vel, then the object can still move off screen into the negatives)
    #shape starts from top left corner so height/width must be adjusted for
    def moveLeft(self):
        if self.rect.x >= self.vel:
            self.rect.x -= self.vel
            
    def moveRight(self):
        if self.rect.x <= winx - (self.width + self.vel):
            self.rect.x += self.vel
            
    def moveUp(self):
        if self.rect.y >= self.vel: 
            self.rect.y -= self.vel
            
    def moveDown(self):
        if self.rect.y <= winy - (self.height + self.vel):
            self.rect.y += self.vel



#ball object class
class Ball(pg.sprite.Sprite):
     def __init__(self, x, y, r, rgb = (255, 255, 255)):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0
        self.vy = 0
        self.rgb = rgb
        #for mass just use ball relative sizes based on r for now
        #self.r =
    
    #check if 2 balls have collided
    #use collide_circle?
    #easy with balls since it's just seeing if the distance between both midpoints is less than both radii added together
#     def ballcollided(self, other):
#        #calculate distance between midpoints using right triangle formula vx^2 + vy^2 = dz^2
#        if (self.x - other.x)**2 + (self.y - other.y)**2 < (self.r + other.r)**2 + .2:
##            return True
#            ballPhysics(self,other)
#        return False
#    def rectcollided(self, rect):
        

#make block 
def spawnBlock():
#    paddle = Block(50, 50, 80, 20, 10)
    paddle = Block((255, 255, 255), 80, 20, random.randrange(10, 300), random.randrange(10, 300))
    return paddle


#spawn a ball in the window
def spawnBall(r = 10):
#    r = random.randrange(2, 15)
#    r = 10
    #initalize objects
    if r == None:
        #lazy random seed
        r = random.randrange(2, 15)
    ball = Ball(100, 100, r)
    #x and y velocity change
    #randomize spawn point and x/y velocities so the balls so don't all go in the exact same pattern
    ball.x = random.randrange(0 + ball.r, winx - ball.r)
    ball.y = random.randrange(0 + ball.r, winy - ball.r)
    ball.vx = random.randrange(-3, 4)
    ball.vy = random.randrange(-4, 5)
    #not sure how to syntax range so that 0 is not included)
    while ball.vx == 0 and ball.vy == 0:
         ball.vx = random.randrange(-2, 4)
         ball.vy = random.randrange(-3, 5)
    ball.rgb = (random.randrange(255), random.randrange(255), random.randrange(255))
    return ball
    



#draws current state onto window
def redrawWin(mouse = 1):
    #recolor background so that previous shape does not stay on screen    
    win.fill((0,0,0))
    #draw shape
    #window, color, starting position and size
#    pg.draw.rect(win, (255, 255, 255), (paddle.x, paddle.y, paddle.width, paddle.height))
    paddle_list.draw(win)
    block_list.draw(win)
    pg.draw.circle(win, mouseball.rgb , [int(mouseball.x), int(mouseball.y)], mouseball.r)
    #draw circle
    for ball in balls:
        pg.draw.circle(win, ball.rgb , [int(ball.x), int(ball.y)], ball.r) 
    #60 updates per second (equivalent to 60 fps?)
    clock.tick(60)
    pg.display.update()   


#checks ball collision
def ballCollided(ball1, ball2):
    #calculate distance between midpoints using right triangle formula vx^2 + vy^2 = dz^2
    if (ball1.x - ball2.x)**2 + (ball1.y - ball2.y)**2 < (ball1.r + ball2.r)**2 + .2:
#            return True
        #change velocity based on physics equations
        ballPhysics(ball1 ,ball2)


#check of blocks are collidingrect or ball
def blockcollide(destroy = 0):
    #destroy if colliding
    for block in block_list:
        if pg.sprite.collide_rect(paddle, block) == True: 
            block.kill()
        for ball in balls:
            #check collision
            ballRectBounce(ball, block)
            if ballRectBounce(ball, block) and destroy == 1:
                #destroy blocks
                    block.kill()
    
        
#define various keypress actions
def keyPress(destroy = 0):
    #get key press for paddle (write as functions in block object? or maybe add inheritence?)       
    keys = pg.key.get_pressed()
    #spawn ball (currently spawns multiple per press, make it so only reads a single press per down press?)
    if keys[pg.K_q]:
        #make more balls
#        ball = spawnBall()
        balls.append(spawnBall(radius))
    
    #check of blocks are colliding
    blockcollide(destroy)
            
    #rect collision (currently allows for movement into a stuck position)   
#    if pg.sprite.collide_rect(paddle, paddle2) == False:
    #move paddle
    if keys[pg.K_UP]:
        paddle.moveUp()
    if keys[pg.K_DOWN]:
        paddle.moveDown()
    if keys[pg.K_LEFT]:
        paddle.moveLeft()
    if keys[pg.K_RIGHT]:
        paddle.moveRight()
#    else:
#        print("stuck")
        
#define ball movement logic
def moveBall(friction = 0, gravity = 0):
    for iterb, ball in enumerate(balls) :



        
#        if ball.y < ball.r:
#            ball.y = ball.r
#            ball.vy = -1
#        elif ball.y > (winy - ball.r):
#            ball. y = winy - ball.r
#            ball.vy = -1
#        if ball.x < ball.r:
#            ball.x = ball.r
#            ball.vx *= -1
#        elif ball.x > (winx - ball.r):
#            ball.x = winx - ball.r
        #move ball (write as functions in ball object?)

        #bounding box so it never goes outside window
        if ball.x < ball.r:
            ball.x = ball.r
        if ball.x > winx - ball.r:
            ball.x = winx - ball.r
        if ball.y < ball.r:
            ball.y = ball.r
        if ball.y > winy - ball.r:
            ball.y = winy - ball.r
                

        
        #perfectly elastic collisions have no loss in momentum so the only thing that is changed is the direction of velocity
        #keep ball moving in same direction if it has already hit wall so that it doenst get  stuck in wall and keep bouncing back and forth
        if (ball.vy <= 0 and ball.y <= ball.r) or (ball.vy >= 0 and ball.y >= (winy - ball.r)):
            if friction > 0:
                if ball.vy < 0:
                    ball.vy += 1
                elif ball.vy > 0:
                    ball.vy -= 1
            ball.vy *= -1
            
        if (ball.vx <= 0 and ball.x <= ball.r) or (ball.vx >= 0 and ball.x >= (winx - ball.r)):
            #make every wall collision cause loss in velocity on top of regular friction
            if friction > 0:
                if ball.vx < 0:
                    ball.vx += 1
                elif ball.vx > 0:
                    ball.vx -= 1
            ball.vx *= -1
            
        #gravity value (downward force) (i believe the ball is falling offscreen in part because of this?)

        ball.vy = ball.vy + gravity
        
        #friction value 
        if ball.vx < 0:
            ball.vx = ball.vx + friction / 50
        elif ball.vx > 0:
            ball.vx = ball.vx - friction / 50
        if ball.vy < 0:
            ball.vy = ball.vy + friction / 50
        elif ball.vy > 0:
            ball.vy = ball.vy - friction / 50
#    #use index and enumerate to get list index
#    for indexb, ball in enumerate(balls):
#        #split move and collision detection?
##        #move ball (write as functions in ball object?)
##        ball.x += ball.vx
##        ball.y += ball.vy
#        
#
#        
#        #basic collision testing
#        #go through list of balls and check if radius 
#        for indexo, other in enumerate(balls):
#            #don't check ball object
##            if indexb != indexo:
#            if ball != other:
##                    print("indexb = ", indexb)
##                    print("indexo = ", indexo)
#                    #check if current ball colldied with others
##                    if ball.ballcollided(other):
##                        #for now just do simple reverse vectors (figure out proper vectors with physics equations)
##                        ball.vy *= -1
##                        ball.vx *= -1
##                        other.vy *= -1
##                        other.vx *= -1    
##                    ball.ballcollided(other)
#                    ballCollided(ball, other)
#       
            
        for paddle in paddle_list:
            ballRectBounce(ball, paddle)  
        
        ballCollided(ball, mouseball)
        #check all balls after current ball
        for ball2 in balls[iterb+1:]:
#            if ball != ball2:
            ballCollided(ball, ball2)
            ballCollided(ball2, ball)
        ball.x += ball.vx
        ball.y += ball.vy

#another calculation mthod?
def altBallPhysics(ball1, ball2):
    XSpeed1 = (ball1.vx * (ball1.r ??? ball2.r) + (2 * ball2.r * ball2.vx)) // (ball1.r + ball2.r)
    YSpeed1 = (ball1.vy * (ball1.r ??? ball2.r) + (2 * ball2.r * ball2.vy)) // (ball1.r + ball2.r)
    XSpeed2 = (ball2.vx * (ball2.r ??? ball1.r) + (2 * ball1.r * ball1.vx)) // (ball1.r + ball2.r)
    YSpeed2 = (ball2.vy * (ball2.r ??? ball1.r) + (2 * ball1.r * ball1.vy)) // (ball1.r + ball2.r)

                    
# basic ball physics perfectly elastic equations                    
#currently no mass/friction/gravity/velocity equalization
def ballPhysics(ball1, ball2):
    #momentum is conserved
    v = math.sqrt((ball1.vx**2) + (ball1.vy**2))
    #rise over runx
    dx = -(ball1.x - ball2.x)
    dy = -(ball1.y - ball2.y)
    XSpeed = dx
    YSpeed = dy
    
    #calculate change in x and y velocities based on current velocities
    if dx > 0:
        if dy > 0:
            Angle = math.degrees(math.atan(dy/dx))
            XSpeed = -v*math.cos(math.radians(Angle))
            YSpeed = -v*math.sin(math.radians(Angle))
        elif dy < 0:
            Angle = math.degrees(math.atan(dy/dx))
            XSpeed = -v*math.cos(math.radians(Angle))
            YSpeed = -v*math.sin(math.radians(Angle))
    elif dx < 0:
        if dy > 0:
            Angle = 180 + math.degrees(math.atan(dy/dx))
            XSpeed = -v*math.cos(math.radians(Angle))
            YSpeed = -v*math.sin(math.radians(Angle))
        elif dy < 0:
            Angle = -180 + math.degrees(math.atan(dy/dx))
            XSpeed = -v*math.cos(math.radians(Angle))
            YSpeed = -v*math.sin(math.radians(Angle))
    elif dx == 0:
        if dy > 0:  
            Angle = -90
        else:
            Angle = 90
        XSpeed = v*math.cos(math.radians(Angle))
        YSpeed = v*math.sin(math.radians(Angle))
    elif dy == 0:
        if dx < 0:
            Angle = 0
        else:
            Angle = 180
        XSpeed = v*math.cos(math.radians(Angle))
        YSpeed = v*math.sin(math.radians(Angle))
        
    ball1.vx = XSpeed
    ball1.vy = YSpeed


#return true if ball collided with rectangle
def ballCollidedRect(ball1, block):
    #remmeber: rectangle origin point is top left corner
    #check if ball is inside invisible larger rectangle around paddle
    if ball1.x >= block.rect.x - ball1.r and ball1.x <= block.rect.x + block.width + ball1.r and ball1.y >= block.rect.y - ball1.r and ball1.y <= block.rect.y + block.height + ball1.r:
        return True
    return False



#reflect ball
def ballRectBounce(ball1, block):
    if ballCollidedRect(ball1, block):
            
        #check if balls is bouncing off sides
        if (ball1.vx > 0 and ball1.x < block.rect.x) or (ball1.vx < 0 and ball1.x > block.rect.x + block.width):
            ball1.vx *= -1
        if (ball1.vy > 0 and ball1.y < block.rect.y) or (ball1.vy < 0 and ball1.y > block.rect.y + block.height):
            ball1.vy *= -1
        return True  
    return False
#        print("collided")
#    if ball1.y > rect.y - ball1.r or ball1.y < rect.y + rect.height + ball1.r:
#        ball1.vy *= -1
        
    
#def clip(val, minval, maxval):
#    return min(max(val, minval), maxval)

      
#main function
#initialize module
pg.init()
winx = 500
winy = 600
#make window of size 500 by 500
win = pg.display.set_mode((winx,winy))
#window name
pg.display.set_caption("Ball Physics")


#    paddle = Block(50, 50, 80, 20, 10)

#    ball = Ball(100, 100, 10)
#
#    #x and y velocity change
#    ball.vx = 6
#    ball.vy = 5
#initalize object groups
block_list = pg.sprite.Group()
paddle_list = pg.sprite.Group()
balls = []
#blocks = []
#make blocks spawn
paddle = spawnBlock()
paddle2 = spawnBlock()
#add blocks to list of blocks
paddle_list.add(paddle)
block_list.add(paddle2)
#randomly spawn more blocks
for x in range(10):
    block_list.add(spawnBlock())
#    ball = spawnBall()
#store currently spawned objects
#    balls.append(ball)
#blocks.append(paddle)
    
friction = 0
gravity = 0
run = True
radius = 10
mouse = 0
destroy = 0
#mouse ball
mouseball = spawnBall()
#window loop
while run == True:
    #update gamestate timer
#        pg.time.delay(10)
    clock = pg.time.Clock()
    #check if certain events have happened (ex. key presses)
    for event in pg.event.get():
        #exit program
        if event.type == pg.QUIT:
            #for some reason if I just call pg.quit() here it seems to cause a "video system not initialized" error
            #pg.quit()
            run = False
        #check if key is pressed down once and if it is spacebar so that multiple balls are not spawned     
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            #make more balls
#            ball = spawnBall()
            balls.append(spawnBall(radius))
        #spawn random blocks
        elif event.type == pg.KEYDOWN and event.key == pg.K_w:
            block_list.add(spawnBlock())
        #activate/deactivate gravity
        elif event.type == pg.KEYDOWN and event.key == pg.K_e:
            if gravity == 0:
                gravity = .5
            else:
                gravity = 0
        #activate/deactivate friction
        elif event.type == pg.KEYDOWN and event.key == pg.K_r:
            if friction == 0:
                friction = 4
            else:
                friction = 0
        #activate/deactivate randomized ball size 
        if event.type == pg.KEYDOWN and event.key == pg.K_a:
            if radius == 10:
                radius = None
            else:
                radius = 10
        #activate/deactivate block destruction 
        if event.type == pg.KEYDOWN and event.key == pg.K_s:
            if destroy == 0:
                destroy = 1
            else:
                destroy = 0
        #mouse launching balls    
        if event.type == pg.MOUSEBUTTONDOWN:
            #make ball
            spawned = spawnBall()
            #mouse press starting xy
            start = pg.mouse.get_pos()
            #set spawn to starting xy (above)
            
            balls.append(spawned)
            spawned.x = start[0]
            spawned.y = start[1]
            spawned.vx = 0
            spawned.vy = 0
            
        if event.type == pg.MOUSEBUTTONUP:

            #get ending position
            end = pg.mouse.get_pos()
            #generate ball velocity based on start vs ending distance ratio
            vx = (start[0] - end[0]) // 10
            vy = (start[1] - end[1]) // 10
            
            #set velocities
            spawned.vx = vx
            spawned.vy = vy
            #add to ball list
#            balls.append(spawned)
            
    #kepress actions
    keyPress(destroy)
    

    
    
    #call function that moves balls around every frame
#    moveBall(1, 1)    
    moveBall(friction, gravity)
    pos = pg.mouse.get_pos()
    mouseball.x = pos[0]
    mouseball.y = pos[1]
    for paddle in paddle_list:
#        print(paddle.rect.x, paddle.rect.y)
        ballRectBounce(mouseball, paddle)
    #draws window contents based on current state
    redrawWin()

           
    
#exit window program       
pg.quit()
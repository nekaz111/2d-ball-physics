#Jeremiah Hsieh ICSI 502 Final Project Breakout
#try to clean up some excess?
#just pong 
#score implementation issue (starts at 10 and 20 for some reason?))
import random
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
    ball.x = random.randrange(200 + ball.r, winx - ball.r - 200)
    ball.y = random.randrange(200 + ball.r, winy - ball.r - 200)
    ball.vx = random.randrange(-5, 5)
    ball.vy = random.randrange(-4, 4)
    #not sure how to syntax range so that 0 is not included)
    while ball.vx == 0:
         ball.vx = random.randrange(-2, 4)
    while ball.vy == 0:
        ball.vy = random.randrange(-4, 4)
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
#    pg.draw.circle(win, mouseball.rgb , [int(mouseball.x), int(mouseball.y)], mouseball.r)
    #draw circle
    for ball in balls:
        pg.draw.circle(win, ball.rgb , [int(ball.x), int(ball.y)], ball.r) 
    #60 updates per second (equivalent to 60 fps?)
    clock.tick(60)
    pg.display.update()   
    
    
#check of blocks are collidingrect or ball
def blockcollide(destroy = 0):
    #destroy if colliding
    for block in block_list:
        if pg.sprite.collide_rect(paddle1, block) == True: 
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

    
    #check of blocks are colliding
    blockcollide(destroy)
            
    #rect collision (currently allows for movement into a stuck position)   
#    if pg.sprite.collide_rect(paddle, paddle2) == False:
    #move paddle1
    if keys[pg.K_LEFT]:
        paddle1.moveLeft()
    if keys[pg.K_RIGHT]:
        paddle1.moveRight()
    #paddle 2 movement
    if keys[pg.K_a]:
        paddle2.moveLeft()    
    if keys[pg.K_d]:
        paddle2.moveRight()
        
#    else:
#        print("stuck")
        
        
#define ball movement logic
def moveBall(player1score, player2score):
    kill = 0
    
    
    
    for ball in balls :
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
#        if (ball.vy <= 0 and ball.y <= ball.r) or (ball.vy >= 0 and ball.y >= (winy - ball.r)):
#            if friction > 0:
#                if ball.vy < 0:
#                    ball.vy += 1
#                elif ball.vy > 0:
#                    ball.vy -= 1
#            ball.vy *= -1
        #ball touched top of window
        if ball.vy <= 0 and ball.y <= ball.r:
            player1score += 1
            print("score: player 1" + str(player1score))
            print("score: player 2" + str(player2score))
            kill = 1
            
        #ball touches bottom    
        if ball.vy >= 0 and ball.y >= (winy - ball.r):
            player2score += 1
            print("score: player 1" + str(player1score))
            print("score: player 2" + str(player2score))
            kill = 1
            
        if (ball.vx <= 0 and ball.x <= ball.r) or (ball.vx >= 0 and ball.x >= (winx - ball.r)):

            ball.vx *= -1
 
            
        for paddle in paddle_list:
            ballRectBounce(ball, paddle)  
                
        ball.x += ball.vx
        ball.y += ball.vy
        #if ball touches bottom
        if kill == 1:
            balls.clear()
            balls.append(spawnBall())
        return player1score, player2score
        
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
            
        #speed up ball every collision
        if ball1.vx > 0:
            ball1.vx += .3
        elif ball1.vx < 0:
            ball1.vx -= .3
        if ball1.vy > 0:
            ball1.vy += .3
        elif ball1.vy < 0:
            ball1.vy -= .3
        return True  
    return False


#make block 
def spawnBlock(y):
#    paddle = Block(50, 50, 80, 20, 10)
    paddle = Block((255, 255, 255), 80, 10, random.randrange(10, 300), y)
    return paddle



#main
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
paddle1 = spawnBlock(50)
paddle2 = spawnBlock(530)
#add blocks to list of blocks
paddle_list.add(paddle1)
block_list.add(paddle2)
#randomly spawn more blocks

#block_list.add(spawnBlock())
#    ball = spawnBall()
#store currently spawned objects
#    balls.append(ball)
#blocks.append(paddle)
 

#spawn first ball
balls.append(spawnBall())
run = True
radius = 10
player1score = 0
player2score = 0
print(player2score)
print("score: player 1" + str(player1score))
print("score: player 2" + str(player2score))
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
            
    #kepress actions
    keyPress()
    

    
    
    #call function that moves balls around every frame
#    moveBall(1, 1)    
    player1score, player2score = moveBall(player1score, player2score)

    #draws window contents based on current state
    redrawWin()


    
#exit window program       
pg.quit()
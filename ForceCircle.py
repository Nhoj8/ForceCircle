import pygame
from pygame.locals import *
import time
import random
import math

pygame.init()
#okokokokokokokthisijakhdsksaj
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 1200
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by John')
 
clock = pygame.time.Clock()

snake_block = 5
snake_speed = 90
apple_arr = []
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

class Snake:
    def __init__(self, x, y, velocityX,velocityY,force,mass,charge,radius):#, ForceX,ForceY lifetime, brain):
        self.x = x
        self.y = y
        self.force = force
        #self.lifetime = lifetime
        #self.brain = brain
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.mass = mass
        self.charge = charge
        self.radius = radius
class Line:
    def __init__(self, x,y, slope, length, radius):
        self.x = x
        self.y = y
        self.slope = slope
        self.length = length
        self.radius = radius
        self.finalx = x + length/math.sqrt(slope*slope+1)#* (1 if slope<0 else -1)
        self.finaly = y
        if slope != 0:
            self.finaly = y + length/math.sqrt(1/slope/slope+1)* (-1 if slope<0 else 1)
        

    def draw(self):
        #pygame.draw.rect(dis,red, (self.x, self.y, self.finalx, self.radius))
        pygame.draw.line(dis,red,(self.x,self.y),(self.finalx,self.finaly),self.radius)

    def calcDistance(self, orbx,orby):
        xintersect = (self.slope*self.slope*self.x+self.slope*(orby-self.y)+orbx)/(self.slope*self.slope+1)
        yintersect = self.y+self.slope*(xintersect-self.x)
        dx = (xintersect-orbx)
        dy = (yintersect-orby)
        return (math.sqrt(dx*dx+dy*dy),dx,dy)

class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class connection:
    def __init__(self, start, end):
        self.weight = 1
        self.start = start
        self.end =end
        self.bias = 0
        self.activation=0
        self.positive = True

class network:
    def __init__(self, neurons):
        self.neurons = neurons
        self.connections = []
        self.connections.append(connection(0, 2))
        self.connections.append(connection(1, 3))
    def update(self,x,y):
        for i in self.neurons:
            i = 0
        #get the starting values
        closest = -1
        distanceclostest = 100000000
        if len(apple_arr) > 0:
            for i in range(len(apple_arr)):
                if(distanceclostest > (apple_arr[i].x-x)*(apple_arr[i].x-x)+(apple_arr[i].y-y) *(apple_arr[i].y-y)):
                    distanceclostest = (apple_arr[i].x-x)*(apple_arr[i].x-x)+(apple_arr[i].y-y) *(apple_arr[i].y-y)
                    closest = i
            self.neurons[0] = apple_arr[closest].x-x
            self.neurons[1] = apple_arr[closest].y-y

            for i in self.connections:# the connections need to be in start order
                self.neurons[i.end] += i.weight * self.neurons[i.start]
                #print(i.weight * self.neurons[i.start])
                print(self.neurons[i.end], i.end)
            

            if abs(self.neurons[2]) > abs(self.neurons[3]):
                #print(x+self.neurons[2]/abs(self.neurons[2]+1))
                return(x+self.neurons[2]/abs(self.neurons[2]-1),y)
            else:
                #print(x,self.neurons[2]/abs(self.neurons[2]-1))
                return(x,y+self.neurons[3]/abs(self.neurons[3]-1))
        else:
            return(x,y)
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    game_over = False
    game_close = False
    x = 103
    y = 103
    num_snakes = 40
    num_apples = 20
    snake_arr = []
    wall_arr = []
    snake_drag = False


    for i in range(round(num_snakes/2)):
        snake = Snake(1.0*random.randint(dis_width/4, 3*dis_width/4), 1.0*random.randint(0, dis_height/4),1.0*(random.randint(0, 100)-50)/100,1.0*(random.randint(0, 100)-50)/100,1.0,10,10,10)#, 0, network([0, 0, 0, 0]))
        snake_arr.append(snake)
    for i in range(round(num_snakes/2)):
        snake = Snake(1.0*random.randint(dis_width/4, 3*dis_width/4), 1.0*random.randint(0, dis_height/4),1.0*(random.randint(0, 100)-50)/100,1.0*(random.randint(0, 100)-50)/100,1.0,10,10,5)#, 0, network([0, 0, 0, 0]))
        snake_arr.append(snake)
    #for i in range(round(num_snakes/3)):
        #snake = Snake(1.0*random.randint(0, dis_width), 1.0*random.randint(0, dis_height),1.0*(random.randint(0, 100)-50)/100,1.0*(random.randint(0, 100)-50)/100,1.0,10,-10)#, 0, network([0, 0, 0, 0]))
        #snake_arr.append(snake)
    floor = Line(dis_width/2,dis_height-10,1,-dis_width/2,20)
    floor2 = Line(dis_width/2,dis_height-10,-1,dis_width/2,20)
    wall_arr.append(floor)
    wall_arr.append(floor2)
    for j in range(num_apples):
        apple = Apple(random.randint(0, dis_width), random.randint(0, dis_height))
        apple_arr.append(apple)

    while not game_over:

 
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
 
            pygame.display.update()
 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in snake_arr:
                    if pygame.Rect((i.x, i.y), (snake_block, snake_block)).collidepoint(event.pos):
                        snake_drag = True
                        dragging_snake = i
            elif event.type == pygame.MOUSEBUTTONUP:
                snake_drag = False
            if snake_drag:
                mouse_x, mouse_y = event.pos
                dragging_snake.x = mouse_x
                dragging_snake.y = mouse_y

        # for i in snake_arr:
        #     for j in apple_arr:
        #         if pygame.Rect((i.x, i.y), (snake_block, snake_block)).colliderect(pygame.Rect((j.x, j.y), (snake_block, snake_block))):
        #             snake_arr.append(Snake(j.x, j.y, 0, network([0, 0, 0, 0])))
        #             i.lifetime = 0
        #             apple_arr.remove(j)
        
        if len(snake_arr) == 0:
            game_over = True

        centerOfmassX = 0
        centerOfmassY = 0
        for i in snake_arr:
            #brainUpdate = i.brain.update(i.x,i.y)
            #i.x += random.randint(-1, 1)
            #i.y += random.randint(-1, 1)
            #i.x = brainUpdate[0]
            #i.y = brainUpdate[1]
            #(i.x,i.y) = i.brain.update(i.x,i.y)
            i.x += i.velocityX
            i.y += i.velocityY
            #if i.force < 0:
            i.velocityX *= 0.999
            i.velocityY *= 0.999
            centerOfmassX += i.x/num_snakes
            centerOfmassY += i.y/num_snakes
        M = 10#Mass
        Q = 10#Charge
        K = 50.0/num_snakes#scalar like big G
        
        for i in range(len(snake_arr)):
            for j in range(i+1,len(snake_arr)):
                dx = (snake_arr[i].x -snake_arr[j].x)
                dy = (snake_arr[i].y -snake_arr[j].y)
                d = math.sqrt(dx*dx+dy*dy)
                #print(i,j)
                R = snake_arr[i].radius+snake_arr[j].radius
                if d != 0:
                    #print("test")
                    force = (d*d*snake_arr[i].mass*snake_arr[j].mass/(R*R)-snake_arr[i].charge*snake_arr[j].charge)*K/(d*d*d*d*d)
                    fx = force*dx
                    fy = force*dy
                    #snake_arr[i].force = force
                    #snake_arr[j].force = force
                    snake_arr[i].velocityX -= fx
                    snake_arr[j].velocityX += fx
                    snake_arr[i].velocityY -= fy
                    snake_arr[j].velocityY += fy
            #print(snake_arr[0].velocityX)
            #for w in wall_arr:

                #(r,rx,ry) = w.calcDistance(snake_arr[i].x,snake_arr[i].y)
                #wallforce = -snake_arr[i].charge*Q*K/(r*r*r*r)
                #snake_arr[i].velocityX += rx*wallforce 
                #snake_arr[i].velocityY += ry*wallforce + 0.0005

        dis.fill(blue)
        for i in snake_arr:
            color = green
            if i.charge < 0:
                color = red
            elif i.charge == 0:
                color = white
            pygame.draw.circle(dis, color, [i.x, i.y], i.radius)
        pygame.draw.circle(dis, red, [centerOfmassX, centerOfmassY], snake_block)
        for w in wall_arr:
            w.draw()
 
        pygame.display.update()
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
 
gameLoop()
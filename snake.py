# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 15:30:49 2018

@author: kuppelur
"""
import pygame
from random import randint
import numpy as np
from scipy.spatial import distance
import math

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
block_size = 10
FPS = 5

dim_input_layer = 5

class Snake:
    def __init__(self,w=20,h=20,autoplay=True,gui=True,brain=None,snake_len = 5):
        self.w = w
        self.h = h
        self.body = []
        self.xdir =1
        self.ydir = 0
        self.len =0
        self.gui = gui
        if gui==True:self.render_init()
        self.snake_len = snake_len
        self.create_snake()     
        self.generate_food()
        self.autoplay = autoplay
        self.dir = 1
        self.train_data = []
        self.brain = brain
        self.prev_dist = w
        self.max_dist = distance.euclidean([0,0], [w,h])
        if brain is not None:
            print("Brain provided")

    def create_snake(self):
        #print(self.snake_len)
        for i in range(0,self.snake_len):
            self.body.append([int(self.w/2)+i, int(self.h/2)])

    def render_init(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode(((self.w)*block_size,(self.h)*block_size))
        pygame.display.set_caption('Snake AI')
        self.gameDisplay.fill(white)
        self.clock = pygame.time.Clock()
        
    def setDir(self,x,y):
        self.xdir = x
        self.ydir = y

    def generate_food(self):
        food = []
        while food == []:
            food = [randint(0, self.w-1), randint(1, self.h-1)]
            if food in self.body: food = []
        self.food = food


    def get_angle_between_points(self, snake = None):
        if snake is None:
            snake = self.body
        vector_a = np.array(self.food) - np.array(snake[-1])
        vector_b = np.array(self.body[-1]) - np.array(snake[-2])

        norm_of_vector_a = np.linalg.norm(vector_a)
        norm_of_vector_b = np.linalg.norm(vector_b)
        if norm_of_vector_a == 0:
            norm_of_vector_a = 10
        if norm_of_vector_b == 0:
            norm_of_vector_b = 10

        vector_a_normalized = vector_a / norm_of_vector_a
        vector_b_normalized = vector_b / norm_of_vector_b
        angle = math.atan2(
            vector_a_normalized[1] * vector_b_normalized[0] - vector_a_normalized[
                0] * vector_b_normalized[1],
            vector_a_normalized[1] * vector_b_normalized[1] + vector_a_normalized[
                0] * vector_b_normalized[0]) / math.pi
        #print(angle)
        return angle,vector_a_normalized,vector_b_normalized

    def key_to_dir(self,dir_key):
        '''
        if event.key == pygame.K_LEFT:
                return 0
        elif event.key == pygame.K_RIGHT:
                return 1
        if event.key == pygame.K_UP:
                return 2
        elif event.key == pygame.K_DOWN:
                return 3
        if dir == 0:
                self.setDir(-1, 0);
        elif dir == 1:
                self.setDir(1, 0);
        if dir == 2:
                self.setDir(0, -1);
        elif dir == 3:
                self.setDir(0, 1);
        '''
        if dir_key == 0:
            return self.xdir,self.ydir
        elif dir_key == 1:
            if self.dir == 0:
                return 0, -1 #up
            elif self.dir == 1:
                return 0, 1 #down
            elif self.dir == 2:
                return 1, 0 #right
            elif self.dir == 3:
                return -1, 0 #left
        elif dir_key == -1:
            if self.dir == 0:
                return 0, 1 #down
            elif self.dir == 1:
                return 0, -1 #up
            elif self.dir == 2:
                return -1, 0 #left
            elif self.dir == 3:
                return 1, 0 #right
        
    def direction_blocked(self,dir_key):
        xdir,ydir = self.key_to_dir(dir_key)
        snake = self.body.copy()
        head = snake[-1].copy()
        snake.pop(0)
        head[0] += xdir
        head[1] += ydir
        snake.append(head)
        #print(head)
        if self.endGame(snake):
            #print("End")
            if self.gui==True:
                pygame.draw.rect(self.gameDisplay, red, [head[0]*block_size, head[1]*block_size, block_size, block_size])
            return 1
        else:
            if self.gui==True:
                pygame.draw.rect(self.gameDisplay, green, [head[0]*block_size, head[1]*block_size, block_size, block_size])
            return 0

    def dir_to_vector(self,dir):
        if dir == 0:
                return(-1, 0);
        elif dir == 1:
                return(1, 0);
        if dir == 2:
                return(0, -1);
        elif dir == 3:
                return(0, 1);

    def update_input_condition_to_train(self,dir):
        old_dist = distance.euclidean(self.body[-1], self.food)
        angle,food_vect,snake_vect = self.get_angle_between_points()
        #if snake moves left
        snake = self.body.copy()
        xdir,ydir = self.key_to_dir(-1)
        snake = self.body.copy()
        head = snake[-1].copy()
        snake.pop(0)
        head[0] += xdir
        head[1] += ydir
        snake.append(head)
        #angle,food_vect,snake_vect = self.get_angle_between_points(snake)
        new_dist = distance.euclidean(snake[-1], self.food)
        if self.direction_blocked(-1):
            score = -1
        elif (self.eat(snake) or new_dist < old_dist):
            score = 1
        else:
            score = 0
        ret = np.array([[self.direction_blocked(-1),
                         self.direction_blocked(0),
                         self.direction_blocked(1),
                         -1,angle,],self.direction_blocked(-1)+score])
        self.train_data.append(ret)

        #if snake moves straight
        snake = self.body.copy()
        xdir,ydir = self.key_to_dir(0)
        snake = self.body.copy()
        head = snake[-1].copy()
        snake.pop(0)
        head[0] += xdir
        head[1] += ydir
        snake.append(head)
        #angle,food_vect,snake_vect = self.get_angle_between_points(snake)
        new_dist = distance.euclidean(snake[-1], self.food)
        if self.direction_blocked(0):
            score = -1
        elif (self.eat(snake) or new_dist < old_dist):
            score = 1
        else:
            score = 0
        ret = np.array([[self.direction_blocked(-1),
                         self.direction_blocked(0),
                         self.direction_blocked(1),
                         0,angle],self.direction_blocked(0)+score])
        self.train_data.append(ret)

        #if snake moves right
        snake = self.body.copy()
        xdir,ydir = self.key_to_dir(1)
        snake = self.body.copy()
        head = snake[-1].copy()
        snake.pop(0)
        head[0] += xdir
        head[1] += ydir
        snake.append(head)
        #angle,food_vect,snake_vect = self.get_angle_between_points(snake)
        new_dist = distance.euclidean(snake[-1], self.food)
        if self.direction_blocked(1):
            score = -1
        elif (self.eat(snake) or new_dist < old_dist):
            score = 1
        else:
            score = 0
        ret = np.array([[self.direction_blocked(-1),
                         self.direction_blocked(0),
                         self.direction_blocked(1),
                         1,angle],self.direction_blocked(1)+score])
        self.train_data.append(ret)
        
    def play_game(self):
        while not self.endGame():
            dir = self.get_input()
            self.update_input_condition_to_train(dir)
            self.dir = dir
            self.update(dir)
            if self.gui:
                self.render()
                self.clock.tick(FPS)
        #print(self.body)
        #print("game end Score:" + str(self.len)+"\r")
        #print(self.train_data[-1][1])
        #self.train_data[-1][1] = -1
        return self.train_data
        if self.gui: pygame.quit()
        
    def get_input(self):
        
        if self.gui:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and not self.autoplay:
                        if event.key == pygame.K_LEFT:
                                return 0
                        elif event.key == pygame.K_RIGHT:
                                return 1
                        if event.key == pygame.K_UP:
                                return 2
                        elif event.key == pygame.K_DOWN:
                                return 3
        if self.autoplay:
            if self.brain is not None:
                head = self.body[-1]
                y = []
                for dir_key in range(0,3):
                    angle,food_vect,snake_vect = self.get_angle_between_points()
                    X = np.array([self.direction_blocked(-1),
                                      self.direction_blocked(0),
                                      self.direction_blocked(1),
                                      dir_key-1,angle]).reshape(-1,dim_input_layer,1) 
                    temp = self.brain.predict(X)
                    #print(dir_key-1)
                    #print(temp)
                    y.append(temp)
                #print(y)
                dir_key = np.argmax(np.array(y))
                dir = self.temp_to_be_removed(dir_key-1)
                #print(dir_key-1,dir,self.dir)
            else:
                dir_key = randint(0,2)
                dir = self.temp_to_be_removed(dir_key-1)
                while (self.dir == 0 and dir == 1) or (self.dir == 1 and dir == 0) or (self.dir == 2 and dir == 3) or (self.dir == 3 and dir == 2):
                    dir_key = randint(0,2)
                    dir = self.temp_to_be_removed(dir_key-1)
        return(dir)

    def dir_to_key(self,dir):
        '''
        if event.key == pygame.K_LEFT:
                return 0
        elif event.key == pygame.K_RIGHT:
                return 1
        if event.key == pygame.K_UP:
                return 2
        elif event.key == pygame.K_DOWN:
                return 3
        '''
        if dir == 0:
            if self.dir == 0:
                return 0
            elif self.dir == 1:
                return 0
            elif self.dir == 2:
                return 1
            elif self.dir == 3:
                return -1
        elif dir == 1:
            if self.dir == 0:
                return 0
            elif self.dir == 1:
                return 0
            elif self.dir == 2:
                return -1
            elif self.dir == 3:
                return 1
        elif dir == 2:
            if self.dir == 0:
                return -1
            elif self.dir == 1:
                return 1
            elif self.dir == 2:
                return 0
            elif self.dir == 3:
                return 0
        elif dir == 3:
            if self.dir == 0:
                return 1
            elif self.dir == 1:
                return -1
            elif self.dir == 2:
                return 0
            elif self.dir == 3:
                return 0

    def temp_to_be_removed(self,dir_key):
        '''
        if event.key == pygame.K_LEFT:
                return 0
        elif event.key == pygame.K_RIGHT:
                return 1
        if event.key == pygame.K_UP:
                return 2
        elif event.key == pygame.K_DOWN:
                return 3
        '''
        if self.dir == 0:
            if dir_key == -1:
                return 3
            elif dir_key == 0:
                return 0
            elif dir_key == 1:
                return 2
        elif self.dir == 1:
            if dir_key == -1:
                return 2
            elif dir_key == 0:
                return 1
            elif dir_key == 1:
                return 3
        elif self.dir == 2:
            if dir_key == -1:
                return 0
            elif dir_key == 0:
                return 2
            elif dir_key == 1:
                return 1
        elif self.dir == 3:
            if dir_key == -1:
                return 1
            elif dir_key == 0:
                return 3
            elif dir_key == 1:
                return 0
            
                
        
    def render(self):
        self.gameDisplay.fill(white)
        pygame.draw.rect(self.gameDisplay, red, [self.food[0]*block_size, self.food[1]*block_size,block_size,block_size])
        for i,point in enumerate(self.body):
            pygame.draw.rect(self.gameDisplay, black, [point[0]*block_size, point[1]*block_size, block_size, block_size])
        pygame.display.update()
        
    def update(self,dir):     
        if dir == 0:
                self.setDir(-1, 0);
        elif dir == 1:
                self.setDir(1, 0);
        if dir == 2:
                self.setDir(0, -1);
        elif dir == 3:
                self.setDir(0, 1);
        grown = self.eat()
        head = self.body[-1].copy()
        if(not grown): self.body.pop(0)
        else: self.len+=1
        head[0] += self.xdir
        head[1] +=self.ydir
        self.body.append(head)
        

    def endGame(self,snake = None):
        if snake is None:
            snake = self.body
        x = snake[-1][0]
        y = snake[-1][1]
        if(x > self.w-1 or x < 0 or y > self.h-1 or y < 0 or (snake[-1] in snake[0:-1])):
           return True;
        else:
            return False;

    def eat(self,snake = None):
        if snake is None:
            prediction_mode = False
            snake = self.body
        else:
            prediction_mode = True
        if snake[-1] == self.food:
            if not prediction_mode:
                self.generate_food()
            return True
        else:
            return False


if __name__ == "__main__":
    game = Snake(autoplay=True,gui=True)
    print(game.play_game())
        

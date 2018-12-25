# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 15:30:49 2018

@author: kuppelur
"""
import pygame
from random import randint

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
block_size = 10
FPS = 10

class Snake:
    def __init__(self,w=40,h=40):
        self.w = w
        self.h = h
        self.body = []
        self.xdir =1
        self.ydir = 0
        self.len =0
        self.render_init()
        self.create_snake()     
        self.generate_food()

    def create_snake(self):
        self.body.insert(0,[int(self.w/2), int(self.h/2)])
        self.body.insert(1,[int(self.w/2)+1, int(self.h/2)])
        self.body.insert(2,[int(self.w/2)+2, int(self.h/2)])

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

    def play_game(self):
        while not self.endGame():
            self.update(self.get_input())
            self.render()
            game.clock.tick(FPS)
        print(self.body)
        print("game end Score:" + str(self.len)) 
        pygame.quit()
        quit()

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                        return 0;
                elif event.key == pygame.K_RIGHT:
                        return 1;
                if event.key == pygame.K_UP:
                        return 2;
                elif event.key == pygame.K_DOWN:
                        return 3;
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

    def endGame(self):
        x = self.body[-1][0]
        y = self.body[-1][1]
        if(x > self.w-1 or x < 0 or y > self.h-1 or y < 0 or (self.body[-1] in self.body[0:-1])):
           return True;
        else:
            return False;

    def eat(self):
        if self.body[-1] == self.food:
            self.generate_food()
            return True
        else:
            return False
    

if __name__ == "__main__":
    game = Snake()
    game.play_game()
        

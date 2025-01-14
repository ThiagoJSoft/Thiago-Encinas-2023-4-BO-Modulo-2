import pygame
import random

from pygame.sprite import Sprite

from game.utils.constants import ENEMY_1, SCREEN_HEIGHT, SCREEN_WIDTH, ENEMY_2
from game.components.bullets.bullet import Bullet


class Enemy(Sprite):
    Y_POS = 20
    X_POS_LIST = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    SPEED_Y = 1
    SPEED_X = 5
    MOV_X = {0: 'left', 1: 'right' }
    SHIP_WIDTH = 40
    SHIP_HEIGHT = 60
    X_POS_LIST_SEC = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275]
    


    def __init__(self, enemy_type=1, x_speed=5, y_speed=2, move_x_for=[50, 120]):
        self.image = ENEMY_1
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS_LIST[random.randint(0, 10)]
        self.rect.y = self.Y_POS
        self.speed_y = self.SPEED_Y
        self.speed_x = self.SPEED_X
        self.movement_x = self.MOV_X[random.randint(0, 1)]
        self.move_x_for = random.randint(30, 100)
        self.index = 0
        self.image_sec = ENEMY_2
        self.image_sec = pygame.transform.scale(self.image_sec, (40, 60))
        self.rect_sec = self.image_sec.get_rect()
        self.rect_sec.x = self.X_POS_LIST_SEC[random.randint(0, 10)]
        self.movement_x_sec = random.choice(['left', 'right'])
        self.speed_x_sec = 10
        self.index_sec = 0
        self.move_sec = 0
        self.type = 'enemy'
        self.shooting_time  = random.randint(30, 50)

    def update(self, ships, game):
        self.rect.y += self.speed_y
        self.shoot(game.bullet_manager)

        if self.movement_x == 'left':
            self.rect.x -= self.speed_x 
        else:
            self.rect.x += self.speed_x
        self.change_movement_x()

        if self.rect.y >= SCREEN_HEIGHT:
            ships.remove(self)
        
        if self.movement_x_sec == 'left' and (self.rect_sec.x <= 10 or self.move_sec <= 0):
            self.movement_x_sec = 'right'
            self.index_sec = 0
        elif self.movement_x_sec == 'right' and (self.rect_sec.x >= SCREEN_WIDTH - self.SHIP_WIDTH or self.move_sec <= 0):
            self.movement_x_sec = 'left'
            self.index_sec = 0

        if self.movement_x_sec == 'left':
            self.rect_sec.x -= self.speed_x_sec
        else:
            self.rect_sec.x += self.speed_x_sec

        self.move_sec += self.speed_x_sec

        
        
        
        

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.image_sec, (self.rect_sec.x, self.rect_sec.y))
    
    def change_movement_x(self):
        self.index += 1
        if (self.index >= self.move_x_for and self.movement_x == 'right') or (self.rect.x >= SCREEN_WIDTH - self.SHIP_WIDTH):
            self.movement_x = 'left'
            self.index = 0
        elif (self.index >= self.move_x_for and self.movement_x == 'left') or (self.rect.x <= 10):
            self.movement_x = 'right'
            self.index = 0
    
    def shoot(self, bullet_manager):
        current_time = pygame.time.get_ticks()
        if self.shooting_time <= current_time:
            bullet = Bullet(self)
            bullet_manager.add_bullet(bullet)
            self.shooting_time += random.randint(30, 50)

    


    



    
    

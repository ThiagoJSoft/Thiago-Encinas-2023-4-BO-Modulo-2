import pygame

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, FONT_STYLE
from game.components.spaceship import Spaceship
from game.components.enemies.enemy_manager import EnemyManager
from game.components.bullets.bullet_manager import BulletManager
from game.components.menu import Menu
from game.components.power_ups.power_up_manager import PowerUpManager



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.death_count = 0
        self.score = 0
        self.best_score = 0
        self.player = Spaceship()
        self.enemy_manager = EnemyManager()
        self.bullet_manager = BulletManager()
        self.menu = Menu('Press Any Key To Start. . . ', self.screen)
        self.power_up_manager = PowerUpManager()

        
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()


    def run(self):
        # Game loop: events - update - draw
        self.score = 0
        self.enemy_manager.reset()
        self.bullet_manager.reset()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input, self)
        self.enemy_manager.update(self)
        self.bullet_manager.update(self)
        self.power_up_manager.update(self)
    
    def reset(self):
        self.power_up_manager.reset()

        
        

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        self.bullet_manager.draw(self.screen)
        self.draw_score()
        self.power_up_manager.draw(self.screen)
        self.draw_power_up_time()
        pygame.display.update()
        pygame.display.flip()

    

    def draw_background(self):
        
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed

    def show_menu(self):
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2
        
        self.menu.reset_screen_color(self.screen)

        if self.death_count > 0:
            if self.score > self.best_score:
                self.best_score = self.score
                self.menu.update_message(f'New Best Score: {self.best_score}')
            else:
                self.menu.update_message(f'Score: {self.score}')
        #else:
            #self.menu.update_message('Press Any Key To Start. . .')        

        icon = pygame.transform.scale(ICON, (80, 120))
        self.screen.blit(icon, (half_screen_width - 50, half_screen_height - 150))
        
        


        self.menu.draw(self.screen, 'Press Any Key To Start. . .')
        self.menu.update(self)

    def update_score(self):
        self.score += 1

    def draw_score(self):
        #font = pygame.font.Font(FONT_STYLE, 30)
        #text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        #text_rect = text.get_rect()
        #text_rect.center = (1000, 50)
        #self.screen.blit(text, text_rect)
        font = pygame.font.Font(FONT_STYLE, 30)
        score_text = f'Score: {self.score}'
        best_score_text = f'Best Score: {self.best_score}'
        score_render = font.render(score_text, True, (255, 255, 255))
        best_score_render = font.render(best_score_text, True, (255, 255, 255))
        score_rect = score_render.get_rect()
        best_score_rect = best_score_render.get_rect()
        score_rect.center = (1000, 50)
        best_score_rect.center = (1000, 80)
        self.screen.blit(score_render, score_rect)
        self.screen.blit(best_score_render, best_score_rect)
    

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks()) / 1000, 2)

            if time_to_show >= 0:
                self.menu.draw(self.screen, f'{self.player.power_up_type.capitalize()} is enabled for {time_to_show} seconds', 540, 50, (255, 255, 255))

            else:
                self.player.has_power_up = False
                self.player.power_up_type = DEFAULT_TYPE
                self.player.set_image()                    

        

                         
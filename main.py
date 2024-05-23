
import pygame
import sys

#Window size is 1024 * 512
# width = pixel * 64
# height = pixel * 32

class HauntingMaze:
    def __init__(self):
        pygame.init()
        
        pygame.mixer.init()
        pygame.mixer.music.load('assets/sfx/background_music.mp3')
        
        self.coin_sound = pygame.mixer.Sound('assets/sfx/coin_sfx.mp3')
        self.monster_sound = pygame.mixer.Sound('assets/sfx/monster_sfx.wav')
        
        #Scaling; 16x16 square pixel
        self.width = 1024
        self.height = 512
        self.pixel = 16
        self.screen = pygame.display.set_mode((self.width, self.height + 50))
        
        #Text Initializer
        self.game_font = pygame.font.SysFont("Arial", 24)
        
        self.load_images()
        self.new_game()
        self.main_loop()

    def load_images(self):
        
        image_files = ["assets/images/robot.png", "assets/images/monster.png", "assets/images/door.png", "assets/images/coin.png"]
        attributes = ["robot", "monster", "door", "coin"]

        for attribute, image_file in zip(attributes, image_files):
            
            image = pygame.image.load(image_file).convert_alpha()
            orig_w, orig_h = image.get_size()
            
            if image_file == "assets/images/coin.png":
                new_height = self.pixel * 1
            elif image_file == "assets/images/door.png":
                new_height = self.pixel * 4
            else:
                new_height = self.pixel * 2  # 16 * 3
            
            
            aspect_ratio = orig_w / orig_h
            new_width = int(new_height * aspect_ratio)
            
            scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))
            
            setattr(self, attribute, scaled_image)

    def main_loop(self):
        clock = pygame.time.Clock()
        while True:
            self.check_events()
            self.update_position()
            self.fog_of_war()
            self.draw_window()
            self.game_over()
            clock.tick(60)        
        
    def new_game(self):
        
        pygame.mixer.music.play(-1)
        # default_locations
        self.x_robot, self.y_robot = self.pixel * 4, self.pixel * 4
        self.x_monster, self.y_monster = self.pixel * 57, self.pixel * 4
        self.x_door, self.y_door = self.pixel * 60, self.pixel * 25
        
        # Movement of Robot init
        self.to_left = False
        self.to_right = False
        self.to_up = False
        self.to_down = False
        
        # Wall coordinates and dimensions (x, y, width, height)
        wall_data = [
            (0, 0, 64, 1),         # Top border
            (0, 31, 64, 1),        # Bottom border
            (0, 1, 1, 31),         # Left border
            (63, 1, 1, 31),        # Right border
            (4, 9, 12, 1),
            (9, 4, 1, 10),
            (9, 17, 1, 11),
            (1, 14, 5, 1),
            (1, 23, 5, 1),
            (5, 15, 1, 5),
            (5, 24, 1, 4),
            (13, 4, 7, 1),
            (19, 5, 1, 4),
            (19, 9, 7, 1),
            (19, 13, 5, 1),
            (19, 14, 1, 6),
            (13, 19, 7, 1),
            (14, 20, 1, 11),
            (18, 25, 6, 1),
            (19, 26, 1, 2),
            (23, 18, 1, 7),
            (29, 1, 1, 10),
            (24, 4, 12, 1),
            (35, 5, 1, 4),
            (29, 14, 1, 17),
            (30, 14, 6, 1),
            (39, 4, 1, 16),
            (40, 4, 10, 1),
            (45, 5, 1, 9),
            (49, 5, 1, 4),
            (39, 24, 1, 7),
            (33, 24, 6, 1),
            (33, 25, 1, 3),
            (49, 13, 1, 11),
            (44, 19, 5, 1),
            (44, 24, 13, 1),
            (50, 25, 1, 6),
            (53, 9, 10, 1),
            (59, 10, 1, 6),
            (54, 13, 6, 1),
            (54, 14, 1, 6),
            (60, 24, 3, 1)
        ]
        self.coin_location = [
            (3 ,16),
            (3, 25),
            (17, 6),
            (21, 23),
            (33, 6),
            (30, 15),
            (37, 26),
            (42, 5),
            (47, 17),
            (56, 15)
        ]
        
        self.walls = [pygame.Rect(x * self.pixel, y * self.pixel, w * self.pixel, h * self.pixel) for x, y, w, h in wall_data]
        self.coins = [pygame.Rect(x * self.pixel, y * self.pixel, self.pixel, self.pixel) for x, y in self.coin_location]
        self.score = 0   
    
    def check_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.to_left = True
                if event.key == pygame.K_d:
                    self.to_right = True
                if event.key == pygame.K_w:
                    self.to_up = True
                if event.key == pygame.K_s:
                    self.to_down = True
                
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.to_left = False
                if event.key == pygame.K_d:
                    self.to_right = False
                if event.key == pygame.K_w:
                    self.to_up = False
                if event.key == pygame.K_s:
                    self.to_down = False
            
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                sys.exit()
    
    def update_position(self):
        if self.to_left:
            new_x = self.x_robot - 2
            if not self.check_collision(new_x, self.y_robot, self.robot):
                self.x_robot = new_x
        if self.to_right:
            new_x = self.x_robot + 2
            if not self.check_collision(new_x, self.y_robot, self.robot):
                self.x_robot = new_x
        if self.to_up:
            new_y = self.y_robot - 2
            if not self.check_collision(self.x_robot, new_y, self.robot):
                self.y_robot = new_y
        if self.to_down:
            new_y = self.y_robot + 2
            if not self.check_collision(self.x_robot, new_y, self.robot):
                self.y_robot = new_y
        
        # monster movement
        if self.x_robot > self.x_monster:
            new_x_monster = self.x_monster + 1.25
            if not self.check_collision(new_x_monster, self.y_monster, self.monster):
                self.x_monster = new_x_monster
        if self.x_robot < self.x_monster:
            new_x_monster = self.x_monster - 1.25
            if not self.check_collision(new_x_monster, self.y_monster, self.monster):
                self.x_monster = new_x_monster
        if self.y_robot > self.y_monster:
            new_y_monster = self.y_monster + 1.25
            if not self.check_collision(self.x_monster, new_y_monster, self.monster):
                self.y_monster = new_y_monster
        if self.y_robot < self.y_monster:
            new_y_monster = self.y_monster - 1.25
            if not self.check_collision(self.x_monster, new_y_monster, self.monster):
                self.y_monster = new_y_monster

        robot_rect = self.get_hitbox(self.x_robot, self.y_robot, self.robot)
        for coin in self.coins:
            if robot_rect.colliderect(coin):
                self.coin_sound.play()
                self.score += 1
                self.coins.remove(coin)
        
    def check_collision(self, x, y, image):
        sprite_rect = self.get_hitbox(x, y, image)
        for wall in self.walls:
            if sprite_rect.colliderect(wall):
                return True
        return False
    
    def get_hitbox(self, x, y, image):
        return image.get_rect(topleft =(x, y))
    
    def game_over(self):
        robot_hitbox = self.get_hitbox(self.x_robot, self.y_robot, self.robot)
        monster_hitbox = self.get_hitbox(self.x_monster, self.y_monster, self.monster)
        door_hitbox = self.get_hitbox(self.x_door, self.y_door, self.door)
        
        if robot_hitbox.colliderect(door_hitbox) and self.score == 10:
            self.success_screen()
            self.new_game()
            self.main_loop()
        
        if robot_hitbox.colliderect(monster_hitbox):
            self.monster_sound.play()
            self.new_game()
    
    def success_screen(self):
        success_text = self.game_font.render("Congratulations! You completed the game!", True, (0, 255, 0))
        retry_text = self.game_font.render("Press 'R' to retry or 'Q' to quit.", True, (0, 255, 0))

        self.screen.fill((0, 0, 0))
        self.screen.blit(success_text, (self.width // 2 - success_text.get_width() // 2, self.height // 2 - 50))
        self.screen.blit(retry_text, (self.width // 2 - retry_text.get_width() // 2, self.height // 2 + 50))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return  
                    elif event.key == pygame.K_q:
                        pygame.mixer.music.stop()
                        sys.exit() 
    
    def fog_of_war(self):
        robot_center_x = self.x_robot + self.robot.get_width() / 2
        robot_center_y = self.y_robot + self.robot.get_height() / 2
        
        distance = self.pixel * 4
        
        self.west_fog = pygame.Rect(0, 0, (robot_center_x - distance), self.height)
        self.north_fog = pygame.Rect(0, 0, self.width, (robot_center_y - distance))
        self.south_fog = pygame.Rect(0, (robot_center_y + distance), self.width, (self.height - (robot_center_y + distance)))
        self.east_fog = pygame.Rect((robot_center_x + distance), 0, (self.width - robot_center_x + distance), self.height)
    
    def draw_window(self):
        
        self.screen.fill((220, 220, 220))
        
        for wall in self.walls:
            pygame.draw.rect(self.screen, (47,79, 79), wall)
        
        self.screen.blit(self.door, (self.x_door, self.y_door))
        self.screen.blit(self.robot, (self.x_robot, self.y_robot))
        self.screen.blit(self.monster, (self.x_monster, self.y_monster))
       
        for coin in self.coins:
            self.screen.blit(self.coin, coin.topleft)
        
        if False:    #to enable fog of war
            pygame.draw.rect(self.screen, (0,0,0), self.west_fog)
            pygame.draw.rect(self.screen, (0,0,0), self.north_fog)
            pygame.draw.rect(self.screen, (0,0,0), self.south_fog)
            pygame.draw.rect(self.screen, (0,0,0), self.east_fog)
        
        # Score display
        coins = self.game_font.render(f"Coins remaining: {10 - self.score}", True, (255, 0, 0))
        self.screen.blit(coins, (25, self.height + 10))   
        
        pygame.display.flip()


if __name__ == "__main__":
    HauntingMaze()
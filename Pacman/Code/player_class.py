from Code.SETTINGS import *
import pygame

vector = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self,pacman,start_pos):
        super().__init__()
        
        self.speed = PLAYER_SPEED
        self.death_image = 112
        self.grid_start_position = vector(start_pos[0],start_pos[1])
        self.grid_position = vector(start_pos[0],start_pos[1])

        self.pixel_start_position = self.calculate_pixel_position()
        self.pixel_position = self.calculate_pixel_position()
        
        self.rect = pygame.Rect(self.pixel_position.x,self.pixel_position.y,TILE_SIZE[0],TILE_SIZE[1])
        
        self.screen = pacman.screen
        
        self.images = pacman.sprite_images
        self.image = self.images[112]
        self.mouth_open = True
        self.image_change_count = 0


        self.wall_rects = pacman.wall_rects
        self.ghost_cell_rects = pacman.ghost_cell_rects

        self.current_direction = vector(0,0)
        
        self.given_direction = vector(self.current_direction.x,self.current_direction.y)

        self.player_lives = 3
        

    def update(self):
        
        if self.player_lives <= 0:
            self.current_direction.update(0,0)
            self.given_direction.update(0,0)
            self.update_death_animation()
        else:            
            self.pixel_position.update(self.pixel_position.x + self.current_direction.x * self.speed,self.pixel_position.y + self.current_direction.y * self.speed)
            

            self.rect.left = round(self.pixel_position.x)
            self.rect.top = round(self.pixel_position.y)
            self.update_player_animation()
            
            if self.player_walls_collision_given_direction():
                if abs(self.current_direction.y) != abs(self.given_direction.y):
                    if self.player_walls_collision_current_direction():
                        self.current_direction.update(0,0) 
                        self.given_direction.update(0,0) 
                else:
                    self.current_direction.update(0,0) 
                    self.given_direction.update(0,0) 

            else:
                self.current_direction.update(self.given_direction.x,self.given_direction.y)

            #set grid pos in reference to pix pos
            self.grid_position.update(self.rect.center[0]//TILE_SIZE[0],self.rect.center[1]//TILE_SIZE[0])

            if self.pixel_position.x  <  -self.rect.width//2:
                self.pixel_position.x = MAZE_SIZE[0] - self.rect.width//2 
            if self.pixel_position.x > MAZE_SIZE[0] - self.rect.width//2 :
                self.pixel_position.x = -self.rect.width//2
            
        
    def draw(self):

        self.screen.blit(self.image,(self.rect.left-self.rect.width//4,self.rect.top-self.rect.height//4))

        

    
    def move(self,direction):
        self.given_direction = direction

    def calculate_pixel_position(self):
        return vector(self.grid_position.x*TILE_SIZE[0]+TILE_SIZE[0]//2,self.grid_position.y*TILE_SIZE[1])


    def player_walls_collision_given_direction(self):
        '''find where the rect will be in the next frame following the given_direction and if it will collide with the wall prevent it from doing so'''

        self.next_player_rect_given_deriction = pygame.Rect(self.rect.left + self.given_direction.x,self.rect.top + self.given_direction.y,self.rect.width,self.rect.height)
        
        for ghost_cell_rect in self.ghost_cell_rects:
            if self.next_player_rect_given_deriction.colliderect(ghost_cell_rect):
                return True
        for wall_rect in self.wall_rects:
            if self.next_player_rect_given_deriction.colliderect(wall_rect):
                return True
        return False

    def player_walls_collision_current_direction(self):
        '''find where the rect will be in the next frame following the current_direction and if it will collide with the wall prevent it from doing so'''

        self.next_player_rect_current_direction = pygame.Rect(self.rect.left + self.current_direction.x,self.rect.top + self.current_direction.y,self.rect.width,self.rect.height)
        
        for ghost_cell_rect in self.ghost_cell_rects:
            if self.next_player_rect_current_direction.colliderect(ghost_cell_rect):
                return True
        for wall_rect in self.wall_rects:
            if self.next_player_rect_current_direction.colliderect(wall_rect):
                return True
        return False

    def update_player_animation(self):

 
        if self.mouth_open:
            if self.current_direction.x < 0:
                self.image = self.images[48]
            elif self.current_direction.x > 0: 
                self.image = self.images[52]
            elif self.current_direction.y < 0:
                self.image = self.images[49]
            elif self.current_direction.y > 0:
                self.image = self.images[53]
            self.image_change_count += 1

            if self.image_change_count >= FPS//6:
                self.mouth_open = False
                self.image_change_count = 0
        else:
            if self.current_direction.x < 0:
                self.image = self.images[50]
            elif self.current_direction.x > 0: 
                self.image = self.images[54]
            elif self.current_direction.y < 0:
                self.image = self.images[51]
            elif self.current_direction.y > 0:
                self.image = self.images[55]
            self.image_change_count += 1

            if self.image_change_count >= FPS//6:
                self.mouth_open = True
                self.image_change_count = 0

    def player_reset(self):
        self.current_direction.update(0,0)
        self.given_direction.update(0,0)
        self.grid_position.update(self.grid_start_position.x,self.grid_start_position.y)
        self.pixel_position.update(self.pixel_start_position.x,self.pixel_start_position.y)
        self.rect.left = self.pixel_start_position.x
        self.rect.top = self.pixel_start_position.y
        self.image = self.images[112]
        
    def get_player_grid_position(self):
        return self.grid_position

    def get_player_direction(self):
        return self.current_direction

    def update_death_animation(self):
        
        if self.death_image == 112:
            self.image = self.images[self.death_image]
            self.image_change_count += 1
            if self.image_change_count >= FPS // 3.5:
                self.death_image = 116
                self.image_change_count = 0
        elif self.death_image < 128:
            self.image = self.images[self.death_image]
            self.image_change_count += 1
            if self.image_change_count >= FPS // 3.5:
                self.death_image += 1
                self.image_change_count = 0

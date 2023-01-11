from Code.SETTINGS import *
import pygame
import random

vector = pygame.math.Vector2

class Ghost(pygame.sprite.Sprite):
    def __init__(self,pacman,behaviour):
        super().__init__()

        self.afraid_mode_seconds = AFRAID_MODE_SECONDS
        self.screen = pacman.screen
        self.behaviour = behaviour
        self.wall_rects = pacman.wall_rects
        self.ghost_cell_rects = pacman.ghost_cell_rects
        self.move_to_be_made = False
        self.respawn_timer = 0
        self.chase_target = vector(-1,-1)
        self.afraid_mode_timer = 0
        self.image_change_count = 0   
        self.change_feet = True    

        self.images = pacman.sprite_images

        if self.behaviour == 1: #Blinky (Red Ghost)
            self.current_direction = vector(1 if random.random() > 0.5 else -1,0)
            self.next_direction = vector(self.current_direction.x,self.current_direction.y)
            self.grid_start_position = vector(13,14)
            self.grid_position = vector(self.grid_start_position.x,self.grid_start_position.y)
            self.next_grid_position = vector(-1,-1)
            self.next_grid_position_ahead = vector(-1,-1)
            self.next_grid_position_left = vector(-1,-1)
            self.next_grid_position_right = vector(-1,-1)
            self.speed = BLINKY_SPEED
            self.pixel_position = self.calculate_pixel_position()
            self.pixel_start_position = self.calculate_pixel_position()
            self.rect = pygame.Rect(self.pixel_position.x,self.pixel_position.y,TILE_SIZE[0],TILE_SIZE[1])
            self.out_of_cell = True
            self.scatter_target = vector(27,0)
            self.mode = pacman.ghost_mode # 1 = chase, 2 = scatter, 3 = afraid, 4 = killed and waiting to respawn, 5 = not yet in play   
            self.enter_play_timer = 0
            self.image = self.images[96]

        if self.behaviour == 2: #Pinky (Pink Ghost)
            self.current_direction = vector(1,0)
            self.next_direction = vector(self.current_direction.x,self.current_direction.y)
            self.grid_start_position = vector(11,17)
            self.grid_position = vector(self.grid_start_position.x,self.grid_start_position.y)
            self.next_grid_position = vector(-1,-1)
            self.next_grid_position_ahead = vector(-1,-1)
            self.next_grid_position_left = vector(-1,-1)
            self.next_grid_position_right = vector(-1,-1)
            self.speed = PINKY_SPEED
            self.pixel_position = self.calculate_pixel_position()
            self.pixel_start_position = self.calculate_pixel_position()
            self.rect = pygame.Rect(self.pixel_position.x,self.pixel_position.y,TILE_SIZE[0],TILE_SIZE[1])
            self.out_of_cell = False
            self.scatter_target = vector(0,0)
            self.mode = 5   # 1 = chase, 2 = scatter, 3 = afraid, 4 = killed and waiting to respawn, 5 = not yet in play  
            self.enter_play_timer = FPS*PINKY_ENTER_PLAY_SECONDS
            self.image = self.images[128]

        if self.behaviour == 3: #Inky (Blue Ghost)
            self.current_direction = vector(-1,0)
            self.next_direction = vector(self.current_direction.x,self.current_direction.y)
            self.grid_start_position = vector(13,17)
            self.grid_position = vector(self.grid_start_position.x,self.grid_start_position.y)
            self.next_grid_position = vector(-1,-1)
            self.next_grid_position_ahead = vector(-1,-1)
            self.next_grid_position_left = vector(-1,-1)
            self.next_grid_position_right = vector(-1,-1)
            self.speed = INKY_SPEED
            self.pixel_position = self.calculate_pixel_position()
            self.pixel_start_position = self.calculate_pixel_position()
            self.rect = pygame.Rect(self.pixel_position.x,self.pixel_position.y,TILE_SIZE[0],TILE_SIZE[1])
            self.out_of_cell = False
            self.scatter_target = vector(27,35)
            self.mode = 5   # 1 = chase, 2 = scatter, 3 = afraid, 4 = killed and waiting to respawn, 5 = not yet in play  
            self.enter_play_timer = FPS*INKY_ENTER_PLAY_SECONDS
            self.image = self.images[136]
            self.pinky_target = vector(-1,-1)
            self.target_direction = vector(-1,-1)

        if self.behaviour == 4: #Clyde (Orange Ghost)
            self.current_direction = vector(-1,0)
            self.next_direction = vector(self.current_direction.x,self.current_direction.y)
            self.grid_start_position = vector(15,17)
            self.grid_position = vector(self.grid_start_position.x,self.grid_start_position.y)
            self.next_grid_position = vector(-1,-1)
            self.next_grid_position_ahead = vector(-1,-1)
            self.next_grid_position_left = vector(-1,-1)
            self.next_grid_position_right = vector(-1,-1)
            self.speed = CLYDE_SPEED
            self.pixel_position = self.calculate_pixel_position()
            self.pixel_start_position = self.calculate_pixel_position()
            self.rect = pygame.Rect(self.pixel_position.x,self.pixel_position.y,TILE_SIZE[0],TILE_SIZE[1])
            self.out_of_cell = False
            self.scatter_target = vector(0,35)
            self.mode = 5   # 1 = chase, 2 = scatter, 3 = afraid, 4 = killed and waiting to respawn, 5 = not yet in play  
            self.enter_play_timer = FPS*CLYDE_ENTER_PLAY_SECONDS
            self.image = self.images[144]
            


    def update(self,player_grid_position,player_direction = vector(-1,-1),blinky_grid_position = vector(-1,-1)):
        self.update_ghost_animation()
        if self.behaviour == 1:
            self.chase_target.update(player_grid_position)
        if self.behaviour == 2:
            self.chase_target.update(player_grid_position.x + player_direction.x*2,player_grid_position.y + player_direction.y*2)
        if self.behaviour == 3:
            self.pinky_target.update(player_grid_position.x + player_direction.x*2,player_grid_position.y + player_direction.y*2)
            self.target_direction.update(self.pinky_target.x-blinky_grid_position.x,self.pinky_target.y-blinky_grid_position.y)
            self.chase_target.update(self.pinky_target.x+self.target_direction.x,self.pinky_target.y+self.target_direction.y)
        if self.behaviour == 4:
            if self.grid_position.distance_to(player_grid_position) > 8:
                self.chase_target.update(player_grid_position)
            else:
                self.chase_target.update(self.scatter_target)

        if self.mode == 3:
            self.afraid_mode_timer += 1

        if self.mode == 4:
            self.respawn_timer += 1
            if self.respawn_timer > GHOST_RESPAWN_SECONDS * FPS:
                self.respawn_timer = 0 
                self.mode = 2
                self.out_of_cell = False
        elif self.mode == 5:
            self.enter_play_timer -= 1
            if self.enter_play_timer <= 0:
                self.mode = 2
                self.out_of_cell = False
        else:
            self.pixel_position.update(self.pixel_position.x + self.current_direction.x * self.speed,self.pixel_position.y + self.current_direction.y * self.speed)

            self.rect.left = round(self.pixel_position.x)
            self.rect.top = round(self.pixel_position.y)

            self.grid_position.update(self.rect.center[0]//TILE_SIZE[0],self.rect.center[1]//TILE_SIZE[1])
        
            if self.pixel_position.x  <  -self.rect.width//2:
                self.pixel_position.x = MAZE_SIZE[0] - self.rect.width//2
                self.rect.left = MAZE_SIZE[0] - self.rect.width//2
                self.grid_position.update(self.rect.center[0]//TILE_SIZE[0],self.rect.center[1]//TILE_SIZE[1])
                self.next_grid_position.update(self.grid_position.x + self.current_direction.x,self.grid_position.y + self.current_direction.y)
                self.move_to_be_made = False
            if self.pixel_position.x > MAZE_SIZE[0] - self.rect.width//2:
                self.pixel_position.x = -self.rect.width//2
                self.rect.left = -self.rect.width//2
                self.grid_position.update(self.rect.center[0]//TILE_SIZE[0],self.rect.center[1]//TILE_SIZE[1])
                self.next_grid_position.update(self.grid_position.x + self.current_direction.x,self.grid_position.y + self.current_direction.y)
                self.move_to_be_made = False

            if not self.move_to_be_made:
                self.move_to_target()
                self.move_to_be_made = True
     
            if self.rect.x % TILE_SIZE[0] == 0 and self.rect.y % TILE_SIZE[1] == 0 and self.move_to_be_made and self.grid_position == self.next_grid_position:
                self.current_direction.update(self.next_direction.x,self.next_direction.y)
                self.move_to_be_made = False

            if self.grid_position == vector(13,14) or self.grid_position == vector(14,14):
                self.out_of_cell = True






                


    def move_to_target(self):
        self.next_grid_position.update(self.grid_position.x + self.current_direction.x,self.grid_position.y + self.current_direction.y)
        self.next_grid_position_ahead.update(self.next_grid_position.x + self.current_direction.x,self.next_grid_position.y + self.current_direction.y)
        self.next_grid_position_left.update(self.next_grid_position.x + self.current_direction.rotate(-90).x,self.next_grid_position.y + self.current_direction.rotate(-90).y)
        self.next_grid_position_right.update(self.next_grid_position.x + self.current_direction.rotate(90).x,self.next_grid_position.y + self.current_direction.rotate(90).y)
        self.min_distance = 10000

        for wall_rect in self.wall_rects:
            if wall_rect.collidepoint(self.next_grid_position_left.x*TILE_SIZE[0],self.next_grid_position_left.y*TILE_SIZE[1]):
                self.next_grid_position_left.update(-1,-1)         
            if wall_rect.collidepoint(self.next_grid_position_ahead.x*TILE_SIZE[0],self.next_grid_position_ahead.y*TILE_SIZE[1]):
                self.next_grid_position_ahead.update(-1,-1)
            if wall_rect.collidepoint(self.next_grid_position_right.x*TILE_SIZE[0],self.next_grid_position_right.y*TILE_SIZE[1]):
                self.next_grid_position_right.update(-1,-1)  

        if self.out_of_cell:
            for cell_rect in self.ghost_cell_rects:
                if cell_rect.collidepoint(self.next_grid_position_left.x*TILE_SIZE[0],self.next_grid_position_left.y*TILE_SIZE[1]):
                    self.next_grid_position_left.update(-1,-1)         
                if cell_rect.collidepoint(self.next_grid_position_ahead.x*TILE_SIZE[0],self.next_grid_position_ahead.y*TILE_SIZE[1]):
                    self.next_grid_position_ahead.update(-1,-1)
                if cell_rect.collidepoint(self.next_grid_position_right.x*TILE_SIZE[0],self.next_grid_position_right.y*TILE_SIZE[1]):
                    self.next_grid_position_right.update(-1,-1)          

        if self.out_of_cell == False:
            self.out_of_cell_target = vector(14,0)
            if self.next_grid_position_left != vector(-1,-1):
                if self.next_grid_position_left.distance_to(self.out_of_cell_target) < self.min_distance:
                    self.min_distance = self.next_grid_position_left.distance_to(self.out_of_cell_target)
                    self.next_direction.update(self.current_direction.rotate(-90)) 
            if self.next_grid_position_ahead != vector(-1,-1):
                if self.next_grid_position_ahead.distance_to(self.out_of_cell_target) < self.min_distance:
                    self.min_distance = self.next_grid_position_ahead.distance_to(self.out_of_cell_target)
                    self.next_direction.update(self.current_direction)        
            if self.next_grid_position_right != vector(-1,-1):
                if self.next_grid_position_right.distance_to(self.out_of_cell_target) < self.min_distance:
                    self.min_distance = self.next_grid_position_right.distance_to(self.chase_target)
                    self.next_direction.update(self.current_direction.rotate(90))  
        else:          
            if self.mode == 1:
                if self.next_grid_position_left != vector(-1,-1):
                    if self.next_grid_position_left.distance_to(self.chase_target) < self.min_distance:
                        self.min_distance = self.next_grid_position_left.distance_to(self.chase_target)
                        self.next_direction.update(self.current_direction.rotate(-90)) 
                if self.next_grid_position_ahead != vector(-1,-1):
                    if self.next_grid_position_ahead.distance_to(self.chase_target) < self.min_distance:
                        self.min_distance = self.next_grid_position_ahead.distance_to(self.chase_target)
                        self.next_direction.update(self.current_direction)        
                if self.next_grid_position_right != vector(-1,-1):
                    if self.next_grid_position_right.distance_to(self.chase_target) < self.min_distance:
                        self.min_distance = self.next_grid_position_right.distance_to(self.chase_target)
                        self.next_direction.update(self.current_direction.rotate(90))
            if self.mode == 2:
                if self.next_grid_position_left != vector(-1,-1):
                    if self.next_grid_position_left.distance_to(self.scatter_target) < self.min_distance:
                        self.min_distance = self.next_grid_position_left.distance_to(self.scatter_target)
                        self.next_direction.update(self.current_direction.rotate(-90)) 
                if self.next_grid_position_ahead != vector(-1,-1):
                    if self.next_grid_position_ahead.distance_to(self.scatter_target) < self.min_distance:
                        self.min_distance = self.next_grid_position_ahead.distance_to(self.scatter_target)
                        self.next_direction.update(self.current_direction)        
                if self.next_grid_position_right != vector(-1,-1):
                    if self.next_grid_position_right.distance_to(self.scatter_target) < self.min_distance:
                        self.min_distance = self.next_grid_position_right.distance_to(self.scatter_target)
                        self.next_direction.update(self.current_direction.rotate(90)) 
            if self.mode == 3:
                self.random_target = vector(random.randint(0,27),random.randint(3,33))
                if self.next_grid_position_left != vector(-1,-1):
                    if self.next_grid_position_left.distance_to(self.random_target) < self.min_distance:
                        self.min_distance = self.next_grid_position_left.distance_to(self.random_target)
                        self.next_direction.update(self.current_direction.rotate(-90)) 
                if self.next_grid_position_ahead != vector(-1,-1):
                    if self.next_grid_position_ahead.distance_to(self.random_target) < self.min_distance:
                        self.min_distance = self.next_grid_position_ahead.distance_to(self.random_target)
                        self.next_direction.update(self.current_direction)        
                if self.next_grid_position_right != vector(-1,-1):
                    if self.next_grid_position_right.distance_to(self.random_target) < self.min_distance:
                        self.min_distance = self.next_grid_position_right.distance_to(self.random_target)
                        self.next_direction.update(self.current_direction.rotate(90))    
            
                
        return self.next_direction

    def calculate_pixel_position(self):
        return vector(self.grid_position.x*TILE_SIZE[0]+TILE_SIZE[0]//2,self.grid_position.y*TILE_SIZE[1])

    def ghost_reset(self):

        self.grid_position.update(self.grid_start_position.x,self.grid_start_position.y)
        self.pixel_position.update(self.pixel_start_position.x,self.pixel_start_position.y)
        
        self.rect.x = self.pixel_start_position.x
        self.rect.y = self.pixel_start_position.y
        self.next_grid_position.update(-1,-1)
        self.next_grid_position_ahead.update(-1,-1)
        self.next_grid_position_left.update(-1,-1)
        self.next_grid_position_right.update(-1,-1)
        self.move_to_be_made = False

        if self.behaviour == 1:
            self.out_of_cell = True
            self.respawn_timer = 0
            self.enter_play_timer = 0
            self.mode = 2
            self.current_direction.update(1 if random.random() > 0.5 else -1,0)
            self.image = self.images[96]
            self.speed = BLINKY_SPEED

        if self.behaviour == 2:
            self.out_of_cell = False
            self.respawn_timer = 0
            self.enter_play_timer = FPS*PINKY_ENTER_PLAY_SECONDS
            self.mode = 5
            self.current_direction.update(1,0)
            self.image = self.images[128]
            self.speed = PINKY_SPEED

        if self.behaviour == 3:
            self.out_of_cell = False
            self.respawn_timer = 0
            self.enter_play_timer = FPS*INKY_ENTER_PLAY_SECONDS
            self.mode = 5
            self.current_direction.update(-1,0)
            self.image = self.images[136]
            self.speed = INKY_SPEED

        if self.behaviour == 4:
            self.out_of_cell = False
            self.respawn_timer = 0
            self.enter_play_timer = FPS*CLYDE_ENTER_PLAY_SECONDS
            self.mode = 5
            self.current_direction.update(-1,0)
            self.image = self.images[144]
            self.speed = CLYDE_SPEED

        self.next_direction.update(self.current_direction.x,self.current_direction.y)


    def draw(self):
            self.screen.blit(self.image,(self.rect.left-self.rect.width//4,self.rect.top-self.rect.height//4))


    def change_mode(self,mode):
        if self.mode != 4 and self.mode != 5:
            self.mode = mode
            if self.mode == 3:
                self.speed = GHOST_AFRAID_SPEED
                self.afraid_mode_timer = 0
            else:
                if self.behaviour == 1:
                    self.speed = BLINKY_SPEED
                elif self.behaviour == 2:
                    self.speed = PINKY_SPEED
                elif self.behaviour == 3:
                    self.speed = INKY_SPEED
                elif self.behaviour == 4:
                    self.speed = CLYDE_SPEED

    def ghost_killed(self):
        self.mode = 4
        self.current_direction.update(0,-1)
        self.next_direction.update(self.current_direction.x,self.current_direction.y)
        self.grid_position.update(14,17)
        self.pixel_position.update(14*TILE_SIZE[0],17*TILE_SIZE[1])
        
        self.rect.x = self.pixel_position.x
        self.rect.y = self.pixel_position.y
        self.next_grid_position.update(-1,-1)
        self.next_grid_position_ahead.update(-1,-1)
        self.next_grid_position_left.update(-1,-1)
        self.next_grid_position_right.update(-1,-1)
        self.move_to_be_made = False
        if self.behaviour == 1:
            self.speed = BLINKY_SPEED
        elif self.behaviour == 2:
            self.speed = PINKY_SPEED
        elif self.behaviour == 3:
            self.speed = INKY_SPEED
        elif self.behaviour == 4:
            self.speed = CLYDE_SPEED

    def update_ghost_animation(self):

        if self.mode == 3:
            if self.change_feet:
                if self.afraid_mode_timer >= (self.afraid_mode_seconds - 2) * FPS:
                    self.image = self.images[70]
                else:
                    self.image = self.images[72]

                self.image_change_count += 1

                if self.image_change_count >= FPS//6:
                    self.change_feet = False
                    self.image_change_count = 0
            else:
                self.image = self.images[73]

                self.image_change_count += 1

                if self.image_change_count >= FPS//6:
                    self.change_feet = True
                    self.image_change_count = 0
        else:
            if self.behaviour == 1:
                if self.change_feet:
                    if self.current_direction.x < 0:
                        self.image = self.images[100]
                    elif self.current_direction.x > 0: 
                        self.image = self.images[96]
                    elif self.current_direction.y < 0:
                        self.image = self.images[102]
                    elif self.current_direction.y > 0:
                        self.image = self.images[98]
                    self.image_change_count += 1

                    if self.image_change_count >= FPS//6:
                        self.change_feet = False
                        self.image_change_count = 0
                else:
                    if self.current_direction.x < 0:
                        self.image = self.images[101]
                    elif self.current_direction.x > 0: 
                        self.image = self.images[97]
                    elif self.current_direction.y < 0:
                        self.image = self.images[103]
                    elif self.current_direction.y > 0:
                        self.image = self.images[99]
                    self.image_change_count += 1

                    if self.image_change_count >= FPS//6:
                        self.change_feet = True
                        self.image_change_count = 0
            if self.behaviour == 2:
                if self.change_feet:
                    if self.current_direction.x < 0:
                        self.image = self.images[132]
                    elif self.current_direction.x > 0: 
                        self.image = self.images[128]
                    elif self.current_direction.y < 0:
                        self.image = self.images[134]
                    elif self.current_direction.y > 0:
                        self.image = self.images[130]
                    self.image_change_count += 1

                    if self.image_change_count >= FPS//6:
                        self.change_feet = False
                        self.image_change_count = 0
                else:
                    if self.current_direction.x < 0:
                        self.image = self.images[133]
                    elif self.current_direction.x > 0: 
                        self.image = self.images[129]
                    elif self.current_direction.y < 0:
                        self.image = self.images[135]
                    elif self.current_direction.y > 0:
                        self.image = self.images[131]
                    self.image_change_count += 1

                    if self.image_change_count >= FPS//6:
                        self.change_feet = True
                        self.image_change_count = 0
            if self.behaviour == 3:
                if self.change_feet:
                    if self.current_direction.x < 0:
                        self.image = self.images[140]
                    elif self.current_direction.x > 0: 
                        self.image = self.images[136]
                    elif self.current_direction.y < 0:
                        self.image = self.images[142]
                    elif self.current_direction.y > 0:
                        self.image = self.images[138]
                    self.image_change_count += 1

                    if self.image_change_count >= FPS//6:
                        self.change_feet = False
                        self.image_change_count = 0
                else:
                    if self.current_direction.x < 0:
                        self.image = self.images[141]
                    elif self.current_direction.x > 0: 
                        self.image = self.images[137]
                    elif self.current_direction.y < 0:
                        self.image = self.images[143]
                    elif self.current_direction.y > 0:
                        self.image = self.images[139]
                    self.image_change_count += 1

                    if self.image_change_count >= FPS//6:
                        self.change_feet = True
                        self.image_change_count = 0
            if self.behaviour == 4:
                if self.change_feet:
                    if self.current_direction.x < 0:
                        self.image = self.images[148]
                    elif self.current_direction.x > 0: 
                        self.image = self.images[144]
                    elif self.current_direction.y < 0:
                        self.image = self.images[150]
                    elif self.current_direction.y > 0:
                        self.image = self.images[146]
                    self.image_change_count += 1

                    if self.image_change_count >= FPS//6:
                        self.change_feet = False
                        self.image_change_count = 0
                else:
                    if self.current_direction.x < 0:
                        self.image = self.images[149]
                    elif self.current_direction.x > 0: 
                        self.image = self.images[145]
                    elif self.current_direction.y < 0:
                        self.image = self.images[151]
                    elif self.current_direction.y > 0:
                        self.image = self.images[147]
                    self.image_change_count += 1

                    if self.image_change_count >= FPS//6:
                        self.change_feet = True
                        self.image_change_count = 0


    def get_ghost_grid_position(self):
        return self.grid_position
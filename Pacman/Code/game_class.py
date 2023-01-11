import pygame, sys

from Code.SETTINGS import *
from Code.player_class import *
from Code.tictac_class import *
from Code.ghost_class import *

vector = pygame.math.Vector2

pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
pygame.mixer.init()
pygame.font.init()
pygame.mixer.set_num_channels(3)
myfont = pygame.font.Font(FONT,24)


class Pacman:
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("PACMAN")
        self.dim_surface = pygame.Surface(WINDOW_SIZE)
        self.dim_surface.set_alpha(230)
        self.dim_surface.fill(BLACK)

        
        self.level = 1
        self.chase_mode_seconds = CHASE_MODE_SECONDS
        self.scatter_mode_seconds = SCATTER_MODE_SECONDS
        self.afraid_mode_seconds = AFRAID_MODE_SECONDS

        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'menu'
        self.player_ready = False
        self.pause = False
        self.options = False

        
        self.wall_rects = []
        self.ghost_cell_rects = []

        self.special_tictac_blink_counter = 0
        self.special_tictac_on = True

        self.score = 0
        self.highscore = 0
        self.ghost_kill_points = 200


        self.all_sprites = pygame.sprite.Group()
        self.tictac_sprites = pygame.sprite.Group()
        self.special_tictac_sprites = pygame.sprite.Group()
        self.ghost_sprites = pygame.sprite.Group()

        self.sounds = []
        self.change_munch = True

        self.sprite_images = []
        self.load_data()

        self.all_sprites_for_reset = self.all_sprites.copy()
        self.tictac_sprites_for_reset = self.tictac_sprites.copy()
        self.special_tictac_sprites_for_reset = self.special_tictac_sprites.copy()

        self.player = Player(self,PLAYER_STARTING_GRID_POS)
        self.all_sprites.add(self.player)

        self.ghost_mode = 2
        self.ghost_mode_timer = 0

        self.blinky = Ghost(self,1)
        self.ghost_sprites.add(self.blinky)
        self.all_sprites.add(self.blinky)
        self.pinky = Ghost(self,2)
        self.ghost_sprites.add(self.pinky)
        self.all_sprites.add(self.pinky)
        self.inky = Ghost(self,3)
        self.ghost_sprites.add(self.inky)
        self.all_sprites.add(self.inky)
        self.clyde = Ghost(self,4)
        self.ghost_sprites.add(self.clyde)
        self.all_sprites.add(self.clyde)

    def run(self):
        while self.running:
            if self.state == 'menu':
                self.menu_events()
                self.menu_update()
                self.menu_draw() 
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game_over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()  
            else:
                self.running = False
                
            self.clock.tick(FPS)
        if self.score == self.highscore:
            with open('Data\high_score.txt','w') as file:
                file.write(str(self.score))

        pygame.quit()
        sys.exit()

#------------------------------------------------------------- helping functions ----------------------------------------------------

    def load_data(self):
        self.menu = pygame.image.load("Images\menu.png")
        self.menu = pygame.transform.scale(self.menu,WINDOW_SIZE)
        self.maze = pygame.image.load("Images\GameBoardSheet.png")
        self.maze = pygame.transform.scale(self.maze,MAZE_SIZE)
        self.sprite_sheet_image = pygame.image.load('Images\SpriteSheet.png').convert_alpha()

        for y in range(0,self.sprite_sheet_image.get_height(),24):
            for x in range(0,self.sprite_sheet_image.get_width(),24):
                self.sprite_images.append(pygame.transform.scale(self.sprite_sheet_image.subsurface(x,y,24,24),(TILE_SIZE[0]*1.5,TILE_SIZE[1]*1.5)))

        with open('Data\walls.txt','r') as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    if char == "W":
                        self.wall_rects.append(pygame.Rect(x_index*TILE_SIZE[0],y_index*TILE_SIZE[1]+UI_TOP,TILE_SIZE[0],TILE_SIZE[1]))
                    elif char == "G":
                        self.ghost_cell_rects.append(pygame.Rect(x_index*TILE_SIZE[0],y_index*TILE_SIZE[1]+UI_TOP,TILE_SIZE[0],TILE_SIZE[1]))
                    elif char == "T":
                        self.tictac = Tictac(self,(x_index*TILE_SIZE[0]+TILE_SIZE[0]//4,y_index*TILE_SIZE[1]+UI_TOP+TILE_SIZE[1]//4,TILE_SIZE[0]//2),(TILE_SIZE[0]//2,TILE_SIZE[1]//2))
                        self.tictac_sprites.add(self.tictac)
                        self.all_sprites.add(self.tictac)
                    elif char == "S":
                        self.special_tictac = Tictac(self,(x_index*TILE_SIZE[0]+TILE_SIZE[0]//4,y_index*TILE_SIZE[1]+UI_TOP+TILE_SIZE[1]//4,TILE_SIZE[0]//2),(TILE_SIZE[0]//2,TILE_SIZE[1]//2),True)
                        self.special_tictac_sprites.add(self.special_tictac)
                        self.all_sprites.add(self.special_tictac)
        with open('Data\high_score.txt','r') as file:
            self.highscore = int(file.read())

        self.sounds.append(pygame.mixer.Sound("Music\game_start.wav"))
        self.sounds.append(pygame.mixer.Sound("Music\intermission.wav"))
        self.sounds.append(pygame.mixer.Sound("Music\munch_1.wav"))
        self.sounds.append(pygame.mixer.Sound("Music\munch_2.wav"))
        self.sounds.append(pygame.mixer.Sound("Music\death_1.wav"))
        self.sounds.append(pygame.mixer.Sound("Music\death_2.wav"))
        self.sounds.append(pygame.mixer.Sound("Music\power_pellet.wav"))
        self.sounds.append(pygame.mixer.Sound("Music\eat_ghost.wav"))

    def pacman_collide_with_tictac(self):
        self.tictac_hitlist = pygame.sprite.spritecollide(self.player,self.tictac_sprites,False)
        self.special_tictac_hitlist = pygame.sprite.spritecollide(self.player,self.special_tictac_sprites,False)

        for tictac in self.tictac_hitlist:
            self.score += 10
            self.tictac_sprites.remove(tictac)
            self.all_sprites.remove(tictac)

            if self.change_munch:
                self.sounds[2].play()
                self.change_munch = False
            else:
                self.sounds[3].play()
                self.change_munch = True

        for tictac in self.special_tictac_hitlist:
            self.score += 50
            self.special_tictac_sprites.remove(tictac)
            self.all_sprites.remove(tictac)
            self.ghost_mode = 3
            self.blinky.change_mode(self.ghost_mode)
            self.pinky.change_mode(self.ghost_mode)
            self.inky.change_mode(self.ghost_mode)
            self.clyde.change_mode(self.ghost_mode)
            self.ghost_mode_timer = 0
            self.sounds[6].play()

    def pacman_collide_with_ghost(self):
        self.ghost_hitlist = pygame.sprite.spritecollide(self.player,self.ghost_sprites,False)

        
        for ghost in self.ghost_hitlist:
            if ghost.mode == 3:
                self.sounds[7].play()    
                if ghost == self.blinky:
                    self.blinky.ghost_killed()
                if ghost == self.pinky:
                    self.pinky.ghost_killed()
                if ghost == self.inky:
                    self.inky.ghost_killed() 
                if ghost == self.clyde:
                    self.clyde.ghost_killed()
                                                        
                self.score += self.ghost_kill_points
                self.ghost_kill_points *= 2
            else:
                self.player.player_lives -= 1
                if self.player.player_lives > 0:
                    self.sounds[5].play()
                    self.reset_board()      
                else:
                    self.sounds[4].play()  
 
    def reset_board(self):
        self.player_ready = False
        self.player.player_reset()
        self.blinky.ghost_reset()
        self.pinky.ghost_reset()
        self.inky.ghost_reset()
        self.clyde.ghost_reset()

        self.ghost_mode = 2
        self.ghost_mode_timer = 0
        if(len(self.tictac_sprites) == 0 and len(self.special_tictac_sprites) == 0):
            self.all_sprites = self.all_sprites_for_reset.copy()
            self.tictac_sprites = self.tictac_sprites_for_reset.copy()
            self.special_tictac_sprites = self.special_tictac_sprites_for_reset.copy()

            self.afraid_mode_seconds = 0.5 if self.afraid_mode_seconds - MODE_SECONDS_REDUCTION_PER_LEVEL <= 0 else self.afraid_mode_seconds - MODE_SECONDS_REDUCTION_PER_LEVEL
            self.scatter_mode_seconds = 0.5 if self.scatter_mode_seconds - MODE_SECONDS_REDUCTION_PER_LEVEL <= 0 else self.scatter_mode_seconds - MODE_SECONDS_REDUCTION_PER_LEVEL
            self.blinky.afraid_mode_seconds = 0.5 if self.blinky.afraid_mode_seconds - MODE_SECONDS_REDUCTION_PER_LEVEL <= 0 else self.blinky.afraid_mode_seconds - MODE_SECONDS_REDUCTION_PER_LEVEL
            self.pinky.afraid_mode_seconds = 0.5 if self.pinky.afraid_mode_seconds - MODE_SECONDS_REDUCTION_PER_LEVEL <= 0 else self.pinky.afraid_mode_seconds - MODE_SECONDS_REDUCTION_PER_LEVEL
            self.inky.afraid_mode_seconds = 0.5 if self.inky.afraid_mode_seconds - MODE_SECONDS_REDUCTION_PER_LEVEL <= 0 else self.inky.afraid_mode_seconds - MODE_SECONDS_REDUCTION_PER_LEVEL
            self.clyde.afraid_mode_seconds = 0.5 if self.clyde.afraid_mode_seconds - MODE_SECONDS_REDUCTION_PER_LEVEL <= 0 else self.clyde.afraid_mode_seconds - MODE_SECONDS_REDUCTION_PER_LEVEL

            self.level += 1

            self.sounds[1].play()

    def draw_tictacs(self):
        self.tictac_sprites.draw(self.screen)
        if self.special_tictac_on:
            self.special_tictac_sprites.draw(self.screen)
            
        self.special_tictac_blink_counter +=1

        if self.special_tictac_blink_counter >= FPS//2:
            if self.special_tictac_on:
                self.special_tictac_on = False
            else:
                self.special_tictac_on = True
            self.special_tictac_blink_counter = 0

    def ghost_change_mode(self):

        if self.ghost_mode == 1 and self.ghost_mode_timer >= FPS * self.chase_mode_seconds:
            self.ghost_mode = 2
            self.blinky.change_mode(self.ghost_mode)
            self.pinky.change_mode(self.ghost_mode)
            self.inky.change_mode(self.ghost_mode)
            self.clyde.change_mode(self.ghost_mode)
            self.ghost_mode_timer = 0
        if self.ghost_mode == 2 and self.ghost_mode_timer >= FPS * self.scatter_mode_seconds:
            self.ghost_mode = 1
            self.blinky.change_mode(self.ghost_mode)
            self.pinky.change_mode(self.ghost_mode)
            self.inky.change_mode(self.ghost_mode)
            self.clyde.change_mode(self.ghost_mode)
            self.ghost_mode_timer = 0   
        if self.ghost_mode == 3 and self.ghost_mode_timer >= FPS * self.afraid_mode_seconds:         
            self.ghost_mode = 2
            self.ghost_kill_points = 200
            self.blinky.change_mode(self.ghost_mode)
            self.pinky.change_mode(self.ghost_mode)
            self.inky.change_mode(self.ghost_mode)
            self.clyde.change_mode(self.ghost_mode)
            self.ghost_mode_timer = 0

#----------------------------------------------------------------- debugging functions ----------------------------------------------------
    def draw_grid(self):
        for x in range(WINDOW_SIZE[0]//TILE_SIZE[0]):
            pygame.draw.line(self.screen, RED,(x*TILE_SIZE[0],0),(x*TILE_SIZE[0],WINDOW_SIZE[1]))
        for y in range(WINDOW_SIZE[1]//TILE_SIZE[1]):
            pygame.draw.line(self.screen, RED,(0,y*TILE_SIZE[1]),(WINDOW_SIZE[0],y*TILE_SIZE[1]))
    
    def draw_wall_rects(self):
        for x in self.wall_rects:
            pygame.draw.rect(self.screen,GREEN,x)
    
    def draw_ghost_cell_rects(self):
        for x in self.ghost_cell_rects:
            pygame.draw.rect(self.screen,GREY,x)

#-------------------------------------------------------------- menu functions -----------------------------------------------------
    def menu_events(self):   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 'playing'
                    self.sounds[0].play()
                if event.key == pygame.K_ESCAPE:
                    self.options = not self.options
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 6:
                    self.options = not self.options
                if event.button == 7:
                    self.state = 'playing'
                    self.sounds[0].play()
            


    def menu_update(self):
        pass

    def menu_draw(self):
        self.screen.blit(self.menu,(0,0))

        text = myfont.render('PRESS THE ESC KEY',False,WHITE)
        self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*28.5-text.get_size()[1]//2))
        text = myfont.render('OR THE SELECT BUTTON FOR CONTROLS',False,WHITE)
        self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*30.5-text.get_size()[1]//2))
        text = myfont.render('PRESS SPACE',False,WHITE)
        self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*32.5-text.get_size()[1]//2))
        text = myfont.render('OR THE START BUTTON TO PLAY',False,WHITE)
        self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*34.5-text.get_size()[1]//2))

        if self.options:
            self.screen.blit(self.dim_surface,(0,0))
            text = myfont.render('KEYBOARD CONTROLS',False,WHITE)
            self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*6-text.get_size()[1]//2))
            text = myfont.render('PRESS THE ARROW KEYS',False,WHITE)
            self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*8.5-text.get_size()[1]//2))
            text = myfont.render('OR THE WASD KEYS TO MOVE PACMAN',False,WHITE)
            self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*10.5-text.get_size()[1]//2))
            text = myfont.render('PRESS THE ESC KEY TO PAUSE',False,WHITE)
            self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*12.5-text.get_size()[1]//2))
            text = myfont.render('GAMEPAD CONTROLS',False,WHITE)
            self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*16-text.get_size()[1]//2))
            text = myfont.render('PRESS THE D-PAD BUTTONS',False,WHITE)
            self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*18.5-text.get_size()[1]//2))
            text = myfont.render('OR THE LEFT ANALOG STICK',False,WHITE)
            self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*20.5-text.get_size()[1]//2))
            text = myfont.render('TO MOVE PACMAN',False,WHITE)
            self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*22.5-text.get_size()[1]//2))
            text = myfont.render('PRESS THE START BUTTON TO PAUSE',False,WHITE)
            self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*24.5-text.get_size()[1]//2))


        pygame.display.update()
    
#-------------------------------------------------------------- playing functions -----------------------------------------------------
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if not self.pause:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.move(vector(-1,0))
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.move(vector(1,0))
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.move(vector(0,-1))
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.move(vector(0,1))
                if event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
                


            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    self.pause = not self.pause
            if event.type == pygame.JOYHATMOTION:
                if not self.pause:
                    if event.value != (0,0):
                        self.player.move(vector(event.value[0],event.value[1]*-1))
            if event.type == pygame.JOYAXISMOTION:
                if not self.pause:
                    if event.joy == 0:
                        for i in range(0,len(joysticks)):
                            if joysticks[i].get_axis(0) < -0.98 and abs(joysticks[i].get_axis(0)) >= abs(joysticks[i].get_axis(1)):
                                self.player.move(vector(-1,0))
                            if joysticks[i].get_axis(0) > 0.98 and abs(joysticks[i].get_axis(0)) >= abs(joysticks[i].get_axis(1)):
                                self.player.move(vector(1,0))
                            if joysticks[i].get_axis(1) < -0.98 and abs(joysticks[i].get_axis(0)) < abs(joysticks[i].get_axis(1)):
                                self.player.move(vector(0,-1))
                            if joysticks[i].get_axis(1) > 0.98 and abs(joysticks[i].get_axis(0)) < abs(joysticks[i].get_axis(1)):
                                self.player.move(vector(0,1))                      
                            


    def playing_update(self):


        if not self.pause:
            if self.player.player_lives == 0:
                self.state = 'game_over'

            self.player.update()

            if self.player_ready:
                self.blinky.update(self.player.get_player_grid_position())
                self.pinky.update(self.player.get_player_grid_position(),self.player.get_player_direction())
                self.inky.update(self.player.get_player_grid_position(),self.player.get_player_direction(),self.blinky.get_ghost_grid_position())
                self.clyde.update(self.player.get_player_grid_position())           
                self.ghost_mode_timer += 1

            if self.player.given_direction != vector(0,0):
                self.player_ready = True
                
            self.pacman_collide_with_tictac()
            if self.score > self.highscore:
                self.highscore = self.score

            if len(self.special_tictac_sprites) == 0 and len(self.tictac_sprites) == 0 :
                self.reset_board()

            self.ghost_change_mode()
                
            self.pacman_collide_with_ghost()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.maze,(0,UI_TOP))


        self.draw_tictacs()

        self.player.draw()

        self.blinky.draw()
        self.pinky.draw()
        self.inky.draw()
        self.clyde.draw()

        if not self.player_ready and self.player.player_lives > 0:
            self.screen.blit(myfont.render('READY!',False,WHITE),(TILE_SIZE[0]*12,-TILE_SIZE[1]//4+TILE_SIZE[1]*20))

        for lives in range(0,self.player.player_lives):
            self.screen.blit(self.sprite_images[48],(TILE_SIZE[0]*2 + TILE_SIZE[0]*(lives*2),TILE_SIZE[1]*34+TILE_SIZE[1]//4))

        self.screen.blit(myfont.render('SCORE:' + str(self.score),False,WHITE),(TILE_SIZE[0]*5,5))
        self.screen.blit(myfont.render('HIGH SCORE:' + str(self.highscore),False,WHITE),(TILE_SIZE[0]*5,TILE_SIZE[1]*1+5))
        self.screen.blit(myfont.render('LEVEL ' + str(self.level),False,WHITE),(TILE_SIZE[0]*14,TILE_SIZE[1]*34+5))
        
        self.player.draw()
        
        if self.pause:
            self.screen.blit(self.dim_surface,(0,0))
            text = myfont.render('PAUSE',False,WHITE)
            self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*9-text.get_size()[1]//2))
            text = myfont.render('PRESS THE ESC KEY',False,WHITE)
            self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*11-text.get_size()[1]//2))
            text = myfont.render('OR THE SELECT BUTTON TO CONTINUE',False,WHITE)
            self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*13-text.get_size()[1]//2))

        pygame.display.update()

#-------------------------------------------------------------- game_over functions -----------------------------------------------------
    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.running = False
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    self.running = False

    def game_over_update(self):
        self.player.update()

    def game_over_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.maze,(0,UI_TOP))

        self.draw_tictacs()

        self.blinky.draw()
        self.pinky.draw()
        self.inky.draw()
        self.clyde.draw()
        
        self.screen.blit(myfont.render('SCORE:' + str(self.score),False,WHITE),(TILE_SIZE[0]*5,5))
        self.screen.blit(myfont.render('HIGH SCORE:' + str(self.highscore),False,WHITE),(TILE_SIZE[0]*5,TILE_SIZE[1]+5))

        self.player.draw()

        if self.player.death_image > 127:
            self.screen.blit(self.dim_surface,(0,0))
            if self.highscore == self.score:
                text = myfont.render('CONGRATULATIONS',False,WHITE)
                self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*8-text.get_size()[1]//2))
                text = myfont.render('YOU ACHIEVED A NEW HIGH SCORE',False,WHITE)
                self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*10-text.get_size()[1]//2))
                text = myfont.render('SCORE:' + str(self.score),False,WHITE)
                self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*12-text.get_size()[1]//2))
                text = myfont.render('PRESS SPACE',False,WHITE)
                self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*14-text.get_size()[1]//2))
                text = myfont.render('OR THE START BUTTON TO EXIT',False,WHITE)
                self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*16-text.get_size()[1]//2))
            else:
                text = myfont.render('BETTER LUCK NEXT TIME',False,WHITE)
                self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*8-text.get_size()[1]//2))
                text = myfont.render('HIGH SCORE:' + str(self.highscore),False,WHITE)
                self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*10-text.get_size()[1]//2))
                text = myfont.render('YOUR SCORE:' + str(self.score),False,WHITE)
                self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*12-text.get_size()[1]//2))
                text = myfont.render('PRESS SPACE',False,WHITE)
                self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*14-text.get_size()[1]//2))
                text = myfont.render('OR THE START BUTTON TO EXIT',False,WHITE)
                self.screen.blit(text,(WINDOW_SIZE[0]//2-text.get_size()[0]//2,TILE_SIZE[1]*16-text.get_size()[1]//2))

        pygame.display.update()
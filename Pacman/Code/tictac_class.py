from Code.SETTINGS import *
import pygame

class Tictac(pygame.sprite.Sprite):
    def __init__(self,pacman,position,size,special_tictac = False):
        super().__init__()
        self.position = position
        
        if special_tictac:
            self.rect = pygame.Rect(position[0]-1,position[1]-1,size[0],size[1]) 
            self.image = pacman.sprite_images[10].subsurface(1,1,TILE_SIZE[0]*1.5//2-1,TILE_SIZE[1]*1.5//2-1)
        else:
            self.rect = pygame.Rect(position[0]-2,position[1]-2,size[0],size[1]) 
            self.image = pacman.sprite_images[8].subsurface(0,0,TILE_SIZE[0]*1.5//2,TILE_SIZE[1]*1.5//2)
        
        
        
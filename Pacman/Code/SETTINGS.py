import pygame

vector = pygame.math.Vector2

#------------------------------ WINDOW SETTINGS ------------------------------
TILE_SIZE = (20,20) # Size of each tile
MAZE_SIZE = (TILE_SIZE[0]*28,TILE_SIZE[1]*31) # Size of maze in terms of tiles

UI_TOP = TILE_SIZE[1]*3 # Top ui buffer in terms of tiles
UI_BOTTOM = TILE_SIZE[1]*2 # Bottom ui buffer in terms of tiles

WINDOW_SIZE = (TILE_SIZE[0]*28,TILE_SIZE[1]*36) # Window size in terms of tiles

FPS = 150 # Frames per second that the game logic runs to, which means the gameplay speed is depended on the FPS value. FPS = 150 gives a quite normal gameplay speed

#------------------------------ COLOUR SETTINGS ------------------------------
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (120,120,120)
YELLOW = (255, 247, 0)
PINK = (255, 0, 195)

FONT = 'Font\Pixeloid.ttf'

#------------------------------ PPLAYER SETTINGS ------------------------------
PLAYER_SPEED = 1 # Max value = 1. If its more than 1 the games collision breaks
PLAYER_STARTING_GRID_POS = vector(13,26) # It should be inside the maze


#------------------------------ DIFFICULTY SETTINGS ------------------------------
BLINKY_SPEED = 0.85 # The speed of the red ghost (MAX = 1)
PINKY_SPEED = 0.8 # The speed of the pink ghost (MAX = 1)
INKY_SPEED = 0.7 # The speed of the blue ghost (MAX = 1)
CLYDE_SPEED = 0.6 # The speed of the orange ghost (MAX = 1)

PINKY_ENTER_PLAY_SECONDS = 4 # How many seconds does it take for pinky to enter play when the game starts or when the board resets
INKY_ENTER_PLAY_SECONDS = 8 # How many seconds does it take for inky to enter play when the game starts or when the board resets
CLYDE_ENTER_PLAY_SECONDS = 12 # How many seconds does it take for clyde to enter play when the game starts or when the board resets

GHOST_RESPAWN_SECONDS = 5 # How many seconds does it take for a ghost to enter play again afer being killed

GHOST_AFRAID_SPEED = 0.5 # The speed of ghosts when they are afraid (MAX = 1)

CHASE_MODE_SECONDS = 20 # How many seconds will the ghosts chase the player actively before changing their mode (it should always be more than 0)
SCATTER_MODE_SECONDS = 7 # How many seconds will the ghosts scatter to their respective corners before changing their mode (it should always be more than 0)
AFRAID_MODE_SECONDS = 6 # How many seconds will the ghosts be vulnerable when the player eats a special tic-tac (it should always be more than 0)

MODE_SECONDS_REDUCTION_PER_LEVEL = 0.5 # How much will the SCATTER_MODE_SECONDS and AFRAID_MODE_SECONDS be reduced for clearing every level

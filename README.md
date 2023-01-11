# Pac-Man

A recreation of the classic arcade video game Pac-Man, made in Python using the pygame library. <br>
To start the game just run **main.py** from your code editor.

# Install Dependencies

```
pip install pygame
```

# List of files

### Code

- **game_class.py**: This class is responsible for the game logic, loading and initializing the required data, registering the players inputs and keeping track of the game state.
- **ghost_class.py**: This class represents a ghost. It keeps track of the behaviour, position, speed and target of the ghost as well. It also calculates the appropriate ghost sprite to draw for every given frame.
- **player_class.py**: This class represents the player. It keeps track of the collider, position, speed and remaining lives of the player. It also receives the players inputs to move thr player character accordingly and calculates the appropriate ghost sprite to draw for every given frame. 
- **tictac_class.py**: This is a simple class that represents the pellets that Pac-Man eats.
- **SETTINGS.py**: This file gives us easy access to modify some of the games variables such as FPS and difficulty settings (ghost speed, ghost behaviour etc).

### Data

- **high_score.txt**: Here we save the high score.
- **walls.txt**: This is the map of the maze. Each character represents an element of the maze (W = wall, T = tictac, S = special tictac, E = empty, G = ghost cell) and its place represents the tile that it occupies.   

### Font

- **Pixeloid.ttf**: A pixelated font that matches aesthetically with the arcade nature of the game.

### Images

- **GameBoardSheet.png**: The graphic of the maze.
- **menu.png**: The Background image for the menu.
- **SpriteSheet.png**: The sprite sheet that includes every sprite for every element of the game.

### Music

- **death_1.wav**: This sound plays when you lose your last life.
- **death_2.wav**: This sound plays when you lose a life thats not your last one.
- **eat_ghost.wav**: This sound plays when you eat a ghost.
- **game_start.wav**: This sound plays when you start the game.
- **intermission.wav**: This sound plays when you beat a level.
- **munch_1.wav**: This sound plays interchangably with munch_2.wav whenever you eat a tictac.
- **munch_2.wav**: See munch_1.wav.
- **power_pellet.wav**: This sound plays when you eat a special tictac.

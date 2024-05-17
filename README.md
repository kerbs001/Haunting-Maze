# HauntingMaze

HauntingMaze is a 2D maze game built using Pygame. The objective of the game is to collect 10 coins scattered throughout the maze and reach the door to win. However, a monster hunts the player, and a fog of war mechanic adds to the challenge by limiting visibility.

## Features

- **Character Movement**: Control the player character using the WASD keys.
- **Monster**: A monster actively hunts the player throughout the maze.
- **Coins**: Collect all 10 coins to unlock the door.
- **Fog of War**: Limited visibility adds to the challenge.
- **Collision Detection**: Avoid walls and navigate through the maze.
- **Win Condition**: Reach the door with all coins collected to win the game.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/hauntingmaze.git
    cd hauntingmaze
    ```

2. **Install dependencies**:
    ```bash
    pip install pygame
    ```

## Usage

Run the game:
```bash
python main.py
```

## Controls
- **Move Left**: Press 'A'
- **Move Right**: Press 'D'
- **Move Up**: Press 'W'
- **Move Down**: Press 'S'

## How to Play
- Navigate through the maze under fog of war using the movement keys.
- Collect all 10 coins scattered all throughout the maze.
- Avoid the monster that actively hunts you.
- Once all coins are collected, reach the door to win the game.

## Code Overview

### Main Class

```python
class HauntingMaze:
    def __init__(self):
        # Initialization
    def load_images(self):
        # Load and scale images
    def main_loop(self):
        # Main game loop
    def new_game(self):
        # Initialize game state
    def check_events(self):
        # Handle user inputs
    def update_position(self):
        # Update character positions
    def check_collision(self, x, y, image):
        # Check for collisions
    def get_hitbox(self, x, y, image):
        # Get sprite hitbox
    def game_over(self):
        # Handle game over conditions
    def success_screen(self):
        # Display success screen
    def fog_of_war(self):
        # Implement fog of war
    def draw_window(self):
        # Render game screen
```



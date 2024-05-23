import pygame
import random

# Maze and Coin Generation Functions
def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]  # 1 represents wall, 0 represents path
    start_x, start_y = 0, 0
    stack = [(start_x, start_y)]
    maze[start_y][start_x] = 0
    
    while stack:
        x, y = stack[-1]
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        
        moved = False
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy][x + dx] = 0
                stack.append((nx, ny))
                moved = True
                break
        
        if not moved:
            stack.pop()
    
    return maze

def place_coins(maze, num_coins):
    width = len(maze[0])
    height = len(maze)
    coins = []
    
    while len(coins) < num_coins:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if maze[y][x] == 0:  # Place coin only on a path
            coins.append((x, y))
    
    return coins

def create_pygame_rects(maze, pixel_size):
    walls = []
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:  # Wall
                walls.append(pygame.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size))
    return walls

def create_coin_rects(coins, pixel_size):
    return [pygame.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size) for x, y in coins]

# Initialize Pygame
pygame.init()
pixel_size = 16
window_size = (1024, 512)
screen = pygame.display.set_mode(window_size)

# Generate Maze and Coins
maze = generate_maze(64, 32)
coins = place_coins(maze, 10)
walls = create_pygame_rects(maze, pixel_size)
coin_rects = create_coin_rects(coins, pixel_size)

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))  # Clear screen
    
    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall)
    
    # Draw coins
    for coin in coin_rects:
        pygame.draw.rect(screen, (255, 215, 0), coin)
    
    pygame.display.flip()
    
pygame.quit()
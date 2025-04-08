# Import necessary libraries
import pygame
import sys
import random
import math
import time # Using time module alongside pygame.time for potential slight variations

# --- Constants and Configuration ---

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20  # Size of each grid cell (and snake segment)
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors (Cyberpunk Palette - Vibrant Neons)
# Using lists to allow easy cycling/selection
COLOR_BLACK = (0, 0, 0)
COLOR_GRID = (20, 20, 40) # Dark blue/purple grid
NEON_PALETTE = [
    (0, 255, 255),  # Cyan
    (255, 0, 255),  # Magenta
    (57, 255, 20),   # Neon Green
    (255, 255, 0),  # Yellow
    (255, 105, 180), # Hot Pink
    (0, 191, 255)   # Deep Sky Blue
]

# Game speed
INITIAL_FPS = 10
FPS_INCREASE_RATE = 0.1 # How much FPS increases per food item eaten

# Snake initial properties
SNAKE_START_POS = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
SNAKE_START_DIRECTION = (1, 0)  # Start moving right

# --- Pygame Initialization ---
pygame.init()
pygame.font.init() # Initialize font module

# Set up the display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Psychedelic Cyberpunk Snake')

# Clock for controlling FPS
clock = pygame.time.Clock()

# Font for score/messages
FONT_SCORE = pygame.font.SysFont('Consolas', 25, bold=True) # Monospaced font often fits cyberpunk
FONT_GAME_OVER = pygame.font.SysFont('Consolas', 50, bold=True)
FONT_RESTART = pygame.font.SysFont('Consolas', 30)

# --- Helper Functions ---

def get_dynamic_color(palette, speed_factor=500):
    """Gets a color from the palette that cycles over time."""
    # Use milliseconds for smooth cycling
    tick = pygame.time.get_ticks()
    # speed_factor controls how fast colors change (lower is faster)
    index = int(tick / speed_factor) % len(palette)
    return palette[index]

def get_pulsing_color(base_color, speed_factor=1.0, min_bright=0.5, max_bright=1.0):
    """Makes a base color pulse in brightness."""
    tick = pygame.time.get_ticks()
    # Use sine wave for smooth pulsing: sin range is -1 to 1, map to min_bright to max_bright
    brightness = (math.sin(tick * speed_factor / 1000.0) + 1) / 2 # Range 0 to 1
    brightness = min_bright + brightness * (max_bright - min_bright) # Map to desired range
    
    # Ensure brightness stays within valid color range [0, 255]
    pulsing_col = tuple(max(0, min(255, int(c * brightness))) for c in base_color)
    return pulsing_col

def draw_grid(surface):
    """Draws a subtle grid on the surface."""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))

def draw_snake(surface, snake_segments, base_color):
    """Draws the snake with pulsing colors."""
    # Head is slightly different
    head_color = get_pulsing_color(base_color, speed_factor=1.5, min_bright=0.7)
    head_rect = pygame.Rect(
        snake_segments[0][0] * GRID_SIZE,
        snake_segments[0][1] * GRID_SIZE,
        GRID_SIZE,
        GRID_SIZE
    )
    pygame.draw.rect(surface, head_color, head_rect)
    # Add a smaller inner rect for effect
    inner_head_rect = head_rect.inflate(-GRID_SIZE * 0.4, -GRID_SIZE * 0.4)
    pygame.draw.rect(surface, COLOR_BLACK, inner_head_rect)


    # Body segments pulse slightly differently
    for i, segment in enumerate(snake_segments[1:]):
        segment_color = get_pulsing_color(base_color, speed_factor=0.8 + i*0.05, min_bright=0.5) # Vary pulse slightly
        segment_rect = pygame.Rect(
            segment[0] * GRID_SIZE,
            segment[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(surface, segment_color, segment_rect)
        # Simple inner rect for contrast
        inner_seg_rect = segment_rect.inflate(-GRID_SIZE * 0.2, -GRID_SIZE * 0.2)
        pygame.draw.rect(surface, COLOR_BLACK, inner_seg_rect, 1) # Outline

def draw_food(surface, food_pos, color):
    """Draws the food item."""
    food_rect = pygame.Rect(
        food_pos[0] * GRID_SIZE,
        food_pos[1] * GRID_SIZE,
        GRID_SIZE,
        GRID_SIZE
    )
    # Draw as a circle within the grid square
    center_x = food_rect.left + GRID_SIZE // 2
    center_y = food_rect.top + GRID_SIZE // 2
    radius = GRID_SIZE // 2
    
    pygame.draw.circle(surface, color, (center_x, center_y), radius)
    # Add a smaller pulsating inner circle
    inner_radius = int(radius * (0.6 + 0.2 * math.sin(pygame.time.get_ticks() / 200.0)))
    inner_color = tuple(max(0, min(255, c + 50)) for c in color) # Slightly brighter inner
    pygame.draw.circle(surface, inner_color, (center_x, center_y), inner_radius)


def place_food(snake_segments):
    """Generates a random position for the food, ensuring it's not on the snake."""
    while True:
        food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        # Check if the generated position overlaps with any snake segment
        if food_pos not in snake_segments:
            return food_pos

def display_score(surface, score):
    """Renders the current score."""
    score_text = f"SCORE: {score}"
    text_surface = FONT_SCORE.render(score_text, True, NEON_PALETTE[1]) # Use Magenta for score
    text_rect = text_surface.get_rect(topleft=(10, 10))
    # Add a subtle background for readability
    bg_rect = text_rect.inflate(10, 5)
    bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA) # Use SRCALPHA for transparency
    bg_surface.fill((0, 0, 20, 180)) # Dark semi-transparent background
    surface.blit(bg_surface, bg_rect)
    surface.blit(text_surface, text_rect)

def game_over_screen(surface, score):
    """Displays the Game Over message and waits for input."""
    # Overlay effect
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200)) # Dark semi-transparent overlay
    surface.blit(overlay, (0, 0))

    # Game Over Text
    game_over_text = FONT_GAME_OVER.render("GAME OVER", True, NEON_PALETTE[0]) # Cyan
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    surface.blit(game_over_text, game_over_rect)

    # Final Score Text
    final_score_text = FONT_SCORE.render(f"FINAL SCORE: {score}", True, NEON_PALETTE[3]) # Yellow
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    surface.blit(final_score_text, final_score_rect)

    # Restart Text
    restart_text = FONT_RESTART.render("Press [R] to Restart or [Q] to Quit", True, NEON_PALETTE[2]) # Neon Green
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
    surface.blit(restart_text, restart_rect)

    pygame.display.flip() # Update the screen to show the message

    # Wait for player input (R or Q)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    waiting = False # Exit the wait loop to restart


# --- Main Game Loop ---

def game_loop():
    """The main function running the game."""
    
    # Game variables initialization
    snake_segments = list(SNAKE_START_POS) # Use list() to create a copy
    snake_direction = SNAKE_START_DIRECTION
    change_to = snake_direction # Buffer for direction change
    
    food_pos = place_food(snake_segments)
    score = 0
    current_fps = INITIAL_FPS
    
    game_over = False

    while not game_over:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle key presses for direction changes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    # Prevent immediate reversal
                    if snake_direction != (0, 1): 
                        change_to = (0, -1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if snake_direction != (0, -1):
                        change_to = (0, 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if snake_direction != (1, 0):
                        change_to = (-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if snake_direction != (-1, 0):
                        change_to = (1, 0)
                # Allow quitting mid-game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        
        # Update snake direction based on buffered input
        snake_direction = change_to

        # --- Game Logic Update ---
        # Move the snake: Calculate new head position
        current_head = snake_segments[0]
        new_head = (current_head[0] + snake_direction[0], current_head[1] + snake_direction[1])

        # Insert the new head at the beginning of the list
        snake_segments.insert(0, new_head)

        # Check for collision with food
        if new_head == food_pos:
            score += 1
            current_fps += FPS_INCREASE_RATE # Increase speed slightly
            food_pos = place_food(snake_segments) # Place new food
            # Don't remove the tail segment - snake grows
        else:
            # Remove the last segment of the snake if no food was eaten
            snake_segments.pop()

        # Check for collisions (Game Over conditions)
        # 1. Collision with screen boundaries
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            game_over = True

        # 2. Collision with itself (check if new_head exists in the rest of the body)
        if new_head in snake_segments[1:]:
            game_over = True

        # --- Drawing ---
        # Fill background (could also make this dynamic/pulsing)
        screen.fill(COLOR_BLACK)

        # Draw the grid
        draw_grid(screen)

        # Draw the food (color cycles through the palette)
        food_color = get_dynamic_color(NEON_PALETTE, speed_factor=300)
        draw_food(screen, food_pos, food_color)

        # Draw the snake (base color cycles, segments pulse)
        snake_base_color = get_dynamic_color(NEON_PALETTE, speed_factor=1000) # Slower cycle for base
        draw_snake(screen, snake_segments, snake_base_color)

        # Draw the score
        display_score(screen, score)

        # --- Update Display & Control Speed ---
        pygame.display.flip() # Update the full screen
        clock.tick(current_fps) # Control the frame rate

    # --- Game Over State ---
    # When the loop breaks (game_over is True)
    game_over_screen(screen, score)
    # The game_over_screen function handles waiting for restart/quit input

# --- Start the Game ---
while True: # Loop to allow restarting
    game_loop() 
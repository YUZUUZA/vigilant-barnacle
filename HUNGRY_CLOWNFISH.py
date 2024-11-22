import pygame
from pygame import mixer
import sys
import random
import time


# Initialize Pygame
pygame.init()
mixer.init()

# Load background music and sound effects
mixer.music.load("bkmusic.mp3")  # Background music
eat_sound = mixer.Sound("eat.wav")  # Sound for eating balls
eat_bad_sound = mixer.Sound("eatbad.wav")  # Sound for hitting a bomb

mixer.music.set_volume(0.5)  # Set background music volume (0.0 to 1.0)
mixer.music.play(-1)  # Play background music in an infinite loop

last_ball_spawn_time = pygame.time.get_ticks()  # Initialize the last ball spawn time

gball_image = pygame.image.load('gball.png')  # Load the new gball image
gball_image = pygame.transform.scale(gball_image, (40, 40))  # Resize the image to a fixed size (e.g., 40x40 pixels)

aball_image = pygame.image.load('aball.png')  # Load the aball image
aball_image = pygame.transform.scale(aball_image, (40, 40))  # Resize to 40x40 (width, height)

bball_image = pygame.image.load('bball.png')  # Load the bball image
bball_image = pygame.transform.scale(bball_image, (40, 40))  # Resize to 40x40 (width, height)

cball_image = pygame.image.load('cball.png')  # Load the cball image
cball_image = pygame.transform.scale(cball_image, (40, 40))  # Resize to 40x40 (width, height)

dball_image = pygame.image.load('dball.png')  # Load the dball image
dball_image = pygame.transform.scale(dball_image, (40, 40))  # Resize to 40x40 (width, height)

bomb_image = pygame.image.load("bomb.png")
bomb_image = pygame.transform.scale(bomb_image, (60, 60))  # Slightly larger dimensions (e.g., 60x60)


# Load the custom font
font_path = "PressStart2P-Regular.ttf"
font_size = 20  # Default font size for most text
score_font_size = 15  # Font size for the score

# Set up a rectangular display
window_size = (1000, 600)  # Rectangular dimensions
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('HUNGRY CLOWNFISH')

# Load and resize images
sea_background_original = pygame.image.load('bk.png')  # Original background image
sea_background = pygame.transform.scale(sea_background_original, window_size)  # Scale background to fit screen

fishbowl_icon = pygame.image.load('fishbowl.png')  # Game icon
fish_player_original = pygame.image.load('fish2.png')  # Original player image
fish_player = pygame.transform.scale(fish_player_original, (80, 45))  # Slightly larger player icon

# Set game icon
pygame.display.set_icon(fishbowl_icon)

# Set initial player position and speed
player_x, player_y = 50, window_size[1] // 2  # Starting position
player_speed_y = 9  # Vertical movement speed

# Ball settings
ball_speed_x = 20  # Ball horizontal speed
ball_radius = 20  # Ball size
balls = []  # List to store balls

# Score settings
score = 0  # Player's score
ball_spawn_rate = 3  # Lower number = faster ball spawn rate

# Track number of orange balls collected
orange_ball_count = 0  # To keep track of how many orange balls have been eaten


# Progress bar settings
progress_bar_width = 300  # Width of the progress bar
progress_bar_height = 20  # Height of the progress bar
progress_bar_x = window_size[0] - progress_bar_width - 10  # Position from the right
progress_bar_y = 10  # Position from the top
progress = 0  # Progress towards filling the bar

# Timer settings
start_time = time.time()  # Start time for the timer
time_limit = 15  # Time limit in seconds

def start_screen():
    # Fill the screen with the background
    screen.blit(sea_background, (0, 0))
    
    # Load fonts for title and subtitle
    try:
        title_font = pygame.font.Font(font_path, 20)  # Increased font size for better visibility
        subtitle_font = pygame.font.Font(font_path, 10)
    except FileNotFoundError:
        title_font = pygame.font.Font(None, 50)  # Use default font if custom font is not found
        subtitle_font = pygame.font.Font(None, 30)

    # Render "HUNGRY CLOWNFISH" title
    title_text = title_font.render("HUNGRY CLOWNFISH", True, (255, 255, 255))
    title_text_x = window_size[0] // 2 - title_text.get_width() // 2
    title_text_y = window_size[1] // 2 - title_text.get_height()
    
    # Render "Click to Start" subtitle
    subtitle_text = subtitle_font.render("Click to Start", True, (255, 255, 255))
    subtitle_text_x = window_size[0] // 2 - subtitle_text.get_width() // 2
    subtitle_text_y = title_text_y + 40  # Slightly below the title
    
    # Display the texts on the screen
    screen.blit(title_text, (title_text_x, title_text_y))
    screen.blit(subtitle_text, (subtitle_text_x, subtitle_text_y))
    
    # Update the screen
    pygame.display.flip()

    # Wait for the player to click to start
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
                waiting = False


# Ball class for the food
class Ball:
    def __init__(self, x, y, ball_type, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = ball_type

    def move(self):
        self.x -= ball_speed_x  # Move the ball to the left

    def draw(self):
        if self.type == "aball":
            screen.blit(aball_image, (self.x - self.width // 2, self.y - self.height // 2))
        elif self.type == "bball":
            screen.blit(bball_image, (self.x - self.width // 2, self.y - self.height // 2))
        elif self.type == "cball":
            screen.blit(cball_image, (self.x - self.width // 2, self.y - self.height // 2))
        elif self.type == "dball":
            screen.blit(dball_image, (self.x - self.width // 2, self.y - self.height // 2))
        elif self.type == "bomb":  # Draw bomb if its type is "bomb"
            screen.blit(bomb_image, (self.x - self.width // 2, self.y - self.height // 2))


# geneerate ball funtions
def generate_ball():
    global ball_spawn_rate
    if random.randint(1, ball_spawn_rate) == 1:  # Random chance to spawn a ball
        ball_y = random.randint(50, window_size[1] - 50)
        ball_types = ["aball", "bball", "cball", "dball", "bomb"]  # Include "bomb" in the ball types
        ball_type = random.choice(ball_types)  # Randomly select a ball type

        # Define size for each type of ball
        if ball_type == "aball":
            ball_size = (40, 40)
        elif ball_type == "bball":
            ball_size = (50, 50)
        elif ball_type == "cball":
            ball_size = (45, 45)
        elif ball_type == "dball":
            ball_size = (55, 55)
        elif ball_type == "bomb":
            ball_size = (60, 60)  # Bomb dimensions are slightly larger

        balls.append(Ball(window_size[0], ball_y, ball_type, ball_size[0], ball_size[1]))

def draw_progress_bar():
    # Define the position and size of the progress bar
    bar_width = 250  # Width of the progress bar
    bar_height = 15  # Height of the progress bar
    bar_x = window_size[0] - bar_width - 10  # X position at the top-right corner
    bar_y = 10  # Y position near the top of the screen

    # Calculate the progress based on the score
    max_score = 100  # Set the maximum score for the progress bar (adjust as needed)
    progress = min(score / max_score, 1)  # Ensure progress doesn't exceed 100%

    # Draw the background of the progress bar (white)
    pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))

    # Draw the filled part of the progress bar (light blue)
    pygame.draw.rect(screen, (173, 216, 230), (bar_x, bar_y, bar_width * progress, bar_height))

    return progress  # Return progress to check if it's 100%


# Timer function (updated to position at top of the screen)
def draw_timer():
    elapsed_time = int(time.time() - start_time)
    remaining_time = max(0, time_limit - elapsed_time)
    font = pygame.font.Font(font_path, font_size)
    timer_text = font.render(f"Time: {remaining_time}", True, (255, 255, 255))
    # Position the timer at the top center
    screen.blit(timer_text, (window_size[0] // 2 - timer_text.get_width() // 2, 10))

# Game over screen
def game_over(message):
    # Fill the screen with the background
    screen.blit(sea_background, (0, 0))  
    
    # Load font with size 12 for game over text
    font = pygame.font.Font(font_path, 12)
    
    # Render game over message
    game_over_text = font.render(message, True, (255, 0, 0))
    
    # Render final score
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    
    # Calculate positions for text
    game_over_text_x = window_size[0] // 2 - game_over_text.get_width() // 2
    game_over_text_y = window_size[1] // 2 - game_over_text.get_height()
    
    score_text_x = window_size[0] // 2 - score_text.get_width() // 2
    score_text_y = game_over_text_y + 40  # Slightly below the game over message
    
    # Display the text on the screen
    screen.blit(game_over_text, (game_over_text_x, game_over_text_y))
    screen.blit(score_text, (score_text_x, score_text_y))
    
    # Update the screen to show the game over screen
    pygame.display.flip()
    
    # Wait for 2 seconds before quitting
    pygame.time.wait(2000)

# Victory screen function
def show_victory_screen():
    # Create a font for the message
    font = pygame.font.Font(font_path, 12)  # Font size for consistency with game over text
    victory_text = font.render("YOU FED THE HUNGRY CLOWNFISH!", True, (255, 255, 255))

    # Calculate the center of the screen
    text_rect = victory_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))

    screen.blit(sea_background, (0, 0)) 

    # Display the victory text on the screen
    screen.blit(victory_text, text_rect)

    # Update the display
    pygame.display.flip()

    # Delay for 3 seconds before ending the game
    pygame.time.delay(3000)  # Delay for 3 seconds before ending the game


start_screen()
start_time = time.time()

#game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement (up and down with arrow keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= player_speed_y
    if keys[pygame.K_DOWN]:
        player_y += player_speed_y

    # Boundary check for the player
    if player_y < 0:
        player_y = 0
    elif player_y > window_size[1] - fish_player.get_height():
        player_y = window_size[1] - fish_player.get_height()

    # Generate new balls
    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    if current_time - last_ball_spawn_time > 200:  # Spawn balls every 200 ms
        generate_ball()
        last_ball_spawn_time = current_time  # Update the last spawn time

    # Move balls and check for collisions
    for ball in balls[:]:  # Iterate over a copy of the list to safely remove items
        ball.move()
        if ball.x < 0:  # Remove balls that go off-screen
            balls.remove(ball)

        # Check for collision between player and ball
        if (
            player_x < ball.x + ball.width
            and player_x + fish_player.get_width() > ball.x
            and player_y < ball.y + ball.height
            and player_y + fish_player.get_height() > ball.y
        ):
            balls.remove(ball)  # Remove the ball when eaten
            
            if ball.type == "aball":
                score += 3
                eat_sound.play()  # Play eat sound
                time_limit += 5  # Extend time by 2 seconds
            elif ball.type == "bball":
                score += 3
                eat_sound.play()
                time_limit += 2  # Extend time by 2 seconds
            elif ball.type == "cball":
                score += 3
                eat_sound.play()
                time_limit += 5  # Extend time by 2 seconds
            elif ball.type == "dball":
                score += 4
                eat_sound.play()
                time_limit += 4  # Extend time by 4 seconds
            elif ball.type == "bomb":
                eat_bad_sound.play()  # Play bomb sound
                game_over("YOU HIT A BOMB!")
                running = False  # End the game if bomb is hit

    # Check for game over condition (if timer runs out)
    elapsed_time = int(time.time() - start_time)
    if elapsed_time >= time_limit:
        game_over("YOU LOSE")
        running = False

    # Draw everything
    screen.blit(sea_background, (0, 0))  # Background
    screen.blit(fish_player, (player_x, player_y))  # Player

    # Draw all balls
    for ball in balls:
        ball.draw()

    # Draw progress bar and timer
    progress = draw_progress_bar()
    draw_timer()

    # Display the score
    font = pygame.font.Font(font_path, score_font_size)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # Display the score at the top-left corner

    # Check if progress bar is full (100%)
    if progress >= 1:  # If progress is 100%
        show_victory_screen()  # Display victory screen
        running = False  # End the game loop

    # Update the screen
    pygame.display.flip()
    pygame.time.Clock().tick(30)  # Control the frame rate
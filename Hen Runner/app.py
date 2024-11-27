import pygame
import random

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound and music

# Game Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
PLAYER_SIZE = (70, 50)  # Width, Height of the player character
OBSTACLE_SIZE = (60, 70)  # Width, Height of obstacles
GROUND_HEIGHT = HEIGHT - 100  # Position of the ground from the bottom of the screen
MAX_JUMP_HOLD = 30  # Limit the maximum jump hold frames
MAX_OBSTACLES = 2  # Max number of obstacles on screen

# Variables for scrolling background
background_x1 = 0
background_x2 = WIDTH
scroll_speed = 5  # Adjust the speed to match the game's feel

# Game Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Run - Endless Runner")
clock = pygame.time.Clock()

# Load Images
player_image = pygame.image.load('assets/images/player.png')
player_image = pygame.transform.scale(player_image, PLAYER_SIZE)  # Resize the image to fit player size
obstacle_image = pygame.image.load('assets/images/obstacle_2.png')
obstacle_image = pygame.transform.scale(obstacle_image, OBSTACLE_SIZE)  # Resize to fit obstacle size
ground_image = pygame.image.load('assets/images/ground.png')
ground_image = pygame.transform.scale(ground_image, (WIDTH, 100))  # Scale it to fit the width of the screen

# Load background images
background_image = pygame.image.load('assets/images/background_img.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
game_background_image = pygame.image.load('assets/images/game_back.jpg')  # Add this line
game_background_image = pygame.transform.scale(game_background_image, (WIDTH, HEIGHT))  # Scale game background

# Load Images (add this part to your existing image loading section)
logo_image = pygame.image.load('assets/images/transf_logo.png')
logo_image = pygame.transform.scale(logo_image, (80, 80))  # Resize the logo if necessary

# Load sounds and music
jump_sound = pygame.mixer.Sound('assets/music/sound_effect.mp3')  # Load jump sound
background_music = 'assets/music/background_music.mp3'  # Path to background music file
game_over_sound = pygame.mixer.Sound('assets/music/game_over_sound.mp3')  # Game over sound

# Define new color constants
SKY_BLUE = (135, 206, 235)      # Sky blue color
DARK_SKY_BLUE = (70, 130, 180)  # Darker sky blue for hover

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = GROUND_HEIGHT  # Align the player's bottom with the ground height
        self.speed_x = 5
        self.jump_power = -20
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True
        self.jump_hold = 0  # Track how long the jump key is held down
        self.is_jumping = False
        self.jump_key_held = False  # To track the state of the jump key

    def update(self, is_mobile):
        keys = pygame.key.get_pressed()

        # Desktop controls (arrow keys)
        if not is_mobile:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed_x
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed_x

        # Mobile controls (tap on the screen)
        if is_mobile:
            if pygame.mouse.get_pressed()[0]:  # Left mouse click (tap)
                if self.on_ground and not self.is_jumping:
                    self.velocity_y = self.jump_power
                    self.on_ground = False
                    self.is_jumping = True
                    jump_sound.play()  # Play the jump sound when the player jumps

        # Jump Mechanics (Spacebar for Desktop)
        if not is_mobile and (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
            if self.on_ground and not self.jump_key_held:
                self.velocity_y = self.jump_power
                self.on_ground = False
                self.is_jumping = True
                jump_sound.play()  # Play the jump sound when the player jumps
                self.jump_key_held = True
                self.jump_hold = 0  # Reset jump_hold when starting a new jump

            if self.is_jumping and self.jump_hold < MAX_JUMP_HOLD:
                self.velocity_y -= 0.5
                self.jump_hold += 1
        else:
            self.is_jumping = False
            self.jump_key_held = False

        # Apply gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Boundary checking
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # Collision with ground
        if self.rect.bottom >= GROUND_HEIGHT:
            self.rect.bottom = GROUND_HEIGHT
            self.on_ground = True
            self.velocity_y = 0
            self.jump_hold = 0  # Reset jump_hold when the player is back on the ground


# Obstacle Class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Game Functions
def create_obstacle():
    x = WIDTH + random.randint(100, 300)
    y = GROUND_HEIGHT - OBSTACLE_SIZE[1]
    speed = 5 + distance // 200
    return Obstacle(x, y, speed)

# Sprite Groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Game Variables
score = 0
distance = 0
font = pygame.font.Font(None, 36)
game_over = False
on_home_screen = True

# Home Screen Button
def draw_play_button(mouse_pos):
    button_width, button_height = 200, 50
    play_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2, button_width, button_height)
    button_color = DARK_RED if play_button.collidepoint(mouse_pos) else RED
    pygame.draw.rect(screen, button_color, play_button)
    
    play_text = font.render('Play', True, WHITE)
    screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 - play_text.get_height() // 2))
    
    return play_button  

# Restart Button
def draw_restart_button():
    font = pygame.font.Font(None, 48)
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, WHITE, restart_button)
    text = font.render('Restart', True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 60))
    return restart_button

# Back Button Function
def draw_back_button():
    button_width, button_height = 100, 40
    back_button = pygame.Rect(WIDTH - button_width - 10, HEIGHT - button_height - 10, button_width, button_height)
    
    # Determine color based on hover
    if back_button.collidepoint(pygame.mouse.get_pos()):
        button_color = DARK_SKY_BLUE
    else:
        button_color = SKY_BLUE
    
    # Draw the button with the determined color
    pygame.draw.rect(screen, button_color, back_button)
    
    back_text = font.render('Back', True, WHITE)
    screen.blit(back_text, (WIDTH - button_width - 10 + (button_width - back_text.get_width()) // 2,
                            HEIGHT - button_height - 10 + (button_height - back_text.get_height()) // 2))
    
    return back_button

# Game Loop
running = True
while running:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()

    # Detect mobile vs desktop (based on whether the mouse is focused or touch event)
    is_mobile = pygame.mouse.get_focused() is False  # Assuming that lack of mouse focus means mobile

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if on_home_screen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_button = draw_play_button(mouse_pos) 
                if play_button.collidepoint(mouse_pos):
                    on_home_screen = False  
                    pygame.mixer.music.load(background_music)  # Load the background music
                    pygame.mixer.music.play(-1)  # Loop the background music indefinitely

        elif game_over:
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                mouse_pos = event.pos if event.type == pygame.MOUSEBUTTONDOWN else None
                restart_button = draw_restart_button()
                if (mouse_pos and restart_button.collidepoint(mouse_pos)) or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            
                    score = 0
                    distance = 0
                    player.rect.centerx = WIDTH // 2
                    player.rect.bottom = GROUND_HEIGHT
                    obstacles.empty()
                    all_sprites.empty()
                    player = Player()
                    all_sprites.add(player)
                    game_over = False
                    pygame.mixer.music.stop()  # Stop current background music
                    pygame.mixer.music.play(-1)  # Play background music again


        # Check for clicking the Back button in the main game
        if not on_home_screen and not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                back_button = draw_back_button()
                if back_button.collidepoint(event.pos):
                    on_home_screen = True
                    pygame.mixer.music.stop()  # Stop the game music when going back to the home screen

    if not on_home_screen and not game_over:
        # Scroll the background
        background_x1 -= scroll_speed
        background_x2 -= scroll_speed

        # If one background goes off the screen, reset its position
        if background_x1 <= -WIDTH:
            background_x1 = WIDTH
        if background_x2 <= -WIDTH:
            background_x2 = WIDTH

        # Update player with is_mobile
        player.update(is_mobile)

        # Create obstacles randomly, but only if there are less than the max allowed
        if len(obstacles) < MAX_OBSTACLES and random.randint(0, 100) < 2:
            obstacle = create_obstacle()
            obstacles.add(obstacle)
            all_sprites.add(obstacle)

        # Update obstacles (without is_mobile argument)
        for obstacle in obstacles:
            obstacle.update()

        # Collision Detection
        if pygame.sprite.spritecollideany(player, obstacles):
            game_over = True
            game_over_sound.play()  # Play the game over sound when the game ends

        distance += 1
        score_text = font.render(f"Distance: {distance}", True, WHITE)

    # Drawing
    screen.fill(BLACK)

    if on_home_screen:
        screen.blit(background_image, (0, 0))
        draw_play_button(mouse_pos)  
    else:
        screen.blit(game_background_image, (background_x1, 0))
        screen.blit(game_background_image, (background_x2, 0))

        screen.blit(ground_image, (0, GROUND_HEIGHT))

        screen.blit(logo_image, (WIDTH - logo_image.get_width() - 10, 10))    

        all_sprites.draw(screen)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render(f"Game Over! Score: {distance}", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            draw_restart_button()
        else:
            # Draw the back button during the game
            draw_back_button()

    pygame.display.flip()

pygame.quit()

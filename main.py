import pygame
import os

pygame.font.init()

###################################################################### Constants ########################################################################
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)
WIDTH, HEIGHT = 900, 500
BULLET_VEL = 3
FPS = 60
MAX_BULLETS = 3
VEL = 5
BORDER = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)

# Load and transform images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))  # loads yellow  spaceship
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (55, 40)), 90)  # rotates and resizes the spaceship images and rotate it accordingly
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))  # loads red  spaceship
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (55, 40)), 270)  # resizes the spaceship images and rotate it accordingly
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

# used for custom events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# store the bullets
red_bullets = []
yellow_bullets = []

# keep track of health
red_health = 10
yellow_health = 10

# creates a pygame window and set caption 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship game")


###################################################################### Functios to draw ########################################################################
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # draw the space background
    WINDOW.blit(SPACE, (0, 0)) 
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDER)  # draws the border rectangle .

    # draw the health data
    red_health_text = HEALTH_FONT.render(f"Health : {red_health}", 1, (255, 255, 255))
    yellow_health_text = HEALTH_FONT.render(f"Health : {yellow_health}", 1, (255, 255, 255))
    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10)) 
    WINDOW.blit(yellow_health_text, (10, 10)) 

    # draw the spaceships
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  # draws the spaceship .
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))  # draws the spaceship.
    
    # Draw the bullets
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, (255, 0, 0), bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, (255, 255, 0), bullet)
    
    # update the display
    pygame.display.update() 


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, (255, 255, 255))
    WINDOW.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)
    # exit game when we have a winner
    exit(0)


###################################################################### Functios to handle logic########################################################################
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # checks if we pressed a key
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # checks if we pressed d key
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # checks if we pressed w key
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:  # checks if we pressed s key
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # checks if we pressed left key
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # checks if we pressed right key
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # checks if we pressed up key
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:  # checks if we pressed down key
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


###################################################################### Game Loop ########################################################################
def main():
    global red_health
    global yellow_health
    red = pygame.Rect(700, 300, 55, 40)  # defines position for red player
    yellow = pygame.Rect(100, 300, 55, 40)  # defines position for red player
    clock = pygame.time.Clock()  # defines clock object that controls FPS
    run = True
    while run:
        clock.tick(FPS)  # controls FPS
        # iterate over the list of events 
        for event in pygame.event.get():
            # checks if user quit the game and accordingly toggles the game loop.
            if event.type == pygame.QUIT:
                run = False
                continue
            # creates bullets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + (yellow.height // 2), 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + (red.height // 2), 10, 5)
                    red_bullets.append(bullet)
            # Check if the bullet hits either spaceship
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1
        # Check if we have a winner
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins"
            draw_winner(winner_text)
        if yellow_health <= 0:
            winner_text = "Red wins"
            draw_winner(winner_text)
        # Keep track of keybresses  to check if the spaceship moves
        keys_pressed = pygame.key.get_pressed() 
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        # Check if bullet goes out of screen, if it collides with spaceship create a custom event
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        # Draw the updated data into the canvas
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    # exit pygame window at end of loop
    pygame.quit()


if __name__ == "__main__":
    main()
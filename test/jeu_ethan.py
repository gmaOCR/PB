import pygame
import sys
import random

# Initialisation de pygame
pygame.init()

# Taille de la fenêtre
width, height = 1026, 900
screen = pygame.display.set_mode((width, height))

# Couleurs et positions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
x, y, red_x, red_y = 50, 50, width // 2, height // 2

# Ajouter une variable pour le temps de début de partie
start_time = pygame.time.get_ticks()

# Vitesse de déplacement et chargement de l'image du personnage
speed, red_speed = 5, 1
character_image = pygame.image.load('photo_2023-12-03_16-20-35.jpg')
character_image = pygame.transform.scale(character_image, (150, 150))
mask = pygame.Surface((150, 150), pygame.SRCALPHA)
pygame.draw.circle(mask, WHITE, (75, 75), 75)
character_image.set_colorkey(BLACK)
mask.blit(character_image, (0, 0))

# Autres configurations
square_x, square_y, square_size, red_size = (width - 150) // 2, (height - 150) // 2, 150, 10
font = pygame.font.Font(None, 36)
lost_message = font.render('Perdu ! Appuyez sur Enter pour recommencer', True, BLUE)
message_rect = lost_message.get_rect(center=(width // 2, height // 2))
lost, last_speed_increase, game_time, blue_appear_time, blue_disappear_time = False, pygame.time.get_ticks(), 0, 0, 0
blue_x, blue_y, blue_size, blue_visible = 0, 0, 20, False


# Fonction pour réinitialiser le jeu
def reset_game():
    global x, y, red_x, red_y, lost, red_speed, last_speed_increase, game_time, blue_visible, start_time
    x, y, red_x, red_y = 50, 50, width // 2, height // 2
    red_speed, lost, blue_visible = 1, False, False
    last_speed_increase, game_time = pygame.time.get_ticks(), 0
    start_time = pygame.time.get_ticks()


# Fonction pour générer une position aléatoire
def generate_random_position(size):
    return random.randint(0, width - size), random.randint(0, height - size)


# Boucle principale
running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and lost: reset_game()

    # Mise à jour du compteur de temps et de la vitesse
    if not lost:
        game_time = (current_time - start_time) / 1000
        if current_time - last_speed_increase > 1000:  # Augmenter la vitesse toutes les secondes
            red_speed *= 1.03
            last_speed_increase = current_time

        # Gérer l'apparition et la disparition du point bleu
        if current_time - blue_appear_time > 15000 and not blue_visible:
            blue_x, blue_y = generate_random_position(blue_size)
            blue_visible, blue_appear_time = True, current_time
        if blue_visible and current_time - blue_appear_time > 3000:
            blue_visible = False

    # Gestion des touches
    if not lost:
        keys = pygame.key.get_pressed()
        x -= speed if keys[pygame.K_LEFT] and x > 0 else 0
        x += speed if keys[pygame.K_RIGHT] and x < width - 150 else 0
        y -= speed if keys[pygame.K_UP] and y > 0 else 0
        y += speed if keys[pygame.K_DOWN] and y < height - 150 else 0

    # Détecter les collisions
    character_rect = pygame.Rect(x, y, 150, 150)
    square_rect = pygame.Rect(square_x, square_y, square_size, square_size)
    red_rect = pygame.Rect(red_x, red_y, red_size, red_size)
    blue_rect = pygame.Rect(blue_x, blue_y, blue_size, blue_size)
    if character_rect.colliderect(square_rect) or character_rect.colliderect(red_rect): lost = True
    if blue_visible and character_rect.colliderect(blue_rect):
        red_speed *= 0.6
        blue_visible = False

    # Déplacer le point rouge
    if not lost:
        red_x += red_speed if red_x < x else -red_speed
        red_y += red_speed if red_y < y else -red_speed

    # Mise à jour de l'écran
    screen.fill(BLACK)
    pygame.draw.rect(screen, YELLOW, square_rect)  # Carré jaune
    pygame.draw.rect(screen, RED, red_rect)  # Point rouge
    screen.blit(mask, (x, y))  # Personnage
    if blue_visible: pygame.draw.rect(screen, BLUE, blue_rect)  # Point bleu
    speed_text = font.render(f'Vitesse: {red_speed:.2f}', True, WHITE)
    screen.blit(speed_text, (width - 200, 10))
    time_text = font.render(f'Temps: {game_time:.2f} s', True, WHITE)
    screen.blit(time_text, (10, 10))
    if lost: screen.blit(lost_message, message_rect)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quitter pygame
pygame.quit()
sys.exit()

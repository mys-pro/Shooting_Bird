import pygame

pygame.init()
WIDTH, HEIGHT = 900, 300
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Bird")

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
pygame.quit()
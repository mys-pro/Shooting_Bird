import pygame
import os
import random
import sys

# Khởi tạo pygame
pygame.init() 
pygame.display.set_caption("Shooting Bird")
icon = pygame.image.load('assets/images/icon.png')
pygame.display.set_icon(icon)

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
FPS = 60
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Xử lý ống ngắm
class viewFinder:
    def __init__ (self):
        pygame.event.set_grab(True) 
        pygame.mouse.set_visible(False)
        self.image = pygame.image.load('assets/images/viewfinder.png').convert_alpha()
        self.image_copy = self.image.copy()
        self.image_smaller = pygame.transform.scale(self.image_copy, (self.image_copy.get_width() // 2, self.image_copy.get_height() // 2))
        self.rect = self.image_smaller.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    def follow_mouse(self):
        self.rect.center = pygame.mouse.get_pos()
    
    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect(center=self.rect.center).topleft)

# Khởi tạo con chim
class birds(pygame.sprite.Sprite):
    def __init__(self, x, y, folder_name, speed, frame_rate):
        super().__init__()
        self.images = []
        folder_path = os.path.join('assets/images/birds', folder_name)
        for file_name in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file_name)
            if os.path.isfile(full_path):
                original_image = pygame.image.load(full_path).convert_alpha()
                smaller_image = pygame.transform.scale(original_image, (original_image.get_width() // 2, original_image.get_height() // 2))
                self.images.append(original_image)

        self.index = 0
        self.image = self.images[self.index]
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Đặt rect vào trung tâm ban đầu
        self.speed = speed
        self.frame_rate = frame_rate
        self.frame_rate_count = 0
        self.direction = "right" if x < SCREEN_WIDTH // 2 else "left"
    
    def toRight(self):
        self.frame_rate_count += 1

        if self.frame_rate_count >= self.frame_rate:
            self.index += 1
            self.frame_rate_count = 0

        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

        self.rect.x += self.speed
        if self.rect.x >= SCREEN_WIDTH:
            self.kill()

    def toLeft(self):
        self.frame_rate_count += 1

        if self.frame_rate_count >= self.frame_rate:
            self.index += 1
            self.frame_rate_count = 0
        if self.index >= len(self.images):
            self.index = 0
        self.image = pygame.transform.flip(self.images[self.index], True, False)

        self.rect.x -= self.speed
        if self.rect.x <= 0:
            self.kill()

    def update(self):
        if self.direction == "right":
            self.toRight()
        else:
            self.toLeft()

    def draw_rect(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Vẽ rect đỏ xung quanh chim
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_rect(screen)  # Vẽ rect của chim

# Lấy background ngẫu nhiên
def get_background(folder_path, SCREEN_WIDTH, SCREEN_HEIGHT):
    backgrounds = []
    for file_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file_name)
        if os.path.isfile(full_path):
             backgrounds.append(pygame.image.load(full_path).convert())
    
    bg = random.choice(backgrounds)
    bg_width, bg_height = bg.get_size()
    scale_factor = max(SCREEN_WIDTH / bg_width, SCREEN_HEIGHT / bg_height)

    new_width = int(bg_width * scale_factor)
    new_height = int(bg_height * scale_factor)
    bg = pygame.transform.scale(bg, (new_width, new_height))

    bg_x = (SCREEN_WIDTH - new_width) // 2
    bg_y = (SCREEN_HEIGHT - new_height) // 2
    return bg, bg_x, bg_y

# Tạo chim
def create_bird(bird_list_folder, speed, frame_rate):
    folder_name = random.choice(bird_list_folder)
    bird_x = random.choice([-100, SCREEN_WIDTH + 100])
    bird_y = random.randrange(20, SCREEN_HEIGHT // 2, 20)
    return birds(bird_x, bird_y, folder_name, speed, frame_rate)

# Vẽ hình ảnh
def draw(SCREEN, background, view_finder, birds_group):
    bg, bg_x, bg_y = background 
    SCREEN.blit(bg, (bg_x, bg_y))

    for bird in birds_group:
        bird.draw(SCREEN)
    view_finder.follow_mouse()
    view_finder.draw(SCREEN)
    pygame.display.update()

def main(SCREEN):
    background = get_background('assets/images/backgrounds/', SCREEN_WIDTH, SCREEN_HEIGHT) # Gọi hàm get_background
    view_finder = viewFinder()
    bird_list_folder = ['bird1', 'bird2']
    spawnBird = pygame.USEREVENT
    pygame.time.set_timer(spawnBird, 1200)
    birds_group = pygame.sprite.Group()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == spawnBird:
                new_bird = create_bird(bird_list_folder, 5, 8)
                birds_group.add(new_bird)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for bird in birds_group:
                    if view_finder.rect.colliderect(bird.rect):
                        bird.kill()

        birds_group.update()
        draw(SCREEN, background, view_finder, birds_group)
        pygame.time.Clock().tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main(SCREEN)
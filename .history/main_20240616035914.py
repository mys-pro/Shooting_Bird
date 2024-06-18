import pygame
import os
import random
import sys

WIDTH, HEIGHT = 1200, 700
FPS = 60

class Bird:
    def __init__(self, image, x, y, speed):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
    
    def update(self):
        self.rect.x += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

def load_background(folder_path, screen_width, screen_height):
    backgrounds = [] # Tạo danh sách rỗng để chứa tên các file hình ảnh
    for file_name in os.listdir(folder_path): # Duyệt qua tất cả các mục trong thư mục
        full_path = os.path.join(folder_path, file_name) # Tạo đường dẫn đầy đủ tới file
        if os.path.isfile(full_path): # Kiểm tra xem đây có phải là file không
             backgrounds.append(pygame.image.load(full_path)) # Nếu là file, thêm vào danh sách background
    
    bg = random.choice(backgrounds)# Chọn ngẫu nhiên một hình nền
    bg_width, bg_height = bg.get_size() # Lấy kích thước hình nền
    scale_factor = max(screen_width / bg_width, screen_height / bg_height) # Tính toán hệ số tỉ lệ để bao phủ toàn bộ cửa sổ

    # Tính toán kích thước mới để bao phủ toàn bộ cửa sổ
    new_width = int(bg_width * scale_factor)
    new_height = int(bg_height * scale_factor)
    bg = pygame.transform.scale(bg, (new_width, new_height)) # Thay đổi kích thước hình nền

    # Tính toán vị trí để căn giữa hình nền
    bg_x = (screen_width - new_width) // 2
    bg_y = (screen_height - new_height) // 2
    return bg, bg_x, bg_y

def create_bird(screen_width, screen_height):
    bird_image = pygame.Surface((50, 50))  # Tạo ảnh hình vuông
    bird_image.fill((255, 0, 0))  # Đỏ
    x = random.choice([-100, screen_width + 100])  # Đặt vị trí ban đầu
    y = random.randint(50, screen_height - 50)  # Vị trí ngẫu nhiên theo chiều cao màn hình
    speed = random.randint(3, 6) * random.choice([-1, 1])  # Tốc độ di chuyển ngẫu nhiên
    bird = Bird(bird_image, x, y, speed)
    return bird

def main():
    pygame.init() # Khởi tạo pygame
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) # Tạo cửa sổ với kích thước WIDTH x HEIGHT
    pygame.display.set_caption("Shooting Bird") # Đặt tiêu đề cửa sổ
    icon = pygame.image.load(r'assets/images/icon.png') # Lấy ảnh icon
    pygame.display.set_icon(icon) # Đặt ảnh icon cho cửa sổ

    cursor_img = pygame.image.load(r'assets/images/viewfinder.png').convert_alpha() # Tải hình ảnh con trỏ chuột
    cursor_img_width, cursor_img_height = cursor_img.get_size()
    pygame.event.set_grab(True) # Giữ con trỏ trong cửa sổ
    pygame.mouse.set_visible(False) # Ẩn con trỏ

    bg, bg_x, bg_y = load_background(r'assets/images/backgrounds/', WIDTH, HEIGHT) # Gọi hàm load_random_background
    # Danh sách các con chim
    birds = []

    # Vòng lặp chính
    running = True
    while running:
        # Xử lý các sự kiện từ bàn phím, chuột
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        # Tạo chim ngẫu nhiên
        if random.randint(0, 100) < 0.02:  # Tạo chim với xác suất nhỏ
            new_bird = create_bird(WIDTH, HEIGHT)
            birds.append(new_bird)

        # Cập nhật và vẽ các con chim
        for bird in birds:
            bird.update()
            bird.draw(SCREEN)

        # Loại bỏ các con chim ra khỏi màn hình
        birds = [bird for bird in birds if -100 <= bird.rect.x <= WIDTH + 100]

        mouse_x, mouse_y = pygame.mouse.get_pos() # Lấy vị trí hiện tại của con trỏ
        SCREEN.blit(bg, (bg_x, bg_y)) # Vẽ hình nền lên màn hình
        SCREEN.blit(cursor_img, (mouse_x - (cursor_img_width // 2), mouse_y - (cursor_img_height // 2))) # Vẽ ảnh ảnh lên vị trí con trỏ
        pygame.display.update() # Cập nhật màn hình
        pygame.time.Clock().tick(FPS) # Điều chỉnh tốc độ khung hình

    pygame.quit() # Dừng chương trình, giải phóng tài nguyên

if __name__ == "__main__":
    main()
import pygame
import random

LYRICS = [
    (1.0, "Anh call để cho..."),
    (2.0, "Em nghe đôi lời"),
    (3.5, "Anh đang ở nơi"),
    (5.0, "Không em không người"),
    (6.0, "Mây và gió đang thay..."),
    (8.0, "Lời anh nhớ em..."),
    (9.5, "Nhớ luôn tiếng cười")
]

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mặt trời của anh")

BLACK = (0, 0, 0)
PINK = (255, 182, 193)
WHITE = (255, 255, 255)

font_path = r"C:\Users\Admin\Downloads\Playwrite_IE\PlaywriteIE-VariableFont_wght.ttf"
font = pygame.font.Font(font_path, 45)

class Heart:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = HEIGHT + 20
        self.size = random.randint(10, 20)
        self.speed = random.uniform(1.5, 3.5)

    def move(self):
        self.y -= self.speed

    def draw(self, surface):
        s = self.size
        pygame.draw.circle(surface, PINK, (int(self.x - s/2), int(self.y)), int(s/2))
        pygame.draw.circle(surface, PINK, (int(self.x + s/2), int(self.y)), int(s/2))
        pygame.draw.polygon(surface, PINK, [
            (self.x - s, self.y), 
            (self.x + s, self.y), 
            (self.x, self.y + s * 1.5)
        ])

def get_current_lyric(elapsed_time):
    current_text = ""
    for start_time, text in LYRICS:
        if elapsed_time >= start_time:
            current_text = text
        else:
            break
    return current_text

hearts = []
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

running = True
while running:
    screen.fill(BLACK)
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if random.random() < 0.1:
        hearts.append(Heart())
    
    for heart in hearts[:]:
        heart.move()
        heart.draw(screen)
        if heart.y < -50:
            hearts.remove(heart)

    text_content = get_current_lyric(elapsed_time)
    if text_content:
        text_surface = font.render(text_content, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
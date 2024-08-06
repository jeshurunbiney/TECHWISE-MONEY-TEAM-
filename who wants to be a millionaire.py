import pygame
import sys

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Who Wants to Be a Millionaire")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load logo
logo = pygame.image.load('/Users/jeshurunbiney/Downloads/logo1.png')
logo_rect = logo.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Questions and answers
questions = [
    {"question": "What is the capital of France?", "choices": ["A: Paris", "B: London", "C: Berlin", "D: Madrid"], "answer": "A"},
    {"question": "What is 2 + 2?", "choices": ["A: 3", "B: 4", "C: 5", "D: 6"], "answer": "B"},
]

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)

def animate_logo():
    for i in range(100):
        screen.fill(BLACK)
        scale = 1 + i / 100
        scaled_logo = pygame.transform.rotozoom(logo, 0, scale)
        scaled_rect = scaled_logo.get_rect(center=logo_rect.center)
        screen.blit(scaled_logo, scaled_rect.topleft)
        pygame.display.update()
        pygame.time.delay(10)
    for i in range(100):
        screen.fill(BLACK)
        scale = 2 - i / 100
        scaled_logo = pygame.transform.rotozoom(logo, 0, scale)
        scaled_rect = scaled_logo.get_rect(center=logo_rect.center)
        screen.blit(scaled_logo, scaled_rect.topleft)
        pygame.display.update()
        pygame.time.delay(10)

def game_loop():
    question_index = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(BLACK)
        
        if question_index < len(questions):
            question = questions[question_index]
            draw_text(question["question"], large_font, WHITE, screen, 50, 50)
            for i, choice in enumerate(question["choices"]):
                draw_text(choice, font, WHITE, screen, 50, 150 + i * 50)
        else:
            draw_text("Congratulations! You've completed the game!", large_font, WHITE, screen, 50, SCREEN_HEIGHT // 2)
        
        pygame.display.update()
        
        # Simulate answering the question
        pygame.time.delay(3000)
        question_index += 1

if __name__ == "__main__":
    animate_logo()
    game_loop()

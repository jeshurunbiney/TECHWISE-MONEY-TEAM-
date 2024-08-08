import pygame
import sys
import random

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Who Wants to Be a Millionaire")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load logo
logo = pygame.image.load('logo1.png')
logo_rect = logo.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Load sounds
correct_sound = pygame.mixer.Sound("mainTheme.mp3")
wrong_sound = pygame.mixer.Sound("wrongBeeps.mp3")
lifeline_sound = pygame.mixer.Sound("lifeline.mp3")
background_music = pygame.mixer.Sound("background_music.mp3")
background_music.play(-1)  # Loop the background music

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Questions and answers
questions = [
    {"question": "What is the capital of France?", "choices": ["A: Paris", "B: London", "C: Berlin", "D: Madrid"],
     "answer": "A"},
    {"question": "What is 2 + 2?", "choices": ["A: 3", "B: 4", "C: 5", "D: 6"], "answer": "B"},
    {"question": "Who wrote 'Hamlet'?", "choices": ["A: Dickens", "B: Shakespeare", "C: Orwell", "D: Chaucer"],
     "answer": "B"},
    # Add more questions as needed
]

# Lifelines
lifelines = {"50/50": True, "Phone a Friend": True, "Ask the Audience": True}

question_index = 0
score = 0
correct_answers = 0
incorrect_answers = 0


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)


def create_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    draw_text(text, font, WHITE, screen, x + 10, y + 10)


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


def use_50_50(choices, correct_answer):
    lifeline_sound.play()
    incorrect_choices = [choice for choice in choices if choice[0] != correct_answer]
    remove_choices = random.sample(incorrect_choices, 2)
    for choice in remove_choices:
        choices.remove(choice)


def game_loop():
    global question_index, score, correct_answers, incorrect_answers

    while question_index < len(questions):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        question = questions[question_index]
        draw_text(question["question"], large_font, WHITE, screen, 50, 50)

        # Draw answer buttons
        buttons = []
        for i, choice in enumerate(question["choices"]):
            btn_x = 50
            btn_y = 150 + i * 100
            buttons.append((choice[0], btn_x, btn_y, 300, 50))
            create_button(choice, btn_x, btn_y, 300, 50, BLUE, GREEN,
                          lambda choice=choice: check_answer(choice, question["answer"], buttons))

        # Display Lifelines
        draw_text("Lifelines:", font, WHITE, screen, 1500, 50)
        for i, (lifeline, available) in enumerate(lifelines.items()):
            color = GREEN if available else RED
            draw_text(f"{lifeline} ({'Available' if available else 'Used'})", font, color, screen, 1500, 100 + i * 50)

        pygame.display.update()


def check_answer(selected_choice, correct_answer, buttons):
    global correct_answers, incorrect_answers

    # Stop all music
    pygame.mixer.stop()

    if selected_choice[0] == correct_answer:
        correct_sound.play()
        correct_answers += 1
    else:
        wrong_sound.play()
        incorrect_answers += 1

    pygame.display.update()
    pygame.time.delay(5000)  # Pause for 5 seconds to let the sound play
    next_question()


def next_question():
    global question_index

    question_index += 1
    if question_index >= len(questions):
        show_statistics()
    else:
        game_loop()


def show_statistics():
    global correct_answers, incorrect_answers

    screen.fill(BLACK)
    draw_text(f"Game Over!", large_font, WHITE, screen, 50, 150)
    draw_text(f"Correct Answers: {correct_answers}", large_font, GREEN, screen, 50, 300)
    draw_text(f"Incorrect Answers: {incorrect_answers}", large_font, RED, screen, 50, 400)
    draw_text(f"Your final score: {correct_answers}", large_font, WHITE, screen, 50, 500)

    pygame.display.update()
    pygame.time.delay(10000)  # Display statistics for 10 seconds
    pygame.quit()
    sys.exit()


def start_game():
    global question_index, score, correct_answers, incorrect_answers
    question_index = 0
    score = 0
    correct_answers = 0
    incorrect_answers = 0
    pygame.mixer.stop()  # Stop the background music when the game starts
    game_loop()


def main_menu():
    while True:
        screen.fill(BLACK)

        draw_text("Who Wants to Be a Millionaire", large_font, WHITE, screen, SCREEN_WIDTH // 2 - 400,
                  SCREEN_HEIGHT // 2 - 200)
        create_button("Start Game", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, BLUE, GREEN, start_game)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    animate_logo()
    main_menu()
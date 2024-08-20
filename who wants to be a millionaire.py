import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
HIGHLIGHT_COLOR = (200, 200, 50)
FONT_SIZE = 48
TIMER_DURATION = 15000  # 15 seconds in milliseconds
PARAGRAPH_SPACE = 75

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Who Wants to Be a Millionaire")

# Load font
font = pygame.font.Font(None, FONT_SIZE)

# Load images and sounds
background_image = pygame.image.load("/Users/jeshurunbiney/Downloads/game background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
logo_image = pygame.image.load("/Users/jeshurunbiney/Downloads/logo1.png")
start_game_icon = pygame.image.load("/Users/jeshurunbiney/Downloads/start game icon.jpeg")
question_sound = pygame.mixer.Sound("/Users/jeshurunbiney/Downloads/main theme.mp3")
question_sound.set_volume(0.2)  # Set volume to 20%

# Questions, answers, and prize money
questions = [
    {"question": "What involves repeating steps until a condition is met?", "options": ["A. Looping", "B. Branching", "C. Selecting", "D. Triggering"], "answer": "A"},
    {"question": "In programming, # is used for", "options": ["A. A hyperlink to social media accounts", "B. A mistake in a line of code", "C. To leave a message or comment in code", "D. Printing numbers"], "answer": "C"},
    {"question": "In Python, which of the following methods is used to add an element to the end of a list?", "options": ["A. append()", "B. add()", "C. insert()", "D. extend()"], "answer": "A"},
    {"question": "How do you define a function in python?", "options": ["A. function myFunction()", "B. def myFunction()", "C. create myFunction()", "D. Command myFunction()"], "answer": "B"},
    {"question": "Which of the following Python data types is immutable?", "options": ["A. List", "B. Dictionary", "C. Tuple", "D. Set"], "answer": "C"},
    {"question": "What is it called when a function is defined inside a class?", "options": ["A. Module", "B. Class", "C. Another function", "D. Method"], "answer": "D"},
    {"question": "What will be the result of 10 % 3?", "options": ["A. 1", "B. 3.333", "C. 0.333", "D. 0"], "answer": "A"},
    {"question": "What will be the output of the following code? L = ['a','b','c','d'] print(''.join(L))", "options": ["A. Error", "B. None", "C. abcd", "D. ['a','b','c','d']"], "answer": "C"},
    {"question": "Which of the following best describes a variable's scope?", "options": ["A. The value assigned to the variable", "B. The section of code where the variable can be accessed", "C. The name given to the variable", "D. The data type of the variable"], "answer": "B"},
    {"question": "What will be the output of the following code? print type(type(int))", "options": ["A. Type'int'", "B. Type'type'", "C. Error", "D. 0"], "answer": "B"},
    {"question": "Which statement is true about recursion?", "options": ["A. Recursion is a method where the solution to a problem depends on solutions to smaller instances of the same problem", "B. Recursion always provides the most efficient solution", "C. Recursion is a loop structure that repeatedly executes a block of code", "D. Recursion can only be used with numerical data types"], "answer": "A"},
    {"question": "Why would a programmer insert print statements into a loop during debugging?", "options": ["A. To make the loop execute faster", "B. To prevent infinite loops from occurring", "C. To track the loops execution and monitor variable values at different stages", "D. To ensure that the loop terminates"], "answer": "C"},
    {"question": "What will be the output of the following program? print \"Hello World\"[::-1]", "options": ["A. dlroW olleH", "B. Hello Worl", "C. d", "D. Error"], "answer": "A"},
    {"question": "What is the purpose of the 'break' statement in a loop?", "options": ["A. To skip the current iteration and proceed to the next iteration", "B. To terminate the loop entirely", "C. To return a value from the loop", "D. To pause the loop execution"], "answer": "B"},
    {"question": "What will be the output of the following program? def myfunc(a): a = a + 2 a = a * 2 return a", "options": ["A. Concatenates string elements of an iterable", "B. Calculates the sum of number elements in an iterable using recursion", "C. Returns the maximum number in an iterable", "D. Splits the iterable into individual elements"], "answer": "B"},
]

prize_money = [
    "$100", "$200", "$300", "$500", "$1,000", "$2,000", "$4,000", "$8,000", "$16,000", "$32,000",
    "$64,000", "$125,000", "$250,000", "$500,000", "$1,000,000"
]

# Game variables
current_question = 0
score = 0
timer_start = 0
selected_answer = None

# Welcome screen variables
logo_rect = logo_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
start_game_icon_rect = start_game_icon.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.2))

def display_welcome_screen():
    screen.fill(BLACK)
    screen.blit(logo_image, logo_rect)
    screen.blit(start_game_icon, start_game_icon_rect)
    pygame.display.flip()

def animate_logo():
    scale_factor = 1.05
    min_scale = 0.5
    max_scale = 1.5
    scale = max_scale  # Start at max scale

    question_sound.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_icon_rect.collidepoint(event.pos):
                    question_sound.stop()  # Stop the sound when starting the game
                    return

        screen.fill(BLACK)
        logo_scaled = pygame.transform.rotozoom(logo_image, 0, scale)
        logo_rect = logo_scaled.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(logo_scaled, logo_rect)
        screen.blit(start_game_icon, start_game_icon_rect)
        pygame.display.flip()

        # Zoom out animation
        scale /= scale_factor
        if scale <= 1:
            return  # Exit the loop when original size is reached

def display_question(question):
    global selected_answer
    screen.blit(background_image, (0, 0))
    question_text = font.render(question["question"], True, WHITE)
    question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(question_text, question_rect)

    for i, option in enumerate(question["options"]):
        option_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + i * PARAGRAPH_SPACE - 20, 600, 50)
        if option_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, option_rect)
            selected_answer = i
        else:
            pygame.draw.rect(screen, BLACK, option_rect)

        option_text = font.render(option, True, WHITE)
        screen.blit(option_text, (option_rect.x + 10, option_rect.y + 10))

    pygame.display.flip()
    question_sound.stop()  # Stop any previous sound
    question_sound.play()  # Play sound for the new question

def check_answer(question, answer):
    global score
    if answer == question["answer"]:
        score += 1
        return True
    return False

def display_score():
    score_text = font.render(f"Score: {prize_money[score]}", True, WHITE)
    screen.blit(score_text, (50, 50))

def display_timer(remaining_time):
    timer_text = font.render(f"Time left: {remaining_time // 1000} seconds", True, WHITE)
    screen.blit(timer_text, (SCREEN_WIDTH - 400, 50))

def main_game_loop():
    global current_question, timer_start, selected_answer
    running = True
    timer_start = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and selected_answer is not None:
                correct = check_answer(questions[current_question], chr(selected_answer + ord('A')))
                if not correct:
                    running = False
                else:
                    current_question += 1
                    if current_question >= len(questions):
                        running = False
                    else:
                        display_question(questions[current_question])
                        timer_start = pygame.time.get_ticks()

        if current_question < len(questions):
            display_question(questions[current_question])
            display_score()
            elapsed_time = pygame.time.get_ticks() - timer_start
            remaining_time = TIMER_DURATION - elapsed_time
            display_timer(remaining_time)
            if remaining_time <= 0:
                current_question += 1
                if current_question >= len(questions):
                    running = False
                else:
                    display_question(questions[current_question])
                    timer_start = pygame.time.get_ticks()

    # Game over screen
    screen.fill(BLACK)
    game_over_text = font.render(f"Game Over! You won: {prize_money[score]}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.wait(5000)

    # Quit Pygame
    pygame.quit()
    sys.exit()

# Display welcome screen and animate logo
animate_logo()

# Wait for user to start the game
while True:
    display_welcome_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_game_icon_rect.collidepoint(event.pos):
                main_game_loop()

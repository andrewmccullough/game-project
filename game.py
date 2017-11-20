# Samarth Kishor (sk4gz) and Andrew McCullough (asm4wm)

import pygame
import gamebox
import random

# Initialize camera
camera = gamebox.Camera(800, 600)

# Create ball
ball = gamebox.from_color(400, 300, 'green', 20, 20)

# Globals
start_game = False
counter = 0
score = 0
stars = []

def background():
    '''Creates a scrolling starry background'''
    global counter
    counter += 1

    # Initialize background
    if start_game:
        for i in range(0, 600, 5):
            stars.append(
                gamebox.from_color(random.randint(0, 800), i, 'white', 2, 2))

        for star in stars:
            camera.draw(star)

    # Scrolling background
    if counter % 10 == 0:
        num_stars = random.randint(5, 10)
        for _ in range(num_stars):
            stars.append(
                gamebox.from_color(random.randint(0, 800), 0, 'white', 2, 2))

    for star in stars:
        star.y += 1
        if star.y > 600:
            stars.remove(star)
        camera.draw(star)


def tick(keys):
    '''Game loop'''
    global start_game
    global score

    # Start the game
    # if start_game == False:
    #     camera.clear('black')
    #     camera.draw(
    #         gamebox.from_text(
    #             400, 300,
    #             'Andrew McCullough (asm4wm) and Samarth Kishor (sk4gz)',
    #             'Arial', 50, 'red'))

    # Controls
    if pygame.K_UP in keys:
        character.y -= 5
    if pygame.K_DOWN in keys:
        character.y += 5
    if pygame.K_LEFT in keys:
        character.x -= 5
    if pygame.K_RIGHT in keys:
        character.x += 5

    # Background
    camera.clear('black')
    background()

    # Draw
    camera.draw(character)

    camera.display()


gamebox.timer_loop(30, tick)

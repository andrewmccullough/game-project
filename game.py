# Samarth Kishor (sk4gz) and Andrew McCullough (asm4wm)

import pygame
import gamebox
import random

# Initialize camera
camera = gamebox.Camera(800, 600)

# Global variables
counter = 0
score = 0
stars = []
blocks = []

# def background():
#
#     '''
#         Creates a scrolling starry background
#     '''
#
#     camera.clear('black')
#
#
#
#     # # Scrolling background
#     # if counter % 10 == 0:
#     #     num_stars = random.randint(5, 10)
#     #     for _ in range(num_stars):
#     #         stars.append(
#     #             gamebox.from_color(random.randint(0, 800), 0, 'white', 2, 2))
#     #
#     # for star in stars:
#     #     star.y += 1
#     #     if star.y > 600:
#     #         stars.remove(star)
#     #     camera.draw(star)

# Create ball sprite
ball = gamebox.from_image(0, 0, "assets/moon.png")
# Create bouncy platform
platform = gamebox.from_color(400, 600, "yellow", 150, 40)

# Generates a fuckton of stars
while len(stars) < 200:
    stars.append(
        gamebox.from_color(
            random.randint(0, 800),
            random.randint(0, 600),
            "white",
            2,
            2
        )
    )

def tick(keys):

    global score

    # Start the game
    # if start_game == False:
    #     camera.clear('black')
    #     camera.draw(
    #         gamebox.from_text(
    #             400, 300,
    #             'Andrew McCullough (asm4wm) and Samarth Kishor (sk4gz)',
    #             'Arial', 50, 'red'))

    camera.clear('black')

    for star in stars:
        camera.draw(star)
    camera.draw(ball)
    camera.draw(platform)

    camera.display()

gamebox.timer_loop(30, tick)

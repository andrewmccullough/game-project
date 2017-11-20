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
colors = ["red", "orange", "green", "blue", "purple"]

# Create ball sprite
ball = gamebox.from_image(400, 600 - 20 - 27, "assets/moon.png")
# Create bouncy platform
platform = gamebox.from_color(400, 600, 'yellow', 150, 40)

# Creates blocks
for row in range(3):
    color = random.choice(colors)
    colors.remove(color)
    blocks_per_row = 5
    for block in range(blocks_per_row):
        blocks.append(
            gamebox.from_color(800 / blocks_per_row * block + 160 / 2,
                               40 * row + 40 / 2, color, 800 / blocks_per_row,
                               40))

# Generates starry background
while len(stars) < 200:
    stars.append(
        gamebox.from_color(
            random.randint(0, 800), random.randint(0, 600), 'white', 2, 2))


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
    for block in blocks:
        camera.draw(block)

    camera.draw(ball)
    camera.draw(platform)

    camera.display()


gamebox.timer_loop(30, tick)

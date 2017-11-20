# Samarth Kishor (sk4gz) and Andrew McCullough (asm4wm)

import pygame
import gamebox
import random

# Global variables
counter = 0
score = 0
stars = []
blocks = []
colors = ["red", "orange", "green", "blue", "purple"]
game_started = False
ball_speed = 10

def vectorize(angle):
    return math.cos(angle) * ball_speed, math.sin(angle) * ball_speed

# Initialize camera
camera = gamebox.Camera(800, 600)

# Create ball sprite
ball = gamebox.from_image(400, 600 - 20 - 27, "assets/moon.png")
# Create bouncy platform
platform = gamebox.from_color(400, 600, 'yellow', 160, 40)

# Creates blocks
for row in range(3):
    color = random.choice(colors)
    colors.remove(color)
    blocks_per_row = 5
    for block in range(blocks_per_row):
        blocks.append(
            gamebox.from_color(800 / blocks_per_row * block + 160 / 2,
                               40 * row + 40 / 2, color,
                               800 / blocks_per_row - 4, 40 - 4))

# Generates starry background
while len(stars) < 200:
    stars.append(
        gamebox.from_color(
            random.randint(0, 800), random.randint(0, 600), 'white', 2, 2))

def tick(keys):

    global score

    if pygame.K_LEFT in keys:
        # moves platform left
        platform.x -= 12

        if game_started == False:
            ball.xspeed, ball.yspeed = vectorize(100)
            game_started = True

    if pygame.K_RIGHT in keys:
        # moves platform right
        platform.x += 12

        if game_started == False:
            ball.xspeed, ball.yspeed = vectorize(80)
            game_started = True

    if platform.x > 800 - 160 / 2:
        # platform has overshot to the right
        platform.x = 800 - 160 / 2
    if platform.x < 160 / 2:
        # platform has overshot to the left
        platform.x = 160 / 2

    camera.clear('black')

    for star in stars:
        camera.draw(star)
    for block in blocks:
        camera.draw(block)

    camera.draw(ball)
    camera.draw(platform)

    camera.display()


gamebox.timer_loop(45, tick)

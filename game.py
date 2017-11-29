# Samarth Kishor (sk4gz) and Andrew McCullough (asm4wm)

import pygame
import gamebox
import random
import math

# Global variables
counter = 0
score = 0
stars = []
blocks = []
colors = ['red', 'orange', 'green', 'blue', 'purple']
game_started = False
ball_speed = 10
ball_angle = 0

# Initialize camera
camera = gamebox.Camera(800, 600)
# Create ball sprite
ball = gamebox.from_image(400, 600 - 20 - 27, 'moon.png')
# Create bouncy platform
platform = gamebox.from_color(400, 600, 'yellow', 160, 40)


def vectorize(angle):
    global ball_angle

    if angle < 0:
        angle = 360 + angle

    ball_angle = angle
    xspeed = math.cos(math.radians(angle)) * ball_speed
    yspeed = math.sin(math.radians(angle)) * ball_speed

    return xspeed, yspeed


def endgame(won, score):
    camera.clear('black')
    if won:
        scoreboard = gamebox.from_text(
            400, 300,
            'You won! Your score was ' + str(score) + '. Press q to quit.',
            'Arial', 30, 'yellow')
    else:
        scoreboard = gamebox.from_text(
            400, 300,
            'You lost. Your score was ' + str(score) + '. Press q to quit.',
            'Arial', 30, 'yellow')
    camera.draw(scoreboard)


def tick(keys):
    global game_started
    global score

    if pygame.K_LEFT in keys:
        # moves platform left
        platform.x -= 12

        if not game_started:
            # releases the ball from the platform
            ball.xspeed, ball.yspeed = vectorize(110)
            game_started = True

    if pygame.K_RIGHT in keys:
        # moves platform right
        platform.x += 12

        if not game_started:
            # releases the ball from the platform
            ball.xspeed, ball.yspeed = vectorize(70)
            game_started = True

    # Correct overshooting
    if platform.x > 800 - 160 / 2:
        # platform has overshot to the right
        platform.x = 800 - 160 / 2
    if platform.x < 160 / 2:
        # platform has overshot to the left
        platform.x = 160 / 2

    # Implement ball speed
    ball.x = ball.x + ball.xspeed
    ball.y = ball.y - ball.yspeed

    # Draw the background within the game loop
    camera.clear('black')

    for star in stars:
        camera.draw(star)

    # Collision detection
    for block in blocks:
        if ball.touches(block):
            if ball_angle > 90 and ball_angle < 180:
                ball.xspeed, ball.yspeed = vectorize(180 + (180 - ball_angle))
            elif ball_angle > 0 and ball_angle < 90:
                ball.xspeed, ball.yspeed = vectorize(0 - ball_angle)

            blocks.remove(block)
            score += 1

        camera.draw(block)

    if ball.touches(platform):
        # We should add something to change resulting vector
        # based on where it hits on the platform
        if 180 < ball_angle < 270:
            ball.xspeed, ball.yspeed = vectorize(180 - (ball_angle - 180))
        elif 270 < ball_angle < 360:
            ball.xspeed, ball.yspeed = vectorize(360 - ball_angle)

    # Bounce the ball off the sides of the screen
    if ball.y > 600 - 54 / 2:
        endgame(False, score)

    if ball.y < 0 + 54 / 2:
        if 0 < ball_angle < 90:
            ball.xspeed, ball.yspeed = vectorize(180 - (ball_angle - 180))
        elif 90 < ball_angle < 180:
            ball.xspeed, ball.yspeed = vectorize(360 - ball_angle)

    if ball.x < 0 + 54 / 2:
        ball.xspeed, ball.yspeed = vectorize(90 - (ball_angle - 90))

    if ball.x > 800 - 54 / 2:
        ball.xspeed, ball.yspeed = vectorize(90 + (90 - ball_angle))

    # End the game
    if len(blocks) == 0:
        endgame(True, score)

    if pygame.K_q in keys:
        gamebox.stop_loop()

    camera.draw(ball)
    camera.draw(platform)
    camera.display()


def main():
    # Create blocks
    for row in range(3):
        color = random.choice(colors)
        colors.remove(color)
        blocks_per_row = 5
        for block in range(blocks_per_row):
            blocks.append(
                gamebox.from_color(800 / blocks_per_row * block + 160 / 2,
                                   40 * row + 40 / 2, color,
                                   800 / blocks_per_row - 4, 40 - 4))

    # Generate starry background
    while len(stars) < 200:
        stars.append(
            gamebox.from_color(
                random.randint(0, 800), random.randint(0, 600), 'white', 2, 2))

    gamebox.timer_loop(45, tick)


if __name__ == '__main__':
    main()

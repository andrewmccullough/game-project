# Samarth Kishor (sk4gz) and Andrew McCullough (asm4wm)

import pygame
import gamebox
import random
from math import sin, cos, radians

###########################
#### Global variables #####
###########################

counter = 0
score = 0
time = 0
health = 3
won = False

# Empty object arrays
stars = []
blocks = []
aliens = []
hearts = []

# "Possiblity arrays" that are randomly chosen from for generation
colors = ['red', 'orange', 'green', 'blue', 'purple']
alien_sprites = [
    'alien_blue.png', 'alien_green.png', 'alien_pink.png', 'alien_purple.png'
]
possible_soundtracks = ['ghostbusters.wav', 'starwars.wav', 'startrek.wav']

# Ball variables
ball_speed = 10
ball_angle = 0

# Game status variables
game_started = False  # Past intro screen
game_active = False  # Ball moving
game_over = False  # Game over

camera = gamebox.Camera(800, 600)

ball = gamebox.from_image(400, 600 - 20 - 27, 'moon.png')
platform = gamebox.from_color(400, 600, 'yellow', 160, 40)

soundtrack = random.choice(possible_soundtracks)
music = gamebox.load_sound(soundtrack)
play = music.play(-1)

#####################################################
#### Calculates ball movement given impact angle ####
#####################################################


def vectorize(angle):
    global ball_angle

    if angle < 0:
        angle = 360 + angle

    ball_angle = angle
    xspeed = cos(radians(angle)) * ball_speed
    yspeed = sin(radians(angle)) * ball_speed

    return xspeed, yspeed


def tick(keys):
    global game_started
    global game_active
    global game_over

    global score
    global counter
    global health
    global time
    global won

    counter += 1

    # Draw the background within the game loop
    camera.clear('black')
    for star in stars:
        camera.draw(star)

    # Quit game at any time
    if pygame.K_q in keys:
        gamebox.stop_loop()

    if not game_started:
        title = gamebox.from_text(400, 200, 'SpaceBreaker', 'Arial', 100,
                                  'green')
        camera.draw(title)
        subtitle = gamebox.from_text(
            400, 260, 'brought to you by Samarth Kishor and Andrew McCullough',
            'Arial', 25, 'green')
        camera.draw(subtitle)
        subsubtitle = gamebox.from_text(400, 300, 'sk4gz // asm4wm', 'Arial',
                                        20, 'green')
        camera.draw(subsubtitle)

        controls = [
            'SPACE to start', 'LEFT and RIGHT arrows to move', 'Q to quit'
        ]
        instructions = [
            'Hit blocks and aliens with the ball for points.',
            "Don't let the aliens hit you!"
        ]

        h = 0

        for control in controls:
            h += 1
            camera.draw(
                gamebox.from_text(400, 340 + 30 * h, control, 'Arial', 25,
                                  'yellow'))

        for instruction in instructions:
            h += 1
            camera.draw(
                gamebox.from_text(400, 360 + 30 * h, instruction, 'Arial', 25,
                                  'yellow'))

        if pygame.K_SPACE in keys:
            game_started = True

    elif game_started and not game_active and not game_over:
        if pygame.K_LEFT in keys:
            game_active = True
            ball.xspeed, ball.yspeed = vectorize(110)

        if pygame.K_RIGHT in keys:
            game_active = True
            ball.xspeed, ball.yspeed = vectorize(70)

        for block in blocks:
            camera.draw(block)

        camera.draw(platform)
        camera.draw(ball)

        # Draw health
        for i in range(health):
            camera.draw(
                gamebox.from_image(800 - 50 - 60 * i, 600 - 60, 'heart.png'))

        if not game_started:
            # Draw start screen
            title = gamebox.from_text(400, 200, 'SpaceBreaker', 'Arial', 60,
                                      'yellow')
            camera.draw(title)

    elif game_started and game_active and not game_over:
        # Increment timer
        if counter % 45 == 0:
            time += 1

        # Create new alien
        if counter % (45 * 3) == 0:
            new_alien = random.choice(alien_sprites)
            aliens.append(
                gamebox.from_image(random.randint(100, 700), 0, new_alien))

        # Update platform location
        if pygame.K_LEFT in keys:
            platform.x -= 14

        if pygame.K_RIGHT in keys:
            platform.x += 14

        # Correct overshooting
        if platform.x > 800 - 160 / 2:
            platform.x = 800 - 160 / 2
        if platform.x < 160 / 2:
            platform.x = 160 / 2

        # Update ball location
        ball.x = ball.x + ball.xspeed
        ball.y = ball.y - ball.yspeed

        # Draw blocks and detect collisions with blocks
        for block in blocks:
            if ball.touches(block):
                if ball_angle > 90 and ball_angle < 180:
                    ball.xspeed, ball.yspeed = vectorize(
                        180 + (180 - ball_angle))
                elif ball_angle > 0 and ball_angle < 90:
                    ball.xspeed, ball.yspeed = vectorize(0 - ball_angle)

                blocks.remove(block)
                score += 1

            camera.draw(block)

        # Detect collisions with platform
        if ball.touches(platform):
            if ball.x <= platform.x and game_started:
                ball.xspeed, ball.yspeed = vectorize(90 +
                                                     (platform.x - ball.x))
            elif ball.x > platform.x and game_started:
                ball.xspeed, ball.yspeed = vectorize(90 -
                                                     (ball.x - platform.x))

        # Draw aliens
        for alien in aliens:
            alien.y += 2

            if ball.touches(alien):
                score += 1
                aliens.remove(alien)

            if platform.touches(alien):
                aliens.remove(alien)
                health -= 1

            if health < 1:
                won = False
                game_over = True

            camera.draw(alien)

        # Bounce the ball off the sides of the screen
        if ball.y > 600 - 54 / 2:
            won = False
            game_over = True

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
            won = True
            game_over = True

        camera.draw(platform)
        camera.draw(ball)

        # Draw health
        for i in range(health):
            camera.draw(
                gamebox.from_image(800 - 50 - 60 * i, 600 - 60, 'heart.png'))

        # Draw timer
        timer = str(time) + ' s'
        camera.draw(
            gamebox.from_text(50, 600 - 40, timer, 'Arial', 25, 'white'))

        # Draw score
        scoreboard = str(score) + ' pts'
        camera.draw(
            gamebox.from_text(50, 600 - 70, scoreboard, 'Arial', 25, 'white'))

    elif game_over:
        # camera.clear('black')
        if won:
            scoreboard = gamebox.from_text(
                400, 300,
                'You won in ' + str(time) + ' seconds! Your score was ' +
                str(score) + '. Press q to quit.', 'Arial', 30, 'yellow')
        else:
            scoreboard = gamebox.from_text(
                400, 300, 'You lost. Your score was ' + str(score) +
                '. Press q to quit.', 'Arial', 30, 'yellow')

        camera.draw(scoreboard)

    camera.display()


def main():
    # Generate blocks
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

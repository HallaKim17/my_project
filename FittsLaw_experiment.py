import pygame
import random
import math
import time

def get_random_radius():
    return random.randint(5,20)


def get_random_position():
    radius = get_random_radius()
    return random.randint(0+radius, WIDTH-radius), random.randint(0+radius,HEIGHT-radius)


def display(screen, radius, position):

    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, position, radius, 1)
    pygame.display.flip()


def click_change(screen, radius, position):
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, position, radius, 1)
    pygame.display.flip()


def distance(x0,x1, y0,y1):
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)


Radius = []
Distance = []
Time = []

if __name__ == "__main__":
    pygame.init()
    WIDTH = 800
    HEIGHT = 600
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fitts Law Experiment")

    clock = pygame.time.Clock()
    running = True
    clicked = False

    radius = get_random_radius()
    position = get_random_position()
    x0, y0 = pygame.mouse.get_pos()
    start = time.time()

    while running:
        clock.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                clicked = False
                x0, y0 = pygame.mouse.get_pos()
                start = time.time()
                # draw the next circle
                radius = get_random_radius()
                position = get_random_position()

        if clicked:
            time_elapsed = time.time() - start
            click_change(screen, radius, position)
            x1, y1 = pygame.mouse.get_pos()
            moving_distance = distance(x0,x1,y0,y1)
            # save data
            Radius.append(radius)
            Distance.append(moving_distance)
            Time.append(time_elapsed)

        display(screen, radius, position)

    pygame.quit()
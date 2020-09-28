import pygame
import random
import math
import time
import pandas as pd


def randomize_radius(radius_list):
    random.shuffle(radius_list)


def randomize_position(distance_list):
    random.shuffle(distance_list)


def display(screen, x, y, width, height):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, [x, y, width, height])
    pygame.display.flip()


def distance(x0,x1, y0,y1):
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)


def make_IVs(size, distance):
    randomize_radius(size)
    randomize_position(distance)
    IVs = list(zip(size, distance))
    return IVs


Size = [20,40,60] * 4  # 3 levels of target size (W)
Distance = [100,200,300,400] * 3  # 4 levels of target distance (D)
Time = []
num_trials = 30
IV = []
click_positions = []

if __name__ == "__main__":
    pygame.init()
    WIDTH = 1000
    HEIGHT = 600
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fitts Law Experiment")

    clock = pygame.time.Clock()
    running = True
    clicked = False

    for i in range(num_trials):
        iv = make_IVs(Size, Distance)
        IV.append(iv)
    IV = sum(IV, [])

    x, y = WIDTH/2 + IV[0][1], HEIGHT/4
    width, height = IV[0][0], HEIGHT/2
    start = time.time()

    num_test = 0

    while running:
        clock.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                clicked = False

                time_elapsed = time.time() - start
                # save data
                Time.append(time_elapsed)
                mouseX, _ = pygame.mouse.get_pos()
                click_positions.append(mouseX - (x+width/2))

                num_test += 1
                print('== ', num_test, ' ==', 'X: ', x, 'Width: ', width)
                if num_test == 12 * num_trials:
                    writer = pd.ExcelWriter('FittsLaw_results.xlsx', engine='xlsxwriter')
                    df = pd.DataFrame({'mouseX': click_positions,
                                        'size': [v[0] for v in IV],
                                       'distance': [v[1] for v in IV],
                                       'time': Time})
                    df.to_excel(writer, header=True)
                    writer.close()
                    running = False
                    break

                if x < WIDTH / 2:
                    x += IV[num_test][1]
                else:
                    x -= IV[num_test][1]
                width = IV[num_test][0]

                start = time.time()

        if clicked:
            pass

        display(screen, x, y, width, height)

    pygame.quit()




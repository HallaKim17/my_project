import pygame
import random
import math
import time
import pandas as pd
import numpy as np


def randomize_array(array):
    random.shuffle(array)


def display_boundary(screen, x, y, width):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, [x, y, width, 5])
    pygame.display.flip()


def display_detect_rect(screen, x, y, height):
    rect = pygame.Rect(x, y, 5, height)
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, [x, y, 5, height])
    pygame.display.flip()
    return rect


def distance(x0,x1, y0,y1):
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)


def make_IVs(w1, distance):
    randomize_array(w1)
    randomize_array(distance)
    IVs = list(zip(w1, w1/3, distance))
    return IVs


def save_data():
    writer = pd.ExcelWriter('NarrowingSteeringLaw_results.xlsx', engine='xlsxwriter')
    df = pd.DataFrame({'width1': [v[0] for v in IV],
                       'width2': [v[1] for v in IV],
                       'distance': [v[2] for v in IV],
                       'time': Time})
    df.to_excel(writer, header=True)
    writer.close()


Width1 = np.array([30,60,90] * 2)  # 3 levels of tunnel width at starting point (W1)
Distance = np.array([300,600] * 3)  # 2 levels of target distance (D)
Time = []
num_trials = 10
click_positions = []
IV = []

if __name__ == "__main__":
    pygame.init()
    WIDTH = 1000
    HEIGHT = 600
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Narrowing Steering Law Experiment")

    clock = pygame.time.Clock()
    running = True
    clicked = False
    start_position = 'left'

    for i in range(num_trials):
        iv = make_IVs(Width1, Distance)
        IV.append(iv)
    IV = sum(IV, [])

    num_test = 0

    x0 = WIDTH/2-IV[num_test][2]/2
    y0 = HEIGHT/2-IV[num_test][0]/2

    x1 = WIDTH/2+IV[num_test][2]/2
    y1 = HEIGHT/2-IV[num_test][1]/2

    start = time.time()
    font = pygame.font.SysFont('Times New Roman', 10)

    while running:
        clock.tick(40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                clicked = False

        mouseX, mouseY = pygame.mouse.get_pos()

        if clicked:
            start = time.time()
            print('///Start timing///')

        screen.fill(WHITE)
        timer = font.render(str(int(time.time() - start)), True, (255, 255, 255))
        screen.blit(timer, (100,100))
        pygame.draw.line(screen, BLUE, [x0, y0], [x1,y1], 3)
        pygame.draw.line(screen, BLUE, [x0, y0+IV[num_test][0]], [x1,y1+IV[num_test][1]], 3)

        if start_position == 'left':
            pygame.draw.rect(screen, BLUE, [x1, y1, 5, IV[num_test][1]])
            rect = pygame.Rect(x1, y1, 5, IV[num_test][1])
            if mouseX > x1:
                pygame.draw.rect(screen, RED, [x1, y1, 5, IV[num_test][1]])

                time_elapsed = time.time() - start
                Time.append(time_elapsed)
                print('///End timing///')

                num_test += 1
                if num_test == 6 * num_trials:
                    save_data()
                    break

                start_position = 'right'
                x0 = WIDTH / 2 + IV[num_test][2] / 2
                y0 = HEIGHT / 2 - IV[num_test][0] / 2

                x1 = WIDTH / 2 - IV[num_test][2] / 2
                y1 = HEIGHT / 2 - IV[num_test][1] / 2

                print('== ', num_test, ' ==', 'Width: ', IV[num_test][0], 'Distance: ', IV[num_test][1])
        else:
            pygame.draw.rect(screen, BLUE, [x1, y1, 8, IV[num_test][1]])
            rect = pygame.Rect(x1, y1, 8, IV[num_test][0])
            if mouseX < x1:
                pygame.draw.rect(screen, RED, [x1, y1, 8, IV[num_test][1]])

                time_elapsed = time.time() - start
                Time.append(time_elapsed)
                print('///End timing///')

                num_test += 1
                if num_test == 6 * num_trials:
                    save_data()
                    break

                start_position = 'left'
                x0 = WIDTH / 2 - IV[num_test][2] / 2
                y0 = HEIGHT / 2 - IV[num_test][0] / 2

                x1 = WIDTH / 2 + IV[num_test][2] / 2
                y1 = HEIGHT / 2 - IV[num_test][1] / 2

                print('== ', num_test, ' ==', 'Width: ', IV[num_test][0], 'Distance: ', IV[num_test][1])

        pygame.display.update()

    pygame.quit()




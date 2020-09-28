import pygame
import random
import math
import time
import pandas as pd


def randomize_radius(radius_list):
    random.shuffle(radius_list)


def randomize_position(distance_list):
    random.shuffle(distance_list)


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


def make_IVs(width, distance):
    randomize_radius(width)
    randomize_position(distance)
    IVs = list(zip(width, distance))
    return IVs


def save_data():
    writer = pd.ExcelWriter('SteeringLaw_results.xlsx', engine='xlsxwriter')
    df = pd.DataFrame({'width': [v[0] for v in IV],
                       'distance': [v[1] for v in IV],
                       'time': Time})
    df.to_excel(writer, header=True)
    writer.close()


Width = [20,40,60] * 2  # 3 levels of target size (W)
Distance = [400,600] * 3  # 2 levels of target distance (D)
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
    pygame.display.set_caption("Steering Law Experiment")

    clock = pygame.time.Clock()
    running = True
    clicked = False
    start_position = 'left'

    for i in range(num_trials):
        iv = make_IVs(Width, Distance)
        IV.append(iv)
    IV = sum(IV, [])

    num_test = 0

    x0 = WIDTH/2-IV[num_test][1]/2
    y0 = HEIGHT/2-IV[num_test][0]/2

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
        pygame.draw.rect(screen, BLUE, [x0, y0, IV[num_test][1], 5])
        pygame.draw.rect(screen, BLUE, [x0, IV[num_test][0]+y0, IV[num_test][1], 5])
        if start_position == 'left':
            pygame.draw.rect(screen, BLUE, [IV[num_test][1]+x0, y0, 8, IV[num_test][0]])
            rect = pygame.Rect(IV[num_test][1] + x0, y0, 8, IV[num_test][0])
            if mouseX > IV[num_test][1]+x0+8:
                pygame.draw.rect(screen, RED, [IV[num_test][1] + x0, y0, 8, IV[num_test][0]])

                time_elapsed = time.time() - start
                Time.append(time_elapsed)
                print('///End timing///')

                num_test += 1
                if num_test == 6 * num_trials:
                    save_data()
                    break

                start_position = 'right'
                x0 = float(WIDTH / 2 - IV[num_test][1] / 2)
                y0 = HEIGHT / 2 - int(IV[num_test][0]) / 2

                print('== ', num_test, ' ==', 'Width: ', IV[num_test][0], 'Distance: ', IV[num_test][1])
        else:
            pygame.draw.rect(screen, BLUE, [x0, y0, 8, IV[num_test][0]])
            rect = pygame.Rect(x0, y0, 8, IV[num_test][0])
            if mouseX < x0:
                pygame.draw.rect(screen, RED, [x0, y0, 8, IV[num_test][0]])

                time_elapsed = time.time() - start
                Time.append(time_elapsed)
                print('///End timing///')

                num_test += 1
                if num_test == 6 * num_trials:
                    save_data()
                    break

                start_position = 'left'
                x0 = WIDTH / 2 - IV[num_test][1] / 2
                y0 = HEIGHT / 2 - IV[num_test][0] / 2

                print('== ', num_test, ' ==', 'Width: ', IV[num_test][0], 'Distance: ', IV[num_test][1])

        pygame.display.update()

    pygame.quit()




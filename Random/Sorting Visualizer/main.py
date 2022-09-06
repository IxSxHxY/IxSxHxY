import random as rd
import pygame
from pygame.locals import *
import time



pygame.init()

pygame.font.init()

class DrawInformation:
    '''
    This class contains all the information that will be drawn
    '''
    WHITE = (255, 255, 255)

    BLACK = (0, 0, 0)

    GRADIENT = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255)
    ]

    BACKGROUND = WHITE

    def __init__(self, width: int, height: int, lst: list[int]) -> None:
        '''

        :param width: the width of the screen
        :param height: the height of the screen
        :param lst: the list that will be sorted
        '''
        self.width = width
        self.height = height
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)
        pygame.display.set_caption('Sorting algorithm visualizer')

        self.text = [
            'R - Randomize list | I - Insertion sort',
            'B - Bubble sort | S - Selection sort'
        ]
        self.font_size = (self.width // 30)
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        self.textSurf = [self.font.render(text, False, self.font_size) for text in self.text]
        for i in self.textSurf:
            i.set_alpha(127)

        self.window = pygame.display.set_mode((width, height), RESIZABLE)

        self.calculate_info()



        # pygame.Rect(startX, startY, width, height)




    def calculate_info(self) -> None:
        '''
        Recalculate everything important like text width
        :return:
        '''
        self.pad_width = self.width // 10
        self.pad_height = self.height // 5
        self.block_width = (self.width - 2 * self.pad_width) // len(self.lst)
        self.block_height = (self.height - self.pad_height) // (self.max_val - self.min_val)

        self.font_size = (self.width // 30)
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        self.textSurf = [self.font.render(text, False, self.font_size) for text in self.text]
        for i in self.textSurf:
            i.set_alpha(127)

    def update_window_size(self, width: int, height: int) -> None:
        '''

        :param width: updated width of screen
        :param height: updated height of screen
        :return: None
        '''
        self.width = width
        self.height = height
        self.calculate_info()


def generate_lst(lower: int, upper: int, size: int) -> list[int]:
    """

    :param lower: lower bound for the generated elements (inclusive)
    :param upper: upper bound for the generated elements (inclusive)
    :param size: the size of the elements
    :return: an array with random generated elements
    """
    return [rd.randint(lower, upper) for _ in range(size)]


def draw(draw_info: DrawInformation) -> None:
    '''


    :return: None
    '''
    draw_info.window.fill(draw_info.BACKGROUND)
    for i, surf in enumerate(draw_info.textSurf):
        text_width, text_height = surf.get_size()
        draw_info.window.blit(surf, (draw_info.width // 2 - text_width // 2, i*text_height))

    pygame.display.update()


def draw_list(draw_info: DrawInformation) -> None:
    draw(draw_info)
    lst = draw_info.lst
    for i, val in enumerate(lst):
        pygame.draw.rect(
            surface=draw_info.window,
            color=draw_info.GRADIENT[i%3],
            rect=pygame.Rect( (draw_info.pad_width + i * draw_info.block_width),
                              (draw_info.height - val * draw_info.block_height),
                              draw_info.block_width,
                              draw_info.block_height * val
                              )
        )
    pygame.display.update()




def insertion_sort(draw_info: DrawInformation) -> list[int]:
    '''
    :param arr: a list of value to be sorted
    :return: sorted list
    '''
    lst = draw_info.lst
    n = len(lst)
    for i in range(1, n):
        while i > 0 and lst[i] < lst[i-1]:
            lst[i], lst[i-1] = lst[i-1], lst[i]
            i -= 1
            time.sleep(0.009)
            draw_list(draw_info=draw_info)
    return lst
    # 6 3 1 -> 3 6 1 -> 3 1 6 -> 1 3 6

def bubble_sort(draw_info: DrawInformation) -> list[int]:
    lst = draw_info.lst
    n = len(lst)
    for i in range(n):
        for j in range(i, n):
            if lst[i] > lst[j]:
                lst[i], lst[j] = lst[j], lst[i]
            time.sleep(0.0005)
            draw_list(draw_info=draw_info)
    return lst

def selection_sort(draw_info: DrawInformation) -> list[int]:
    lst = draw_info.lst
    n = len(lst)
    for i in range(n):
        min_idx, min_val = i, lst[i]
        for j in range(i, n):
            if min_val > lst[j]:
                min_idx = j
                min_val = lst[j]
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        time.sleep(0.1)
        draw_list(draw_info=draw_info)
    return lst

def main() -> None:
    run = True

    width = 600
    height = 500
    min_val = 0
    max_val = 100
    length = 50
    lst = generate_lst(lower=min_val, upper=max_val, size=length)

    clock = pygame.time.Clock()


    draw_info = DrawInformation(width=600, height=500, lst=lst)
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Usually wise to be able to close your program.
                run = False
            if event.type == VIDEORESIZE:
                width, height = draw_info.window.get_size()
                draw_info.update_window_size(width, height)
                pygame.display.update()
            if event.type == VIDEOEXPOSE:  # handles window minimising/maximising
                width, height = draw_info.window.get_size()
                draw_info.update_window_size(width, height)
                pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    draw_info.lst = generate_lst(lower=min_val, upper=max_val, size=length)
                if event.key == pygame.K_i:
                    draw_info.lst = insertion_sort(draw_info)
                if event.key == pygame.K_b:
                    draw_info.lst = bubble_sort(draw_info)
                if event.key == pygame.K_s:
                    draw_info.lst = selection_sort(draw_info)

        draw_list(draw_info=draw_info)

    pygame.quit()


if __name__ == '__main__':
    main()

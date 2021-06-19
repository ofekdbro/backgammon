import pygame
import Graphics
import Constants
import numpy
from Board import Board
import Dice
from pygame.locals import *

pygame.init()


def main():
    running = True
    clock = pygame.time.Clock()
    pygame.display.flip()
    Graphics.draw_window()
    Constants.setup_colX()
    Constants.setup_colY()
    #Graphics.draw_all_units_start_phase()
    firstDice = Dice.roll()
    secondDice = Dice.roll()
    Graphics.show_dice(firstDice, 1)
    Graphics.show_dice(secondDice, 2)
    Graphics.draw_dice_roll()
    board = Board()
    board.draw_game_board(firstDice, secondDice)
    while running:
        clock.tick(Constants.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if Graphics.is_dice_roll_pressed(pos):
                    firstDice = Dice.roll()
                    secondDice = Dice.roll()
                    Graphics.dice_roll_pressed(firstDice, secondDice)
                print(pos)
                if Graphics.is_triangle_pressed(pos):
                    if firstDice == secondDice:
                        result = [secondDice, secondDice, firstDice, firstDice]
                    else:
                        result = [firstDice, secondDice]
                    pos = Graphics.convert_pos_to_row(pos)
                    board.newturn(pos, result)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()

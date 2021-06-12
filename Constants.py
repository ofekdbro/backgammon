import pygame
import numpy
import Dice

Screen = pygame.display.set_mode((800, 600))
Background = pygame.image.load("Backgammon_Board_Check.png").convert()
Black_Unit = pygame.image.load("Black_Unit.png").convert_alpha()
White_Unit = pygame.image.load("White_Unit.png").convert_alpha()
Unit_width = 50
Border_width = 20
Unit_Height = 40
Border_Height = 23
Screen_Width = 800
Screen_Height = 600
colX = numpy.zeros(12, int)
colY = numpy.zeros(2, int)
Dice_image = ["", pygame.image.load("Dice_1.png"), pygame.image.load("Dice_2.png"), pygame.image.load("Dice_3.png"),
              pygame.image.load("Dice_4.png"), pygame.image.load("Dice_5.png"), pygame.image.load("Dice_6.png")]
White_player_win_screen = pygame.image.load("White_player_win_screen.png")
Black_player_win_screen = pygame.image.load("Black_player_win_screen.png")
FPS = 60


def setup_colX():  # this is an array only for x cordination
    colX[1] = 30
    colX[2] = 90
    colX[3] = 155
    colX[4] = 210
    colX[5] = 270
    colX[6] = 330
    colX[7] = 430
    colX[8] = 490
    colX[9] = 550
    colX[10] = 610
    colX[11] = 670
    colX[0] = 730  # because i work with % 0 = 12


def setup_colY():  # this is an array only for y cordinations
    colY[1] = 23
    colY[0] = 540

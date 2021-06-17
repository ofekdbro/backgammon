import pygame.image

import Board
import Dice
import Constants


def draw_window():  # draw the backgammon background
    Constants.Screen.blit(Constants.Background, (0, 0))
    Constants.pygame.display.update()


def draw_Unit_Start(color, col, quantity):  # draw the starting posisions for the units
    i = 0
    if col <= 12:
        if col == 1:
            while i < quantity:
                Constants.Screen.blit(color, (Constants.colX[col % 12],
                                              Constants.colY[1] + (Constants.Unit_Height * i)))
                i += 1
        elif col == 5:
            while i < quantity:
                Constants.Screen.blit(color, (Constants.colX[col % 12],
                                              (Constants.colY[1] + (Constants.Unit_Height * i))))
                i += 1
        elif col == 7:
            while i < quantity:
                Constants.Screen.blit(color, (Constants.colX[col % 12],
                                              Constants.colY[1] + (Constants.Unit_Height * i)))
                i += 1
        elif col == 12:
            while i < quantity:
                Constants.Screen.blit(color, (Constants.colX[col % 12],
                                              Constants.colY[1] + (Constants.Unit_Height * i)))
                i += 1
    elif col > 12:
        if col == 13:
            while i < quantity:
                Constants.Screen.blit(color, (Constants.colX[col % 12],
                                              Constants.colY[0] - (Constants.Unit_Height * i)))
                i += 1
        elif col == 17:
            while i < quantity:
                Constants.Screen.blit(color, (Constants.colX[col % 12],
                                              Constants.colY[0] - (Constants.Unit_Height * i)))
                i += 1
        elif col == 19:
            while i < quantity:
                Constants.Screen.blit(color, (Constants.colX[col % 12],
                                              Constants.colY[0] - (Constants.Unit_Height * i)))
                i += 1
        elif col == 24:
            while i < quantity:
                Constants.Screen.blit(color, (Constants.colX[col % 12],
                                              Constants.colY[0] - (Constants.Unit_Height * i)))
                i += 1  #


def draw_all_units_start_phase():  # activate the "draw_Unit_Start" with only one method
    draw_Unit_Start(Constants.White_Unit, 1, 2)
    draw_Unit_Start(Constants.Black_Unit, 5, 5)
    draw_Unit_Start(Constants.Black_Unit, 7, 3)
    draw_Unit_Start(Constants.White_Unit, 12, 5)
    draw_Unit_Start(Constants.Black_Unit, 13, 5)
    draw_Unit_Start(Constants.White_Unit, 17, 3)
    draw_Unit_Start(Constants.White_Unit, 19, 5)
    draw_Unit_Start(Constants.Black_Unit, 24, 2)


def draw_dice_roll():  # drawing the dice roll  button
    Constants.Screen.blit(pygame.image.load("Dice_Roll.png"),
                          (Constants.Screen_Width / 2 - 23, Constants.Screen_Height / 2 - 60))


def dice_roll_pressed(firstDice, secondDice):  # shows the dices which were given graphically
    show_dice(firstDice, 1)
    show_dice(secondDice, 2)


def show_dice(num, place):  # show the dice in the middle of the board the num is reference for which cube to presnt
    # and place is for  where to put the cube (the lower or upper) 1 = upper other is lower
    if place == 1:
        Constants.Screen.blit(Dice.get_image(num), (Constants.Screen_Width / 2 - 20,
                                                    Constants.Screen_Height / 2 - 250))
    else:
        Constants.Screen.blit(Dice.get_image(num), (Constants.Screen_Width / 2 - 20,
                                                    Constants.Screen_Height / 2 - 200))


def convert_pos_to_row(pos):
    # is needed to use the method "get_row_col" before and then,
    # gets row and col an return the exact triangle the unit is on
    x, y = get_row_col(pos)
    print(x + (12 * ((y - 1) ** 2)))
    return x + (12 * ((y - 1) ** 2))


def draw_game_board(arr, dice1, dice2):  # refreshing screen basically
    i = 1
    draw_window()
    show_dice(dice1, 1)
    show_dice(dice2, 2)
    draw_dice_roll()
    while i <= 24:
        if arr[i] > 0:
            show_unit(Constants.White_Unit, i, arr[i])
        else:
            show_unit(Constants.Black_Unit, i, abs(arr[i]))
        i += 1


def show_unit(color, col, quantity):  # gets the units color, which col, and quantity and shows them on screen
    i = 0
    if col > 12:
        while i < quantity:
            Constants.Screen.blit(color, (Constants.colX[col % 12],
                                          Constants.colY[0] - (Constants.Unit_Height * i)))
            i += 1
    else:
        while i < quantity:
            Constants.Screen.blit(color, (Constants.colX[col % 12],
                                          Constants.colY[1] + (Constants.Unit_Height * i)))
            i += 1


def is_triangle_pressed(pos):
    return get_row_col(pos) is not None


def is_dice_roll_pressed(pos):  # checks if the dice roll button pressed and returns true\false
    x, y = pos
    if 382 <= x <= 420:
        if 370 >= y >= 240:
            return True
    return False


def get_row_col(pos):  # gets x,y positions and return which row and col are pressed
    x, y = pos
    if 30 <= x <= 70:
        if 24 <= y <= 240:
            return 1, 1
        return 1, 0
    elif 87 <= x <= 140:
        if 24 <= y <= 240:
            return 2, 1
        return 2, 0
    elif 145 <= x <= 200:
        if 24 <= y <= 240:
            return 3, 1
        return 3, 0
    elif 206 <= x <= 250:
        if 24 <= y <= 240:
            return 4, 1
        return 4, 0
    elif 270 <= x <= 306:
        if 24 <= y <= 240:
            return 5, 1
        return 5, 0
    elif 325 <= x <= 375:
        if 24 <= y <= 240:
            return 6, 1
        return 6, 0
    elif 431 <= x <= 467:
        if 24 <= y <= 240:
            return 7, 1
        return 7, 0
    elif 485 <= x <= 537:
        if 24 <= y <= 240:
            return 8, 1
        return 8, 0
    elif 554 <= x <= 585:
        if 24 <= y <= 240:
            return 9, 1
        return 9, 0
    elif 604 <= x <= 652:
        if 24 <= y <= 240:
            return 10, 1
        return 10, 0
    elif 672 <= x <= 701:
        if 24 <= y <= 240:
            return 11, 1
        return 11, 0
    elif 724 <= x <= 776:
        if 24 <= y <= 240:
            return 12, 1
        return 12, 0
    else:
        return None

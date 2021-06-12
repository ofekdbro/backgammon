import numpy
import Graphics
import pygame
from Unit import Unit
import Constants


class Board:

    def __init__(self):
        self.board = numpy.zeros(29, int)  # 1-24 is the board, 25
        self.Unit_List = []
        self.board[1] = 2
        self.add_list(2, 1, 1, self.Unit_List)
        self.board[5] = -5
        self.add_list(5, -1, 5, self.Unit_List)
        self.board[7] = -3
        self.add_list(3, -1, 7, self.Unit_List)
        self.board[12] = 5
        self.add_list(5, 1, 12, self.Unit_List)
        self.board[13] = -5
        self.add_list(5, -1, 13, self.Unit_List)
        self.board[17] = 3
        self.add_list(3, 1, 17, self.Unit_List)
        self.board[19] = 5
        self.add_list(5, 1, 19, self.Unit_List)
        self.board[24] = -2
        self.add_list(2, -1, 24, self.Unit_List)
        self.counter = 0  # count the turns - white = even, black = odd

    def add_list(self, num, color, place, unit_list):
        for i in range(num):
            unit = Unit(color, place)
            unit_list.append(unit)

    def search_unit_by_place(self, place):  # gets the triangle's place and search in the list if any unit
        # has this row or else returning None
        for i in range(len(self.Unit_List)):
            if place == self.Unit_List[i].place:
                return self.Unit_List[i]

    def turn(self, dice1, dice2, pos):
        if self.search_unit_by_place(pos) is not None:
            if self.counter % 2 == 0 and self.search_unit_by_place(pos).color == 1 \
                    or self.counter % 2 == 1 and self.search_unit_by_place(pos).color == -1:
                result = [0, 0, 0, 0]
                if dice1 == dice2:
                    result = [dice1, dice1, dice1, dice1]
                else:
                    result = [dice1, dice2]
                i = 0
                while not self.check_win() and sum(result) > 0 and i < len(result):  # if no one won
                    if not self.is_returning():
                        # if there is a unit which needs to get back to the game
                        while sum(result) > 0 and i < len(result) and not self.is_burn():
                            # checks if the player isn't in a "burn phase"
                            self.legal_move(self.search_unit_by_place(pos), result[i], dice1, dice2)
                            # checks if it is legal move
                            result[i] = 0
                            i += 1
                        for pos in pygame.event.get():
                            if Graphics.is_triangle_pressed(pos):
                                pos = Graphics.convert_pos_to_row(pos)
                        while sum(result) > 0 and i < len(result) and self.is_burn():
                            # if in "burn phase" it burns the Unit
                            self.burn(self.search_unit_by_place(pos), result[i])
                            result[i] = 0
                            i += 1
                    else:
                        while sum(result) > 0 and i < len(result) and self.is_returning():
                            self.returning(self.search_unit_by_place(pos), result[i])
                            result[i] = 0
                            # returns the Unit to the game
                            i += 1
                self.counter += 1
            else:
                Constants.Screen.blit(pygame.image.load("Press_again.png"), (0, Constants.Screen_Height / 2 - 60))

    def move_unit(self, unit, steps, dice1, dice2):
        self.board[unit.place] -= 1 * unit.color
        self.board[unit.place + (steps * unit.color)] += 1 * unit.color
        unit.set_place(unit.place + (steps * unit.color))
        Graphics.draw_game_board(self.board, dice1, dice2)  # prints the board graphically

    def legal_move(self, unit, steps, dice1, dice2):
        if unit is not None:
            if 24 >= unit.place + (steps * unit.color) >= 1:
                # checks if in the board
                if (self.board[unit.place + (steps * unit.color)]) * unit.color >= 0:
                    # checks if step on the same color so the unit will be able to move there
                    self.move_unit(unit, steps, dice1, dice2)
                elif abs(self.board[unit.place + (steps * unit.color)]) == 1:  # checks if the unit is eatable
                    self.eat_unit(unit, self.search_unit_by_place(self.board[unit.place + (steps * unit.color)]),
                                  steps)
            else:
                self.move_to_edge(unit, steps)

    def eat_unit(self, unit, unit2, steps):  # let unit1 to eat the second unit
        unit2.set_place(self.board[26 - self.counter % 2])
        self.move_unit(unit, steps)

    def move_to_edge(self, unit, steps):
        if unit.place + (steps * unit.color) < 1:
            self.move_unit(unit, abs(steps - unit.place))
        else:
            self.move_unit(unit, abs((unit.place + steps) - 24))

    def burn(self, unit, dice):  # burns the unit
        if unit.place == dice or unit.place == 24 - dice:
            if abs(self.board[unit.place]) > 0:
                self.board[unit.place] += 1 * unit.color
                self.board[27 + self.counter % 2] += 1 * unit.color
            else:
                self.move_unit(unit, dice)

    def is_returning(self):  # checks if the player needs to return any of his units
        if self.board[25 + self.counter % 2] != 0:
            return True
        return False

    def returning(self, unit, dice):  # returns the
        if self.counter % 2 == 0:
            if self.board[abs(dice - 24)] > 0:
                self.board[25] -= 1
                self.move_unit(unit, (abs(dice - 24)))
            else:
                if self.board[dice] < 0:
                    self.move_unit(unit, dice)
                    self.board[26] += 1

    def is_burn(self):  # checks if the player is in burn phase and return True\False
        if self.counter % 2 == 0:
            if self.sum_board(19) + self.board[28] == 15:
                return True
        else:
            if self.sum_board(1) + self.board[27] == -15:
                return True
        return False

    def sum_board(self, i):  # sums the both ends of the boards
        sum = 0
        if i == 19:
            for i in range(19, 24):
                sum += self.board[i]
        elif i == 1:
            for i in range(1, 6):
                sum += self.board[i]
        return sum

    def check_win(self):  # checks if anyone won and shows the win screen
        if self.board[27] == -15:
            Constants.Screen.blit(Constants.Black_player_win_screen, (400, 300))
            return True
        elif self.board[28] == 15:
            Constants.Screen.blit(Constants.White_player_win_screen, (400, 300))
            return True
        return False


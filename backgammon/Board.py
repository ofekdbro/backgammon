import numpy
import Graphics
import pygame
from Unit import Unit
import Constants


class Board:

    def __init__(self):
        self.turn = 0
        self.mode = "from"
        self.x_from = None
        self.x_to = None

        self.board = numpy.zeros(29, int)  # 1-24 is the board, 25 is for returning black, 26 is for returning white
        # 27 is for burned
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

    def helper(self, pos):  # checks if the pos is valid for the move
        if self.mode == "from":
            if self.search_unit_by_place(pos) is not None:
                if self.counter == 0 and self.search_unit_by_place(pos).color == 1 \
                        or self.counter == 1 and self.search_unit_by_place(pos).color == -1:
                    return pos
        elif self.mode == "to":
            # check if the plsce is empty or
            # if there is the other color only 1 return pos
            # else none
            if self.search_unit_by_place(pos) is None or \
                    (self.search_unit_by_place(pos) and abs(self.board[pos]) == 1):
                return pos
        return None

    def calcSteps(self):  # calculates the steps from x to y
        if self.x_from is None or self.x_to is None:
            return 0
        return abs(self.x_from - self.x_to)

    def newturn(self, pos, result):
        if self.turn < len(result):
            if self.mode == "from":
                ret = self.helper(pos)
                if ret:
                    self.x_from = ret
                    if self.is_returning():
                        self.return_unit(self.search_unit_by_place(ret), ret)
                    # elif self.is_burn():
                    # x = self.burn(ret)
                    # if not x:
                    self.mode = "to"
            elif self.mode == "to":
                ret = self.helper(pos)
                if ret:
                    self.x_to = ret
                    if self.calcSteps() != 0:
                        if self.is_eating(self.x_to):
                            self.eat_unit(self.search_unit_by_place(self.x_from),
                                          self.search_unit_by_place(self.x_to), self.calcSteps())
                        else:
                            self.new_move_unit(self.search_unit_by_place(self.x_from), self.calcSteps())
                        self.draw_game_board(result[0], result[1])  # prints the board graphically
                        self.mode = "from"
                    else:
                        self.mode = "from"
                        self.turn -= 1

                    self.x_from = None
                    self.x_to = None
                    self.turn += 1
                    if self.turn == len(result):
                        self.turn = 0
                        self.mode = "from"
                        self.x_from = None
                        self.x_to = None
                        self.counter = (self.counter + 1) % 2

    def is_eating(self, pos):  # checks if eating unit is valid
        if self.search_unit_by_place(pos) is not None:
            if self.board[pos] * self.search_unit_by_place(self.x_from).color == -1:
                return True
        return False

    def new_move_unit(self, unit, steps):
        self.board[unit.place] -= 1 * unit.color
        self.board[unit.place + (steps * unit.color)] += 1 * unit.color
        unit.set_place(unit.place + (steps * unit.color))

    def eat_unit(self, unit, unit2, steps):  # let unit1 to eat the second unit
        self.board[unit2.place] = 0
        unit2.set_place(25 + self.counter)
        self.board[unit2.place] += 1 * unit2.color
        self.new_move_unit(unit, steps)

    def move_to_edge(self, unit, steps):
        if unit.place + (steps * unit.color) < 1:
            self.move_unit(unit, abs(steps - unit.place))
        else:
            self.move_unit(unit, abs((unit.place + steps) - 24))

    def new_burn(self, pos):
        if abs(self.board[pos]) > 0:
            self.board[self.search_unit_by_place(pos)] -= 1 * (self.counter * -1)
            self.board[27 + self.counter] += 1 * (self.counter * -1)
            return True
        else:
            return False

    def burn(self, unit, pos):  # burns the unit
        if unit.place == pos or unit.place == 24 - pos:
            if abs(self.board[unit.place]) > 0:
                self.board[unit.place] += 1 * unit.color
                self.board[27 + self.counter] += 1 * unit.color
            else:
                return False

    def is_returning(self):  # checks if the player needs to return any of his units
        if self.board[25 + self.counter] != 0:
            return True
        return False

    def return_unit(self, unit, pos):  # returns the unit
        if self.counter == 0:
            if self.board[pos] >= 0:
                self.board[25] -= 1
                self.new_move_unit(unit, pos)
        else:
            if self.board[pos] <= 0:
                self.new_move_unit(unit, pos)
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

    def draw_game_board(self, dice1, dice2):  # refreshing screen basically
        i = 1
        Graphics.draw_window()
        Graphics.show_dice(dice1, 1)
        Graphics.show_dice(dice2, 2)
        Graphics.draw_dice_roll()
        while i <= 24:
            if self.board[i] > 0:
                Graphics.show_unit(Constants.White_Unit, i, self.board[i])
            else:
                Graphics.show_unit(Constants.Black_Unit, i, abs(self.board[i]))
            i += 1

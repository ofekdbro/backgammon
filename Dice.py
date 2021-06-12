import random
import Constants


def roll():
    return random.randint(1, 6)


def get_image(num):
    return Constants.Dice_image[num]

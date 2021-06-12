import Constants


class Unit:

    def __init__(self, color, place):  # constructor
        self.place = place
        self.color = color

    def set_place(self, place):  # change the unit place
        self.place = place

    def place(self):  # returns the place
        return self.place

    def color(self):  # returns the color
        return self.color

    def unit_image(self):  # returns the image of the unit by the color
        if self.color > 0:
            return Constants.White_Unit
        return Constants.Black_Unit

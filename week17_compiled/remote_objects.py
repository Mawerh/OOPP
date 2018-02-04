class Device:
    def __init__(self, type, brand, name, location, power):
        self.type = type
        self.brand = brand
        self.name = name
        self.location = location
        self.power = power

class Room:
    def __init__(self, name, length, width, position_x, position_y):
        self.name = name
        self.length = length
        self.width = width
        self.position_x = position_x
        self.position_y = position_y

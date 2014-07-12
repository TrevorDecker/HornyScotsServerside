from enum import Enum

class Food(Enum):
    Drink = 1
    Appetizer = 2
    Main = 3
    Dessert = 4

class Item:
    def __init__(self, id, name, price, section, score = 0):
        self.id = id
        self.name = name
        self.price = price
        self.section = section
        self.score = score

    def setType(self, type):
        self.type = type
    
    
    

from Item import Food
from Item import Item
import xmltodict
import urllib2
import json
from random import randint, random
import config

class Meal:
    base_scores = {Food.Drink : .5, Food.Appetizer : .5, Food.Main : .8, Food.Dessert : .2, Food.Unknown: 0.8}
    base_scale = {Food.Drink : 1000, Food.Appetizer : 1000, Food.Main : 20, Food.Dessert : 3, Food.Unknown: 1000}

    remaining_weight = {Food.Drink : .5, Food.Appetizer : .5, Food.Main : .5, Food.Dessert : .5, Food.Unknown: .5}
    total_weight = {Food.Drink : -.25, Food.Appetizer : -.25, Food.Main : -.25, Food.Dessert : -.25, Food.Unknown: -.25}
    base_weight = {Food.Drink : .5, Food.Appetizer : .5, Food.Main : .5, Food.Dessert : .5, Food.Unknown: .5}

    threshold = .25
    def __init__(self, total = 20):
        self.menu = {
            Food.Drink : [],
            Food.Appetizer : [],
            Food.Main : [],
            Food.Dessert : [],
            Food.Unknown : []}
        self.section_menu = []
        self.order = {
            Food.Drink : [],
            Food.Appetizer : [],
            Food.Main : [],
            Food.Dessert : [],
            Food.Unknown : []}
        self.options = {}
        self.total = total
        self.remaining = total
        self.count = 0
        
    def base(self, type):
        if type == Food.Unknown:
            return (Meal.base_scores[type] - (len(self.order[type]) + len(self.order[Food.Main])) * Meal.base_scale[type])
        return (Meal.base_scores[type] - len(self.order[type]) * Meal.base_scale[type])
    
    def parse_section(self, section):
        section_id = str(section["@id"])
        self.section_menu.append([])

        if not isinstance(section["items"]["item"], list):
          section["items"]["item"] = [section["items"]["item"]]

        for item in section["items"]["item"]:
            try:
                new_item = Item(item, section_id)
                self.menu[new_item.type].append(new_item)
                self.section_menu[-1].append(new_item)
                self.count += 1
            except TypeError:
                pass


    def generate_meal(self, menu):
        if menu["item-choices"]:
            for option in menu["item-choices"]["choice"]:
                self.options[option["@id"]] = { "min": option.get("min",0) , "max": option.get("max", 2) , "desc": option["name"], "options": option["options"] }
        
        if menu["menu-sections"]:
            for section in menu["menu-sections"]["section"]:
                Meal.parse_section(self, section)

        while self.remaining/self.total > min(0.2,random()) and self.count > 0:        
            for key in self.menu:
                items = self.menu[key]
                if key == Food.Drink:
                    if randint(1, 100) <= config.drink_chance:
                        continue
                if len(items) > 0:
                    item_index = randint(0, len(items) - 1)
                    item = items.pop(item_index)
                    self.eval_item(item)
                    self.count -= 1
                
        return self.order, self.total - self.remaining

    def eval_item(self, item):
        if (self.remaining == 0):
            return False
        
        if item.options:
            for option in item.options:
                item.set_option(option, self.options[option], self.remaining)
        
        remaining_scale = item.price / self.remaining
        if (remaining_scale > 1):
            return False
        
        type = item.type
        total_scale = item.price / self.total
        score = Meal.remaining_weight[type] * remaining_scale + Meal.total_weight[type] * total_scale + Meal.base_weight[type] * Meal.base(self, type)

        if (score > Meal.threshold):
            self.order[type].append(item.to_json())
            self.remaining -= item.price
            return True
        
        return False

if __name__ == "__main__":
    req = urllib2.Request('https://qa2.ghbeta.com/services/restaurant/menu?restaurantId=266581&format=xml&apiKey=IYdXcHyPq0I5adBKgDMQVpagmgU2jFuP')
    r = urllib2.urlopen(req) 
    p = r.read()
    x = xmltodict.parse(p)
    meal = Meal()
    order = meal.generate_meal(x)
    
    for items in order.values():
        for item in items:
            print item.name, item.price, str(item.type), item.config
        
        
        
        
        

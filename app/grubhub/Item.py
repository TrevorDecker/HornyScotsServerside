from enum import Enum
import config
from random import random

class Food(Enum):
    Drink = 1
    Appetizer = 2
    Main = 0
    Dessert = 3
    Unknown = 4

class Item:
    def __init__(self, item, section):
        self.id = item["@id"]
        self.name = item["name"]
        self.lower_name = self.name.lower()
        self.price = float(item["price"])
        self.section = section
        self.type = self.get_tag(item["tags"])
        if item["choices"]:
            if len(item["choices"]["choice-ref"]) == 1:
                self.options = [item["choices"]["choice-ref"]["@id"]]
            else:
                self.options = [choice["@id"] for choice in item["choices"]["choice-ref"]]
        else:
            self.options = None
        self.config = {}

    def to_json(self):
      return {
        "id": self.id,
        "name": self.name,
        "config": self.config,
        "type": self.type,
        "price": self.price,
      }

    def get_tag(self, tags):
        if tags:
            if "DRINK" in tags["tag"]:
                return Food.Drink
            if "DESSERT" in tags["tag"]:
                return Food.Dessert    
        
        if self.is_type(config.drink_base):
            return Food.Drink
        if self.is_type(config.appetizer_base):
            return Food.Appetizer
        if self.is_type(config.main_base):
            return Food.Main
        if self.is_type(config.dessert_base):
            return Food.Dessert
        if self.price > config.main_min_price:
            return Food.Main
        return Food.Unknown

    def is_type(self, type_base):
        return any(part in self.lower_name for part in type_base)
    
    def add_option(self, id, desc, data):
        if id not in self.config:
            self.config[id] = {"desc": desc, "select": []}
        self.config[id]["select"].append((data["@id"], data["description"]))
    
    def set_option(self, option_id, options, cash):
        insert = 0
        options_list = options["options"].values()[0]
        if not isinstance(options_list, list):
            options_list = [options_list]
        for option in options_list:
            price = float(option.get("option-price", 0))
            price_ratio = price/cash
            if price_ratio > random() or (insert < options["min"] and random() > 0.3):
                self.price += price
                self.add_option(option_id, options["desc"], option)
                insert += 1
            if insert == options["max"]:
                return
            

from Item import Food
from Item import Item

class Meal:
    main_price = 10
    
    base_scores = {Food.Drink : .5, Food.Appetizer : .5, Food.Main : .8, Food.Dessert : .2}
    base_scale = {Food.Drink : -1, Food.Appetizer : -.2, Food.Main : -.6, Food.Dessert : -3}

    remaining_weight = {Food.Drink : .5, Food.Appetizer : .5, Food.Main : .5, Food.Dessert : .5}
    total_weight = {Food.Drink : -.25, Food.Appetizer : -.25, Food.Main : -.25, Food.Dessert : -.25}
    base_weight = {Food.Drink : .5, Food.Appetizer : .5, Food.Main : .5, Food.Dessert : .5}

    threshold = .75
    def __init__(self, total = 15):
        self.menu = {
            Food.Drink : array(),
            Food.Appetizer : array(),
            Food.Main : array(),
            Food.Dessert : array() }
        self.order = {
            Food.Drink : array(),
            Food.Appetizer : array(),
            Food.Main : array(),
            Food.Dessert : array() }
        self.total = total
        self.remaining = total
        
    def base(type):
        return (Meal.base_scores.get(type) - len(self.order[type]) * Meal.base_scale.get(type))
    
    def parse_section(section):
        id = section["@id"]
        items = array()
        tag = 0
        if "DRINK" in section["items"]["item"][0]["tags"]["tag"]:
            tag = Food.Drink
        if "DESSERT" in section["items"]["item"][0]["tags"]["tag"]:
            tag = Food.Dessert
        
        total_price = 0
        for item in section["items"]["item"]:
            price = float(item["price"])
            items.append(Item(item["@id"], item["name"], price, id))
            total_price += price

        if (not tag):
            avg_price = total_price / len(items)
            if avg_price > Meal.main_price:
                tag = Food.Main
            else:
                tag = Food.Appetizer

        for item in items:
            item.setType(tag)
            self.menu[tag].append(item)
        

    def generate_meal(menu):
        for section in menu["menu"]["menu-sections"]["section"]:
            parse_section(section)
        
        for type in self.menu:
            for item in type:
                eval_item(item)

        return self.order

    def eval_item(item):
        remaining_scale = item.price / self.remaining
        if (remaining_scale > 1):
            return False
        
        type = item.type
        total_scale = item.price / self.total
        score = Meal.remaining_weight[type] * remaining_scale + Meal.total_weight[type] * total_scale + Meal.base_weight[type] * Meal.base(type)
        
        if (score > Meal.threshold):
            self.order[type].append(item)
            self.remaining -= item.price
            return True
        
        return False

        
        
        
        
        
        

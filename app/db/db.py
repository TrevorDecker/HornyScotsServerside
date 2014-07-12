from pymongo import MongoClient

class DB(object):
  """docstring for DB"""
  def __init__(self, host="localhost", port=27017):
    super(DB, self).__init__()
    self.client = MongoClient('localhost', 27017)
    self.db = client.linkedin_hack
    self.searches = db.searches
    self.meals = db.meals

  def make_search(lat, lng, count):
    search = {
      "lat": lat,
      "lng": lng,
      "request_num": count,
      "found": 0,
      "complete": 0,
      "sent": 0,
    }
    return self.searches.insert(search)

  def add_meal(meal, search_id):
    self.searches.update({_id: search_id}, {$inc : { found: 1, complete: 1 }})
    meal["sent"] = False
    meal["search_id"] = search_id
    self.meals.insert(meal)

  def fail_thread(search_id):
    self.searches.update({_id: search_id}, {$inc : { complete: 1 }})

  def get_meal(search_id):
    meal = self.meals.find_one({search_id: search_id, sent: False})
    if meal is None:
      return None
    self.searches.update({_id: search_id}, {$inc : { sent: 1 }})
    self.meals.update({_id: meal._id, search_id: search_id}, {$set : { sent: False }})
    return meal


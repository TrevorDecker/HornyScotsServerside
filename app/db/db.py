from pymongo import MongoClient

class DB(object):
  """docstring for DB"""
  def __init__(self, host="localhost", port=27017):
    super(DB, self).__init__()
    self.client = MongoClient('localhost', 27017)
    self.db = self.client.linkedin_hack
    self.searches = self.db.searches
    self.meals = self.db.meals

  def make_search(self, lat, lng, count):
    search = {
      "lat": lat,
      "lng": lng,
      "request_num": count,
      "found": 0,
      "complete": 0,
      "sent": 0,
    }
    return self.searches.insert(search)

  def add_meal(self, content, search_id):
    self.searches.update({"_id": search_id}, { "$inc" : { "found": 1, "complete": 1 }})
    content["sent"] = False
    content["search_id"] = search_id
    self.meals.insert(content)

  def fail_thread(self, search_id):
    self.searches.update({"_id": search_id}, { "$inc" : { "complete": 1 }})

  def get_meal(self, search_id):
    meal = self.meals.find_one({"search_id": search_id, "sent": False})
    if meal is None:
      return None
    self.searches.update({"_id": search_id}, { "$inc" : { "sent": 1 }})
    self.meals.update({"_id": meal._id, "search_id": search_id}, {"$set" : { "sent": False }})
    return meal


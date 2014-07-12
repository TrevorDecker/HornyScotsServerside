#!/usr/bin/python
import thread,time
import threading
import random
from Menu import Meal

import sys
sys.path.append('../db')
import db
TAX = 1.0875
TIP = 1.15
TOTAL_SPEND = 15

#must be defined before startSearch
#serach id is the session id for th serach
#tryNum is the number that is being used this is mostly just a seed
def thread_func(search_id,(tryNum,(gh,lat,lng,rest_list))):
  meal = None
  rest = None
  DB = db.DB()
  while meal is None:
    rest_index = random.randint(0,len(rest_list) - 1)
    rest = rest_list.pop(rest_index)
    menu = gh.rest_menu(rest["id"],lat,lng)
    meal = Meal(total = (TOTAL_SPEND/TAX - rest["deliveryFee"]) / TIP)
    meal, price = meal.generate_meal(menu)
    if price < rest["orderMin"]:
      meal = None
  if meal is None:
      #send fail message
    DB.fail_thread(search_id)
  else:
    #send sucss message to server
    order = meal[0] + meal[0.5] + meal[1] + meal[2] + meal[3]
    print order
    content = { "rest": rest, "order": order}
    DB.add_meal(content,search_id)


#called by controler 
def start_search(gh, neededMeals,serach_id,lat,lan,rest_list):
  maxTrys = 2*neededMeals
  tryNum = 0
  success = 0
  while (tryNum <= maxTrys and success <= neededMeals): 
    tryNum += 1
    try:
      thread.start_new_thread(thread_func,(serach_id,(tryNum,(gh,lat,lan,rest_list))))
      success += 1
    except:
      print "thread failed trying again\n"
  return success

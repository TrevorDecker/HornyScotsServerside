#!/usr/bin/python
import thread,time
import threading
import random
import sys
sys.path.append('../db')
import db
import grubhub as gh

#must be defined before startSearch
#serach id is the session id for th serach
#tryNum is the number that is being used this is mostly just a seed
def thread_func(search_id,(tryNum,(lat,lng,rest_ids))):
    meal = None
    tryCount = 0
    maxTrys = 10
    DB = db.DB()
    rest_id = rest_ids(random.randint(0,len(rest_ids)))
    menu = gh.rest_menu(rest_id,lat,lng)
    while meal  is None and tryCount < maxTrys:
        meal = Meal()
        meal = meal.generate_meal(menu)
    if order is None:
        #send fail message
        DB.fail_thread(search_id)
    else:
         #send sucss message to server 
         DB.add_meal(meal,search_id)


#called by controler 
def startSearch(neededMeals,serach_id,lat,lan,restids):
    maxTrys = 2*neededMeals
    tryNum = 0;
    meals = 0;
    while (tryNum <= maxTrys and meals <= neededMeals): 
        tryNum += 1
        try:
            thread.start_new_thread(thread_func,(serach_id,(tryNum,(lat,lan,restids))))
            success += 1
        except:
           print "thread failed trying again\n"
    #wait until all the threads are done
    while(threading.active_count() > 1):
        time.sleep(1)
    return  meals >= neededMeals

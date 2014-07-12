#!/usr/bin/python
import thread,time
import threading
import random
import sys
sys.path.append('../db')
import db


#must be defined before startSearch
#serach id is the session id for th serach
#tryNum is the number that is being used this is mostly just a seed
def thread_func(search_id,(tryNum,_)):
    meal = None
    tryCount = 0
    maxTrys = 10
    DB = db.DB()
    while meal  is None and tryCount < maxTrys:
        #might be infinite loop
        meal = random.randint(0,10)#call meal create
    if meal is None:
        #send fail message
        DB.fail_thread(search_id)
    else:
         #send sucss message to server 
         DB.add_meal(meal,search_id)


#called by controler 
#neededMeals the number of meals that are needed
#serach_id is the session id for the search 
#db = mongodb database
def startSearch(neededMeals,serach_id):
    maxTrys = 2*neededMeals
    tryNum = 0;
    meals = 0;
    while (tryNum <= maxTrys and meals <= neededMeals): 
        tryNum += 1
        try:
            thread.start_new_thread(thread_func,(serach_id,(tryNum,0)))
            success += 1
        except:
           print "thread failed trying again\n"
    #wait until all the threads are done
    while(threading.active_count() > 1):
        time.sleep(1)
    return  meals >= neededMeals

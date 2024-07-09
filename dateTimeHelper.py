import time                      # for time stuff
from datetime import timedelta   # also for time stuff
# from pathlib import Path         # to get location of home directory
# import configparser              # to create / read config file
# import sqlite3                   # to store/edit time logs in sqlite files

def calcTimeDiff(start: time.struct_time, end: time.struct_time):
   '''
   Returns time difference between two time.struct_time objects as a timedelta
   '''

   diff = timedelta(seconds = (time.mktime(end) - time.mktime(start)))

   return diff


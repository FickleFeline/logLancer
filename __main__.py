from pathlib import Path # to get location of home directory
import configparser # to create / read config file
import csv # to read / write log dictionaries
import time # for time stuff
from datetime import timedelta # also for time stuff
# import textual
# import argparse

class TimeEntry:
   def __init__(self, start: str, end: str, desc: str, tags: str):
      self.start = start
      self.end = end
      self.desc = desc
      self.tags = tags

def calcTimeDiff(start: time.struct_time, end: time.struct_time):
   '''
   Returns time difference between two time.struct_time objects as a timedelta
   '''

   diff = timedelta(seconds = (time.mktime(end) - time.mktime(start)))

   return diff

def startTimeLog(config: configparser.ConfigParser, storage : Path | str = "", desc: str = "", tags: str = ""):
   '''
   Creates a new entry in the current log file with all the needed data.
   If there's no current log file, it creates a new one.
   '''

   # Read || Create log file
   fields = config["expansions"]["fields"].split(",")

   # TODO: Get commandlilne (and/or TUI) arguments. i.e.: tags, description, etc...
   timeFormat = config["settings"]["timeFormat"]
   currentTime = time.gmtime()

   formattedTime = time.strftime(timeFormat, currentTime)

   newTimeLog = {"startTime":formattedTime, "endTime":"", "description": desc, "tags": tags}

   if not Path("{storage}/{currentTime.tm_year}-{currentTime.tm_mon}.csv").exists():
      with open(f"{storage}/{currentTime.tm_year}-{currentTime.tm_mon}.csv", "w") as logData:
         writer = csv.DictWriter(logData, fieldnames=fields)
         writer.writeheader()
         writer.writerow(newTimeLog)
         print(f"File written to: {storage}/{currentTime.tm_year}-{currentTime.tm_mon}.csv")

   # with open(f"{storage}/{currentTime.tm_year}-{currentTime.tm_mon}.csv", "a") as logData:
      # reader = csv.DictReader(logData)
      # logs = [row for row in reader]

   ## {{{ Testing params
   # thePast = time.strptime("24-04-15 Mon 11:30:59", timeFormat)
   ## }}}
   # print(calcTimeDiff(thePast, currentTime))


def creatDefConfig():

   # TODO: Write a function that creates a default config file

   pass

def main():

   #importing config
   config = configparser.ConfigParser()
   _ =config.read("./config.ini")

   #init storage folder:
   storage = config["settings"]["storeDataHere"]
   if (storage == ""):
      storage = Path.home() / ".logLanceData"

      # Create storage folder if it doesn't already exist
      if not Path(storage).is_dir():
         storage.mkdir()
         print(f"{storage} created!")

   elif not Path(storage).is_dir():
      print(f"The path you've given in config.ini -> storeDataHere:\n({storage})\nis invalid!\nPlease make sure the folder exists and that the path is correct")
      exit("err: invalid storage folder path")


   startTimeLog(config, storage = storage)

   return

#========================#
if __name__ == '__main__':
    main()

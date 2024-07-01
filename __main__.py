from pathlib import Path         # to get location of home directory
import configparser              # to create / read config file
import csv                       # to import/export the sqlite db to csv files
import sqlite3                   # to store/edit time logs in sqlite files
from sqlite3.dbapi2 import connect
import time                      # for time stuff
from datetime import timedelta   # also for time stuff
# import textual
# import argparse

# {{{ Helper functions

def initDefConfig():

   # TODO: Write a function that creates a default config file

   pass

def importFromCSV():
   '''
   Import data from a CSV file and create a new SQLite database from it
   '''

   pass

def exportToCSV():
   '''
   Export the SQLite databse into a CSV file.
   '''

   pass

def initDB(config: configparser.ConfigParser, pathToDB: Path | str, args: dict):
   '''
   Initiate a new time log database, based information in the config.ini file
   '''

   columns = args.keys()

   connection = sqlite3.connect(pathToDB)
   cursor = connection.cursor()

   cursor.execute(f"CREATE TABLE logs({", ".join(columns)})")

   # res = cursor.execute("SELECT name FROM sqlite_master")
   # print(res.fetchone())

   pass

def updateDB(db):
   '''
   Update database columns based on extensinos
   (Add new ones, delete no longer relevant ones)
   THIS WILL DESTROY INFORMATION WHEN DELETING COLUMNS!
   '''

   pass

def calcTimeDiff(start: time.struct_time, end: time.struct_time):
   '''
   Returns time difference between two time.struct_time objects as a timedelta
   '''

   diff = timedelta(seconds = (time.mktime(end) - time.mktime(start)))

   return diff

def getTimeLog(pathToCurrentLogFile: Path | str, range: int, which: int):
   '''
   Return the desired time log from the log file as a dictionary
   
   range:
   0: Return the whole log file
   1: Return only the last log
   2: Return specified log (by ID)

   which:
   ID of the desired log
   '''

   #Read pathToLogFile and convert it into a dictionary

   pass

def writeLogToLogFile(pathToLogFile: Path | str, log: dict):

   '''
   Writes the passed log into the provided log file.
   If it's ID is already present the old entry will be overwritten!
   '''

   pass
# }}} End of Helper funcitons

# {{{ User Facing functions

def startTimeLog(config: configparser.ConfigParser, pathToCurrentLogFile: Path | str, args: dict):
   '''
   Creates a new entry in the current log file with all the needed data.
   If there's no current log file, it creates a new one.
   '''

   # Is there a current logFile at the given path?
   ## No:
   ### init one
   ### create new timeLogEntry
   ### writeLogToLogFile()
   ### return

   # Get last log
   # Check for running task -> is there one?
   ## Yes:
   ### endTimeLog()
   ### create new timeLogEntry
   ### write to currentTimeLogFile
   ## No:
   ### create new timeLogEntry
   ### writeLogToLogFile()

   initDB(config = config, pathToDB = pathToCurrentLogFile, args = args)

   pass

def endTimeLog(config: configparser.ConfigParser, pathToCurrentLogFile: Path | str):
   '''
   Insert end dateTime to the passed log in the current log file
   '''
   
   # Get last log
   # Check whether it has an end time
   ## Yes:
   ### Throw warning
   ## No:
   ### add end time to timeLog
   ### writeLogToLogFile()

   pass

def modifTimeLog():

   pass

def deleteTimeLog():

   pass

# }}} End of User Facing functions

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


   timeFormatInStorage = config["settings"]["timeFormatInStorage"]
   currentTime = time.gmtime()

   formattedTime = time.strftime(timeFormatInStorage, currentTime)

   pathToCurrentLogFile = f"{storage}/{currentTime.tm_year}-{currentTime.tm_mon}-{currentTime.tm_mday}.tLog" # "tLog" stadns for "time log"

   # TODO: Get commandlilne (and/or TUI) arguments. i.e.: tags, description, etc...
   #{{{ PLACHOLDER VARIABLES TO BE EVENTUALLY CHANGED INTO ARGS
   description = "this is a task description"
   tags = ["FT", "00"]
   #}}}

   logArgs = {}
   logArgs["starTime"] = formattedTime
   logArgs["endTime"] = ""
   logArgs["desc"] = description
   logArgs["tags"] = tags
   

   startTimeLog(config= config, pathToCurrentLogFile= pathToCurrentLogFile, args= logArgs)

   ## {{{ Testing params
   # thePast = time.strptime("24-04-15 Mon 11:30:59", timeFormatInStorage)
   ## }}}
   # print(calcTimeDiff(thePast, currentTime))

   return

#========================#
if __name__ == '__main__':
    main()

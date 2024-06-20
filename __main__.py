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

def startTimeLog(config: configparser.ConfigParser, pathToCurrentLog: Path | str, args: dict):
   '''
   Creates a new entry in the current log file with all the needed data.
   If there's no current log file, it creates a new one.
   '''
   
   # TODO: Check for the least line of the file and
   # - If it has no end time ask user to confirm new log.
   # -- If they answer yes: add current time to endTime
   # -- if no: exith with an explanation.
   # - Else append the csv file with the new log.
   if not Path(pathToCurrentLog).exists(): # if it doesn't exist creat and append the new log entry to it
      with open(pathToCurrentLog, 'a', newline='') as csvfile:
         writer = csv.DictWriter(csvfile, fieldnames=args.keys())
         writer.writeheader()
         writer.writerow(args)
         # TODO: Figure out how to only have one title row when appending instead of adding one with every new appending of the file?
         ###
      return

   #else chechk the last 2 lines for an endTime key and value
   newestEntryRaw = lastNlines(pathToCurrentLog, 2)
   newestEntryProcessed = {}
   reader = csv.DictReader(newestEntryRaw)
   for row in reader:
      newestEntryProcessed = row
   if newestEntryProcessed["endTime"] == "":
      print("No end time found!\nWould you like to end the currently running entry and start a new one with the provided details?")
      # {{{ Testing params
      consent = True
      # }}}

      if consent:
         # TODO: In the csv file set an endTime to last entry and appent the new one to the end of the file.

         pass #placeholder pass
      else:
         print("Understood. Exiting w/o making any changes")
         return

   else:
      print(f"End time found: {newestEntryProcessed["endTime"]}")

# Function to read
# last N lines of the file
def lastNlines(fname, N):
   #Definitely not copy pasted from https://www.geeksforgeeks.org/python-reading-last-n-lines-of-a-file/ ...
     
    # assert statement check
    # a condition
    assert N >= 0
     
    # declaring variable
    # to implement 
    # exponential search
    pos = N + 1
     
    # list to store
    # last N lines
    lines = []
     
    # opening file using with() method
    # so that file get closed
    # after completing work
    with open(fname) as f:
         
        # loop which runs
        # until size of list
        # becomes equal to N
        while len(lines) <= N:
             
            # try block
            try:
                # moving cursor from
                # left side to
                # pos line from end
                f.seek(-pos, 2)
         
            # exception block 
            # to handle any run 
            # time error
            except IOError:
                f.seek(0)
                break
             
            # finally block 
            # to add lines 
            # to list after
            # each iteration
            finally:
                lines = list(f)
             
            # increasing value
            # of variable
            # exponentially
            pos *= 2
             
    # returning the
    # whole list
    # which stores last
    # N lines
    return lines[-N:]


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


   timeFormatInStorage = config["settings"]["timeFormatInStorage"]
   currentTime = time.gmtime()

   formattedTime = time.strftime(timeFormatInStorage, currentTime)

   pathToCurrentLog = f"{storage}/{currentTime.tm_year}-{currentTime.tm_mon}-{currentTime.tm_mday}.csv"

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
   

   startTimeLog(config= config, pathToCurrentLog= pathToCurrentLog, args= logArgs)

   ## {{{ Testing params
   # thePast = time.strptime("24-04-15 Mon 11:30:59", timeFormatInStorage)
   ## }}}
   # print(calcTimeDiff(thePast, currentTime))

   return

#========================#
if __name__ == '__main__':
    main()

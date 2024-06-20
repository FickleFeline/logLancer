import configparser
import time
from datetime import timedelta
# import textual
# import argparse

def calcTimeDiff(start: time.struct_time, end: time.struct_time):
   '''
   Returns time difference between two time.struct_time objects as a timedelta
   '''

   diff = timedelta(seconds = (time.mktime(end) - time.mktime(start)))

   return diff

def startTimeLog(config: configparser.ConfigParser):
   '''
   Creates a new entry in the current log file with all the needed data
   '''

   # NOTE: Get commandlilne (and/or TUI) arguments. i.e.: tags, description, etc...
   timeFormat = config["settings"]["timeFormat"]
   currentTime = time.gmtime()

   # {{{ Testing params
   thePast = time.strptime("24-04-15 Mon 11:30:59", timeFormat)
   # }}}

   
   formattedTime = time.strftime(timeFormat, currentTime)

   print(calcTimeDiff(thePast, currentTime))

   pass

def creatDefConfig():

   # TODO: Write a function that creates a default config file

   pass

def main():

   #importing config
   config = configparser.ConfigParser()
   _ =config.read("./config.ini")

   startTimeLog(config)

   return

#========================#
if __name__ == '__main__':
    main()

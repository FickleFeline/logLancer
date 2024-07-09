from pathlib import Path         # to get location of home directory
import configparser              # to create / read config file
import sqlite3                   # to store/edit time logs in sqlite files
import time                      # for time stuff
import argparse                  # for parsing CLI arguments
# import pandas as pd              # to display dicts nicely on CLI
# import csv                     # to import/export the sqlite db to csv files
# import textual                  # for creating a TUI
# from datetime import timedelta   # also for time stuff
from dbHandler import *
from dateTimeHelper import *

# TODO:
################################################################################################################
# - [ ] Start implementing dynamic cli flags and a system to handle them.                                      #
# -- Best start would be to edit the burnt in flags to be dynamically added;                                   #
#    this way you don't have to wait until you have an idea for an extension xd                                #
#                                                                                                              #
# - [ ] Handle the `--addTags` & `--removeTags` flags correctly:                                               #
# -- [ ] `--addTags`: when creating a new db entry just load its contents into the tags field BUT              #
#        when using it with the modify command make it add (only) the not yet present tags to the tags field!  #
#                                                                                                              #
# -- [ ] `--removeTags`: when called w/ the modify command have it remove any tags present in the passed list  #
#        (and prevent it from freking out when trying to remove a tag that's not present in an entry)          #
################################################################################################################

# {{{ Classes

# }}} End of Classes

# {{{ Helper functions

def initDefConfig():
   '''
   Initiates a default logLancer configuration at the root folder of the program.
   '''

   defaultConfig= configparser.ConfigParser(allow_no_value=True)
   defaultConfig['settings'] = {
      '\n'
      '# Note that in the `timeFormat` variable below you have to put two `%` signs bc the configparser uses `%` as a delimiter\n'
      'timeformatinstorage' : '%%y-%%m-%%d %%H:%%M:%%S',
      'timeformatdisplayed' : '%%y-%%m-%%d %%a %%H:%%M:%%S',
      '\n'
      '# Path to the folder you\'d like to store logLancer data (No `"`s needed around it!)\n'
      '# If left blank it defaults to ~/.logLancerData\n'
      'storedatahere' : ''
   }
   defaultConfig['extensions'] = {
      '\n'
      '# Fields ahve to be separated by a single comma and nothing else. No trailing comma at the end of the line!\n'
      'fields' : 'startTime,endTime,description,tags'
   }

   with open("./config.ini", 'w') as configfile:
      defaultConfig.write(configfile)




# {{{ CSV Import / Export should be a separate tool, nut a built in...
# def importFromCSV():
#    '''
#    Import data from a CSV file and create a new SQLite database from it
#    '''
# 
#    pass

# def exportToCSV():
#    '''
#    Export the SQLite databse into a CSV file.
#    '''
# 
#    pass
# }}} 



def updateDBColumns(db):
   '''
   Update database columns based on extensinos
   (Add new ones, delete no longer relevant ones)
   THIS WILL DESTROY INFORMATION WHEN DELETING COLUMNS!
   '''

   pass

def getTimeLog(connection: sqlite3.Connection, range: int, which: list[int]):
   '''
   Return the desired time log from the log file as a dictionary
   
   Range:
   0: Return the whole log file
   1: Return only the last log
   2: Return specified log (or range of logs) by rowid

   which:
   rowid of the desired log(s) (if relevant)
   '''

   #Read pathToLogFile and convert it into a dictionary

   pass

def writeLogToLogFile(pathToLogFile: Path | str, log: dict):

   '''
   Writes the passed log into the provided log file.
   If it's rowid is already present the old entry will be overwritten!
   '''

   pass


# obsolete # def getTestInput():
# obsolete # 
# obsolete #    
# obsolete #    #{{{ PLACHOLDER VARIABLES TO BE EVENTUALLY CHANGED INTO logArgs
# obsolete #    description = "this is a task description"
# obsolete #    tags = ["FT", "00"]
# obsolete #    #}}}
# obsolete # 
# obsolete #    config = configparser.ConfigParser()
# obsolete #    _ =config.read("./config.ini")
# obsolete #    timeformatinstorage = config["settings"]["timeformatinstorage"]
# obsolete #    currentTime = time.gmtime() # Storing time info in gmt. This should be converted into time.localtime() when displaying to the user
# obsolete #    formattedTime = time.strftime(timeformatinstorage, currentTime)
# obsolete # 
# obsolete #    testInput:dict[str, int|str|list[int|str]] = {}
# obsolete #    testInput["startTime"] = formattedTime
# obsolete #    testInput["endTime"] = ""
# obsolete #    testInput["description"] = description
# obsolete #    testInput["tags"] = tags
# obsolete # 
# obsolete #    return testInput

# }}} End of Helper funcitons

#{{{ TUI/CLI Shenanigans

def parseCLI():
   '''
   Handle user input (or lack there of) from the command line
   '''

   # TODO: Dynamically add arguments so that extensions can add their own!

   # Adding basic info about the app
   parser = argparse.ArgumentParser(
      prog="logLancer",
      description="A flexible terminal tool for keeping time logs of your activities",
      epilog="=== Yeah... 🦆 ==="
   )


   # {{{ Adding arguments
   _ = parser.add_argument("-s",
                           "--startLog",
                           help = "End any currently running logs and start a new one and any additional arguments will edit this newly created entry",
                           action = "store_true")

   _ = parser.add_argument("-e",
                           "--endLog",
                           help = "Add an end time to the latest log, if it is still, running (and any additional arguments will edit this newly created entry?)",
                           action= "store_true")

   _ = parser.add_argument("-t",
                           "--addTags",
                           type= str,
                           help = "Add tags (separated by `, `) to the selected entry \n(on using -s/--startLog for eg.)",
                           action= "extend",
                           nargs= "+",
                           dest= "tags")

   _ = parser.add_argument("-T",
                           "--removeTags",
                           type= str,
                           help = "Remove tags (separated by `, `) from the selected entry \n(on using -s/--startLog for eg.)",
                           action= "extend",
                           nargs= "+",
                           dest= "removeTags")

   _ = parser.add_argument("-d",
                           "--description",
                           type= str,
                           help= "Define the description of the selected entry")

   ## Add extension arguments (if there's any)


   # }}} End of Adding arguments


   retArgs = vars(parser.parse_args()).copy() # Using .copy() @ the end bc w/o it after conversion both the namespace variables and the retArgs dict would point to the same memory address, ergo changing one would change the other as well and vica-versa.
   
   return retArgs


def initTTUI(): # initTextualTerminalUserInterface

   pass

#}}} End of TUI/CLI Shenanigans

# {{{ User Facing functions
def getUserInput(config: configparser.ConfigParser):

   # TODO: Get commandlilne (and/or TUI) arguments. i.e.: tags, description, etc...
   # Two ways to get user inputs:
   # 1) [/] using CLI
   # -- [x] Burnt in fields
   # -- [ ] Dynamic fields and extension required inputs !!!
   # 2) [ ] using Textual TUI
   # -- This route first has to have a MWP Textual TUI that lets the user call sth like "start new time log" function that then prompts them to input params


   userInput = parseCLI()

   # print(f'User input:\n- {userInput}')

   formattedUserInput = {}

   # Filling in fields based on user input
   for key in config["extensions"]["fields"].split(','):
      # print(f"Key: {key}")
      if " ".join(userInput.keys()).find(key) != -1: # If the field has a user input value assigned do this, otherwise assigne an empty string as value
         formattedUserInput[f'{key}'] = userInput[f'{key}']
      else:
         formattedUserInput[f'{key}'] = ''

   # Adding rest of the user inputs as nonField key & value pairs
   for key in userInput.keys():
      if " ".join(formattedUserInput.keys()).find(key) == -1: # If the userInput key not present in formatted user input key add its value as nonField
         formattedUserInput[f'{key}-nonField'] = userInput[f'{key}']
         # print(f"KeyS: {userInput.keys()}\nKey: {key}")


   # print(formattedUserInput)
   return formattedUserInput


def editTimeLog():

   pass

def deleteTimeLog():

   pass


# }}} End of User Facing functions

def main():

   #importing config or init the default one, if there's none
   config = configparser.ConfigParser()
   if Path("./config.ini").exists():
      _ =config.read("./config.ini")
   else:
      initDefConfig()
      _ =config.read("./config.ini")

   #init storage folder:
   storage = config["settings"]["storedatahere"]
   if (storage == ""):
      storage = Path.home() / ".logLanceData"

      # Create storage folder if it doesn't already exist
      if not Path(storage).is_dir():
         storage.mkdir()
         config["settings"]["storeDateHere"] = str(storage)
         print(f"{storage} created!")
   elif not Path(storage).is_dir():
      print(f"The path you've given in config.ini -> storedatahere:\n({storage})\nis invalid!\nPlease make sure the folder exists and that the path is correct")
      exit("err: invalid storage folder path")


   timeformatinstorage = config["settings"]["timeformatinstorage"]
   currentTime = time.gmtime() # Storing time info in gmt. This should be converted into time.localtime() when displaying to the user

   lcTime = time.localtime(time.mktime(currentTime)) # current local time
   formattedTime = time.strftime(timeformatinstorage, currentTime)

   pathToCurrentLogFile = f"{storage}/{lcTime.tm_year}-{lcTime.tm_mon}.timelog"
   del lcTime


   logArgs = getUserInput(config)
   fieldArgs = {}

   for key in logArgs.keys():
      if key.find("nonField") == -1:
         fieldArgs[f'{key}'] = logArgs[f'{key}']
      if key.find("startTime") != -1:
         fieldArgs[f'{key}'] = formattedTime

   
   # Is there a current logFile at the given path?
   if not Path(pathToCurrentLogFile).exists():
   ## No:
      ## init one
      msg = "No existing database found for the provided time period; creating new one..."
      print(msg)
      initDB(config = config, pathToDB= pathToCurrentLogFile, fieldArgs= fieldArgs)

   #{{{ open and setup connection to time log database
   connection = sqlite3.connect(pathToCurrentLogFile)
   connection.row_factory = sqlite3.Row # Queries now return Row objects
   #}}}

   startTimeLog(config= config, connection= connection, fieldArgs= fieldArgs)

   ## {{{ Testing params
   # thePast = time.strptime("24-04-15 Mon 11:30:59", timeformatinstorage)
   ## }}}
   # print(calcTimeDiff(thePast, currentTime))

   connection.close()
   return

#========================#
if __name__ == '__main__':
    main()

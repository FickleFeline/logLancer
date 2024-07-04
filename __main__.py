from pathlib import Path         # to get location of home directory
import configparser              # to create / read config file
import sqlite3                   # to store/edit time logs in sqlite files
import time                      # for time stuff
from datetime import timedelta   # also for time stuff
import argparse                  # for parsing CLI arguments
# import pandas as pd              # to display dicts nicely on CLI
# import csv                     # to import/export the sqlite db to csv files
# import textual                  # for creating a TUI


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


def initDB(config: configparser.ConfigParser, pathToDB: Path | str, fieldArgs: dict):
   '''
   Initiate a new time log database, based information in the config.ini file
   '''

   columns = fieldArgs.keys()

   connection = sqlite3.connect(pathToDB)
   cursor = connection.cursor()

   try:
      cursor.execute(f"CREATE TABLE logsTable({", ".join(columns)})")

   except Exception as e:
      print(f"logLancer is trying to create an already existing table in the function 'initDB()'\n\nException:\n{e}")

   # res = cursor.execute("SELECT name FROM sqlite_master")
   # print(res.fetchone())

   connection.commit()
   cursor.close()

   connection.close()

def updateDBColumns(db):
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

def updateDBRow(connection: sqlite3.Connection, rowToUpdate: sqlite3.Row , updatedFieldsAsDict: dict):
   '''
   Updates row in the database using the current connection,
   based on available fields in the provided dictionary.
   (Dict keys are CASE SENSITIVE)

   Returns the updated row as a dictionary
   '''

   cursor = connection.cursor()

   # {{{ Prepping the sql command for execution in a safe way™️(?)
   editedRow = {}
   dynamicTokens = ""
   for key in rowToUpdate.keys(): # In theory this block should prevent sql injections bc this way the operation uses placeholder tokens (instead of using f"strings" for adding variable values into it)??
      if key != "rowid":
         dynamicTokens += f"{key} = :{key}, "
         if " ".join(updatedFieldsAsDict.keys()).find(key) == -1: # If the key can't be found in the updatedFieldsAsDict's keys, just copy rowToUpdate's values.
            editedRow[f'{key}'] = rowToUpdate[f'{key}']
         else:
            editedRow[f'{key}'] = updatedFieldsAsDict[f'{key}']

   dynamicTokens = dynamicTokens[:-2]

   editRow = f"""
      UPDATE logsTable SET {dynamicTokens} WHERE rowid = {rowToUpdate['rowid']}
   """
   # }}}

   ## add end time to timeLog
   _ = cursor.execute(editRow, editedRow)

   ## writeLogToLogFile()
   connection.commit()
   # print("==============================\nRow with added edited fields:")
   # print(list(cursor.execute("SELECT rowid, * FROM logsTable").fetchall()[-1]))

   cursor.close()
   return editedRow

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
   Handle user input from the command line or lack there of
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
                           "--tags",
                           type= str,
                           help = "Define tags (separated by `, `) on the selected entry \n(on using -s/--startLog for eg.)",
                           action= "extend",
                           nargs= "+",)

   _ = parser.add_argument("-d",
                           "--description",
                           type= str,
                           help= "Define the description of the selected entry")

   ## Add extension arguments (if there's any)


   # }}} End of Adding arguments


   retArgs = vars(parser.parse_args()).copy() # Using .copy() @ the end bc w/o it after conversion both the namespace variables and the retArgs dict would point to the same memory address, ergo changing one would change the other as well and vica-versa.
   
   # if args.tags is not None:
      # NOTE: TO CONSIDER: When processing tags take escape characters into account
      # E.g.: "foo, bar, beer, one\, single\, tag"
      # Bc rn escaped commas aren't really escaped: when splitting the tags
      # arg into a list it ignors the effect `\` should have on text...
   #    print(f"Tags as read:\n- {args.tags}\nTags as list:\n- {args.tags.split(", ")}")

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
      if " ".join(userInput.keys()).find(key) != -1: # If the field has a user input value assign it, otherwise assigne an empty string as value
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

def startTimeLog(config: configparser.ConfigParser, connection: sqlite3.Connection, fieldArgs: dict):
   '''
   Puts an endTime on the latest entry w/o an endTime (if there's any) then,
   creates a new entry in the current log file with all the needed data.
   '''

   cursor = connection.cursor()

   # Check for running task -> is there one?

   try:
      lastRow = cursor.execute("SELECT rowid, * FROM logsTable").fetchall()[-1]
      if lastRow["endTime"] == "": # this line checks the value of the endTime field. If it's empty that means that the task is still running.
         ## Yes:
         endTimeLog(config = config, connection= connection, logArgs= fieldArgs, row = lastRow)
         # print(list(cursor.execute("SELECT rowid FROM logsTable").fetchall()[-1]))
   except Exception as e:
      msg = "No entries in database; skipping endTime check"
      print(f"---\nAn exception occured:\n- {e}\nGuess:\n- {msg}\n---\n")


   ## create new timeLogEntry

   dynamicTokens = ""
   for key in fieldArgs.keys():
      dynamicTokens += f":{key}, "
      if isinstance(fieldArgs[f'{key}'], list):
            fieldArgs[f'{key}'] = f"{"; ".join(fieldArgs[f'{key}'])}"

   dynamicTokens = dynamicTokens[:-2]

   addNewRow = f"""
      INSERT INTO logsTable VALUES
         ({dynamicTokens})
   """
   _ = cursor.execute(addNewRow, fieldArgs)
   

   ## writeLogToLogFile()

   connection.commit()

   # print("============================================\nNew row added:")
   # print(list(cursor.execute("SELECT rowid, * FROM logsTable").fetchall()[-1]))

   cursor.close()
   return


def endTimeLog(config: configparser.ConfigParser, row:sqlite3.Row , logArgs: dict, connection: sqlite3.Connection):
   '''
   Insert end time to the passed log in the current log file
   '''
   
   localLogArgs = logArgs

   # Get log

   # Check whether it has an end time

   if row["endTime"] != '':
      ## Yes:
      ## Throw warning
      msg = "This entry already has an end time"
      print(msg)
      return
   else:
      ## No:
      addedEndTime = {"endTime" : localLogArgs["startTime"]}
      row = updateDBRow(connection= connection, rowToUpdate= row, updatedFieldsAsDict=addedEndTime)

      # print("==============================\nRow with added end time:")
      # print(list(cursor.execute("SELECT rowid, * FROM logsTable").fetchall()[-1]))

      detailTimeLog(config= config, row= row)


def editTimeLog():

   pass

def deleteTimeLog():

   pass

def detailTimeLog(config: configparser.ConfigParser, row: sqlite3.Row):
   '''
   Print the passed db row to the screen
   '''

   timeFormatInStorage = config["settings"]["timeFormatInStorage"]
   timeFormatDisplayed = config["settings"]["timeFormatDisplayed"]
   
   this = {}

   for key in row.keys():
      this[f'{key}'] = row[f'{key}']

   this["startTime"] = (time.strftime(timeFormatDisplayed, time.strptime(this["startTime"], timeFormatInStorage)))
   this["endTime"] = (time.strftime(timeFormatDisplayed, time.strptime(this["endTime"], timeFormatInStorage)))
   
   print("===\nEnded log's details:")
   print(''.join('{}:\n- {}\n'.format(key, val) for key, val in this.items())[:-1])
   print("===")



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

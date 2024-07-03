from pathlib import Path         # to get location of home directory
import configparser              # to create / read config file
import sqlite3                   # to store/edit time logs in sqlite files
import time                      # for time stuff
from datetime import timedelta   # also for time stuff
# import csv                       # to import/export the sqlite db to csv files
# import textual
# import argparse

# {{{ Helper functions

def initDefConfig():

   # TODO: Write a function that creates a default config file
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
   defaultConfig['expansions'] = {
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


def initDB(config: configparser.ConfigParser, pathToDB: Path | str, logArgs: dict):
   '''
   Initiate a new time log database, based information in the config.ini file
   '''

   columns = logArgs.keys()

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
   2: Return specified log (by rowid)

   which:
   rowid of the desired log
   '''

   #Read pathToLogFile and convert it into a dictionary

   pass

def writeLogToLogFile(pathToLogFile: Path | str, log: dict):

   '''
   Writes the passed log into the provided log file.
   If it's rowid is already present the old entry will be overwritten!
   '''

   pass
# }}} End of Helper funcitons

# {{{ User Facing functions

def startTimeLog(config: configparser.ConfigParser, connection: sqlite3.Connection, logArgs: dict):
   '''
   Puts an endTime on the latest entry w/o an endTime (if there's any) then,
   creates a new entry in the current log file with all the needed data.
   '''

   cursor = connection.cursor()

   # Check for running task -> is there one?

   try:
      lastRow = cursor.execute("SELECT rowid, endTime FROM logsTable").fetchall()[-1]
      if lastRow["endTime"] == "": # this line checks the value of the endTime field. If it's empty that means that the task is still running.
         ## Yes:
         endTimeLog(config = config, connection= connection, logArgs= logArgs, rowid= lastRow["rowid"])
         # print(list(cursor.execute("SELECT rowid FROM logsTable").fetchall()[-1]))
   except Exception as e:
      msg = "No entries in database; skipping endTime check"
      print(f"---\nAn exception occured:\n- {e}\nGuess:\n- {msg}\n---\n")


   ## create new timeLogEntry

   dynamicTokens = ""
   for key in logArgs.keys():
      dynamicTokens += f":{key}, "
      if isinstance(logArgs[f'{key}'], list):
            logArgs[f'{key}'] = f"{"; ".join(logArgs[f'{key}'])}"

   dynamicTokens = dynamicTokens[:-2]

   addNewRow = f"""
      INSERT INTO logsTable VALUES
         ({dynamicTokens})
   """
   _ = cursor.execute(addNewRow, logArgs)
   

   ## writeLogToLogFile()

   connection.commit()

   # print("============================================\nNew row added:")
   # print(list(cursor.execute("SELECT rowid, * FROM logsTable").fetchall()[-1]))

   cursor.close()
   return


def endTimeLog(config: configparser.ConfigParser, rowid: int, logArgs: dict, connection: sqlite3.Connection | str = ""): # TODO: Add func variables: "connection". if these are not provided give them a blank string as value and deal with it below.
   '''
   Insert end dateTime to the passed log in the current log file
   '''
   
   localLogArgs = logArgs
   localConnection :sqlite3.Connection

   # {{{ If there's no connection passed create one to the current db
   if connection == "":
      storage = config["settings"]["storedatahere"]
      pathToCurrentLogFile = f"{storage}/{localLogArgs["startTime"].tm_year}-{localLogArgs["startTime"].tm_mon}.timelog"
      connection = sqlite3.connect(pathToCurrentLogFile)
      connection.row_factory = sqlite3.Row # Queries now return Row objects
   else:
      localConnection = connection
   # }}}

   # Get log

   cursor = localConnection.cursor()
   row = cursor.execute(f"SELECT rowid, * FROM logsTable WHERE rowid = {rowid}").fetchone()


   # Check whether it has an end time

   if row["endTime"] != '':
      ## Yes:
      ## Throw warning
      msg = "This entry already has an end time"
      print(msg)
      return
   else:
      ## No:
      editedRow = {}
      dynamicTokens = ""
      for key in row.keys():
         if key != "rowid" or key != "endTime":
            dynamicTokens += f"{key} = :{key}, "
            editedRow[f'{key}'] = row[f'{key}']

      editedRow["endTime"] = localLogArgs["startTime"]

      dynamicTokens = dynamicTokens[:-2]

      editRow = f"""
         UPDATE logsTable SET {dynamicTokens} WHERE rowid = {rowid}
      """

      
      ## add end time to timeLog

      _ = cursor.execute(editRow, editedRow)


      ## writeLogToLogFile()

      localConnection.commit()
      # print("==============================\nRow with added end time:")
      # print(list(cursor.execute("SELECT rowid, * FROM logsTable").fetchall()[-1]))

      cursor.close()

      # {{{ if there was no connection passed in the function call close previously created connection
      if connection == "":
         localConnection.close()
      # }}}

def modifTimeLog():

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
      print("NO!!!")
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

   formattedTime = time.strftime(timeformatinstorage, currentTime)

   pathToCurrentLogFile = f"{storage}/{currentTime.tm_year}-{currentTime.tm_mon}.timelog"

   # TODO: Get commandlilne (and/or TUI) arguments. i.e.: tags, description, etc...
   #{{{ PLACHOLDER VARIABLES TO BE EVENTUALLY CHANGED INTO logArgs
   description = "this is a task description"
   tags = ["FT", "00"]
   #}}}

   logArgs = {}
   logArgs["startTime"] = formattedTime
   logArgs["endTime"] = ""
   logArgs["desc"] = description
   logArgs["tags"] = tags
   

   
   # Is there a current logFile at the given path?
   if not Path(pathToCurrentLogFile).exists():
   ## No:
      ## init one
      msg = "No existing database found for the provided time period; creating new one..."
      print(msg)
      initDB(config = config, pathToDB= pathToCurrentLogFile, logArgs= logArgs)

   #{{{ open and setup connection to time log database
   connection = sqlite3.connect(pathToCurrentLogFile)
   connection.row_factory = sqlite3.Row # Queries now return Row objects
   #}}}


   startTimeLog(config= config, connection= connection, logArgs= logArgs)

   ## {{{ Testing params
   # thePast = time.strptime("24-04-15 Mon 11:30:59", timeformatinstorage)
   ## }}}
   # print(calcTimeDiff(thePast, currentTime))

   connection.close()
   return

#========================#
if __name__ == '__main__':
    main()

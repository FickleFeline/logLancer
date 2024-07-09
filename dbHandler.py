from pathlib import Path         # to get location of home directory
import configparser              # to create / read config file
import sqlite3                   # to store/edit time logs in sqlite files
import time                      # for time stuff

#}}} End of Imports


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

def detailTimeLog(config: configparser.ConfigParser, row: sqlite3.Row):
   '''
   Print the passed db row to the screen
   '''

   timeFormatInStorage = config["settings"]["timeFormatInStorage"]
   timeFormatDisplayed = config["settings"]["timeFormatDisplayed"]
   
   this = {}

   for key in row.keys():
      this[f'{key}'] = row[f'{key}']

      # {{{ Format escape charachters in string inputs (safely?)
      if type(this[f'{key}']) == str:
         this[f'{key}'] = this[f'{key}'].replace("\\n", "\n") # new line
         this[f'{key}'] = this[f'{key}'].replace("\\t", "\t") #tab
      # }}} End of Format escape charachters in string inputs (safely?)

   this["startTime"] = (time.strftime(timeFormatDisplayed, time.strptime(this["startTime"], timeFormatInStorage)))
   this["endTime"] = (time.strftime(timeFormatDisplayed, time.strptime(this["endTime"], timeFormatInStorage)))
   
   print("===\nEnded log's details:")
   print(''.join('{}:\n- {}\n'.format(key, val) for key, val in this.items())[:-1])
   print("===")

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

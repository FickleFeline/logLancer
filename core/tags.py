
import argparse                   # for parsing CLI arguments
# from pathlib import Path          # to get location of home directory
# import configparser               # to create / read config file
# import sqlite3                    # to store/edit time logs in sqlite files
# import time                       # for time stuff
# import pandas as pd             # to display dicts nicely on CLI
# import csv                      # to import/export the sqlite db to csv files
# import textual                  # for creating a TUI
# from datetime import timedelta  # also for time stuff
# from dbHandler import *
# from dateTimeHelper import *

def defineFlags(parser:argparse.ArgumentParser):

   thisParser = parser

   _ = thisParser.add_argument("-t",
                           "--addTags",
                           type= str,
                           help = "Add tags to the selected entry (on using -s/--startLog for eg.)\nUseage e.g.:\n`logLancer -s -t \"tag1\" \"tag2\" \"etc\" --someOtherFlagOptionally`",
                           action= "extend",
                           nargs= "+",
                           dest= "tags")

   _ = thisParser.add_argument("-T",
                           "--removeTags",
                           type= str,
                           help = "remove tags to the selected entry (on using -s/--startLog for eg.)\nUseage e.g.:\n`logLancer -s -T \"tag1\" \"tag2\" \"etc\" --someOtherFlagOptionally`",
                           action= "extend",
                           nargs= "+",
                           dest= "removeTags")

   return thisParser



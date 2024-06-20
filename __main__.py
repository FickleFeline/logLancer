import time
# import textual
# import argparse

def calcTimeDiff(start, end, format):
   '''
   Returns time difference between two dateTime objects in the given format
   '''

   diff = time.strftime(format, time.localtime(time.mktime(end) - time.mktime(start)))

   return diff


def main():
   # This is the main function #
   currentTime = time.localtime()

   timeFormat = "%y-%m-%d %a %H:%M:%S"
   formattedTime = time.strftime(timeFormat, currentTime)

   print (formattedTime)

   return

#========================#
if __name__ == '__main__':
    main()

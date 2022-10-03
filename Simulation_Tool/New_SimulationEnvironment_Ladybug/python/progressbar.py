from __future__ import print_function

import time
import math

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = 'X', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = 100 * (iteration / float(total))
    #percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
   
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    message = "\r"
    message +=  "%s |%s| %s %% %s" % (prefix, bar, str(round(percent, decimals)), suffix)

    #print(message),
    print(message,end="")

    # Print New Line on Complete
    if iteration == total: 
        
        print(message)

if __name__ == "__main__"  :
    for i in range(12):
        printProgressBar(i,11, length=20)
        time.sleep(0.2)

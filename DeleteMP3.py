import os
import glob

def Start():
    y = 0
    try:
        for x in glob.glob('/home/yasser/Desktop/desktop/Python_Bot/*.mp3'):
            y += 1
            print("removing " + x)
            os.remove(x)
    finally:
        print("Done, removed " + str(y) + " files")
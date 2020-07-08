import os
import glob

def image_flush(filepath,exception=None):
    files=glob.glob(filepath)
    for f in files:
        if f!=exception:
            os.remove(f)
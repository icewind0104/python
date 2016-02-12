#!/bin/python3

import os, sys

def getFile(path, tail='', hid=False):
# tail used to find witch files their name end by tail
    path = path + '/' if path[-1] !='/' else path	# append '/'

    dirList = []
    for x in os.listdir(path):
        if (os.path.isdir(path+x)
            or
            (((not hid) or (hid and x[1] != '.' or x[-1] != '~'))
            and ((not tail) or (tail and x.endswith(tail))))):
# choose to except hidden or unmatch files and does not affect directors
            dirList.append(x)

    allFiles = [f for f in dirList if os.path.isfile(path + f)]
    d = [f for f in dirList if os.path.isdir(path + f)]
    for f in d:
        allFiles += getFile(path + f, tail, hid)
    return allFiles

print(len(sys.argv))

#print(getFile(Path, tail))


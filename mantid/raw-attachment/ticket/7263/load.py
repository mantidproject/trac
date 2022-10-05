from mantid.simpleapi import *

import time

s = 'MUSR00015189.nxs'
n = 30

start = time.time()
for i in range(n):
    w = Load(Filename=s)
    print w,type(w)
end = time.time()

print "Duration = %f seconds" % (end-start)

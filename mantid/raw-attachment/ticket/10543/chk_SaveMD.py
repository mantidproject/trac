#Basic python script to isolate a crash case when using SaveMD()

import sys,os
#Import Mantid computatinal modules
sys.path.append(os.environ['MANTIDPATH'])
from mantid.simpleapi import *     

#Change path and file to point appropriately to the MD workspace you want to load
path='C:\Users\mid\Documents\Mantid\Powder\CalcProj\\'  #will read input and save output to this directory
file='zrh_1000_PCalcProj.nxs'
print "*** Loading in Workspace: ",path+file
md=LoadMD(path+file)
print "  md.id(): ",md.id()

#Create a 1D cut
print "*** Using BinMD() to create a cut"
cut=BinMD(md,AlignedDim0="|Q|,1,10,1",AlignedDim1="DeltaE,0,900,100")
print "  cut.id(): ",cut.id()

#Save this cut
cutfile='cut.nxs'
print "*** Saving cut to file: ",path+cutfile
SaveMD(cut,path+cutfile)

#Load the "cut" workspace back in
print "*** Loading file: ",path+cutfile
cut2=LoadMD(path+cutfile)
print "  cut2.id(): ",cut2.id()

#Now save the cut2 workspace back out - this step usually crashes
cut2file='cut2.nxs'
print "*** Attempting to re-save workspace"
try:
    print "*** Saving file: ",path+cut2file
    SaveMD(cut2,path+cut2file)
except:
    print "*** Unable to save workspace to file: ",path+cut2file


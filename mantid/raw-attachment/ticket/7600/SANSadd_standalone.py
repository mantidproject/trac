from mantidsimple import *
from shutil import copyfile
# mantidinstall/bin/mantid.user.properties     needs e.g.
#     datasearch.directories = U:/Processed ; N:/cycle_09_4
#     defaultsave.directory = C:/Mantidinstall/genie

path="/archive/ndxsans2d/instrument/data/cycle_13_2/"
#path="Y:/cycle_12_1/"
# put this at end of file        runlist=[11972,11981]

def add_runs(path,runlist):
  print "here we go"
# assume pathout,  assume runs are all integers, will crash at present if try adding to an nnn-add
#                 U:/ needs to point to //isis/inst$/ndxSans2d/user/
#
# 25/03/10   BUG  - at least from RKH's office,  python insists on putting  an extra  "\user"   in the output path ! 
#                 so is saving to    u:\user\processed\  instead of  u:\processed    thereby creating    u:\user\user\processed\
#                 it does this regardless of which of the two versions of "pathout" I use below.
#  so you may need to move the created add files !
#
  pathout=""
  #pathout="//isis/inst$/ndxSans2d/processed/"  
  pfix="SANS2D"
  sfix=".nxs"
  b=range(len(runlist)-1)
 #
 # get the first file in list
  nzeros=8-len(str(runlist[0]))
  fpad=""
  for ii in range(nzeros):
	fpad+="0"
#
  filename=path+pfix+fpad+str(runlist[0])+sfix
  print "reading file:   "+filename
  m1=LoadNexus(Filename=filename,OutputWorkspace="added")
  
  for i in b:
    snum=str(runlist[i+1])
    nzeros=8-len(snum)
    fpad=""
    for ii in range(nzeros):
	  fpad+="0"
    filename=path+pfix+fpad+snum
    print "reading file:   "+filename+sfix   
    m2=LoadNexus(Filename=filename+sfix,OutputWorkspace="wtemp")
    Plus("added","wtemp","added")
    mantid.deleteWorkspace("wtemp")
# now save the added file
  #print "pathout="+pathout
  print "writing file:   "+pathout+pfix+fpad+snum+"-add"+sfix
  SaveNexusProcessed("added",pathout+pfix+fpad+snum+"-add"+sfix)  
  mantid.deleteWorkspace("added")
# copy the log file for last run to U:/ , though search list should find it in orgianal space also.
  copyfile(path+pfix+fpad+snum+".log",pathout+pfix+fpad+snum+".log")


# Rob's code
#def fname(rnum):
 # path=nr.isisDataDir
 #inst=nr.isisInstrument
 # ext=nr.isisExt
 # 
 #nzeros=8-len(str(rnum))
 # fpad=""
  #for i in range(nzeros):
    #fpad+="0"

  #filename=path+inst+fpad+str(rnum)+ext
  #return filename

# In the interests of sanity run the stuff from the bottom so that function gets redefined before it is run
# Just run the two lines below for subseqent additions

runlist=[19675, 19682, 19689]
add_runs(path,runlist)

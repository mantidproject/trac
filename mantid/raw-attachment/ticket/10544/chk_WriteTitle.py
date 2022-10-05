#Basic python script to verify that changed workspace titles took effect

import sys,os
#Import Mantid computatinal modules
sys.path.append(os.environ['MANTIDPATH'])
from mantid.simpleapi import *     

#Change path and file to point appropriately to the MD workspace you want to load
path='C:\Users\mid\Documents\Mantid\Powder\CalcProj\\'  #will read input and save output to this directory
file='zrh_1000_PCalcProj.nxs'
print "*** Loading in Workspace: ",path+file
ws=LoadMD(path+file)
title_orig=ws.getTitle()
print "  Original title: ",title_orig
#change title
title_new=title_orig+' this is a new title'
print "  Title to be added to workspace: ",title_new
ws.setTitle(title_new)
#print new title
title_current=ws.getTitle()
print "  Title set in workspace: ",title_current

if title_current == title_orig:
    print "Setting workspace title did not take"
elif title_current == title_new:
    print "The new title was set properly in the workspace"
    #in this case, save the workspace, then re-load it to see if the new title is still there
    file='zrh_1000_PCalcProj_newTitle.nxs'
    print "*** Saving workspace: ",path+file
    SaveMD(ws,path+file)
    print "*** Loading workspace: ",path+file
    wsReload=Load(path+file)
    title_reload=wsReload.getTitle()
    if title_reload == title_new:
        print "--> The new title was saved and recalled properly!"
        print "  Title to be saved: ",title_new
        print "  Title from reloaded workspace: "
    else:
        print "--> title mismatch between the workspace to be saved and the reloaded workspace...unlucky..."
        print "  Title to be saved: ",title_new
        print "  Title from reloaded workspace: ",title_reload
else:
    print "Problem: Title mismatch between original and that set"
    



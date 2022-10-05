#Basic python script to verify that changed workspace comments took effect

import sys,os
#Import Mantid computatinal modules
sys.path.append(os.environ['MANTIDPATH'])
from mantid.simpleapi import *     

#Change path and file to point appropriately to the MD workspace you want to load
path='C:\Users\mid\Documents\Mantid\Powder\CalcProj\\'  #will read input and save output to this directory
file='zrh_1000_PCalcProj.nxs'
print "*** Loading in Workspace: ",path+file
ws=LoadMD(path+file)
comment_orig=ws.getComment()
print "  Original comment: ",comment_orig
#change comment
comment_new=comment_orig+' this is a new comment'
print "  Comment to be added to workspace: ",comment_new
ws.setComment(comment_new)
#print new comment
comment_current=ws.getComment()
print "  Comment set in workspace: ",comment_current

if comment_current == comment_orig:
    print "Setting workspace comment did not take"
elif comment_current == comment_new:
    print "The new comment was set properly in the workspace"
    #in this case, save the workspace, then re-load it to see if the new comment is still there
    file='zrh_1000_PCalcProj_newComment.nxs'
    print "*** Saving workspace: ",path+file
    SaveMD(ws,path+file)
    print "*** Loading workspace: ",path+file
    wsReload=Load(path+file)
    comment_reload=wsReload.getComment()
    if comment_reload == comment_new:
        print "--> The new comment was saved and recalled properly!"
        print "  Comment to be saved: ",comment_new
        print "  Comment from reloaded workspace: "
    else:
        print "--> Comment mismatch between the workspace to be saved and the reloaded workspace...unlucky..."
        print "  Comment to be saved: ",comment_new
        print "  Comment from reloaded workspace: ",comment_reload
else:
    print "Problem: comment mismatch between original and that set"
    



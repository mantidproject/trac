from IndirectJumpFit import JumpRun
sname = 'iris21360_graphite002_QLd_Workspace'
qrange = [0.0, 5.0]
verbOp = False
plotOp = False
saveOp = False

filename = sname+'.nxs' # path name for nxs file
LoadNexusProcessed(Filename=filename, OutputWorkspace=sname)
JumpRun(sname,'CE',0,qrange[0],qrange[1],verbOp,plotOp,saveOp)


import IndirectBayes as Main

nbins = [1, 1]
nbs = [50, 30]
sname = 'irs26176_graphite002_red'
rname = 'irs26173_graphite002_res'
resNormFile = 'irs26173_graphite002_ResNorm'
erange = [-0.5, 0.5]
fitOp = [True, 'Sloping', False, True] # elastic, background, width, resnorm 
loopOp = True
verbOp = False
plotOp = 'None'
saveOp = False

spath = sname+'.nxs'   # path name for sample nxs file
LoadNexusProcessed(Filename=spath, OutputWorkspace=sname)
rpath = rname+'.nxs'    # path name for res nxs file
LoadNexusProcessed(Filename=rpath, OutputWorkspace=rname)
rspath = resNormFile+'_Paras.nxs'    # path name for resNorm nxs file
LoadNexusProcessed(Filename=rspath, OutputWorkspace=resNormFile)
Main.QuestRun(sname,rname,resNormFile,nbs,erange,nbins,fitOp,loopOp,verbOp,plotOp,saveOp)
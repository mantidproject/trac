import IndirectBayes as Main

nbins = ['1', '1']
sname = 'irs26176_graphite002_red'
rname = 'irs26173_graphite002_res'
rsname = 'irs26173_graphite002_ResNorm'
wfile = ''
erange = [-0.5, 0.5]
fitOp = [True, 'Sloping', False, True] #elastic, background, width, resnorm
loopOp = True
verbOp = True
plotOp = False
saveOp = False

spath = sname+'.nxs'    # path name for sample nxs file
LoadNexusProcessed(Filename=spath, OutputWorkspace=sname)
rpath = rname+'.nxs'    # path name for res nxs file
LoadNexusProcessed(Filename=rpath, OutputWorkspace=rname)
rspath = rsname+'_Paras.nxs'    # path name for resNorm nxs file
LoadNexusProcessed(Filename=rspath, OutputWorkspace=rsname)
Main.QLRun('QL',sname,rname,rsname,erange,nbins,fitOp,wfile,loopOp,verbOp,plotOp,saveOp)
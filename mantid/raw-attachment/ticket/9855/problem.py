SHOWPROBLEM = True

LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12008/nexus/CORELLI_687.nxs.h5', OutputWorkspace='COR_687')
ConvertUnits(InputWorkspace='COR_687', OutputWorkspace='COR_687_d', Target='dSpacing')

if SHOWPROBLEM is False:
  Rebin(InputWorkspace='COR_687_d', OutputWorkspace='COR_687_d', Params='0.04')
else:
  Rebin(InputWorkspace='COR_687_d', OutputWorkspace='COR_687_d', Params='0.004')
  
ws = mtd["COR_687_d"]
print "After Rebin in d-spacing, Memory size of workspace %s is %.5f MB" %(str(ws), ws.getMemorySize()/1024./1024.)

ConvertUnits(InputWorkspace='COR_687_d', OutputWorkspace='COR_687_d', Target='TOF')

ws = mtd["COR_687_d"]
print "After ConvertUnits to TOF, Memory size of workspace %s is %.5f MB" %(str(ws), ws.getMemorySize()/1024./1024.)
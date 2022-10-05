import os.path

def readPlotList(filename):
	'''
	Reads in a text file with run numbers to plot. 8 first characters of each line are nexus file
	names without extension that must be loaded.
	
	Returns a list of nexus file names to load
	'''
	if not os.path.exists( filename ):
		raise Exception('Cannot find file ' + filename)
		
	dir = os.path.dirname( filename )
	fileList = []
	
	f = open(filename,'r')
	for line in f:
		if len(line) >= 8:
			runName = os.path.join( dir, line[:8] + '.nxs' )
			fileList.append( runName )
	f.close()
	
	return fileList
	
def setNumericAxis(wsname):
	from mantidsimple import createNumericAxis, mtd
	thPlot = mtd[wsname]
	axis = createNumericAxis(thPlot.getNumberHistograms())
	thPlot.replaceAxis( 1, axis )	
	
def createThermoWS( fileList ):
	'''
	Loads the nexus files in fileList. The files must contain workspace groups, each member
	workspace must contain 1 spectrum.
	'''
	i = 0
	nEntries = -1
	groups = []
	thermoWS = []
	
	# load the file
	for f in fileList:
		wsName = '_thermo_plot_' + str(i)
		i += 1
		ws = Load( f, OutputWorkspace = wsName )
		# check that all workspaces have the same size
		n = ws.getNumberOfEntries()
		if nEntries < 0:
			nEntries = n
		elif n != nEntries:
			raise Exception('Workspace groups have different sizes')
		groups.append( wsName )
	
	for i in range( 1, nEntries+1 ):
		# construct a comma-separated list of member workspace names
		workspaces = ('_'+str(i)+',').join(groups)+'_'+str(i)
		thPlot = ConjoinSpectra(InputWorkspaces=workspaces,OutputWorkspace='ThermoPlot_'+str(i),WorkspaceIndex=0)
		thermoWS.append( thPlot.getName() )
		setNumericAxis(thPlot.getName())
		ax1 = thPlot.getAxis(1)
		for i in range(ax1.length()):
			ax1.setValue(i,i)
		
#	for ws in groups:
#		DeleteWorkspace( ws )

	return thermoWS

if __name__ == "__main__":
	fileList = readPlotList(r'PlotList.txt')
	workspaces = createThermoWS( fileList )
	m = importMatrixWorkspace(workspaces[0])
	m.plotGraph2D()
	m.plotGraph3D()
	

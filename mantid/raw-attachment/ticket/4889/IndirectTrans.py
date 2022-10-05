# Transmission main
#
from mantidsimple import *
from mantidplotpy import *
import numpy

def UnwrapMon(inWS):
# Unwrap monitor - inWS contains M1,M2,S1  - outWS contains unwrapped Mon
	outWS = 'Mon'
#Unwrap s1>2 to L of S2 (M2) ie 38.76  Ouput is in wavelength
	alg = UnwrapMonitor(InputWorkspace=inWS,OutputWorkspace=outWS,LRef='37.86')
	join = float(alg.getPropertyValue("JoinWavelength"))
#Fill bad (dip) in spectrum
	RemoveBins(outWS,outWS,join-0.001,join+0.001,Interpolation="Linear")
	FFTSmooth(outWS,outWS,0)									# Smooth - FFT
	mtd.deleteWorkspace(inWS)								# delete monWS
	return outWS

def TransMon(type,file,verbose):
	if verbose:
		mtd.sendLogMessage('Raw file : '+file)
	LoadRaw(Filename=file,OutputWorkspace='__m1',SpectrumMin=1,SpectrumMax=1)
	LoadRaw(Filename=file,OutputWorkspace='__m2',SpectrumMin=2,SpectrumMax=2)		
	LoadRaw(Filename=file,OutputWorkspace='__det',SpectrumMin=3,SpectrumMax=3)		
# Check for single or multiple time regimes
	MonTCBstart = mtd['__m1'].readX(0)[0]
	SpecTCBstart = mtd['__det'].readX(0)[0]	
	mtd.deleteWorkspace('__det')								# delete monWS
	monWS = '__Mon'
	if (SpecTCBstart == MonTCBstart):
		monWS = UnwrapMon('__m1')	# unwrap the monitor spectrum and convert to wavelength
		RenameWorkspace(monWS,'__Mon1')		
	else:
		ConvertUnits('__m1','__Mon1',"Wavelength")
	ConvertUnits('__m2','__Mon2',"Wavelength")		
	mtd.deleteWorkspace('__m2')								# delete monWS
	Xin = mtd['__Mon1'].readX(0)
	xmin1 = mtd['__Mon1'].readX(0)[0]
	xmax1 = mtd['__Mon1'].readX(0)[len(Xin)-1]
	Xin = mtd['__Mon2'].readX(0)
	xmin2 = mtd['__Mon2'].readX(0)[0]
	xmax2 = mtd['__Mon2'].readX(0)[len(Xin)-1]
	wmin = max(xmin1,xmin2)
	wmax = min(xmax1,xmax2)
	CropWorkspace('__Mon1','__Mon1',wmin,wmax)
	RebinToWorkspace('__Mon2','__Mon1','__Mon2')
	monWS = file[0:8] +'_'+ type
	Divide('__Mon2','__Mon1',monWS)
	mtd.deleteWorkspace('__Mon1')								# delete monWS
	mtd.deleteWorkspace('__Mon2')								# delete monWS

def IDATransStart(sfile,cfile,verbose=False):
	TransMon('Sam',sfile,verbose)
	TransMon('Can',cfile,verbose)
	samWS = sfile[0:8] + '_Sam'
	canWS =cfile[0:8] + '_Can'
	trWS = sfile[0:8] + '_Tr'
	Divide(samWS,canWS,trWS)
	trans = numpy.average(mtd[trWS].readY(0))
	transWS = sfile[0:8] + '_Trans'
	workdir = mantid.getConfigProperty('defaultsave.directory')
	group = samWS +','+ canWS +','+ trWS
	GroupWorkspaces(InputWorkspaces=group,OutputWorkspace=transWS)
	path = os.path.join(workdir,transWS+'.nxs')
	SaveNexusProcessed(transWS,path)
	if verbose:
		mtd.sendLogMessage('Transmission : '+str(trans))
		mtd.sendLogMessage('Output file created : '+path)
	

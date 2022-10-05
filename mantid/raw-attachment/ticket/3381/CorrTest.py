# Correction - applies absoption correction 

from MantidFramework import *
from mantidsimple import *
from mantidplot import *
import math, os.path as op

def ReadNxsFile(name,ana,ext):
	workdir = mantid.getConfigProperty('defaultsave.directory')
	file = name+'_'+ana+'_'+ext+'.nxs'
	path = op.join(workdir, file)					# path name for nxs file
	LoadNexusProcessed(file,name)

def getEfixed(workspace, detIndex=0):
    det = mtd[workspace].getDetector(detIndex)
    try:
        efixed = det.getNumberParameter('Efixed')[0]
    except AttributeError:
        ids = det.getDetectorIDs()
        det = mtd[workspace].getInstrument().getDetector(ids[0])
        efixed = det.getNumberParameter('Efixed')[0]
    return efixed

def conjoincreated(input, name, unit):
	dataX = []
	dataY = []
	dataE = []
	NoSpectra = 0
	specDet = []
	for ws in input:
		curWS = mtd[ws]
		nSpec = curWS.getNumberHistograms()
		NoSpectra += nSpec
		axis1 = curWS.getAxis(1)
		for s in range(0, nSpec):
			det = curWS.getDetector(s)
			specDet.append([axis1.spectraNumber(s), det.getID()])
			readX = curWS.readX(s)
			readY = curWS.readY(s)
			readE = curWS.readE(s)
			for i in range(0, len(readX)):
				dataX.append(readX[i])
			for i in range(0, len(readY)):
				dataY.append(readY[i])
			for i in range(0, len(readE)):
				dataE.append(readE[i])
	conjoined = CreateWorkspace(name, dataX, dataY, dataE, NoSpectra, UnitX=unit).workspace() #Comes with a spectra axis from 1->NoSpectra
	newSpectraAxis = createSpectraAxis(len(specDet)) # We one that has the correct spectrum numbers as defined by the input workspace
	for i in range(len(specDet)):
		newSpectraAxis.setValue(i,specDet[i][0])
		spectra = conjoined.getSpectrum(i)
		spectra.setDetectorID(specDet[i][1])
	conjoined.replaceAxis(1, newSpectraAxis)
	# We need to do this each time because a band new workspace has been created with no instrument and hence no detector IDs
	# The first time it will take a bit of time but subsequent runs it will be very quick
	LoadInstrument(Workspace=conjoined,InstrumentName='OSIRIS',RewriteSpectraMap=False)

def CorrRun(ncan,sname,cname,geom):
	workdir = mantid.getConfigProperty('defaultsave.directory')
	samWS=sname
	ext = 'ass'
	assWS = ext
	tmp = mantid.getMatrixWorkspace(samWS)
	s_hist = tmp.getNumberHistograms()
	efixed = getEfixed(samWS)
	ConvertUnits(samWS,samWS,'Wavelength','Indirect',efixed)
	if ncan > 1:
		canWS = cname
		efix = getEfixed(canWS)
		ediff = efix-efixed
		if ediff > 0.001:
			error = 'Can efixed (' +str(efix) + ') not = Sample (' +str(efixed) +')'	
			exit(error)
		ConvertUnits(canWS,canWS,'Wavelength','Indirect',efixed)
	corrWS = sname +'_Correct_'+ cname[3:8]
	csamWS = 'SamCor'
	ccanWS = 'CanCor'
	for n in range(0,s_hist):
		ExtractSingleSpectrum(samWS,csamWS,n)
		if ncan == 1:
			if n == 0:
				CloneWorkspace(csamWS,corrWS)				# for first time, rename tempWS as output WS
			else:
				list = [corrWS,csamWS]
				conjoincreated(list, corrWS, 'Wavelength')
#				ConjoinWorkspaces(corrWS,csamWS)				# subsequent times, add tempWS to output WS
		else:
			ExtractSingleSpectrum(canWS,ccanWS,n)
			smcWS = 'SminusC'
			Minus(csamWS,ccanWS,smcWS)
			
			if n == 0:
				CloneWorkspace(smcWS,corrWS)				# for first time, rename tempWS as output WS
			else:
				list = [corrWS,smcWS]
				conjoincreated(list, corrWS, 'Wavelength')
#				ConjoinWorkspaces(corrWS,smcWS)				# subsequent times, add tempWS to output WS
	if ncan > 1:
		 ConvertUnits(canWS,canWS,'DeltaE','Indirect',efixed)
	ConvertUnits(samWS,samWS,'DeltaE','Indirect',efixed)
	CloneWorkspace(corrWS,'corr')
	ConvertUnits('corr','corrE','DeltaE','Indirect',efixed)
	ConvertUnits(corrWS,corrWS,'DeltaE','Indirect',efixed)
#	mantid.deleteWorkspace(csamWS)
#	mantid.deleteWorkspace(ccanWS)
	mantid.deleteWorkspace(smcWS)
	SaveNexusProcessed(corrWS,op.join(workdir,corrWS+'.nxs'))

def CorrStart(prog,ncan,ana,sname,cname,geom):
	ReadNxsFile(sname,ana,'red')
	tWS = mantid.getMatrixWorkspace(sname)
	s_hist = tWS.getNumberHistograms()       # no. of hist/groups in sam
	if ncan == 2:
		ReadNxsFile(cname,ana,'red')
		tWS = mantid.getMatrixWorkspace(cname)
		c_hist = tWS.getNumberHistograms()       # no. of hist/groups in sam
		if s_hist != c_hist:								# check that no. groups are the same
			error = 'Can histograms (' +str(c_hist) + ') not = Sample (' +str(s_hist) +')'	
			exit(error)
	if prog == 'Correct':
		CorrRun(ncan,sname,cname,geom)



#Fury - version for individual spectra
import os.path as op

prefix = 'irs'
ana_dict = {'xtal' : 'PG', 'refl' : '002', 'code' : 1, 'efix' : 0.1}
prog = 'FURY'

inWS = 'In'
s_load = LoadNexusProcessedDialog(OutputWorkspace=inWS,Message="Sample file")
s_path = s_load.getPropertyValue("Filename")
s_file = op.basename(s_path)
print 'Sample file : ' + s_file
tmp = mantid.getMatrixWorkspace(inWS)
s_hist = tmp.getNumberHistograms()
e_range = "-0.5,0.005,0.5"
samWS = 'Sam'
sqtWS = 'Sqt'
sam_list = []
# loop over all histograms/groups
for n in range(0, s_hist):
	n1=str(n)
	stmpWS = sqtWS + str(n)
# get individual group into temp WS
	ExtractSingleSpectrum(inWS,samWS,n1)
# rebin to constant delta-e
	Rebin(samWS,samWS,e_range)
# perform FFT
	FFT(samWS, stmpWS)
# get modulus - index 2
	ExtractSingleSpectrum(stmpWS,stmpWS,2)
	sam_list.append(stmpWS)
#	if n == 0:
# for first time, rename tempWS as output WS
#		RenameWorkspace(stmpWS,sqtWS)
#	else:
# subsequent times, add tempWS to output WS
#		ConjoinWorkspaces(sqtWS,stmpWS)
s_graph=plotSpectrum(sam_list,0)
# delete temp WS
mantid.deleteWorkspace(inWS)
mantid.deleteWorkspace(samWS)

r_load = LoadNexusProcessedDialog(OutputWorkspace=inWS,Message="Resolution file")
r_path = r_load.getPropertyValue("Filename")
r_file = op.basename(r_path)
print 'Resolution file : ' + r_file
tmp = mantid.getMatrixWorkspace(inWS)
r_hist = tmp.getNumberHistograms()

# check that no. groups are the same
if s_hist == r_hist:
	resWS = 'Res'
	rqtWS = 'Rqt'
	iqtWS = 'Iqt'
	res_list = []
	iqt_list = []
	for n in range(0, s_hist):
		n1=str(n)
		rtmpWS = rqtWS + str(n)
		itmpWS = iqtWS + str(n)
# get individual group into temp WS
		ExtractSingleSpectrum(inWS,resWS,n1)
# rebin to constant delta-e
		Rebin(resWS,resWS,e_range)
# perform FFT
		FFT(resWS, rtmpWS)
# get modulus - index 2
		ExtractSingleSpectrum(rtmpWS,rtmpWS,2)
		res_list.append(rtmpWS)
		Divide(stmpWS,rtmpWS,itmpWS)
#		if n == 0:
# for first time, rename tempWS as output WS
#			RenameWorkspace(tmpWS,sqtWS)
#		else:
# subsequent times, add tempWS to output WS
#			ConjoinWorkspaces(sqtWS,tmpWS)
	r_graph=plotSpectrum(res_list,0)

else:
# error message
	print 'Vanadium histograms (' +v_hist + ') not = Sample (' + s_hist +')'


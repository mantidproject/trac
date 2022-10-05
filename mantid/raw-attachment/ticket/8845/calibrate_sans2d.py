import tube
from tube_calib_fit_params import TubeCalibFitParams
import numpy
#ws = Load(Filename=r'\\olympic\Babylon5\Public\rkh\SANS2dTubes\SANS2D60024183.nxs',Precount='0')
#ws = ws.rebin('5.5,100000,100000', PreserveEvents=False)
#ws = Integration(ws)
#for i in range(ws.getNumberHistograms()):
#	if ws.readY(i)>1500:
#	  ws.dataY(i)[:] = 0
#SaveNexusDialog(ws)

ws = Load('work_with_this_data.nxs')
known_pos1 = numpy.array([-0.475,	-0.437,	-0.353,	-0.315,	-0.231,	-0.193,	-0.109,	-0.071,	0.013,	0.051,	0.135,	0.173,	0.257,	0.295,	0.379,	0.417])
known_pos2 = numpy.array([-0.445,	-0.407,	-0.323,	-0.285,	-0.201,	-0.163,	-0.079,	-0.041,	0.043,	0.081,	0.165,	0.203,	0.287,	0.325,	0.409,	0.447])

# left tubes
knownPositions = known_pos1
funcForm = [2]*len(knownPositions)
pixel_positions = numpy.array([20, 39, 80, 100, 140, 160, 200, 220, 262, 282, 323, 342, 383, 401, 444, 462])
margin=10
fitPar = TubeCalibFitParams(pixel_positions, outEdge=10.0, inEdge=10.0)
tubes = range(60)
caltable = tube.calibrate(ws, 'rear-detector',knownPositions, funcForm, rangeList=tubes,plotTube=[10,20,30,40,50], margin=margin, fitPar=fitPar)




# right tubes
knownRight = known_pos2
pixel_right = [29, 47, 90, 109, 152, 172, 215, 234, 277, 297, 340, 359, 402, 422, 465, 484]

fitPar = TubeCalibFitParams(pixel_right, outEdge=10.0, inEdge=10.0)
tubes = range(60,120)
caltable = tube.calibrate(ws, 'rear-detector',knownRight, funcForm, rangeList=tubes, plotTube= [60,80,90,100], margin=margin, fitPar=fitPar, calibTable=caltable)


ApplyCalibration(ws, caltable)
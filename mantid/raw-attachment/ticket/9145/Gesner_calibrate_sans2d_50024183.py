import tube
from tube_calib_fit_params import TubeCalibFitParams
from tube_calib import getCalibration  #rkh
import numpy
#ws = Load(Filename=r'\\olympic\Babylon5\Public\rkh\SANS2dTubes\SANS2D60024183.nxs',Precount='0')
#ws = ws.rebin('5.5,100000,100000', PreserveEvents=False)
#ws = Integration(ws)
#for i in range(ws.getNumberHistograms()):
#	if ws.readY(i)>1500:
#	  ws.dataY(i)[:] = 0
#SaveNexusDialog(ws)

#ws = Load('work_with_this_data.nxs')
# slighlty changed mask positions for a data set with M4 out, ~60 counts/pixel
# due to b/s shadow, edge 9 has to be ingored for tubes 36 to 43 (in 0 to 119), which will be  left 18,19,20 ,21  and right 18,19,20,21 ,
#                                                                                                                                which are here  tubes 19 to 22   and 79 to 82,  
#                                                                                                                                  or python        range(18,22) and range(78,82)     [I think!]
ws0=Load(Filename='c:/mantidinstall/data/SANS2D50024183.nxs')
ws=Integration(ws0)
known_pos1 = numpy.array([-0.485,	-0.447,	-0.372,	-0.334,	-0.259,	-0.221,	-0.146,	-0.108,	-0.033,	0.005,	0.08,	0.118,	0.193,	0.231,	0.306,	0.344,	0.419,	0.457])
known_pos2 = numpy.array([-0.455,	-0.417,	-0.342,	-0.304,	-0.229,	-0.191,	-0.116,	-0.078,	-0.003,	0.035,	0.11,	0.148,	0.223,	0.261,	0.336,	0.374,	0.449,	0.487])

# left tubes
knownPositions = known_pos1
funcForm = [2]*len(knownPositions)
#pixel_positions = numpy.array([20, 39, 80, 100, 140, 160, 200, 220, 265, 287, 323, 342, 383, 401, 444, 462,485,495])
pixel_positions = numpy.array([8,30,65,87,125,145,180,205,240,270,302,330,350,372,405,435,465,490])
# margin is really for Gaussian, outEdge, inEdge are pixel tolerances for edges (are these absolute, or relative to the fitted edge?), should avoid spikes etc at edges if keep > 10 pixles clear?
margin=10
fitPar = TubeCalibFitParams(pixel_positions, outEdge=10.0, inEdge=10.0)

#  this should be 60, but make smaller for debug, but thenchange the plotTube list
tubes = range(60)
#  the plotTube list defines which tubes get TubePlotnn and FittedTubenn workspaces left to check           e.g.      plotTube=[10,20,30,40,50]
caltable = tube.calibrate(ws, 'rear-detector',knownPositions, funcForm, rangeList=tubes,plotTube=[0,1,58,59], margin=margin, fitPar=fitPar)

# now do left tubes 18 to 21 skipping the 9th edge
knownPositions2 =  numpy.array([-0.485,	-0.447,	-0.372,	-0.334,	-0.259,	-0.221,	-0.146,	-0.108,	0.005,	0.08,	0.118,	0.193,	0.231,	0.306,	0.344,	0.419,	0.457])
funcForm = [2]*len(knownPositions2)
pixel_positions2 = numpy.array([8,30,65,87,125,145,180,205,270,302,330,350,372,405,435,465,490])
# margin is really for Gaussian, outEdge, inEdge are pixel tolerances for edges (are these absolute, or relative to the fitted edge?), should avoid spikes etc at edges if keep > 10 pixles clear?
margin=10
fitPar = TubeCalibFitParams(pixel_positions2, outEdge=10.0, inEdge=10.0)
tubes = range(18,22)
#  the plotTube list defines which tubes get TubePlotnn and FittedTubenn workspaces left to check           e.g.      plotTube=[10,20,30,40,50]
caltable = tube.calibrate(ws, 'rear-detector',knownPositions2, funcForm, rangeList=tubes,plotTube=tubes, margin=margin, fitPar=fitPar, calibTable=caltable)


# right tubes
knownRight = known_pos2
funcForm = [2]*len(knownRight)
#pixel_right = [29, 47, 90, 109, 152, 172, 215, 234, 277, 297, 340, 359, 402, 422, 465, 484]
pixel_right=pixel_positions+10
print len(pixel_right), " edges right", pixel_right
fitPar = TubeCalibFitParams(pixel_right, outEdge=10.0, inEdge=10.0)
# range (60,120) does start at 61, which is right0
tubes = range(60,120)
caltable = tube.calibrate(ws, 'rear-detector',knownRight, funcForm, rangeList=tubes, plotTube=[0,1,58,59], margin=margin, fitPar=fitPar, calibTable=caltable)

# now redo tubes right 18 to 21, skipping 9th edge
# find some python wat to chop out the 9th elemnet of a list or array!
knownRight2 = numpy.array([-0.455,	-0.417,	-0.342,	-0.304,	-0.229,	-0.191,	-0.116,	-0.078,	0.035,	0.11,	0.148,	0.223,	0.261,	0.336,	0.374,	0.449,	0.487])
funcForm = [2]*len(knownRight2)
pixel_right2=numpy.array([18,40,75,97,135,155,190,215,280,312,340,360,382,415,445,475,500])
print len(pixel_right2), " edges right", pixel_right2
fitPar = TubeCalibFitParams(pixel_right2, outEdge=10.0, inEdge=10.0)
tubes = range(78,82)
caltable = tube.calibrate(ws, 'rear-detector',knownRight2, funcForm, rangeList=tubes, plotTube=tubes, margin=margin, fitPar=fitPar, calibTable=caltable)



# to see the resukts in show instrument, the "Full 3d" plot does not get adjusted, need to try "cylindrical Y" view
ApplyCalibration(ws, caltable)


# REPLACE the EVENT mode file
ApplyCalibration(ws0, caltable)

SaveNexus(ws0,'c:/mantidinstall/data/SANS2D50024183.nxs')

SaveNexus("calibTable",'c:/mantidinstall/genie/tube_calibrationTable_1to1.nxs')

# why do this ? no change and  no useful info in them
#ModifyDetectorDotDatFile(ws,"c:/mantidinstall/data/detector_gastubes_01.dat","c:/mantidinstall/data/detector_gastubes_01__calibrated.dat")	


# thus is the method to UNDO a calibration
#empty_instr = LoadEmptyInstrument('c:/MANTIDINSTALL/instrument/LARMOR_Definition.xml')
#CopyInstrumentParameters(empty_instr, ws_Cal_14)

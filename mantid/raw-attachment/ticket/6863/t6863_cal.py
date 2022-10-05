######################################################################
#
# This is a partial copy from LeBailFitScript.py
#
# Python Script as Step 1 of Le Bail Fitting to
# 1. Load file
# 2. Create LeBailFitInput
# 3. Fit Peaks
#
# Step 1:   Load data, model (HKL list) and starting instrument parameters values,
#           and do an initial LeBailFit/calculation to see how much the starting
#           values are off;

#|-------------------------------------------------------------------------------------------
#|Step 2.1: Fit single peaks for TOF_h, Alpha, Beta, and Sigma;
#|
#|Step 2.2: Plot parameters (TOF_H, Alpha, Beta and Sigma) against d-spacing;
#|
#|Step 2.3: Remove the peaks with bad fit;
#|
#|Step 2.4: Refine instrument geometry parameters; 
#| 
#|          It is possible to loop back to Step 2 to include more peaks with single peaks
#|-------------------------------------------------------------------------------------------
#
# Step 5: Do Le Bail Fit from previous result to see whether the peak parameters are 
#         close enough for Le Bail Fit
#
# !Step 6: Fit Alpha, Beta and apply the change to 
#
# !Step 7: Save the result files to HDD for Step 6, LeBailFit in random walk;
# 
# Step 8: Save the result files to HDD for Step 6, LeBailFit in random walk;
#
# Step 7: Not in this script;
#
# Step 8: Process Monte Carlo results from Step 6
#
#
######################################################################
from Calibration_ImportInformation import *

#--------------  Definition of Global Variables ---------------------
bankid = 0

datafilename = "" 
hklfilename = ""
irffilename = ""

# montecarlofilename = ""
# expirffilename = ""

datawsname = ""
instrparamwsname = ""
braggpeakparamwsname = ""

# outdataws1name = ""

minpeakheight = 0.001

# Range for Le Bail Fit of all peaks 
startx = -1
endx =  -1
# Range for fitting single peaks for step 1~3 
tofmin_singlepeaks = -1
tofmax_singlepeaks = -1

backgroundtype = "Polynomial"
backgroundorder = 6
bkgdtablewsname = ""
bkgdwsname = ""
bkgdfilename = ""
usrbkgdpoints = ''

latticesize = 4.1568899999999998
#--------------------------------------------------------------------


def setupGlobals(infofilename):
    """ Set up globals values
    """
    global datafilename, hklfilename, irffilename  
    global datawsname, instrparamwsname, braggpeakparamwsname
    global bkgdtablewsname, bkgdwsname, bkgdfilename, backgroundorder
    global tofmin_singlepeaks, tofmax_singlepeaks, startx, endx
    global bankid, latticesize
    global usrbkgdpoints

    bankid, calibDict = importCalibrationInformation(infofilename)
    bankid = int(bankid)

    datafilename = calibDict["DataFileDir"] + calibDict[bankid]["DataFileName"] 
    hklfilename  = calibDict["HKLFileDir"]  + calibDict[bankid]["HKLFileName"]
    irffilename  = calibDict["IrfFileDir"]  + calibDict[bankid]["IrfFileName"]
    
    startx = float(calibDict[bankid]["LeBailFitMinTOF"])
    endx   = float(calibDict[bankid]["LeBailFitMaxTOF"])

    # Name of workspaces
    datawsname = calibDict[bankid]["DataWorkspace"]
    instrparamwsname     = "Bank%sInstrumentParameterTable" % (bankid)
    braggpeakparamwsname = 'BraggPeakParameterTable'

    # Background related
    usrbkgdpoints   = calibDict[bankid]["UserSpecifiedBkgdPts"]
    bkgdwsname      = datawsname+"_Background"
    backgroundtype  = calibDict["BackgroundType"]
    backgroundorder = int(calibDict["BackgroundOrder"])
    bkgdfilename    = calibDict["WorkingDir"] + datawsname + "_Parameters.bak'"
    bkgdwsname      = datawsname + "_Background"
    bkgdtablewsname = datawsname + "_Background_Parameters"

    # Other constants
    latticesize   = calibDict[bankid]["LatticeSize"]

    return

#------------------------------------------------------------------------------
# TableWorkspace Processing
#------------------------------------------------------------------------------
def parseRefineGeometryMCResultWorkspace(tablews):
    """ Parse the refinement result workspac
    """
    numrows = tablews.rowCount()
    numcols  = tablews.columnCount()
    colnames = tablews.getColumnNames()

    parameterdict = {}

    for irow in xrange(numrows):
        ppdict = {}
        for icol in xrange(numcols):
            colname = colnames[icol]
            value = tablews.cell(irow, icol)
            ppdict[colname] = value
        # ENDFOR Column
        chi2 = ppdict["Chi2"]

        parameterdict[chi2] = ppdict
    # ENDFOR

    return parameterdict


#def updateInstrumentParameterValue(tablews, paramdict):
#    """ Update the value to an instrument parameter table
#    """
#    paramnames = paramdict.keys()
#    for parname in paramnames: 
#        parvalue = paramdict[parname]
#	# print "%s = %f" % (parname, parvalue)
#	if parname.count("Chi2") == 0:
#	    # Only update parameters nothing to do with chi2
#            UpdatePeakParameterTableValue(InputWorkspace=tablews,
#		Column='Value',
#                ParameterNames=[parname],
#		NewFloatValue=parvalue)
#
#    return

	
def doStep3():
    """ Step 3: to check whether the refinement result is good for low-d region
    """
    global startx, endx
    global datawsname, instrparamwsname, braggpeakparamwsname
    global bkgdtablewsname, bkgdwsname, backgroundtype, backgroundorder
    global bankid
    global usrbkgdpoints

    # 1. Process background 
    bkgdwsname = datawsname+"_Background"
    ProcessBackground(InputWorkspace=datawsname, 
            OutputWorkspace=bkgdwsname, 
            Options='SelectBackgroundPoints',
            LowerBound=startx, 
            UpperBound=endx, 
            BackgroundType=backgroundtype,
            BackgroundPoints=usrbkgdpoints,
            NoiseTolerance='0.10000000000000001')

    functionstr = "name=%s,n=%d" % (backgroundtype, backgroundorder)
    for iborder in xrange(backgroundorder+1):
        functionstr = "%s,A%d=%.5f" % (functionstr, iborder, 0.0)
    print "Background function: %s" % (functionstr)

    Fit(Function='name=Polynomial,n=6,A0=0.657699,A1=3.68433e-05,A2=-1.29638e-08,A3=1.16778e-12,A4=-4.71439e-17,A5=8.8499e-22,A6=-6.26573e-27',
            InputWorkspace=bkgdwsname,
            MaxIterations='1000',
            Minimizer='Levenberg-MarquardtMD',
            CreateOutput='1',
            Output=bkgdwsname,
            StartX=startx,
            EndX=endx)

    # 2. Do calculation
    usemcresult = True
    try:
        bestmdws = mtd["BestMCResult1"]
    except KeyError:
        usemcresult = False

    outwsname = datawsname + "_Calculated"
    if usemcresult is True:
        # Use MC N results 
        paramdict = parseRefineGeometryMCResultWorkspace(bestmtdws)

        raise NotImplementedError("Case 1")

        index = 0
        maxoutput = 1
        for chi2 in sorted(paramdict.keys()):
            # 1. Update parameter values
            updateInstrumentParameterValue(mtd["Bank%sInstrumentParameterTable1"%(bankid)], paramdict[chi2])
	    
	    print "Fit range: %f , %f" % (startx, endx)
	
            LeBailFit(InputWorkspace=datawsname,
                OutputWorkspace=outwsname,
                InputParameterWorkspace='Bank%dInstrumentParameterTable1'%(bankid),
                OutputParameterWorkspace='Bank%dInstrumentParameterTable1_%d'%(bankid, index),
                InputHKLWorkspace='BraggPeakParameterTable1',
                OutputPeaksWorkspace='BraggPeakParameterTable2_%d'%(index),
                Function='Calculation',		            
		FitRegion                       = '%f, %f' % (startx, endx),
                BackgroundType='Polynomial',
                BackgroundParametersWorkspace=bkgdtablewsname, 
                UseInputPeakHeights='0',
                PeakRadius='8',
                Minimizer='Levenberg-Marquardt')

            print "Pattern %s:  Instrumental Geometry Chi^2 = %.5f" % ('CalculatedPattern%d'%(index), chi2)
            index += 1
            if index >= maxoutput:
            	break
        # ENDFOR
    else:
        # Use Version 2 result
       
        # data from manually refinement
        # for pair in [("Dtt1", 22529.600), ("Dtt1t", 22747.400), ("Zerot", 15.792320), ("Width", 1.1072)]:

        # data from Jason's
        # for pair in [("Dtt1", 22584.512), ("Dtt1t", 22604.852), ("Zerot", 11.317320), ("Width", 1.0521)]:

        index = 0
        print "Fit range: %f , %f" % (startx, endx)
        LeBailFit(InputWorkspace=datawsname,
            OutputWorkspace=outwsname,
            InputParameterWorkspace='Bank1InstrumentParametersTable',
            OutputParameterWorkspace='Bank%dInstrumentParameterTable1_%d'%(bankid, index),
            InputHKLWorkspace='BraggPeakParameterTable1',
            OutputPeaksWorkspace='BraggPeakParameterTable2_%d'%(index),
            Function='Calculation',
	    FitRegion                       = '%f, %f' % (startx, endx),
            BackgroundType='Polynomial',
            BackgroundParametersWorkspace=bkgdtablewsname, 
            UseInputPeakHeights='0',
            PeakRadius='8',
            Minimizer='Levenberg-Marquardt')

    return

def main(argv):
    """ Main
    """    
    setupGlobals("Calibration_Information.config")
    
    print "Le Bail Fit Calibration Instrument... Step 3"
    doStep3()

    return


if __name__=="__main__": 
    main(["LeBailFitScript"])

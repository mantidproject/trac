####################################################################################################
#
# This script is migrated from Calibration_Step3.py. 
# The plan is to convert it to a Mantid algorithm later. 
#
######################################################################
#--------------  Definition of Global Variables ---------------------
bankid = 0

datafilename = "" 
hklfilename = ""
irffilename = ""

# montecarlofilename = ""
# expirffilename = ""

datawsname = ""
instrparamwsname = ""

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

class ExamineProfileParameters:
    """ Class to do it
    """
    def __init__(self):
        """ Initialization
        """

        return

    def importGlobals(self, infofilename):
        """ Import global (all scripts) variables 
        """
        self.bankid = 2

        # Material
        self.latticesize   = 4.1568899999999998 

        # Input files
        self.datafilename = "PG3_11486-2.dat"
        self.hklfilename  = "LB4853b2.hkl"
        self.irffilename  = "2011B_HR60b2.irf"
        
        self.datawsname = "PG3_11486"

        self.backgroundtype  = "Polynomial"
        self.usrbkgdpoints   = "5243,8910,11165,12153,13731,15060,16511,17767,19650,21874,23167,24519,36000,44282,49000, 60000., 71240"
        self.bkgdtablewsname = "PG3_11486_Background_Parameters"

        # self.inputparamwsname = str('Bank%dInstrumentParameterTable1_Step2'%(self.bankid))
        # self.braggtablewsname = str("BraggPeakParameterTable1")

        # Output properties
        self.bkgdwsname = "PG3_11486_Background"
        self.outwsname  = "PG3_11486_Calculated"

        # Data range
        #self.startx = float(calibDict[self.bankid]["LeBailFitMinTOF"])
        #self.endx   = float(calibDict[self.bankid]["LeBailFitMaxTOF"])

        return

    def _processInputs(self):
        """ Process properties
        """
        # Input


        return

    def PyExec(self):
        """ Main execution body
        """
        # Process input
        self._processInputs()

        if self.loaddata is True: 
            # Load data file 
            LoadAscii(
                    Filename        = self.datafilename, 
                    OutputWorkspace = self.datawsname, 
                    Unit            = 'TOF'
                    ) 
            
            # Load .irf file and .hkl file 
            CreateLeBailFitInput(
                    FullprofParameterFile   = self.irffilename, 
                    ReflectionsFile         = self.hklfilename, 
                    LatticeConstant         = float(self.latticesize), 
                    Bank                    = self.bankid,
                    InstrumentParameterWorkspace    =  self.inputparamwsname,
                    BraggPeakParameterWorkspace     =  self.braggtablewsname,
                    )

        if self.process_bkgd is True:
            # [Background]
            # Remove peaks and get pure background (hopefully)
            ProcessBackground(
                    Options         =   'SelectBackgroundPoints',
                    InputWorkspace  =   self.datawsname, 
                    OutputWorkspace =   self.bkgdwsname, 
                    LowerBound      =   self.startx, 
                    UpperBound      =   self.endx, 
                    BackgroundType  =   self.backgroundtype,
                    BackgroundPoints=   self.usrbkgdpoints,
                    NoiseTolerance  =   '0.10000000000000001')
   
            # Fit background points
            bkgdfunction = 'name=%s,n=6,A0=0.,A1=0.,A2=0.,A3=0.,A4=0.,A5=0.,A6=0, StartX=%f, EndX=%f.' % (self.bkgdtype, self.startx, self.endx)
            print "Background function: %s" % (bkgdfunction)
            f = Fit(
                    Function        =   bkgdfunction,
                    InputWorkspace  =   self.bkgdwsname,
                    Output          =   self.bkgdwsname,
                    MaxIterations   =   '1000',
                    Minimizer       =   'Levenberg-MarquardtMD',
                    CreateOutput    =   '1',
                    StartX          =   self.startx,
                    EndX            =   self.endx)
            print f
    
        # [Le Bail calculation]
        index = 0
        print "Fit range: %f , %f" % (self.startx, self.endx)
        LeBailFit(
                Function                =   'Calculation',
                InputWorkspace          =   self.datawsname, 
                OutputWorkspace         =   self.outwsname,
                InputParameterWorkspace =   self.inputparamwsname,
                OutputParameterWorkspace=   "Dummy_ParameterTable",
                InputHKLWorkspace       =   self.braggtablewsname,
                OutputPeaksWorkspace    =   'BraggPeakParameterTable2_%d'%(index),
    	        FitRegion               =   '%f, %f' % (self.startx, self.endx),
                BackgroundType          =   self.bkgdtype, #'Polynomial',
                UseInputPeakHeights     =   False, 
                PeakRadius              =   '8',
                BackgroundParametersWorkspace   =   self.bkgdtablewsname
                )
    
        return

def main(argv):
    """ Main
    """    
    globalfilename = "/home/wzz/Projects/MantidTests/LeBailFit/Test2013B/Bank2/Calibration_Information.config"

    runner = ExamineProfileParameters()
    runner.importGlobals(globalfilename)

        
    runner.loaddata         = True
    runner.process_bkgd     = True

    runner.startx =  7085.
    runner.endx   = 70500.
    
    runner.bkgdtype = "Chebyshev"
    #runner.bkgdtype = "Polynomial"

    runner.inputparamwsname = 'Bank%dInstrumentParameterTable_Raw'%(runner.bankid)
    runner.outwsname        = runner.datawsname + "_Guessed"
    runner.braggtablewsname = "BraggPeakParameterTable_Raw"

        #if False: 
        #    runner.irffilename  = "2013A_HR60b2.irf"
        #    print "Using special input .irf file: %s. " % (runner.irffilename)

    runner.PyExec()

    return


if __name__=="__main__": 
    main(["LeBailFitScript"])


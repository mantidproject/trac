""" Modified from system test SNSPowderRedux """
from mantid.simpleapi import *

def getSaveDir():
        """determine where to save - the current working directory"""
        import os
        return os.path.abspath(os.path.curdir)

class PG3Analysis():
    ref_file  = 'PG3_4844_reference.gsa'
    cal_file  = "PG3_FERNS_d4832_2011_08_24.cal"
    char_file = "PG3_characterization_2011_08_31-HR.txt"

    def requiredFiles(self):
        files = [self.ref_file, self.cal_file, self.char_file] 
        files.append("PG3_4844_event.nxs") # /SNS/PG3/IPTS-2767/0/
        files.append("PG3_4866_event.nxs") # /SNS/PG3/IPTS-2767/0/
        files.append("PG3_5226_event.nxs") # /SNS/PG3/IPTS-2767/0/
        return files

    def runTest(self):
        savedir = getSaveDir()

        # run the actual code
        SNSPowderReduction(Instrument="PG3", RunNumber=4844, Extension="_event.nxs",
                           PreserveEvents=True,
                           CalibrationFile=self.cal_file,
                           CharacterizationRunsFile=self.char_file,
                           LowResRef=15000, RemovePromptPulseWidth=50,
                           Binning=-0.0004, BinInDspace=True, FilterBadPulses=True,
                           SaveAs="gsas and fullprof and pdfgetn", OutputDirectory=savedir,
                           NormalizeByCurrent=True, FinalDataUnits="dSpacing",
			   LowResolutionSpectraOffset=-1)


test = PG3Analysis()
test.runTest()

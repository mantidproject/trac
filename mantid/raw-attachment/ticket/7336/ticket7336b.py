""" Modified from system test SNSPowderRedux """
from mantid.simpleapi import *

def getSaveDir():
        """determine where to save - the current working directory"""
        import os
        return os.path.abspath(os.path.curdir)



class SeriesAndConjoinFilesTest():
    cal_file   = "PG3_FERNS_d4832_2011_08_24.cal"
    char_file  = "PG3_characterization_2012_02_23-HR-ILL.txt"
    ref_files  = ['PG3_9829_reference.gsa', 'PG3_9830_reference.gsa']
    data_files = ['PG3_9829_event.nxs', 'PG3_9830_event.nxs']

    def requiredMemoryMB(self):
        """Requires 3Gb"""
        return 3000

    def requiredFiles(self):
        files = [self.cal_file, self.char_file]
        files.extend(self.ref_files)
        files.extend(self.data_files)
        return files

    def runTest(self):
        savedir = getSaveDir()

        # reduce a sum of runs - and drop it
        SNSPowderReduction(Instrument="PG3", RunNumber=[9829,9830], Extension="_event.nxs",
                           Sum=True, # This is the difference with the next call
                           PreserveEvents=True, VanadiumNumber=-1,
                           CalibrationFile=self.cal_file,
                           CharacterizationRunsFile=self.char_file,
                           LowResRef=15000, RemovePromptPulseWidth=50,
                           Binning=-0.0004, BinInDspace=True, FilterBadPulses=True,
                           SaveAs="gsas", OutputDirectory=savedir,
                           NormalizeByCurrent=True, FinalDataUnits="dSpacing",
			  LowResolutionSpectraOffset=2)
			  
	return

test = SeriesAndConjoinFilesTest()
test.runTest()

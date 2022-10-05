from mantid.simpleapi import *
import ISISCommandInterface as ici
import isis_instrument

# create a dummy instrument setup, here starting up with LARMOR
# the values below are probably somewhat ga ga
class BILBY(isis_instrument.LARMOR):
	WAV_RANGE_MIN = 2.5
	WAV_RANGE_MAX = 12.0

	def on_load_sample(self, ws_name, beamcentre, isSample):
		print ws_name
		ws = mtd[ws_name]
		out = Rebin(ws, '30500,500,38500', False)
		RenameWorkspace(out, OutputWorkspace=ws_name)
	def setDetector(self, name):
		bank = self.get_low_angle_detector()
		bank._shape = bank._DectShape(20, 3072, True, 61440)
		bank.set_first_spec_num(0)
		return self.setDefaultDetector()
	def get_TOFs(self, nm):
		return 30500, 38500
	def move_components(self, ws, bx, by):
		return [0,0], [-bx, -by]
	
	def curr_detector_position(self, ws_name):
		return [0,0]
	
ici.ReductionSingleton().set_instrument(BILBY())

# load a random mask file
ici.MaskFile('MaskSANS2DReductionGUI.txt')

# load mcstas event data
ici.AssignSample('BBY0000014.tar')

# set detector. PLEASE NOTE IT WOULD BE BETTER IF LoadBBY ASSSIGNED SOME
# UNIQUE NAME FOR EACH BANK
ici.Detector('bank')

# manual set sample info since this is not set in this nexus file
# This is NOT PRETTY. BETTER IF THE LoadBBY add sample information
# Here just done as below for testing
ici.ReductionSingleton().get_sample().geometry.height = 1.0
ici.ReductionSingleton().get_sample().geometry.width = 1.0
ici.ReductionSingleton().get_sample().geometry.thickness = 1.0
print ici.ReductionSingleton().get_sample().geometry.shape
print ici.ReductionSingleton().get_sample().geometry.height
print ici.ReductionSingleton().get_sample().geometry.width 
print ici.ReductionSingleton().get_sample().geometry.thickness

ici.WavRangeReduction(2.2, 12	)
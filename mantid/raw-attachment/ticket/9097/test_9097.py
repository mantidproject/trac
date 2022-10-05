#Create a new 'calibration' file
ws = LoadNexus('22024')
MoveInstrumentComponent(ws, 'rear-detector(x=0)',Y=0.1)
SaveNexus(ws, 'new_calibration_file.nxs')
mtd.clear()


#Update the Mask file to include the calibration file
file_path = FileFinder.getFullPath('MaskSANS2DReductionGUI.txt')

mask_file = open(file_path, 'r')
mask_content = mask_file.read()
mask_file.close()

new_mask_file = open('sans2dmask.txt','w')
new_mask_file.write(mask_content)
new_mask_file.write('\nTUBECALIBFILE = new_calibration_file.nxs')
new_mask_file.close()




import ISISCommandInterface as ici
import SANSBatchMode as batch
import os

# Function to check that the calibration file is being used.
def checkWsCalibrated(ws):
  det00 = ws.getInstrument().getComponentByName('rear-detector(x=0)/rear-detector(0,0)')
  det10 = ws.getInstrument().getComponentByName('rear-detector(x=1)/rear-detector(1,0)')
  #usually these two detectors have the same Y, but because we moved rear-detector(x=0) the calibration file, it will differ.
  print det10.getPos().Y(), det00.getPos().Y(), abs(det10.getPos().Y() - det00.getPos().Y())
  assert (0.1 - abs(det10.getPos().Y() - det00.getPos().Y()) < 0.0001)



MASKFILE = FileFinder.getFullPath('sans2dmask.txt')
if not os.path.isabs(MASKFILE):
	MASKFILE = './'+MASKFILE


# run reduction in single mode
ici.SANS2D()
ici.MaskFile(MASKFILE)
ici.AssignSample('22048')
#check calibrated
checkWsCalibrated(mtd['22048_sans_nxs'])
ici.AssignCan('22023')
#check calibrated
checkWsCalibrated(mtd['22023_sans_nxs'])
ici.TransmissionSample('22041','22024')
ici.TransmissionCan('22024', '22024')
reduced = ici.WavRangeReduction()
RenameWorkspace(reduced, OutputWorkspace='single_test_rear')

# run reductin in batch mode
ici.SANS2D()
ici.MaskFile(MASKFILE)
fit_settings = batch.BatchReduce(FileFinder.getFullPath('sans2d_reduction_gui_batch.csv'),
				'.nxs', combineDet='rear')
# prove the result is the same
result = CheckWorkspacesMatch('single_test_rear', 'trans_test_rear', 1.0e-10)
assert (result == 'Success!')


# run reduction in batch mode without the calibration
ici.SANS2D()
ici.MaskFile('MaskSANS2DReductionGUI.txt')
fit_settings = batch.BatchReduce(FileFinder.getFullPath('sans2d_reduction_gui_batch.csv'),
				'.nxs', combineDet='rear')
# prove the result is the same
result = CheckWorkspacesMatch('single_test_rear', 'trans_test_rear', 1.0e-10)
assert (result != 'Success!')


import numpy as np


def getLarmorRowColumn(index):	
	return index%512,index/512

def getSansIndexFromLarmor(index):
	row, column = getLarmorRowColumn(index)
	row_sans = int((row * 192) / 512)
	column_sans = int( (column * 192) / 80)
	return column_sans * 192 + row_sans

def createLarmorData(sansrun, larmorfile):
  larmor = LoadEmptyInstrument('/apps/mantid/mantid_develop2/Code/Mantid/instrument/LARMOR_Definition.xml')
  larmor = larmor.rebin('5.0, 200, 100000')
 
  sans2d = LoadNexus(sansrun)
  sans2d = sans2d.rebin('5.0, 200, 100000')

  for i in [0,1]:
    larmor.getAxis(i).setUnit(sans2d.getAxis(i).getUnit().unitID())
  
  for i in range(8):
    larmor.setY(i, sans2d.readY(i))
    larmor.setE(i, sans2d.readE(i))
	
  for i in range(40960):
    t_index = getSansIndexFromLarmor(i) + 8
    larmor.setY(i+10, sans2d.readY(t_index))
    larmor.setE(i+10, sans2d.readE(t_index))


  cloned_sans = CropWorkspace(sans2d,EndWorkspaceIndex=40969)

  for i in range(40970):
    cloned_sans.setY(i, larmor.readY(i))
    cloned_sans.setE(i, larmor.readE(i))

  LoadInstrument(cloned_sans, InstrumentName='LARMOR')

  #SaveNexus(cloned_sans, larmorfile)
  SaveNexus(larmor, larmorfile)



createLarmorData('SANS2D14273','LARMOR00000073.nxs')
createLarmorData('SANS2D14253', 'LARMOR00000053.nxs')
createLarmorData('SANS2D14270', 'LARMOR00000070.nxs')
createLarmorData('SANS2D14272', 'LARMOR00000072.nxs')

full_path = FileFinder.getFullPath('LARMOR00000073.nxs')
import h5py
h5f = h5py.File(full_path, 'r+')
sample = h5f['mantid_workspace_1/sample']
sample['geom_height'][:] = 8.0
sample['geom_id'][:] = 3
sample['geom_thickness'][:] = 2.0
sample['geom_width'] [:]= 8.0
h5f.close()



from ISISCommandInterface import *

LOQ()
MaskFile(r'C:\Backup\Backup_folder1\work\code\Mantid\git\mantid\Test\systemtests\Data\LOQ\MASK.094AA')

# Set data file
dataFile = r'C:\Backup\Backup_folder1\work\code\Mantid\git\mantid\Test\systemtests\Data\LOQ\LOQ54431.raw'
AssignSample(dataFile)

# Load flood file
floodFile = r'C:\Backup\Backup_folder1\work\code\Mantid\git\mantid\Test\systemtests\Data\LOQ\FLAT_CELL.061'
Load(floodFile,'flood',FirstColumnValue="SpectrumNumber")

# Crop workspaces to the detectors used in the reduction (as defined in the mask file)
CropToDetector('flood','floodCrop')
CropToDetector('54431_sans_raw','dataCrop')

Divide('dataCrop','floodCrop', 'DataDividedFlood')

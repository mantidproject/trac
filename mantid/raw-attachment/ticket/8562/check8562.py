import ISISCommandInterface as i
import SANSBatchMode as batch

MASKFILE = FileFinder.getFullPath('MaskLOQData.txt')
BATCHFILE = FileFinder.getFullPath('loq_batch_mode_reduction.csv')

i.LOQ()
i.MaskFile(MASKFILE)
fit_settings = batch.BatchReduce(BATCHFILE, '.nxs', combineDet='rear', saveAlgs={})
valid_flood = RenameWorkspace('first_time_rear')


i.LOQ()
MASKFILE = FileFinder.getFullPath('loqmask.txt')
i.MaskFile(MASKFILE)
fit_settings = batch.BatchReduce(BATCHFILE, '.nxs', combineDet='rear', saveAlgs={})
invalid_flood = RenameWorkspace('first_time_rear')

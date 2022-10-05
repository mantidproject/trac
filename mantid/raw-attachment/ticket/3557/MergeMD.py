import time
LoadEventNexus(Filename='C:/mantid/Test/AutoTestData/CNCS_7860_event.nxs',OutputWorkspace='CNCS_7860_event_NXS',CompressTolerance='0.10000000000000001')

start = time.time();
for omega in xrange(0, 20):
 print "Starting omega %03d degrees" % omega
 CreateMDWorkspace(Dimensions='3',Extents='-5,5,-5,5,-5,5',Names='Q_sample_x,Q_sample_y,Q__sample_z',Units='A,A,A',SplitInto='5',SplitThreshold='2000',MaxRecursionDepth='3',
  MinRecursionDepth='3', OutputWorkspace='CNCS_7860_event_MD')

 # Convert events to MD events
 AddSampleLog("CNCS_7860_event_NXS", "omega", "%s" % omega, "Number Series")
 AddSampleLog("CNCS_7860_event_NXS", "chi", "%s" % 0, "Number Series")
 AddSampleLog("CNCS_7860_event_NXS", "phi", "%s" % 0, "Number Series")
 ConvertToDiffractionMDWorkspace(InputWorkspace='CNCS_7860_event_NXS',OutputWorkspace='CNCS_7860_event_MD',OutputDimensions='Q (sample frame)',LorentzCorrection='1')
 
 SaveMD("CNCS_7860_event_MD", "C:/Users/spu92482/Desktop/CNCS/CNCS_7860_event_rotated_%03d.nxs" % omega)
 print time.time() - start, " seconds since start."
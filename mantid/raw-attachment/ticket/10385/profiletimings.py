
import time


Load(Filename='/Users/spu92482/Desktop/multiperiod_crash/INTER00027731.raw', OutputWorkspace='INTER00027731', LoaderName='LoadRaw', LoaderVersion=3)
start_time = time.time()
SaveNexusProcessed(InputWorkspace='INTER00027731', Filename='/Users/spu92482/Desktop/demo1.nxs')
end_time = time.time()
print str(end_time - start_time)+ " seconds "



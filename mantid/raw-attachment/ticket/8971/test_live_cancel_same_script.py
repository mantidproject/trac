import mantid
from mantid.simpleapi import StartLiveData
import time

######################### Time based cancellation #####################################################
print
print "Starting time-based live event cancellation demo"
print

MAX_MONITOR_TIME = 10 # in seconds

output_ws, last_timestamp, monitor_live = StartLiveData(UpdateEvery='5', Instrument='FakeEventDataListener',
                                                        OutputWorkspace='ws')
if monitor_live:
    start_time = time.time()
    while (time.time() - start_time) < MAX_MONITOR_TIME:
        time.sleep(0.5)
    monitor_live.cancel() # it's a request so it's not immediate
    while monitor_live.isRunning():
        pass
    print "\nTimeout reached, killed MonitorLiveData"

######################### Number of events based cancellation #########################################
print "-"*80
print
print "Starting number of events-based live event cancellation demo"
print

MAX_NUMBER_EVENTS = 2000

output_ws, last_timestamp, monitor_live = StartLiveData(UpdateEvery='5',Instrument='FakeEventDataListener',
                                                        PreserveEvents='1', OutputWorkspace='ws')
if monitor_live:
    while output_ws.getNumberEvents() < MAX_NUMBER_EVENTS:
        time.sleep(0.5)
    monitor_live.cancel()
    print
    print "Maximum number of events reached/succeeded, killed MonitorLiveData"
    print "Total number of events recorded=%d" % output_ws.getNumberEvents()

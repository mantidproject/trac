from mantid.simpleapi import StartLiveData
#
# Pairs with test_live_cancel_different_script2. This script starts the live event
# capture from the fake listener
#

StartLiveData(UpdateEvery='5', Instrument='FakeEventDataListener',
              OutputWorkspace='ws')

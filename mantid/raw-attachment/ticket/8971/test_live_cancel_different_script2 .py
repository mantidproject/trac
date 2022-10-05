from mantid import AlgorithmManager
#
# Pairs with test_live_cancel_different_script1. This script grabs the running MonitorLiveData
# algorithm and cancels it
#

monitor_alg = AlgorithmManager.newestInstanceOf("MonitorLiveData")
# request cancel
monitor_alg.cancel()
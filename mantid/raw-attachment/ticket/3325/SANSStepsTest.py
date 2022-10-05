import unittest
from mantid.simpleapi import *
from mantid.api import IEventWorkspace
import isis_reduction_steps as steps

class SliceEventTest(unittest.TestCase):
    class ReducerWrapper():
        tstart = None
        tstop = None
        def set_slices(self, tstart, tstop):
            self.tstart = tstart
            self.tstop = tstop
        def getSlicesLimits(self):
            return self.tstart, self.tstop
	
    def setUp(self):
        config['default.instrument'] = 'SANS2D'
        
    def test_normal(self):
	ws = LoadEventNexus('22048')
        slicer = steps.SliceEvent()
        reducer = self.ReducerWrapper()
        
        reducer.set_slices(0.1, 200.0)        
        slicer.execute(reducer, ws)
        point = mtd['ws']

        self.assertTrue(not isinstance(point, IEventWorkspace))

    def test_do_not_slice(self):
        ws = LoadEventNexus('22048')
        slicer = steps.SliceEvent()
        reducer = self.ReducerWrapper()
        
        slicer.execute(reducer, ws)
        point = mtd['ws']

        self.assertTrue(not isinstance(point, IEventWorkspace))



if __name__ == "__main__":			
    unittest.main()
        

from mantid.simpleapi import _set_properties

class SubAlg(PythonAlgorithm):

    def PyInit(self):
        pass

    def PyExec(self):
        #this algorithm should never show up in history!
	pass

AlgorithmFactory.subscribe(SubAlg)


class BasicAlg(PythonAlgorithm):

    def PyInit(self):
        pass

    def PyExec(self):
        alg = self.createChildAlgorithm('SubAlg')
        alg.initialize()
        args = {}
        kwargs = {}
        _set_properties(alg, *args, **kwargs)
        alg.execute()


AlgorithmFactory.subscribe(BasicAlg)

class ChildAlg(DataProcessorAlgorithm):

    def PyInit(self):
        pass

    def PyExec(self):
        alg = self.createChildAlgorithm('BasicAlg')
        alg.initialize()
        args = {}
        kwargs = {}
        _set_properties(alg, *args, **kwargs)
        alg.execute()


AlgorithmFactory.subscribe(ChildAlg)

class ParentAlg(DataProcessorAlgorithm):

    def PyInit(self):
        self.declareProperty(MatrixWorkspaceProperty('OutputWorkspace', '', Direction.Output),
                             doc="Name to give the output workspace.")

    def PyExec(self):
        ws_name = self.getPropertyValue("OutputWorkspace")
        alg = self.createChildAlgorithm('ChildAlg')
        alg.initialize()
        args = {}
        kwargs = {}
        _set_properties(alg, *args, **kwargs)
        alg.execute()

        ws = CreateWorkspace([0, 1, 2], [0, 1, 2], OutputWorkspace=ws_name)
        self.setProperty('OutputWorkspace', ws)

AlgorithmFactory.subscribe(ParentAlg)

#############################################################

ws_name = '__tmp_test_algorithm_history'

alg = AlgorithmManager.createUnmanaged('ParentAlg')
alg.initialize()
alg.setProperty("OutputWorkspace", ws_name)
alg.execute()
history = mtd[ws_name].getHistory()

alg_hists = history.getAlgorithmHistories()
assert history.size() == 1
assert len(alg_hists) == 1

alg_history = history.getAlgorithmHistory(0)
assert alg_history.name() == "ParentAlg"
assert alg_history.childHistorySize() == 2

child_history = alg_history.getChildAlgorithmHistory(0)
assert child_history.name() == "ChildAlg"
assert child_history.childHistorySize() == 1

create_workspace_history = alg_history.getChildAlgorithmHistory(1)
assert create_workspace_history.name() == "CreateWorkspace"
assert len(create_workspace_history.getProperties()) == 12
assert create_workspace_history.childHistorySize() == 0

basic_history = child_history.getChildAlgorithmHistory(0)
assert basic_history.name() == "BasicAlg"
assert basic_history.childHistorySize() == 0
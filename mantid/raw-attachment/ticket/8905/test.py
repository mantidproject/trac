from mantid.api import PythonAlgorithm, AlgorithmFactory
from mantid.kernel import FloatArrayProperty, StringArrayProperty, StringArrayMandatoryValidator, Direction

from pdb import set_trace as tr

class TestSetPropertyGroup(PythonAlgorithm):

  def category(self):
    return "Test"

  def name(self):
    return 'TestSetPropertyGroup'

  def PyInit(self):
    self.declareProperty(FloatArrayProperty('Property0', values=[], direction=Direction.Input), doc='this is Property0')
    arrvalidator = StringArrayMandatoryValidator()
    self.declareProperty(StringArrayProperty('Property1', values=[], validator=arrvalidator, direction=Direction.Input), doc='this is Property1')
    self.declareProperty(FloatArrayProperty('Property2', values=[], direction=Direction.Input), doc='this is Property2')

    self.setPropertyGroup('Property1','This is a group')
    self.setPropertyGroup('Property2','This is a group')

    self.declareProperty(FloatArrayProperty('Property3', values=[], direction=Direction.Input), doc='this is Property3')

  def PyExec(self):
    pass

AlgorithmFactory.subscribe(TestSetPropertyGroup)

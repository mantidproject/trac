export MANTIDPATH='/path/to/MantidPlot'
PYTHONPATH=$MANTIDPATH:$PYTHONPATH
PATH=$MANTIDPATH:$PATH
SYSTEMTESTDIR='/path/to/systemtests/repository'
python $SYSTEMTESTDIR/InstallerTesting/runSystemTests.py --frameworkLoc=$SYSTEMTESTDIR/StressTestFramework --tests-regex=BASISAutoReduction --loglevel=error

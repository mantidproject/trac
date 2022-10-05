# The following should load runs 15189 - 15191
ws = PlotAsymmetryByLogValue(FirstRun='MUSR00015189.nxs',LastRun='MUSR00015191.nxs',LogValue='run_number')

# Should load runs 15192, 15193 only
ws = PlotAsymmetryByLogValue(FirstRun='MUSR00015189.nxs',LastRun='MUSR00015193.nxs',LogValue='run_number')

# Should remove runs 15189, 15190, 15191, and load nothing
ws = PlotAsymmetryByLogValue(FirstRun='MUSR00015192.nxs',LastRun='MUSR00015193.nxs',LogValue='run_number')

# Should load runs 15189, 15190, 15191 and remove nothing
ws = PlotAsymmetryByLogValue(FirstRun='MUSR00015189.nxs',LastRun='MUSR00015193.nxs',LogValue='run_number')

# Should remove runs 15189, 15190, 15191, and load nothing
ws = PlotAsymmetryByLogValue(FirstRun='MUSR00015192.nxs',LastRun='MUSR00015193.nxs',LogValue='run_number')

# Should load runs 15189, 15190, 15191, and remove runs 15192, 15193
ws = PlotAsymmetryByLogValue(FirstRun='MUSR00015189.nxs',LastRun='MUSR00015191.nxs',LogValue='run_number')

# Should remove everything and load 15189 - 15193 (LogValue changed)
ws = PlotAsymmetryByLogValue(FirstRun='MUSR00015189.nxs',LastRun='MUSR00015193.nxs',LogValue='sample_magn_field')

# Should remove everything and load 15189 - 15193 (Function changed)
ws = PlotAsymmetryByLogValue(FirstRun='MUSR00015189.nxs',LastRun='MUSR00015193.nxs',LogValue='run_number',Function='Min')

# Should remove everything and load 15189 - 15193 (Type changed)
ws = PlotAsymmetryByLogValue(FirstRun='MUSR00015189.nxs',LastRun='MUSR00015193.nxs',LogValue='run_number',Type='Differential')

# Should remove everything and load 15189 - 15193 (Periods changed)
ws = PlotAsymmetryByLogValue(FirstRun='MUSR00015189.nxs',LastRun='MUSR00015193.nxs',LogValue='run_number',Green=2,Red=1)

# Should remove everything and load 15189 - 15193 (Detector grouping changed)
ws = PlotAsymmetryByLogValue(FirstRun='MUSR00015189.nxs',LastRun='MUSR00015193.nxs',LogValue='run_number',ForwardSpectra='1-32',BackwardSpectra='33-64')

# Should remove everything and load 15189 - 15193 (Time limits changed)
ws = PlotAsymmetryByLogValue(FirstRun='MUSR00015189.nxs',LastRun='MUSR00015193.nxs',LogValue='run_number',TimeMin=0.5,TimeMax=1.5)

# Should remove everything and load 15189 - 15193 (DeadTimeCorrections changed)
ws = PlotAsymmetryByLogValue(FirstRun='MUSR00015189.nxs',LastRun='MUSR00015193.nxs',LogValue='run_number',DeadTimeCorrType='FromRunData')
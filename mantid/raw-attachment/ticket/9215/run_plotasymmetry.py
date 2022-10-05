ws = PlotAsymmetryByLogValue(FirstRun="C:/Users/dsl37522/mantid-code/UsageData/hifi/HIFI00051636.nxs",LastRun="C:/Users/dsl37522/mantid-code/UsageData/hifi/HIFI00051736.nxs",LogValue="run_number")

ws = PlotAsymmetryByLogValue(FirstRun="C:/Users/dsl37522/mantid-code/UsageData/hifi/HIFI00051636.nxs",LastRun="C:/Users/dsl37522/mantid-code/UsageData/hifi/HIFI00051736.nxs",LogValue="run_number",Red=2,Green=1)

ws = PlotAsymmetryByLogValue(FirstRun="C:/Users/dsl37522/mantid-code/UsageData/hifi/HIFI00051636.nxs",LastRun="C:/Users/dsl37522/mantid-code/UsageData/hifi/HIFI00051736.nxs",LogValue="run_number",DeadTimeCorrType="FromRunData")

ws = PlotAsymmetryByLogValue(FirstRun="C:/Users/dsl37522/mantid-code/UsageData/hifi/HIFI00051636.nxs",LastRun="C:/Users/dsl37522/mantid-code/UsageData/hifi/HIFI00051736.nxs",LogValue="run_number",DeadTimeCorrType="FromSpecifiedFile",DeadTimeCorrFile="C:/Users/dsl37522/Desktop/test_files/dead_times_processed.nxs")

ws = PlotAsymmetryByLogValue(FirstRun="C:/Users/dsl37522/mantid-code/UsageData/hifi/HIFI00051636.nxs",LastRun="C:/Users/dsl37522/mantid-code/UsageData/hifi/HIFI00051736.nxs",LogValue="run_number",ForwardSpectra="1-32",BackwardSpectra="33-64")

ws = PlotAsymmetryByLogValue(FirstRun="C:/Users/dsl37522/mantid-code/UsageData/MUSR00015189.nxs",LastRun="C:/Users/dsl37522/mantid-code/UsageData/MUSR00015193.nxs",LogValue="run_number",ForwardSpectra="1-32",BackwardSpectra="33-64")

ws = PlotAsymmetryByLogValue(FirstRun="C:/Users/dsl37522/mantid-code/UsageData/MUSR00015189.nxs",LastRun="C:/Users/dsl37522/mantid-code/UsageData/MUSR00015193.nxs",LogValue="run_number",DeadTimeCorrType="FromSpecifiedFile",DeadTimeCorrFile="C:/Users/dsl37522/Desktop/test_files/dead_times_processed.nxs")

ws = PlotAsymmetryByLogValue(FirstRun="C:/Users/dsl37522/mantid-code/UsageData/MUSR00015189.nxs",LastRun="C:/Users/dsl37522/mantid-code/UsageData/MUSR00015193.nxs",LogValue="run_number",DeadTimeCorrType="FromRunData")

ws = PlotAsymmetryByLogValue(FirstRun="C:/Users/dsl37522/mantid-code/UsageData/MUSR00015189.nxs",LastRun="C:/Users/dsl37522/mantid-code/UsageData/MUSR00015193.nxs",LogValue="Field_Danfysik",DeadTimeCorrType="FromRunData",Red=2,Green=1)

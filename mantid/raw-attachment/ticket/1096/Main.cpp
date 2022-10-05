// If you get the message  “This application has failed to start because MSVCR80.dll was not found. Re-installing the application may fix this problem.”
// when running to run this main.cpp in debug mode then try to uncomment the line below (see also http://blogs.msdn.com/dsvc/archive/2008/08/07/part-2-troubleshooting-vc-side-by-side-problems.aspx for more details)
//#pragma comment(linker, "\"/manifestdependency:type='Win32' name='Microsoft.VC80.CRT' version='8.0.50608.0' processorArchitecture='X86' publicKeyToken='1fc8b3b9a1e18e3b' \"") 

#include <iostream>
#include <iomanip>
#include "Benchmark.h"
#include "UserAlgorithmTest.h"
#include "MantidAPI/FrameworkManager.h"
//#include "MantidAPI/Workspace.h"
//#include "MantidDataObjects/Workspace1D.h" 
#include "MantidDataObjects/Workspace2D.h" 

#include <boost/timer.hpp>

using namespace Mantid::API;
using namespace Mantid::Kernel;
using namespace Mantid::Geometry;
using namespace Mantid::DataObjects;

void test();

int main()
{

  FrameworkManagerImpl& fm = FrameworkManager::Instance();
/*
//  UserAlgorithmTest userTest;
 // userTest.RunAllTests();
  
 // Benchmark b;
 // b.RunPlusTest(10584,2000);
  //b.RunPlusTest(15584,2000);
  //b.RunPlusTest(2584,2000);

//#if defined _DEBUG
  //NOTE:  Any code in here is temporary for debugging purposes only, nothing is safe!
  //load a raw file
    IAlgorithm* loader = fm.createAlgorithm("LoadRaw");
    loader->setPropertyValue("Filename", "../../../Test/Data/MER02257.raw");

    std::string outputSpace = "outer";
    loader->setPropertyValue("OutputWorkspace", outputSpace);    
    loader->execute();

  Workspace* w = fm.getWorkspace(outputSpace);
  Workspace2D* output2D = dynamic_cast<Workspace2D*>(w);
  const int numberOfSpectra = output2D->getNumberHistograms();
      clock_t start = clock();
  int FailCount =0;
  int SuccessCount = 0;
  V3D total;
  for (int j = 0; j <= numberOfSpectra; ++j) 
	{
    try{
		// Now get the detector to which this relates
		IDetector_const_sptr det = output2D->getDetector(j);
    // Solid angle should be zero if detector is masked ('dead')
    V3D v = det->getPos();
    total += v;
    SuccessCount++;
  }
      catch (...)
      { 
        FailCount++;
      }
	} // loop over spectra
  clock_t end = clock();
    std::cout << double(end - start)/CLOCKS_PER_SEC << std::endl;
    std::cout << "Success " << SuccessCount << " | Failed " << FailCount << std::endl;
    std::cout << total << std::endl;
//#endif
*/
//STEVES looking at a problem with ConvertUnits
    for (int i = 0 ; i < 200 ; ++i)
    {
      fm.exec("LoadRaw","Filename=C:/mantid/Test/Data/MAR11001.RAW;OutputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe");
      fm.exec("LoadDetectorInfo","Workspace=_Conv_ETrans_tempory_WS_MAR11001.spe;DataFilename=C:/mantid/Test/Data/MAR11001.RAW");
      fm.exec("MaskDetectors","Workspace=_Conv_ETrans_tempory_WS_MAR11001.spe;SpectraList=1,2,3,4,4124,2526,1126,3626");
      fm.exec("FlatBackground","InputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;OutputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;StartX=18000;EndX=19500;Mode=Mean");
      fm.exec("NormaliseToMonitor","InputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;OutputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;MonitorSpectrum=1;IntegrationRangeMin=1000;IntegrationRangeMax=2000");
      fm.exec("ConvertUnits","InputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;OutputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;Target=DeltaE;EMode=Direct;EFixed=13");
      fm.exec("Rebin","InputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;OutputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;Params=1,0.1,13");
      fm.exec("DetectorEfficiencyCor","InputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;OutputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;IncidentEnergy=13");
      fm.exec("GroupDetectors","InputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;OutputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;MapFile=C:/Users/wht13119/Desktop/docs/Excitations/mari_res.map");
      fm.exec("LoadRaw","Filename=C:/mantid/Test/Data/MAR11060.RAW;OutputWorkspace=_ETrans_norm_tempory_WS");
      fm.exec("LoadDetectorInfo","Workspace=_ETrans_norm_tempory_WS;DataFilename=C:/mantid/Test/Data/MAR11060.RAW");
      fm.exec("ConvertUnits","InputWorkspace=_ETrans_norm_tempory_WS;OutputWorkspace=_ETrans_norm_tempory_WS;Target=Energy");
      fm.exec("Rebin","InputWorkspace=_ETrans_norm_tempory_WS;OutputWorkspace=_ETrans_norm_tempory_WS;Params=0,20,20");
      fm.exec("GroupDetectors","InputWorkspace=_ETrans_norm_tempory_WS;OutputWorkspace=_ETrans_norm_tempory_WS;MapFile=C:/Users/wht13119/Desktop/docs/Excitations/mari_res.map");
      fm.exec("Divide","LHSWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;RHSWorkspace=_ETrans_norm_tempory_WS;OutputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe");
      fm.exec("ReplaceSpecialValues","InputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;OutputWorkspace=_Conv_ETrans_tempory_WS_MAR11001.spe;NaNValue=0;InfinityValue=0");
      std::cerr << i << std::endl;
    }

  fm.clear();
  exit(0);

}


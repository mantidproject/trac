//----------------------------------------------------------------------
// Includes
//----------------------------------------------------------------------
#include "Muon_StaticKuboToyabe.h"
#include <cmath>

namespace Mantid
{
namespace CurveFitting
{

using namespace Kernel;
using namespace API;

DECLARE_FUNCTION(Muon_StaticKuboToyabe)

void Muon_StaticKuboToyabe::init()
{
  declareParameter("A", 0.2);
  declareParameter("Delta", 0.2);
}


void Muon_StaticKuboToyabe::functionLocal(double* out, const double* xValues, const int& nData)const
{
    const double& A = getParameter("A");
    const double& G = getParameter("Delta");
  
 
   for (int i = 0; i < nData; i++) {
       // double diff=xValues[i]-peakCentre;
	   // double e=pow(gs*xValues[i],2.0);
        out[i] = A*(exp(-pow(G*xValues[i],2)/2)*(1-pow(G*xValues[i],2))*2./3.+1./3.);
    }
}
void Muon_StaticKuboToyabe::functionDerivLocal(API::Jacobian* out, const double* xValues, const int& nData)
{
  calNumericalDeriv(out, xValues, nData);
}




} // namespace CurveFitting
} // namespace Mantid

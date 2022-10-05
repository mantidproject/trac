//----------------------------------------------------------------------
// Includes
//----------------------------------------------------------------------
#include "Muon_ExpDecayOsc.h"
#include <cmath>

namespace Mantid
{
namespace CurveFitting
{

using namespace Kernel;
using namespace API;

DECLARE_FUNCTION(Muon_ExpDecayOsc)

void Muon_ExpDecayOsc::init()
{
  declareParameter("A", 0.2);
  declareParameter("lambda", 0.2);
  declareParameter("frequency", 0.5);
  declareParameter("phi", 0.0);
}


void Muon_ExpDecayOsc::functionLocal(double* out, const double* xValues, const int& nData)const
{
    const double& gA0 = getParameter("A");
    const double& gs = getParameter("lambda");
	const double& gf = getParameter("frequency");
	const double& gphi = getParameter("phi");
  
 
   for (int i = 0; i < nData; i++) {
        out[i] = gA0*exp(-gs*xValues[i])*cos(2*3.1415926536*gf*xValues[i]+gphi);
    }
}
void Muon_ExpDecayOsc::functionDerivLocal(API::Jacobian* out, const double* xValues, const int& nData)
{
  calNumericalDeriv(out, xValues, nData);
}




} // namespace CurveFitting
} // namespace Mantid

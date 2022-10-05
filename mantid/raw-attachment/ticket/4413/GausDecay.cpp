//----------------------------------------------------------------------
// Includes
//----------------------------------------------------------------------
#include "Muon_GausDecay.h"
#include <cmath>

namespace Mantid
{
namespace CurveFitting
{

using namespace Kernel;
using namespace API;

DECLARE_FUNCTION(Muon_GausDecay)

void Muon_GausDecay::init()
{
  declareParameter("A", 0.2);
  declareParameter("sigma", 0.2);
}


void Muon_GausDecay::functionLocal(double* out, const double* xValues, const int& nData)const
{
    const double& A = getParameter("A");
    const double& G = getParameter("sigma");

 
   for (int i = 0; i < nData; i++) {
        out[i] = A*exp(-G*G*xValues[i]*xValues[i]);
    }
}
void Muon_GausDecay::functionDerivLocal(API::Jacobian* out, const double* xValues, const int& nData)
{
  calNumericalDeriv(out, xValues, nData);
}




} // namespace CurveFitting
} // namespace Mantid



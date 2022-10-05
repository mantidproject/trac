//----------------------------------------------------------------------
// Includes
//----------------------------------------------------------------------
#include "Muon_ExpDecay.h"
#include <cmath>

namespace Mantid
{
namespace CurveFitting
{

using namespace Kernel;
using namespace API;

DECLARE_FUNCTION(Muon_ExpDecay)

void Muon_ExpDecay::init()
{
  declareParameter("A", 0.2);
  declareParameter("lambda", 0.2);
}


void Muon_ExpDecay::functionLocal(double* out, const double* xValues, const int& nData)const
{
    const double& A = getParameter("A");
    const double& lambda = getParameter("lambda");

 
   for (int i = 0; i < nData; i++) {
        out[i] = A*exp(-lambda*xValues[i]);
    }
}
void Muon_ExpDecay::functionDerivLocal(API::Jacobian* out, const double* xValues, const int& nData)
{
  calNumericalDeriv(out, xValues, nData);
}




} // namespace CurveFitting
} // namespace Mantid



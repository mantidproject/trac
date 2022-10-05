//----------------------------------------------------------------------
// Includes
//----------------------------------------------------------------------
#include "Muon_Stretched_Exponential.h"
#include <cmath>

namespace Mantid
{
namespace CurveFitting
{

using namespace Kernel;
using namespace API;

DECLARE_FUNCTION(Muon_Stretched_Exponential)

void Muon_Stretched_Exponential::init()
{
  declareParameter("A", 0.2);
  declareParameter("lambda", 0.2);
  declareParameter("beta",0.2);
}


void Muon_Stretched_Exponential::functionLocal(double* out, const double* xValues, const int& nData)const
{
    const double& A = getParameter("A");
    const double& G = getParameter("lambda");
	const double& b = getParameter("beta");

 
   for (int i = 0; i < nData; i++) {
        out[i] = A*exp(-pow(G*xValues[i],b));
    }
}
void Muon_Stretched_Exponential::functionDerivLocal(API::Jacobian* out, const double* xValues, const int& nData)
{
  calNumericalDeriv(out, xValues, nData);
}




} // namespace CurveFitting
} // namespace Mantid



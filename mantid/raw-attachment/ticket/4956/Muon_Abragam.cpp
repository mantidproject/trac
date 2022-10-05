//----------------------------------------------------------------------
// Includes
//----------------------------------------------------------------------
#include "Muon_Abragam.h"
#include <cmath>

namespace Mantid
{
namespace CurveFitting
{

using namespace Kernel;
using namespace API;

DECLARE_FUNCTION(Muon_Abragam)

void Muon_Abragam::init()
{
	declareParameter("A", 0.2);
	declareParameter("omiga", 0.5);
	declareParameter("phi", 1);
	declareParameter("sigma", 1);
	declareParameter("tao",1);
}


void Muon_Abragam::functionLocal(double* out, const double* xValues, const int& nData)const
{
    const double& A = abs(getParameter("A"));
    const double& w = abs(getParameter("omiga"));
    const double& phi = abs(getParameter("phi"));
	const double& sig = abs(getParameter("sigma"));  
	const double& t = abs(getParameter("tao"));
 
   for (int i = 0; i < nData; i++) {
	   double A1=A*cos(w*xValues[i]+phi);
	   double A2=-(sig*sig*t*t)*(exp(-xValues[i]/t)-1+(xValues[i]/t));
	   double A3=exp(A2);

        out[i] = A1*A3;
    }
}
void Muon_Abragam::functionDerivLocal(API::Jacobian* out, const double* xValues, const int& nData)
{
  calNumericalDeriv(out, xValues, nData);
}




} // namespace CurveFitting
} // namespace Mantid

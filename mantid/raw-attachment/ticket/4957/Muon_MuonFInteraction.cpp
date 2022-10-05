//----------------------------------------------------------------------
// Includes
//----------------------------------------------------------------------
#include "Muon_MuonFInteraction.h"
#include <cmath>

namespace Mantid
{
namespace CurveFitting
{

using namespace Kernel;
using namespace API;

DECLARE_FUNCTION(Muon_MuonFInteraction)

void Muon_MuonFInteraction::init()
{
	declareParameter("lambda", 0.2);
	declareParameter("omiga", 0.5);
	declareParameter("Beta", 1);
	declareParameter("A", 1);
}


void Muon_MuonFInteraction::functionLocal(double* out, const double* xValues, const int& nData)const
{
    const double& lambda = getParameter("lambda");
    const double& omiga = getParameter("omiga");
    const double& beta = getParameter("Beta");
	const double& A = getParameter("A");  
 
   for (int i = 0; i < nData; i++) {
	   double A1=exp(-pow(lambda*xValues[i],beta))*A/6;
	   double A2=cos(1.732050808*omiga*xValues[i]);
	   double A3=(1.0-1.0/1.732050808)*cos(((3.0-1.732050808)/2.0)*omiga*xValues[i]);
	   double A4=(1.0+1.0/1.732050808)*cos(((3.0+1.732050808)/2.0)*omiga*xValues[i]);

       out[i] = A1*(3+A2+A3+A4);
    }
}
void Muon_MuonFInteraction::functionDerivLocal(API::Jacobian* out, const double* xValues, const int& nData)
{
  calNumericalDeriv(out, xValues, nData);
}




} // namespace CurveFitting
} // namespace Mantid

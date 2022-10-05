//----------------------------------------------------------------------
// Includes
//----------------------------------------------------------------------
#include "Muon_DynamicKuboToyabe.h"
#include <cmath>

namespace Mantid
{
namespace CurveFitting
{

using namespace Kernel;
using namespace API;

DECLARE_FUNCTION(Muon_DynamicKuboToyabe)

void Muon_DynamicKuboToyabe::init()
{
  declareParameter("A", 0.2);
  declareParameter("Delta", 0.2);
  declareParameter("Field",0.0);
  declareParameter("hopping rate",0.0);
  declareParameter("endX",15);
}

//--------------------------------------------------------------------------------------------------------------------------------------

double midpnt(double func(const double, const double, const double,const double),
	const double a, const double b, const int n, const double g, const double w0) {
// quote & modified from numerical recipe 2nd edtion (page147)	
	
	double x,tnm,sum,del,ddel;
	int it,j;
	static double s;

	if (n==1) { return (s =0.5*(b-a)*func(a,g,w0,b)+func(b,g,w0,b));
	} else {

		for (it=1,j=1;j<n-1;j++) it *= 3;
		tnm = it;
		del = (b-a)/(3*tnm);
		ddel=del+del;
		x = a+0.5*del;
		sum =0.0;
		for (j=0;j<it;j++) {
			sum += func(x,g,w0,b);
			x += ddel;
			sum += func(x,g,w0,b);
			x += del;
		}
		s=(s+(b-a)*sum/tnm)/3.0;
		return s;
	}
}

void polint (double* xa, double* ya, const double x, double& y, double& dy) {
	int i, m, ns = 0;
	double den, dif, dift, ho, hp, w;

	const int n = sizeof xa;
	double c[n],d[n];
	dif = fabs(x-xa[0]);
	for (i=0;i<n;i++){
		if((dift=fabs(x-xa[i]))<dif) {
			ns=i;
			dif=dift;
		}
		c[i]=ya[i];
		d[i]=ya[i];
	}
	y=ya[ns--];
	for (m=1;m<n;m++) {
		for (i=0;i<n-m;i++) {

			ho=xa[i]-x;
			hp=xa[i+m]-x;
			w=c[i+1]-d[i];
//			if((den=ho-hp)==0.0) error message!!!; delete next line.
			den=ho-hp;
			den=w/den;
			d[i]=hp*den;
			c[i]=ho*den;
		}
		y += (dy=(2*(ns+1)<(n-m) ? c[ns+1] : d[ns--]));

	}
}


double integral (double func(const double, const double, const double, const double),
				const double a, const double b, const double g, const double w0) {
	const int JMAX = 14, JMAXP = JMAX+1, K=5;
	const double EPS = 3.0e-9;  //error smaller than this value
	int i,j;
	double ss,dss;
	double h[JMAXP], s[JMAX], h_t[K], s_t[K];
	
	h[0] = 1.0;
	for (j=1; j<= JMAX; j++) {
		s[j-1]=midpnt(func,a,b,j,g,w0);
		if (j >= K) {
			for (i=0;i<K;i++) {
				h_t[i]=h[j-K+i];
				s_t[i]=s[j-K+i];
			}
			polint(h_t,s_t,0.0,ss,dss);
			if (fabs(dss) <= fabs(ss)) return ss;
		}
		h[j]=h[j-1]/9.0;
	}
	return 0.0;
}


//--------------------------------------------------------------------------------------------------------------------------------------
// cast all integers into doubles
double ZFKT (const double q)
{
	return((0.3333333333)+(0.6666666667)*(1.0-q)*exp(-q/2.0));
}
//Zero field KuboToyabe function.


double f1(const double x, const double G, const double w0, const double b) {
	
	return( exp(-G*G*x*x/2)*sin(w0*x)); 
}
//integration function for general static KuboToyabe.

double gz (const double x, const double G, const double F) 
{
	double w0 = 2.0*3.1415926536*0.01355342*F;
//	double Integral = 0;
	const double q = G*G*x*x;
	
	if (w0 == 0.0) {
		return (ZFKT(q)); 
	}
	else {
		
		if (F>2.0*G) { w0 = 2*3.1415926*0.01355342*F ;} else { w0 =2*3.1415926*0.01355342*2.0*G; }
			
		double p = G*G/(w0*w0);
		double HKT = 1.0-2.0*p*(1-exp(-q/2.0)*cos(w0*x))+2.0*p*p*w0*integral(f1,0.0,x,G,w0);
		if (F>2.0*G) {return (HKT);} 
		else {return (ZFKT(q)+ (F/2.0/G)*(HKT-ZFKT(q)));}	 
		
   }
}






void Muon_DynamicKuboToyabe::functionLocal(double* out, const double* xValues, const size_t nData)const
{
    const double& A = getParameter("A");
    const double& G = abs(getParameter("Delta"));
	const double& F = abs(getParameter("Field"));
	const double& v = abs(getParameter("hopping rate"));


	
	
	
	//do{stepsize=stepsize/10;}while (xValues[0]<stepsize);
	//make sure stepsize is smaller than spacing between xValues.
	



	const int n = 1000;
	const double stepsize = abs(getParameter("endX")/n);
	double funcG[n];

	double Integral = 0.0;
	if (v == 0.0) {
		for (int i = 0; i < nData; i++) {
			out[i] = A*gz(xValues[i],G,F);
		}
	} 
//	else if {
	else {
		for (int i = 0; i < n; i++) {
			if (v*i*stepsize>5.0 && v>10.0*G) {
				funcG[i] = funcG[i-1]*exp(-2*G*G*stepsize/v);//fast hopping approx
			} else {
				double Integral=0.0;
				for (int c = 1; c <= i; c++) {
					Integral= gz(c*stepsize,G,F)*exp(-v*c*stepsize)*funcG[i-c]*(stepsize) + Integral; 
				}
				funcG[i] = (gz(i*stepsize,G,F)*exp(-v*i*stepsize) + v*Integral);
			}
		}
		for (int i = 0; i < nData; i++) {
			double a =xValues[i]/stepsize;
			out[i] = A*(funcG[int(a)]);
		}

   }
}


void Muon_DynamicKuboToyabe::functionDerivLocal(API::Jacobian* out, const double* xValues, const size_t nData)
{
  calNumericalDeriv(out, xValues, nData);
}




} // namespace CurveFitting
} // namespace Mantid

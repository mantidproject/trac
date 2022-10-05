pro creategr,a,b,sq,gr,q,hydrogen=hydrogen,rho=rho,sigma=sigma,interactive=interactive,qminpla=qminpla,qmaxpla=qmaxpla,d1=d1,qmaxft=qmaxft,scannr=scannr,qualstring=qualstring,backfile=backfile,usehq=usehq,sbs=sbs,sb2=sb2,l=l,maxr=maxr,ignq=ignq,lowfit=lowfit,normf=normf,help=help,displq=displq,disply=disply,packfrac=packfrac,comment=comment,nlowfit=nlowfit,error=error

if not var_defined(hydrogen) then hydrogen=0
if not var_defined(rho) then rho=0.02205
if not var_defined(sigma) then sigma=10.631
if not var_defined(interactive) then interactive=1
if not var_defined(qmaxft) then qmaxft=!pi*10
if not var_defined(qminpla) then qminpla=5
if not var_defined(qmaxpla) then qmaxpla=50
if not var_defined(d1) then d1=0.627
if not var_defined(scannr) then scannr=9999
if not var_defined(backfile) then backfile='backpdf.dat'
if not var_defined(usehq) then usehq=0
if not var_defined(sbs) then sbs=(4.1491+2*5.803)^2
if not var_defined(sb2) then sb2=4.1491^2+2*5.803^2
if not var_defined(l) then l=[1,20]
if not var_defined(maxr) then maxr=20
if not var_defined(ignq) then ignq=7
if not var_defined(q) then q=findgen(2500)*.02
if not var_defined(normf) then normf='normdatapdf.dat'
if not var_defined(help) then help=0
if not var_defined(displq) then displq=[min(q),max(q)]
if not var_defined(packfrac) then packfrac=1.
if not var_defined(qualstring) then qualstring=''
if not var_defined(comment) then comment='You may note Qmax, background, normalization,mask etc. here' 
if not var_defined(lowfit) then lowfit=0
if not var_defined(nlowfit) then nlowfit=10
if help eq 1 then begin
print,'USAGE: creategr,a,b,sq,gr,q,hydrogen=hydrogen,rho=rho,sigma=sigma,interactive=interactive,qminpla=qminpla,d1=d1,qmaxft=qmaxft,scannr=scannr,backfile=backfile,usehq=usehq,sbs=sbs,sb2=sb2,l=l,maxr=maxr,ignq=ignq,normf=normf,help=help,displq=displq,disply=disply,packfrac=packfrac,comment=comment,lowfit=lowfit'
print,'a: a variable for scan to be FT (input)'
print,'b: b variable for scan to be FT (input)'
print,'sq: S(Q) (ouput)'
print,'gr: g(r) with Lorch (output)'
print,' q: (input) Q, default findgen(2500)*.02'
print,'hydrogen =1/2 (try a hydrogen Placzek, 2 is preferred) =0 (no Hydrogen Placzek)
print,' rho: density in molecules /A^3, default=0.02205 silica glass'
print,'interactive=0 no plots'
print,' qminpla (default=5A^-1) minimum Q to fit a Polynomial as self scattering background'
print,' qmaxpla (default=50A^-1) maximum Q to fit a Polynomial as self scattering background'
print,' d1 = diameter of the sample in cm (default = 0.627, a quarter inch)'
print,' qmaxft: maximum Q for FT (default= 10 x pi)'
print,'scannr scannr used for output files'
print,'backfile= name of the backgroundfile created with makeback'
print,'usehq=1 use high Q behavior for normalization, =0 use absolute normalization'
print,'sbs= (sum of b)^2 default sbs=(4.1491+2*5.803)^2 (SiO2)'
print,'sb2= (sum of b^2) default sb2=4.1491^2+2*5.803^2 (SiO2)'
print,'l= [1,20] display range of the FT'
print,'maxr=20 maximum r where FT is calculated'
print,'ignq=5 minimum Q values to be ignored'
print,'lowfit: (default 0) if lowfit=1 then a polynomial is used to extrapolate to Q->0'
print,' normf: default normf=-normdatapdf.dat- normalization file generated withcreanorm' 
print,'qualstring : string to be added to file names for better identification, default: no strings attached'
print,'packfrac: (default 1.) packing fraction of the sample'
print,'comment: contains a string that is written int the output file proceeded by #, e.g. Qmax can be noted here'
return
end

qign=ignq
; define material constants for Vanadium
rhovana=0.0722 ;density Vanadium uc/A^3
sigmavana=5.08 ;elastic scattering cross section 
d1vana=0.627 ; diameter of our standard vanadium bar

;read normalization file
openr,1,normf,err=err
close,1
if err ne 0 then begin
print,err,'no normalization file'
stop
return
end
restore,normf

;read  background file
openr,1,backfile,err=err
close,1
if err ne 0 then begin
print,err,'no background file'
return
end
restore,backfile

normall=normpdf(0,*)+normpdf(1,*)+normpdf(2,*)+normpdf(3,*)+normpdf(4,*)+normpdf(5,*)
normall=reform(normall)

smb=a-aback ;sample minus background
smb(where (normall gt 0))=smb(where (normall gt 0))/normall(where (normall gt 0)) ;normalize the data to vanadium
if var_defined(error) and var_defined(ebacka) then begin
 esmb=sqrt(error^2+ebacka^2)
esmb(where (normall gt 0))=esmb(where (normall gt 0))/normall(where (normall gt 0))
endif
if lowfit then begin             ;extrapoation to Q->0
res=poly_fit(q(qign:qign+nlowfit)^2,smb(qign:qign+nlowfit),2)
if interactive then begin
plot,q(0:qign+nlowfit*3),smb(0:qign+nlowfit*3),ps=2,title='Extrapolation to Q->0',xtit='Q/A!e-1'
oplot,q(qign:qign+nlowfit*3),smb(qign:qign+nlowfit),ps=2,color=255
oplot,q(0:qign+nlowfit),poly(q(0:qign+nlowfit)^2,res)
oplot,q(0:qign+nlowfit*3),q(0:qign+nlowfit*3)*0+mean(smb(qign:qign+nlowfit))
prtc
end
smb(0:qign)=poly(q(0:qign)^2,res)
end
if not lowfit then begin
smb(0:qign)=mean(smb(qign:qign+nlowfit))
if interactive then begin
plot,q(0:qign+nlowfit*3),smb(0:qign+nlowfit*3),ps=2,title='Extrapolation to Q->0',xtit='Q/A!e-1'
oplot,q(0:qign+nlowfit*3),q(0:qign+nlowfit*3)*0+mean(smb(qign:qign+nlowfit))
prtc
end
end

if n_elements(smb) ne 2500 then print,' Careful. This does not appear to be a standard file'

; Placzek "correction"

if (hydrogen eq 0) then respla=poly_fit(q(fr(q,qminpla):fr(q,qmaxpla))^2,smb(fr(q,qminpla):fr(q,qmaxpla)),2)
if (hydrogen eq 2) then begin
aa=[10,6,.5,6.,.1]
respla=curvefit(q(fr(q,qminpla):fr(q,qmaxpla)),smb(fr(q,qminpla):fr(q,qmaxpla)),q(fr(q,qminpla):fr(q,qmaxpla))+0+1,aa,funct='pseudovoigt',/noder)
pseudovoigt,q,aa,pla
end

if interactive then begin ; plot the fitted polynomial/ pseudovoigt
if not var_defined(disply) then disply=[min(smb),max(smb)]
plot,q,smb,xra=displq,yra=disply,ytit='Normalized intensity',xtit='Q/A!e-1'
oplot,q,q*0+rho*sigma*d1^2/(rhovana*sigmavana*d1vana^2)*packfrac,color=255,th=3,li=2
if hydrogen eq 0 then oplot,q,poly(q^2,respla),color=255
if hydrogen eq 2 then oplot,q,pla,color=255
prtc
endif
bsmb=b-bback
bsmb(where (normpdf gt 0))=bsmb(where (normpdf gt 0))/normpdf(where (normpdf gt 0))
if hydrogen eq -1 then sq=smb-rho*sigma*d1^2/(rhovana*sigmavana*d1vana^2)*packfrac
if hydrogen eq 0 then sq=smb-poly(q^2,respla)
if hydrogen eq 2 then sq=smb-pla


; define S(Q) either by high Q normalization or by absolute normalization

if usehq and hydrogen eq 0 then begin
sq=sq/poly(max(q)^2,respla);*rhovana*sigmavana/rho/sigma
if var_defined(error) and var_defined(ebacka) then esq=esmb/poly(max(q)^2,respla)
endif
if usehq and hydrogen eq 2 then begin
sq=sq/pla(fr(q,49));*rhovana*sigmavana/rho/sigma
if var_defined(error) and var_defined(ebacka) then esq=esmb/pla(fr(q,49))
endif
if not usehq then begin
sq=sq/rho/sigma/d1^2*rhovana*sigmavana*d1vana^2/packfrac
if var_defined(error) and var_defined(ebacka) then esq=esmb/rho/sigma/d1^2*rhovana*sigmavana*d1vana^2/packfrac
endif
if interactive then begin
plot,q,sq,ytit='A (S(Q)-1)',xtit='Q/ A!e-1',chars=2
prtc
endif

if hydrogen eq 1 then begin
hplazcek,q,b,normpdf,pla
if interactive then begin
plot,q,smb
oplot,q,pla,color=255
prtc
endif
endif
;;;sq=smb-pla
;;;stop
nr=maxr/.01

fteqs,q(0:fr(q,qmaxft)),sq,rr,ft
fteqs,q(0:fr(q,qmaxft)),sq,findgen(nr)*.01,ft1
fteqs,q(0:fr(q,qmaxft)),sq,findgen(nr)*.01,ftl,l=1

f1=rho*sigma/rhovana/sigmavana*d1^2/d1vana^2
ft=ft/2/!pi^2/rho/sbs*sb2/packfrac
ft1=ft1/2/!pi^2/rho/sbs*sb2/packfrac
ftl=ftl/2/!pi^2/rho/sbs*sb2/packfrac
if interactive then begin
plot,findgen(nr)*.01,ft1,xra=[l(0),l(1)],ytit='g(r)-1',xtit='r/A',chars=2
oplot,findgen(nr)*.01,ftl,color=255,th=2
oplot,rr,ft,ps=2
prtc
plot,findgen(nr)*.01,ft1*findgen(nr)*.01,xra=[1,maxr],ytit='PDF = r (g(r)-1)/A',xtit='r/A',chars=2
oplot,findgen(nr)*.01,ftl*findgen(nr)*.01,color=255,th=2
oplot,rr,ft*rr,ps=2
prtc
endif
if scannr gt 9999 and scannr le 99999 then astring=string(scannr,format='(i5)')
if scannr gt 999 and scannr le 9999 then astring=string(scannr,format='(i4)')
if scannr gt 99 and  scannr le 999 then astring=string(scannr,format='(i3)')
if scannr gt 9 and  scannr le 99 then astring=string(scannr,format='(i2)')
if scannr lt 10 then astring=string(scannr,format='(i)')
wstd,findgen(nr)*.01,ft1,'NOM_'+astring+qualstring+'ftf.dat',comment=comment
wstd,findgen(nr)*.01,ft1*findgen(nr)*.01,'NOM_'+astring+qualstring+'ftfrgr.dat',comment=comment
wstd,findgen(nr)*.01,ft1*findgen(nr)*.01,'NOM_'+astring+qualstring+'ftfrgr.gr',comment=comment
wstd,findgen(nr)*.01,ftl,'NOM_'+astring+qualstring+'ftl.dat',comment=comment
wstd,findgen(nr)*.01,ftl*findgen(nr)*.01,'NOM_'+astring+qualstring+'ftlrgr.gr',comment=comment
wstd,rr,ft,'NOM_'+astring+qualstring+'ftnat.dat',comment=comment
if (not var_defined(error)) or (not var_defined(ebacka)) then wstd,q,sq,'NOM_'+astring+qualstring+'SQ.dat',comment=comment
if var_defined(error) and var_defined(ebacka) then wstd,q,[[reform(sq)],[reform(esq)]],'NOM_'+astring+qualstring+'SQ.dat',comment=comment,nz=3


gr=ftl

return
end


C SRSLIB PROGRAM SMFFT
C                     
C PURPOSE: SMOOTHS DATA BY FILTERING OUT HIGH HARMONICS IN FT SPECTRUM
C             
C LIMITATIONS:
C             
C 1. ARRAYS DIMENSIONED FOR MAXIMUM 32800 POINTS
C 2. NO CHECKS FOR VALID INPUT DATA ARE MADE    
C 3. ABSCISSA VALUES ASSUMED EQUIDISTANT        
C 4. NAG FFT ROUTINES 
C
C GLOBALS:
C
C CDSQ   : LOGARITHM OF POWER SPECTRUM  
C WF     : WIENER FILTER ORDINATE (DECIBELS)
C RNOISE : NOISE LEVEL                      
C RJLEV  : REJECTION LEVEL                  
C ITURN  : NUMBER OF ITERATIONS             
C NUMBER : NO OF OUTLIER POINTS             
C J0     : THESHOLD FREQUENCY               
C
C LOCAL VARIABLES: 
C                  
C X     : ABSCISSA VALUES
C YORIG : ORIGINAL ORDINATE VALUES 
C YANS  : SMOOTHED ORDINATE VALUES 
C YDIF  : RESIDUAL ORDINATE VALUES 
C TITLE : INPUT FILE TITLE RECORD  
C ANSWER: USER ANSWER TO PROMPT    
C IDSN  : INPUT FILE NAME          
C IREJ  : OUTLIER REJECTION FLAG
C FOUR  : CONSTANT 4.3429448    
C EPS7  : CONSTANT 10E-7        
C IPOS  : SCREEN POSITION POINTER
C NPOINT: NUMBER OF INPUT POINTS 
C                                
	SUBROUTINE SMOO(smoo_get, smoo_put)
	EXTERNAL smoo_get, smoo_put
	PARAMETER (np=512,nph=256,mn=33000)
	COMMON /WIEN/ CDSQ(mn),WF(mn),RNOISE,ITURN,NUMBER,J0,RJLEV    
	real*4 Xin(mn),Yin(mn),Ein(mn),Xout(mn),Yout(mn),Eout(mn)
	LOGICAL*1 IDSN(44)	
	real*4 X(mn), YORIG(mn), YANS(mn), YDIF(mn)	

	DATA IREJ/1/,IPOS/770/
	DATA FOUR/4.3429448/,EPS7/10.0E-7/
	DATA INPUT/1/,ITERM/5/,IPRINT/6/,IDEV/5/,IOUT/17/,IWF/18/	
C
C=========READ INPUT DATA                                               00000970
C                                                                       00000980
	call module_get_int(smoo_get, 'lptin', lptin)	
	call module_get_real_array(smoo_get, 'Xin', Xin, lptin)	
	call module_get_real_array(smoo_get, 'Yin', Yin, lptin)	
	call module_get_real_array(smoo_get, 'Ein', Ein, lptin)	
	call module_get_int(smoo_get, 'ider', ider)	

	if(lptin.eq.0)then              !check #points
	  call module_error(" smoo>",
	1 "ERROR  ** No input data", " ")
	  call module_put_int(smoo_put, 'kill', 1)	
	  RETURN
	endif
	do n=1,lptin
	 X(n)=xin(n)
	 yorig(n)=yin(n)
	end do

	npoint= lptin
	irej = 1
C          
C=========FILTER DATA
C                    
	jflag=0
c	ider=0
      CALL FILTER (X,YORIG,YANS,YDIF,NPOINT,IREJ,NHALF,JFLAG,IDER)           

	do I=1,NHALF
	 IF (CDSQ(I).LT.EPS7) CDSQ(I)=EPS7
	 IF (WF(I).LT.EPS7) WF(I)=EPS7    
	 CDSQ(I)=FOUR*ALOG(CDSQ(I)/RNOISE)
	 WF(I)=FOUR*ALOG(WF(I))           
	end do             

	lptout=lptin
	do n=1,lptout
	 yout(n)=yans(n)
	end do
	call module_put_int(smoo_put, 'lptout', LPTOUT)       
	call module_put_real_array(smoo_put, 'Xout', Xout, lptout)	
	call module_put_real_array(smoo_put, 'Yout', Yout, lptout)	
	call module_put_real_array(smoo_put, 'Eout', Eout, lptout)
	call module_put_int(smoo_put, 'kill', 0)	
c
	RETURN
	END
C++++++++++++++++++++++++++++++++++++++++++++++++
      SUBROUTINE FILTER (X,YOR,Y,YDIF,NPOINT,IREJ,NHALF,JFLAG,IDER)    
C                                                      
C PURPOSE: FOURIER FILTERS INPUT DATA                 
C                                                      
	parameter (mn=33000)
	real*4 X(mn),YOR(mn),Y(mn),YDIF(mn),Z(mn)
	real*4 DER1(mn),DER2(mn)
	INTEGER NPOINT,IREJ,NHALF,JFLAG
C                                                        
C INPUT ARGUMENTS:                                       
C                                                        
C     X       : ABSCISSA VALUES                          
C     YOR     : ORDINATE VALUES                            
C     NPOINT  : NUMBER OF COORDINATE VALUES              
C     JFLAG   : CUT-OFF FREQUENCY OVERRIDING J0 IF JFLAG>0   
C     IREJ    : OUTLIER REJECTION FLAG, 2 FOR YES, 1 FOR NO   
C                                                  
C RETURNED VALUES :                                
C                                                
C     Y       : SMOOTHED ORDINATES              
C     YDIF    : RESIDUALS                       
C     NHALF   : NUMBER OF FOURIER SPECTRUM POINTS   
C                                        
C GLOBALS:                               
C                                             
	COMMON /WIEN/ CDSQ(mn),WF(mn),RNOISE,ITURN,NUMBER,J0,RJLEV 
	REAL*4 CDSQ,WF,RNOISE,RJLEV
	INTEGER ITURN,NUMBER,J0
C                                                    
C CALLS   5: REJECT , C06EAF , FILTER , C06GBF , C06EBF 
C CALLED BY: MAIN                                  
C                                                  
C LOCAL VARIABLES:                                
C                                                
	DOUBLE PRECISION COEFF(mn),A(mn),B(mn),C(mn),D(mn)
	dimension LIER(mn),ILST(26)
	INTEGER N2,M,MPLUS1,M1,NFULL,N0,KK,K,N0K1
	LOGICAL INVERS
C                                                 
C A, B  :REAL AND AND IMAGINARY PART OF FT     
C LIERS : INDICES OF OUTLIER POINTS           
C                                             
	DATA ZERO/0.0/,P6/0.6931451/,IPRINT/6/
C                                               
	ITURN=0                                     
	ICOUNT = IDER
	NUMBER=0
C                                        
C=========FIND OUTLIER REJECTION LEVEL FOR NPOINT POINTS
C                                               
C      CALL REJECT (NPOINT,RJLEV)               
C      WRITE (IPRINT,250) NPOINT,RJLEV           
C                                             
C=========FIND M POWER OF 2 SUCH THAT 2**M<N<=2**(M+1)   
C                                             
	IFLAG = 0
	M=ALOG(FLOAT(NPOINT))/P6
	IF (NPOINT.EQ.2**M) M=M-1
	MPLUS1=M+1
	NHALF=2**M
C                                           
C=========FIND DIFFERENCE BETWEEN NPOINT AND 2**MPLUS1  
C                                    
	NFULL=2*NHALF
	MDIFF=NFULL-NPOINT
	WRITE (IPRINT,280) MDIFF,MPLUS1,NFULL
	do I=1,NPOINT
	 Y(I)=YOR(I)
	end do
C                                 
C=========SUBTRACT CUBIC SPLINE TIED AT FIRST AND LAST POINTS  
C                                         
 20	continue
	ICOUNT = ICOUNT - 1

	CALL SUBSPLINE(NPOINT,X,Y,Z,DER1,DER2)
      DO 30 I=1,NPOINT
         YI=Y(I)
         Y(I)=YI-Z(I)
  30  CONTINUE
C                                 
C=========SET POINTS BETWEEN NPOINT AND 2**MPLUS1 TO 0 IF MDIFF>0  
C                                     
      IF (MDIFF.EQ.0) GOTO 50
      DO 40 I=1,MDIFF
         Y(NPOINT+I)=ZERO
  40  CONTINUE
C                                            
C=========FOURIER TRANSFORM                           
C         VALUES RETURNED IN A AND B ARE THE           
C         THE COSINE AND SINE COEFFICIENTS, RESPECTIVELY. 
C                                                
  50  IFAIL=0
	ITURN=ITURN+1
	IF ( IFLAG .EQ. 0 ) THEN
	 do I=1,NFULL
	  COEFF(I)=Y(I)
	 end do
	ELSE
	 JFLAG = 0
	 do I=1,NFULL
	  COEFF(I) = Z(I)
	 end do
	ENDIF

	CALL C06EAF (COEFF,NFULL,IFAIL)
c      WRITE (IPRINT,200) NFULL
C                                      
C=========ASSIGN FOURIER COEFFICIENTS      
C                                           
      N2=(NFULL+1)/2
c      WRITE (IPRINT,210) N2
      A(1)=COEFF(1)
      B(1)=0.0
      DO 70 J=2,N2
         NJ=NFULL-J+2
         A(J)=COEFF(J)
         A(NJ)=COEFF(J)
         B(J)=COEFF(NJ)
         B(NJ)=-COEFF(NJ)
  70  CONTINUE
      IF (MOD(NFULL,2).NE.0) GOTO 80
      A(N2+1)=COEFF(N2+1)
      B(N2+1)=0.0
C                                           
C=========CALCULATE POWER SPECTRUM CDSQ    
C                                 
      FPOINT=FLOAT(NFULL)/4.0
      N21=N2+1
  80  DO 90 I=1,N21
         AA=A(I)
         BB=B(I)
         CDSQ(I)=(AA*AA+BB*BB)/FPOINT
  90  CONTINUE
      FFFF=FLOAT(NFULL)/FLOAT(NPOINT)
      NPHALF=NPOINT/2
      K=NPHALF/2
      SUMN0=ZERO
      FNK=FLOAT(NPHALF)/(FLOAT(2*K))
      DO 100 KK=1,K
         J=FLOAT(N21)-FLOAT(KK)*FFFF+1.0
         SUMN0=SUMN0+CDSQ(J)
  100 CONTINUE
C                                               
C=========FIND FLUCTUATION LEVEL OF FOURIER HARMONICS 
C                                           
	RNOISE=SUMN0/FLOAT(2*K)
	SIGMA2=FNK*SUMN0
	SIGMA=SQRT(SIGMA2)
c      WRITE (IPRINT,290) SIGMA,RNOISE
C                                       
C=========CALCULATE FILTER FUNCTION AND MULTIPLY FOURIER COEFFICIENTS
C                                        
	CALL WIENER (A,B,N21,JFLAG)
c      WRITE (IPRINT,220) N2,J0       
	write(IPRINT,220) N2
C                                     
C=========INVERSE FOURIER TRANSFORM   
C                                  
	IFLAG = IFLAG + 1
	ISTEM= IDER/2
	STEM= -1*ISTEM
	IF (IDER.EQ.0 .OR. ICOUNT.LT.IDER - 1) THEN

       DO 110 J=2,N2
         C(J)=A(J)
         D(J)=B(J)
         NJ=NFULL-J+2
         C(NJ)=C(J)
         D(NJ)=-D(J)

  110  CONTINUE

      ELSE IF (IDER.EQ.1) THEN

       DO 111 J=2,N2
         C(J)=FLOAT(J)*-B(J)
         D(J)=FLOAT(J)*A(J)
         NJ=NFULL-J+2
         C(NJ)=C(J)
         D(NJ)=-D(J)
  111 CONTINUE

      ELSE IF ( IDER .EQ. 2 ) THEN

       DO 112 J=2,N2
         CTEM= STEM*FLOAT(J)**IDER
         C(J)=CTEM*A(J)
         D(J)=CTEM*B(J)
         NJ=NFULL-J+2
         C(NJ)=C(J)
         D(NJ)=-D(J)
  112  CONTINUE
      ENDIF


      COEFF(1)=A(1)
      DO 120 J=2,N2
         NJ=NFULL-J+2
         COEFF(J)=0.5*(C(J)+C(NJ))
         COEFF(NJ)=0.5*(D(J)-D(NJ))
  120 CONTINUE
      IF (MOD(NFULL,2).EQ.0) COEFF(N2+1)=A(N2+1)
C                                          
	CALL C06GBF (COEFF,NFULL,IFAIL)
	CALL C06EBF (COEFF,NFULL,IFAIL)
	IDERLAST= IDER
c      WRITE (IPRINT,230) NFULL                 
C                                             
C=========RESTORE ORDINATES TO ORIGINAL SCALE BY ADDING "BACKGROUND"
C                                            
      IF (IFLAG .EQ. 1 ) THEN

         DO I=1,NPOINT
           Y(I) = COEFF(I)
         END DO
         IF ( IDER .EQ. 0 ) THEN
         DO I=1,NPOINT
            Y(I) = Y(I) + Z(I)
         END DO
         GOTO 9999
         ENDIF
      ELSE
         DO I=1,NPOINT
           Z(I) = COEFF(I)
           Y(I) = Y(I) + Z(I)
         END DO
      ENDIF

      IF ( IFLAG .LT. 2 ) GOTO 50
C
C      IF (IDER .EQ. 0 .OR. ICOUNT .LT. IDER - 1 ) THEN
C       DO 130 I=1,NPOINT             
C         YI=COEFF(I)                
C         TYPE *,YI
C         Y(I)=YI+Z(I)
C  130  CONTINUE                      
C      ELSE IF (IDER .EQ. 1) THEN
C       DO 131 I=1,NPOINT           
C         YI=COEFF(I)              
C         Y(I)=YI+DER1(I)
C  131  CONTINUE                      
C      ELSE IF (IDER .EQ. 2) THEN
C       DO 132 I=1,NPOINT             
C         YI=COEFF(I)               
C         Y(I)=YI+DER2(I)
C  132  CONTINUE                     
C      END IF
c9999   WRITE (IPRINT,240) NPOINT    
9999	continue
C      JFLAG = 0
C      J0 = 0
C      IF ( ICOUNT .GT. -1 ) GOTO 20
C                                   
C=========CALCULATE RESIDUALS      
C                                   
      DO 140 I=1,NPOINT                  
         YDIF(I)=YOR(I)-Y(I)
  140 CONTINUE
      IF (IREJ.EQ.1) GOTO 180
C                                           
C=========FIND OUTLIERS FOR CYCLE ITURN      
C                                            
      IDN=NUMBER
      NUMBER=0
      DO 150 I=1,NPOINT
         DIF=ABS(YDIF(I))/SIGMA
         IF (DIF.LE.RJLEV) GOTO 150
         NUMBER=NUMBER+1
         LIER(NUMBER)=I
  150 CONTINUE
c      WRITE (IPRINT,300) NUMBER,ITURN        
c      WRITE (IPRINT,260) (LIER(K),K=1,NUMBER) 
	IF (NUMBER.LE.0) GOTO 180
	IDN=NUMBER-IDN
	IF (IDN.EQ.0) GOTO 180
C                                      
C=========REPLACE OUTLIER ORDINATE WITH CURRENT SMOOTHED ORDINATE VALUE
C                                                                      
c      WRITE (IPRINT,310)              
      DO 170 I=1,NPOINT
         DO 160 K=1,NUMBER
            IF (I.EQ.LIER(K)) GOTO 170
  160    CONTINUE
         Y(I)=YOR(I)
  170 CONTINUE
      GOTO 20
C                                           
C=========NO MORE OUTLIERS TO BE REPLACED  
C                                        
c  180 WRITE (IPRINT,270) NUMBER,ITURN    
180	continue
	RETURN
C                             
  200 FORMAT(' > FORWARD FFT FOR ',I5,' POINTS COMPLETE')
  210 FORMAT(' > ASSIGNING ',I5,' FOURIER COEFFICIENTS')
c  220 FORMAT(' > WIENER FILTER CALCULATED FOR '
c     + ,I5,' COEFFICIENTS',/,
c     + 11x,' CUT-OFF FREQUENCY ',I4)
220	FORMAT(' fourier> filter at ',I5,' coefficients')
  230 FORMAT(' > INVERSE FFT FOR ',I5,' POINTS COMPLETE')
  240 FORMAT(' > BASELINE ORDINATES ADDED TO ',I5,' POINTS')
  250 FORMAT (11x,' REJECTION LEVEL FOR ',I5,' POINTS:',E13.5)
  260 FORMAT (128(8I5,/))
  270 FORMAT (11x,I6,' OUTLIER POINTS REJECTED IN ',I3,' CYCLES')
  280 FORMAT (' fourier> ',I6,' points set to zero to padd 2**',I4,
  	1'=',I5,' data points')
  290 FORMAT (11x,' SIGMA=',E13.5,' RNOISE=',E13.5)
  300 FORMAT (11x,I6,' OUTLIER POINTS FOR CYCLE',I5)
  310 FORMAT (' REPEATING FILTERING TO REJECT OUTLIERS')
	END

C+++++++++++++++++++++++++++++++
	SUBROUTINE REJECT (N,X)
C                                              
C PURPOSE: COMPUTATES OUTLIER REJECTION LEVEL FOR RANDOM NUMBERS 
C          WITH NORMAL DISTRIBUTION       
C                           
C CALLS   0:                 
C CALLED BY: FILTER          
C                            
	NP=2*(N/2)
	X=3.8+0.15*(ALOG(FLOAT(N))/ALOG(2.0)-6.0)
C                                                            
C...USE NEXT LINE OR IBM SCIENTIFIC SUBROUTINE LIBRARY ROUTINE NDTRI 
C                                       
CIBM  P=(1.0-0.01/2.0)**(1.0/FLOAT(NP))
CIBM      CALL NDTRI (P,X,D,IER) 
	RETURN
	END

C++++++++++++++++
	SUBROUTINE WIENER (A,B,N,JFLAG)
C                                
C PURPOSE: CALCULATES WIENER FILTER FUNCTION  
C                                  
	parameter (mn=33000)
	DOUBLE PRECISION A(mn),B(mn)
	INTEGER N,JFLAG
C                           	
	COMMON /WIEN/ CDSQ(mn),WF(mn),RNOISE,ITURN,NUMBER,J0,RJLEV
	DOUBLE PRECISION C,D,WFI,ALPHA
	REAL*4 CDSQ,WF,RNOISE,RJLEV
	INTEGER ITURN,NUMBER,J0
C                                                   	
C     WF= CD1/(1+CD1),  WHERE CD1=CD/RNOISE, AND  CD=C*C+D*D 	
C     AS  CD1>1                                     	
C     AND EXTRAPOLATION OF CD1 UP TO J1, WHERE J1 EQUALS  	
C     THE HARMONIC NUMBER, WHERE CD1 (DB) < -20 DB.  	
C                                                     	
C CALLS   0:                                     	
C CALLED BY: FILTER                              	
C                                                 	
	      DATA ONE/1.0/,TWO/2.0/,ZERO/0.0/,FOUR/4.3429448/,DBLEV/-20.0/
C                                        	
c      WRITE(6,1)
c1     FORMAT(/,11X,'>> INPUT ALPHA :'$)
c      ACCEPT *,ALPHA
	do IK=1,N
	 WF(IK)=ZERO
	end do
	J0=1
	J1=1
	XX=ZERO
	XY=ZERO
	YM=ZERO
      DO 40 J=1,N
         CD1=CDSQ(J)/RNOISE
         CD2=ALOG(CD1)
         IF (JFLAG.NE.0) GOTO 20
         IF (J0.GT.1) GOTO 50
         IF ((CD1.LE.ONE).AND.(J0.EQ.1)) J0=J
         GOTO 30
  20     IF (JFLAG.LT.J) GOTO 50
  30	WF(J)=CD1/(ONE+CD1)
         XX=XX+FLOAT(J*J)
         XY=XY+FLOAT(J)*CD2
         YM=YM+CD2
  40  CONTINUE
  50  IF (JFLAG.NE.0) J0=JFLAG
	RJ0F=FLOAT(J0)
	XM=(ONE+RJ0F)/TWO
	YM=YM/RJ0F
	A1=(XY-RJ0F*XM*YM)/(XX-RJ0F*XM**2)
	B1=YM-A1*XM
	J1=(DBLEV/FOUR-B1)/A1
	do J=J0,J1
	 S=EXP(A1*FLOAT(J)+B1)
	 WF(J)=S/(ONE+S)
	end do
c     ALPHA = 0.2
c     
	do I=1,N
	 WFI=WF(I)
	 C=A(I)
	 D=B(I)
c        WFI = WFI / ( 1. + DEXP ( DFLOAT ( I - J0 ) / ( ALPHA *
c    +       DFLOAT ( J0 ) ) ) )
	 A(I)=WFI*C
	 B(I)=WFI*D
	end do
	RETURN
	END

	subroutine SUBSPLINE(n,x,y,z,der1,der2)
c
c..	This subroutine evaluates a crude background z(i)
c	to be used as a baseline subtraction
c	and also 1st to 3rd derivatives.
	parameter  (nmax=33000,knots=10)
	real*4	x(n),y(n),z(nmax),der1(nmax),der2(nmax)
	real*4	val(4)
	real*4	xknot(knots),yknot(knots)
	real*4	dknot(knots),work(3*knots)
c
	ntem= n/(knots-1)
	xknot(1)= x(1)
	xknot(knots)= x(n)
	yknot(1)= y(1)
	yknot(knots)= y(n)
c
	do l=1,knots-2
c	iimin= l*ntem - jnint(0.5*float(ntem))
	 iimin= l*ntem - nint(0.5*float(ntem))
	 call MINMAX2(y(iimin),ntem,yknot(l+1),yt,imin,imax)
	 item= iimin + imin -1
	 xknot(l+1)= x(item)
	end do
c
	call TB04A(knots,xknot,yknot,dknot,work)
c
	iopt= 1
	do i= 1,n
	 call TG02A(iopt,knots,xknot,yknot,dknot,x(i),val)
	 z(i)= val(1)
	 der1(i)= val(2)
	 der2(i)= val(3)
	end do
c
	return
	end
c
	subroutine MINMAX2(z,n,zmin,zmax,imin,imax)
	real*4 z(n)
c
c This subroutine finds the minimum and maximum values in a graph
c and additionally gives the bin no. associated with these values.
c
	zmin=z(1)
	zmax=z(1)
	imin=1
	imax=1
	do 10 i=1,n
	 if (z(i) .gt. zmax) then
		zmax=z(i)
		imax=i
		goto 10
	 end if
	 if (z(i) .lt. zmin) then
		zmin=z(i)
		imin=i
	 end if
 10	continue
c
	return
	end
* CMS REPLACEMENT HISTORY, Element MINMAX2.FOR
* *1    13-APR-1988 10:45:13 CMM "V2.3 Baseline elements inserted"
* CMS REPLACEMENT HISTORY, Element MINMAX2.FOR

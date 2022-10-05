CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
C
c (subroutines LOGQYN and STPACK copied from ASYM_RF.FOR 4/1/96.  PJCK)

c 11/1/1999 J.S. Lord   Added DEVA file access

      PROGRAM ASYM
C     ------------
C
      REAL    X(200),YI(200),YD(200),C(65536),F(2048,200),B(2048,200)
      REAL    DELTA(32),EI(200),ED(200)
      LOGICAL AGAIN
      integer inst
      DATA    NCAL /32/
C
      CALL ASKSIZ(SIZE,IWIDTH)
      CALL CALIB(DELTA,NCAL)
      WRITE(*,*)
c      CALL LOGQYN(' Instrument>  Are data from MuSR (else EMU) ?','Y',
c     *             LMUSR)

57	write(*,*)'Select instrument:'
	write(*,*)'1. MuSR'
	write(*,*)'2. EMU'
	write(*,*)'3. DEVA'
	read(*,*)inst
	if(inst.lt.1 .or. inst.gt.3) goto 57

      WRITE(*,*)
   1  WRITE(*,100)
 100  FORMAT(' >  First and last run number ?  : ',$)
      READ(*,*,ERR=1) ISTART,IEND
      IF (ISTART.LT.1 .OR. IEND.LT.ISTART) GOTO 1
      NRUNS=IEND-ISTART+1
      IF (NRUNS.GT.200) GOTO 1
   2  WRITE(*,110)
 110  FORMAT(' >  Balance parameter alpha ?    : ',$)
      READ(*,*,ERR=2) ALPHA
      IF (ALPHA.LT.0.01 .OR. ALPHA.GT.100.0) GOTO 2
      K=1
      DO 10 IRUN=ISTART,IEND
        CALL GETFIL(IRUN,NT,NH,H,C,DXTIME,NFRAMS,inst)
        IF (NCAL.LE.32 .AND. NCAL.NE.NH) STOP ' # of Hist mismatch!'
        CALL FORBCK(C,NH,NT,ALPHA,F(1,K),B(1,K),DELTA,DXTIME,NFRAMS)
        X(K)=H
        K=K+1
  10  CONTINUE
      WRITE(*,*)
   3  WRITE(*,120)
 120  FORMAT(' >  First and last time channel ?  : ',$)
      READ(*,*,ERR=3) I1,I2
      IF (I1.LT.1 .OR. I2.GT.NT .OR. I2.LT.I1) GOTO 3
      DO 20 K=1,NRUNS
        CALL INTSYM(F(1,K),B(1,K),I1,I2,YI(K),EI(K))
        CALL DIFSYM(F(1,K),B(1,K),I1,I2,YD(K),ED(K))
  20  CONTINUE
      WRITE(*,*)
      WRITE(*,*)' Integral Asymmetry'
      CALL PLOT(X,YI,EI,NRUNS,1,SIZE,IWIDTH)
      WRITE(*,*)
      WRITE(*,*)' Differential Asymmetry'
      CALL PLOT(X,YD,ED,NRUNS,2,SIZE,IWIDTH)
      WRITE(*,*)
      CALL LOGQYN(' >  Try another time window ?','Y',AGAIN)
      WRITE(*,*)
      IF (AGAIN) GOTO 3
      END
C
      SUBROUTINE CALIB(DELTA,NCAL)
C     ----------------------------
C
      REAL         DELTA(*)
      CHARACTER*60 FILNAM
C
      WRITE(*,*)
   1  WRITE(*,100)
 100  FORMAT(' INPUT>  Calibration Filename ?   : ',$)
      READ(*,200,ERR=1) NNN,FILNAM
 200  FORMAT(Q,A)
      IF (NNN.EQ.0) THEN
        WRITE(*,*)
   2    WRITE(*,110)
 110    FORMAT(' Calibration>  Dead time ? (nS)  : ',$)
        READ(*,*,ERR=2) DTIME
        DO 10 I=1,NCAL
  10      DELTA(I)=DTIME
        NCAL=1000
      ELSE
      OPEN(UNIT=2,FILE=FILNAM,STATUS='OLD',FORM='FORMATTED',READONLY,
     *     ERR=2)
        READ(2,*)
        READ(2,*)
        READ(2,*)
        READ(2,*)
        DO 20 I=1,NCAL
  20      READ(2,*,ERR=3,END=3) DELTA(I)
   3    NCAL=I-1
        CLOSE(UNIT=2)
        WRITE(*,*)
        WRITE(*,*)' No. of detectors in calibration file = ',NCAL
      ENDIF
      END
C
      SUBROUTINE FORBCK(C,NH,NT,ALPHA,F,B,DELTA,DX,NFRAMS)
C     ----------------------------------------------------
C
      REAL C(NH,NT),F(*),B(*),DELTA(*),DELTA2(32)
C
      DO 10 I=1,NH
  10    DELTA2(I)=DELTA(I)/(DX*FLOAT(NFRAMS))
      NH2=NH/2
      DO 30 J=1,NT
        SUMF=0.0
        SUMB=0.0
        DO 20 I=1,NH2
          IB=I+NH2
          DI=C(I,J)
          DIB=C(IB,J)
          SUMF=SUMF+DI/(1.0-DI*DELTA2(I))
          SUMB=SUMB+DIB/(1.0-DIB*DELTA2(I))
  20    CONTINUE
        F(J)=SUMF
        B(J)=ALPHA*SUMB
  30  CONTINUE
      END
C
      SUBROUTINE INTSYM(F,B,I1,I2,YI,EI)
C     ----------------------------------
C
      REAL F(*),B(*)
C
      SUMF=0.0
      SUMB=0.0
      DO 10 I=I1,I2
        SUMF=SUMF+F(I)
        SUMB=SUMB+B(I)
  10  CONTINUE
      YI=(SUMF-SUMB)/(SUMF+SUMB)
      VARI=(1.0+YI*YI)/(SUMF+SUMB)
      EI=SQRT(VARI)
      END
C
      SUBROUTINE DIFSYM(F,B,I1,I2,YD,ED)
C     ----------------------------------
C
      REAL F(*),B(*)
C
      SUM=0.0
      VARD=0.0
      DO 10 I=I1,I2
        FBNORM=1.0/(F(I)+B(I))
        Z=(F(I)-B(I))*FBNORM
        SUM=SUM+Z
        VARD=VARD+(1.0+Z*Z)*FBNORM
  10  CONTINUE
      YD=SUM/FLOAT(I2-I1+1)
      ED=SQRT(VARD)/FLOAT(I2-I1+1)
      END
C
C***<plottting routines>************************************************
C
      SUBROUTINE ASKSIZ(SIZE,IWIDTH)
C     ------------------------------
C
   1  WRITE(*,100)
 100  FORMAT(' PLOT>  Character Size ? (def=1.5)  : ',$)
      READ(*,200,ERR=1) NNN,SIZE
 200  FORMAT(Q,F)
      IF (NNN.EQ.0) SIZE=1.5
      IF (SIZE.LT.0.001) GOTO 1
   2  WRITE(*,110)
 110  FORMAT(' PLOT>  Line-widths ?    (def=1; try 5 for PS) : ',$)
      READ(*,210,ERR=2) NNN,IWIDTH
 210  FORMAT(Q,I)
      IF (NNN.EQ.0) IWIDTH=1
      IF (IWIDTH.LT.1 .OR. IWIDTH.GT.21) GOTO 2
      END
C
      SUBROUTINE PLOT(X,Y,E,N,ISYM,SIZE,IWIDTH)
C     -----------------------------------------
C
      REAL         X(*),Y(*),E(*),YLOW(200),YHIGH(200)
      LOGICAL      LWRITE,LERROR
      CHARACTER*60 FILNAM
C
      CALL MAXMIN(X,Y,N,XMIN,XMAX,YMIN,YMAX)
      WRITE(*,*)
      CALL LOGQYN(' Plot>  Display the error-bars ?','N',LERROR)
      WRITE(*,*)
      CALL PGBEGIN(0,'?',1,1)
      CALL PGSCH(SIZE)
      CALL PGSLW(IWIDTH)
      CALL PGENV(XMIN,XMAX,YMIN,YMAX,0,0)
      CALL PGPOINT(N,X,Y,4)
      IF (LERROR) THEN
        DO 10 I=1,N
          YLOW(I)=Y(I)-E(I)
          YHIGH(I)=Y(I)+E(I)
  10    CONTINUE
        CALL PGERRY(N,X,YLOW,YHIGH,0.0)
      ENDIF
      IF (ISYM.EQ.1) THEN
        CALL PGLABEL('Field  (G)','Asymmetry','Integral Asymmetry')
      ELSEIF (ISYM.EQ.2) THEN
        CALL PGLABEL('Field  (G)','Asymmetry','Differential Asymmetry')
      ENDIF
      CALL PGEND
      WRITE(*,*)
      CALL LOGQYN(' Output>  Write out an ASCII file ?','N',LWRITE)
      IF (LWRITE) THEN
        WRITE(*,*)
   1    WRITE(*,100)
 100    FORMAT(' Output>  Filename ?  : ',$)
        READ(*,200,ERR=1) FILNAM
 200    FORMAT(A)
        OPEN(UNIT=3,FILE=FILNAM,STATUS='NEW',FORM='FORMATTED',ERR=1)
        DO 20 I=1,N
          WRITE(3,110) X(I),Y(I),E(I)
 110      FORMAT(X,F7.1,2F9.5)
  20    CONTINUE
        CLOSE(UNIT=3)
      ENDIF
      END
C
      SUBROUTINE MAXMIN(X,Y,N,XMIN,XMAX,YMIN,YMAX)
C     ------------------------------------------
C
      REAL X(*),Y(*)
C
      XMIN=+1.0E20
      XMAX=-1.0E20
      YMIN=+1.0E20
      YMAX=-1.0E20
      DO 10 I=1,N
        IF (X(I).LT.XMIN) XMIN=X(I)
        IF (X(I).GT.XMAX) XMAX=X(I)
        IF (Y(I).LT.YMIN) YMIN=Y(I)
        IF (Y(I).GT.YMAX) YMAX=Y(I)
  10  CONTINUE
      XDIF=(XMAX-XMIN)/20.0+1.0E-10
      YDIF=(YMAX-YMIN)/20.0+1.0E-10
      XMIN=XMIN-XDIF
      XMAX=XMAX+XDIF
      YMIN=YMIN-YDIF
      YMAX=YMAX+YDIF
      WRITE(*,*)
   1  WRITE(*,100) YMIN,YMAX
 100  FORMAT(' Plot>  Ymin & Ymax ?  (def=',F7.3',',F7.3')  : ',$)
      READ(*,200,ERR=1) NNN,YMIN1,YMAX1
 200  FORMAT(Q,2F)
      IF (NNN.NE.0) THEN
        YMIN=YMIN1
        YMAX=YMAX1
      ENDIF
      END
CC
C***<logical question>**************************************************
C
      SUBROUTINE LOGQYN(S,D,L)
C     ------------------------
C
      LOGICAL      L,L2
      CHARACTER*1  D,D2,A
      CHARACTER*45 STRING
      CHARACTER    S(*)
C
      IF (D.EQ.'Y') THEN
        L=.TRUE.
        D2='N'
        L2=.FALSE.
      ELSEIF (D.EQ.'N') THEN
        L=.FALSE.
        D2='Y'
        L2=.TRUE.
      ELSE
        WRITE(*,*)' Default should be Y or N !'
        RETURN
      ENDIF
      CALL STPACK(STRING,S,45)
   1  WRITE(*,100)STRING,D
      READ(*,110)N,A
      IF (N.EQ.0) RETURN
      IF (A.EQ.'y' .OR. A.EQ.'T' .OR. A.EQ.'t') A='Y'
      IF (A.EQ.'n' .OR. A.EQ.'F' .OR .A.EQ.'f') A='N'
      IF (A.EQ.D) THEN
        RETURN
      ELSEIF (A.EQ.D2) THEN
        L=L2
        RETURN
      ENDIF
      GOTO 1
 100  FORMAT(A45' Y/N (def=',A1')  : ',$)
 110  FORMAT(Q,:,A1)
      END

C
      SUBROUTINE STPACK(STRING,S,N)
C     -----------------------------
C
      CHARACTER STRING(*),S(*)
C
      DO 10 I=1,N
        STRING(I)=S(I)
        IF (S(I).EQ.'?') GOTO 20
  10  CONTINUE
  20  DO 30 J=I+1,N
  30    STRING(J)=' '
      END
C
C***<hacked from Steve Johnston's program mcs_read.for>*****************
C
        SUBROUTINE GETFIL(IRUN,NT,NH,H,C,DXTIME,NFRAMS,inst)
C       -----------------------------------------------------
C
        REAL    C(*)
        integer inst
C
	character*80 mcs_file
	integer*4 file
        integer*4 ncan
	integer*2 ib(512)
	integer*2 istfla,rescod,nrun,numhis,histlen,numrec,reclen,i
	integer*2 t0bin(32),tgood_begin(32),tgood_end(32),j
	integer*2 ngroups,branch(4),crate(4),first(4),ndev(4)
	integer*2 begin,end
	integer*4 res_pscnds,ntotal(32)
	character rtitle*40, devtyp(4)*4
	character*9 start_date,stop_date
	character*8 start_time,stop_time
	logical*1 rgmode
	integer*2 nreads, framread
	character*32 grouping
        integer*4 rdata
	dimension rdata(64,2048)
	integer a,rtot,asy
	real redgrn,ntot(32),alpha,totred,totgrn,temp
	character*60 comment
c
	equivalence
	1 (istfla,ib(1)), (rescod,ib(2)), (res_pscnds,ib(7)),
	1 (nrun,ib(4)), (start_date,ib(110)), (stop_date,ib(115)),
	1 (start_time,ib(120)), (stop_time,ib(124)), (rtitle,ib(70)),
	1 (numhis,ib(16)), (histlen,ib(15)), (numrec,ib(65)),
	1 (reclen,ib(66)), (t0bin(1),ib(256-3*32)),
	1 (tgood_begin(1),ib(256-2*32)), (tgood_end(1),ib(256-32)),
	1 (ntotal(1),ib(256)), (branch(1),ib(512-5*4)),
	1 (crate(1),ib(512-4*4)), (first(1),ib(512-3*4)),
	1 (ndev(1),ib(512-2*4)), (devtyp(1),ib(512-4)),
	1 (ngroups,ib(512)),(comment,ib(431)),
	1 (rgmode,ib(67)),(nreads,ib(68)),(framread,ib(69))
C
	file=0
	type *,' '
c
c  ***  manufacture file name and search VAX & HUB ***
c
        FILE=irun
	type *,' '
	redgrn=1
        IF (inst.eq.1) THEN
	  write(mcs_file,1070)file
        ELSE IF (inst.eq.2) THEN
	  write(mcs_file,1071)file
	ELSE
	  write(mcs_file,1072)file
        ENDIF
	open(1,file=mcs_file,status='OLD',form='UNFORMATTED',
     1  err=201,readonly)
	goto 205
201     IF (inst.eq.1) THEN
	  write(mcs_file,1060)file
        ELSE IF (inst.eq.2) THEN
	  write(mcs_file,1061)file
        ELSE
	  write(mcs_file,1062)file
        ENDIF
	type *,'File not present in uVAX,searching the HUB'
	open(1,file=mcs_file,status='OLD',form='UNFORMATTED',
     1  err=202,readonly)
	goto 205
202     IF (inst.eq.1) THEN
	  write(mcs_file,1080)file
        ELSE IF (inst.eq.2) THEN
	  write(mcs_file,1081)file
        ELSE
	  write(mcs_file,1082)file
        ENDIF
	type *,'File not present in uVAX,searching the HUB'
	open(1,file=mcs_file,status='OLD',form='UNFORMATTED',
     1  err=203,readonly)
	goto 205
203	type *,'File not present in HUB,re-enter valid file number'
	type *,' '
        RETURN
c
c  ***  enter data from MCS file into decimal form (from binary)  ***
c
205	read(1) ib
	if (rgmode.eq.0) goto 99
	redgrn=2
99	do 100 ih=1,numhis*redgrn
100	   read(1) (rdata(ih,i),i=1,histlen)
	close(1)
	rtitle(30:30)=rtitle(29:29)
c
c  ***  print title and header of file  ***
c
	type *,' '
102	rtitle(11:11)=' '
	rtitle(20:20)='K'
	rtitle(29:29)='G'
	type *,' '
	type *,'Sample                : ',rtitle(1:11)
	type *,'Temperature           : ',rtitle(12:20)
	type *,'Field                 : ',rtitle(21:29)
        READ(RTITLE(21:28),*) H
	if (rtitle(30:30).ne.'l') goto 801
	type *,'Orientation           : LONGITUDINAL'
	goto 803
801	if (rtitle(30:30).ne.'t') goto 802
	type *,'Orientation           : TRANSVERSE'
	goto 803
802	type *,'Orientation           : ',rtitle(30:30)
	numgroup=5
803	type *,'Collimation           : ',rtitle(31:40)
	type *,' '
	type *,'Start time            : ',start_time
	type *,'Stop time             : ',stop_time
	type *,'Start date            : ',start_date
	type *,'Stop date             : ',stop_date
	type *,' '
	type 1020,res_pscnds
	ncan=int(nreads)*int(framread)
	type 1030,ncan
	type 1040,numhis
	type 1050,histlen
        NH=numhis
        NT=histlen
        DXTIME=FLOAT(res_pscnds)/1000.0
        NFRAMS=ncan
        K=0
        DO J=1,NT
          DO I=1,NH
            K=K+1
            C(K)=FLOAT(RDATA(I,J))
          ENDDO
        ENDDO
1020	format(' Resolution            : ',1i6,' pS')
1030	format(' Total no. of frames   : ',1i8)
1040	format(' Number of histograms  : ',1i3)
1050	format(' Number of time bins   : ',1i5)
1060	format('MUSR$DISK:[MUMGR.DATA]MUS',i5.5,'.RAW')
1070	format('MUSR$DISK0:[DATA.MUSR]R',i5.5,'.RAL')
1080	format('SCRATCH$DISK:[MUMGR.RESTORE]USR',i5.5,'.RAW')
1061	format('MUSR$DISK:[EMUMGR.DATA]EMU',i5.5,'.RAW')
1071	format('EMU$DISK0:[DATA.EMU]R',i5.5,'.RAL')
1081	format('SCRATCH$DISK:[EMUMGR.RESTORE]EMU',i5.5,'.RAW')
1062	format('MUT$DISK:[MUTMGR.DATA]MUT',i5.5,'.RAW')
1072	format('MUT$DISK0:[DATA.MUT]R',i5.5,'.RAL')
1082	format('SCRATCH$DISK:[MUTMGR.RESTORE]MUT',i5.5,'.RAW')
	end
C
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

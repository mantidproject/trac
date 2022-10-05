CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
C
      PROGRAM ASYM_RG
C     ---------------
C
C  9-FEB-97 C A Scott   Corrected typo in error calc in INTSYM
C                       Effect of typo was to underestimate
C                       error by a factor of 1.4
C
C 18-MAY-1998 J S Lord  Version for 16 Red & 16 Green histograms on EMU
C 
C    NOV-1998 S P Cottrell  Version for 32 Red & 32 Green histograms on muSR
C
C  7-JAN-1999 S P Cottrell  Added run numbers in titles on graph, fixed size
C                           of graph components and added facility to
C                           create a PGPLOT.PS file immediately after
C                           viewing plot
C
C 29-APR-2006 S P Cottrell Reads only NeXus files
C
C 4-OCT-2006  S P Cottrell Can dig scans out of multiperiod data files
C
C 
      REAL      X(200),YI(200),YD(200),C(256000)
      REAL      F(2,2048,200),B(2,2048,200)
      REAL      EI(200),ED(200),HP,H
      LOGICAL   AGAIN,LMORE
      INTEGER   LRG,RP,GP
      CHARACTER TITLE*60
	character*4 beamstr
	integer beam
C
      write(*,*)'Multiperiod scans'
77	write(*,78)
78	format(' Beamline? ',$)
	read(*,79)beamstr
79	format(A4)
	if(beamstr(1:3).eq.'EMU' .or. beamstr(1:3).eq.'emu') then
	  beam=1
	else if(beamstr(1:4).eq.'MUSR' .or. beamstr(1:4).eq.'musr') then
	  beam=2
	else if(beamstr(1:4).eq.'DEVA' .or. beamstr(1:4).eq.'deva') then
	  beam=3
	else
	  goto 77
	endif
      WRITE(*,*)

C      CALL ASKSIZ(SIZE,IWIDTH)
C     We probably don't need this facility, so fix character size and
C     linewidth
      SIZE = 1.25
      IWIDTH = 1

      WRITE(*,*)
      K=0
   1  WRITE(*,*)
      WRITE(*,100)
 100  FORMAT(' >  First and last run number ?  : ',$)
      READ(*,*,ERR=1) ISTART,IEND
      IF (ISTART.LT.1 .OR. IEND.LT.ISTART) GOTO 1
      NRUNS=IEND-ISTART+1
      IF ((K+NRUNS).GT.200) THEN
        WRITE(*,*)' No more than 200 runs allowed!'
        GOTO 1
      ENDIF
      DO 10 IRUN=ISTART,IEND
        K=K+1
	IF (IRUN.EQ.ISTART) THEN
           CALL GETFIL(IRUN,NT,NH,H,C,DXTIME,NFRAMS,
     +		TITLE,LRG,.TRUE.,beam)
           PRINT *,' '
	   PRINT *,' Number of periods: ', LRG
	   PRINT *,' Total number of histograms: ', NH
	   HP = NH/LRG
	   PRINT *,' Histograms in each period: ', HP

  150	   PRINT *,' Enter Period for ''Red'' data'
	   READ (*,*) RP
	   PRINT *,' Enter Period for ''Green'' data'
	   READ (*,*) GP
           IF (((RP*HP) .GT. NH) .OR. ((GP*HP) .GT. NH)) GOTO 150

	ELSE
           CALL GETFIL(IRUN,NT,NH,H,C,DXTIME,NFRAMS,
     +		TITLE,LRG,.FALSE.,beam)
	ENDIF

        CALL FORBCK(C,NH,NT,F(1,1,K),B(1,1,K),RP,GP,HP)
        X(K)=H
  10  CONTINUE

      WRITE(*,*)
      CALL LOGQYN(' >  Another set of runs ?','N',LMORE)
      IF (LMORE) GOTO 1
      NRUNS=K

      WRITE(*,*)
   3  WRITE(*,120)
 120  FORMAT(' >  First and last time channel ?  : ',$)
      READ(*,*,ERR=3) I1,I2
      IF (I1.LT.1 .OR. I2.GT.NT .OR. I2.LT.I1) GOTO 3
      DO 20 K=1,NRUNS
        CALL INTSYM(F(1,1,K),B(1,1,K),I1,I2,YI(K),EI(K))
        CALL DIFSYM(F(1,1,K),B(1,1,K),I1,I2,YD(K),ED(K))
  20  CONTINUE

      WRITE(TITLE(21:39),130)I1,I2
 130  FORMAT('  Bins: ',I4' - ',I4)
      WRITE(TITLE(40:60),140)ISTART,IEND
 140  FORMAT('  Runs: ',I5' - ',I5)

      WRITE(*,*)
      WRITE(*,*)' Integral Asymmetry'
      CALL PLOT(X,YI,EI,NRUNS,1,SIZE,IWIDTH,TITLE)
      WRITE(*,*)
      WRITE(*,*)' Differential Asymmetry'
      CALL PLOT(X,YD,ED,NRUNS,2,SIZE,IWIDTH,TITLE)
      WRITE(*,*)
      CALL LOGQYN(' >  Try another time window ?','Y',AGAIN)
      WRITE(*,*)
      IF (AGAIN) GOTO 3
      END
C
      SUBROUTINE FORBCK(C,NH,NT,F,B,RP,GP,HP)
C     ------------------------------
C
      INTEGER RP,GP,FB
      REAL HP,C(NH,NT),F(2,*),B(2,*)
C
      FB=HP/2
      DO 30 J=1,NT
        F(1,J)=0.
        B(1,J)=0.
        F(2,J)=0.
        B(2,J)=0.
	do 29 K=1,FB
	  F(1,J)=F(1,J)+C(K+((RP-1)*HP),J)
	  F(2,J)=F(2,J)+C(K+((GP-1)*HP),J)
	  B(1,J)=B(1,J)+C(K+(((RP-1)*HP)+FB),J)
	  B(2,J)=B(2,J)+C(K+(((GP-1)*HP)+FB),J)
  29	continue
  30  CONTINUE
      END
C
      SUBROUTINE INTSYM(F,B,I1,I2,YI,EI)
C     ----------------------------------
C
      REAL F(2,*),B(2,*)
C
      SUMFR=0.0
      SUMBR=0.0
      SUMFG=0.0
      SUMBG=0.0
      DO 10 I=I1,I2
        SUMFR=SUMFR+F(1,I)
        SUMBR=SUMBR+B(1,I)
        SUMFG=SUMFG+F(2,I)
        SUMBG=SUMBG+B(2,I)
  10  CONTINUE
      YIF=(SUMFG-SUMFR)/(SUMFG+SUMFR)
      YIB=(SUMBG-SUMBR)/(SUMBG+SUMBR)
      YI=YIB-YIF
      VARIF=(1.0+YIF*YIF)/(SUMFG+SUMFR)
      VARIB=(1.0+YIB*YIB)/(SUMBG+SUMBR)
      EI=SQRT(VARIF+VARIB)             ! VARIB prev YARIB
      END
C
      SUBROUTINE DIFSYM(F,B,I1,I2,YD,ED)
C     ----------------------------------
C
      REAL F(2,*),B(2,*)
C
      SUM=0.0
      VARD=0.0
      DO 10 I=I1,I2
        FNORM=1.0/(F(2,I)+F(1,I))
        ZF=(F(2,I)-F(1,I))*FNORM
        BNORM=1.0/(B(2,I)+B(1,I))
        ZB=(B(2,I)-B(1,I))*BNORM
        SUM=SUM+ZB-ZF
        VARD=VARD+(1.0+ZF*ZF)*FNORM+(1.0+ZB*ZB)*BNORM
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
      SUBROUTINE PLOT(X,Y,E,N,ISYM,SIZE,IWIDTH,TITLE)
C     -----------------------------------------------
C
      REAL      X(*),Y(*),E(*),YLOW(200),YHIGH(200)
      LOGICAL   LPRINT,LWRITE,LERROR
      CHARACTER FILNAM*60,TITLE*60
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
        CALL PGLABEL('Field  (G)','Integral Asymmetry',TITLE)
      ELSEIF (ISYM.EQ.2) THEN
        CALL PGLABEL('Field  (G)','Average Asymmetry',TITLE)
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

      WRITE (*,*)
      CALL LOGQYN(' Print>  Create a PGPLOT.PS file ?','N',LPRINT)
      IF (LPRINT) THEN
         CALL PGBEGIN(0,'/PS',1,1)
         CALL PGSCH(SIZE)
         CALL PGSLW(IWIDTH)
         CALL PGENV(XMIN,XMAX,YMIN,YMAX,0,0)
         CALL PGPOINT(N,X,Y,4)
         IF (LERROR) THEN
            DO 30 I=1,N
               YLOW(I)=Y(I)-E(I)
               YHIGH(I)=Y(I)+E(I)
  30        CONTINUE
            CALL PGERRY(N,X,YLOW,YHIGH,0.0)
         ENDIF
         IF (ISYM.EQ.1) THEN
            CALL PGLABEL('Field  (G)','Integral Asymmetry',TITLE)
         ELSEIF (ISYM.EQ.2) THEN
            CALL PGLABEL('Field  (G)','Average Asymmetry',TITLE)
         ENDIF
         CALL PGEND
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
C
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
      SUBROUTINE GETFIL(IRUN,NT,NH,H,C,DXTIME,NFRAMS,
     +			TITLE,LRG,PRNT,beam)
C     ---------------------------------------------------------
C
        include 'muon_def.inc'
	integer*4 file
	character*80 mcs_file
	integer*4 rdata(128,2048)
c
        REAL      C(*),H
        CHARACTER TITLE*60
        LOGICAL   PRNT
	integer lrg, beam
C
	file=irun

c
c  ***  manufacture file name and search VAX & HUB ***
c
	if(beam .eq. 1) then
        write(mcs_file,1070)file
	else if(beam .eq. 2) then
        write(mcs_file,1071)file
	else if(beam .eq. 3) then
        write(mcs_file,1072)file
	endif
	goto 205
201     if(beam .eq. 1) then
	write(mcs_file,1060)file
	else if(beam .eq. 2) then
        write(mcs_file,1061)file
	else if(beam .eq. 3) then
        write(mcs_file,1062)file
	endif
	type *,'File not present in FEM, searching restore directory'
	goto 205
202     if(beam .eq. 1) then
	write(mcs_file,1080)file
	else if(beam .eq. 2) then
        write(mcs_file,1081)file
	else if(beam .eq. 3) then
        write(mcs_file,1082)file
	endif
	type *,'File not present in restore directory, searching...'
	goto 205
203	type *,
     + 'File not present. May need to be restored from the archive.'
	type *,' '
	STOP

205     status=NXMread(mcs_file)

        do ih=1,NXM_histogram_number
	   do ic=1,NXM_histogram_length
              rdata(ih,ic) = NXM_histogram_counts(ih,ic)
           enddo
        enddo
	
        NH=NXM_histogram_number
        NT=NXM_histogram_length
        DXTIME=NXM_histogram_Resolution/1000.0
        NFRAMS=NXM_beam_frames
        LRG= NXM_run_switching_states
        K=0
        DO J=1,NT
          DO I=1,NH
            K=K+1
            C(K)=FLOAT(RDATA(I,J))
          ENDDO
        ENDDO

	if (PRNT) THEN
c
c  ***  print title and header of file  ***
c
	   type *,' '
	   type *,' '
	   type *,'Sample                : ', NXM_sample_name
	   type *,'Temperature           : ', NXM_sample_temperature
	endif

	type *,'Field                 : ', NXM_sample_magnetic_field
        H = NXM_sample_magnetic_field

	if (PRNT) THEN
	   type *,'Orientation           : ', NXM_detector_orientation
	   type *,'Start time            : ', NXM_run_start_time
	   type *,'Stop time             : ', NXM_run_stop_time
 	   type *,' '
	   type 1020, NXM_histogram_resolution
	   type 1030, NXM_beam_frames
	   type 1040, NXM_histogram_number
	   type 1050, NXM_histogram_length
	endif

1020	format(' Resolution            : ',1f10.2,' pS')
1030	format(' Total no. of frames   : ',1i8)
1040	format(' Number of histograms  : ',1i4)
1050	format(' Number of time bins   : ',1i5)

c	for EMU:
1060	format('scratch$disk:[emumgr.restore]emu',i8.8,'.nxs') ! 2nd
1070	format('emu$disk0:[data.emu]emu',i8.8,'.nxs') ! 1st
1080	format('inst$disk:[emumgr.data]emu',i8.8,'.nxs') ! 3rd
c	for MUSR:
1061	format('scratch$disk:[mumgr.restore]musr',i8.8,'.nxs') ! 2nd
1071	format('musr$disk0:[data.musr]musr',i8.8,'.nxs') ! 1st
1081	format('inst$disk:[mumgr.data]musr',i8.8,'.nxs') ! 3rd
c	for DEVA:
1062	format('scratch$disk:[mutmgr.restore]mut',i8.8,'.nxs') ! 2nd
1072	format('mut$disk0:[data.mut]mut',i8.8,'.nxs') ! 1st
1082	format('inst$disk:[mutmgr.data]mut',i8.8,'.nxs') ! 3rd
	end
C
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

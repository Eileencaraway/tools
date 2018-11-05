void WaveVector_isf(int &Qmodu){
int Qsq,a;
	for(int i=0;i<QIMax_isf;i++){
	    QvectorX1[i] = 0;
		QvectorY1[i] = 0;
	}
	Qcount1 = 0;
	for(int KX=0;KX<(Qmodu+1);KX++){
		for(int KY=-Qmodu;KY<(Qmodu+1);KY++){
			Qsq=KX*KX + KY*KY;
			if(Qsq==Qmodu){
			  if(Qcount1<QIMax_isf){
			       QvectorX1[Qcount1] = KX;
					QvectorY1[Qcount1] = KY;
					Qcount1++;
			  }else{
			    goto sss;
			  }
			}		
		}	
	}
sss:cout << "wave-vector for ISF :   " << 2.0*PI/L[1]*sqrt(double(Qmodu)) << "  number:  "<<Qcount1<<endl;
}
void Dynamics(int &s_witch){
	const double Poverlap=0.09;
	int ttel, ddt,Qmodu,KX,KY;
	double tm,dx,dy,rxii,ryii,r2a,dr2;
	double Qreal,vol,fact,vtime,Kai4,rub;
	if(s_witch==1){
		Itvacf++;
		if((Itvacf%it0)==0){
			//new t=0
			t0++;
			ttel = ((t0 - 1)%T0Max) + 1;
			ttv0[ttel] = Itvacf;
			for(int i=0; i<N; i++){
				rx0[i][ttel] = Particles[i].R_R[0][ind];
				ry0[i][ttel] = Particles[i].R_R[1][ind];			
			}		
		}
	tm = min (t0, T0Max);
	for(int t=1;t<(tm+1);t++){
		ddt = Itvacf - ttv0[t] + 1;
		if(ddt<Dyn_TMAx){
			nisf[ddt]++;
//====compute Q(t): self part
			Qself0[ddt] = 0.0;
			for(int i=0; i<N;i++){
				dx = Particles[i].R_R[0][ind] - rx0[i][t];
				dy = Particles[i].R_R[1][ind] - ry0[i][t];
				rxii = dx;
				ryii = dy;
				rxii -=  L[0]*round(rxii/L[0]);
			    ryii -=  L[1]*round(ryii/L[1]);
				r2a = rxii*rxii + ryii*ryii;
				//======MSD
				dr2 = dx*dx + dy*dy;
				r2t[ddt] += dr2 ;                     
				r4t[ddt]  +=  dr2*dr2;
				//======Q(t)
				if(r2a<Poverlap){
				   Qself[ddt]++;
				   Qself0[ddt]++;
				}
				//=========compute Fs(t): self-intermediate scattering function
				if(Qcount1>0){
					for(int Qs=0; Qs<Qcount1;Qs++){
					  KX = QvectorX1[Qs];
					  KY = QvectorY1[Qs];
					  ISF[ddt] += cos(2*PI/L[1]*(KX*dx+KY*dy));
					}			
				}			
			}
			Kai4_1self[ddt] += Qself0[ddt]*Qself0[ddt];		
		}
	}	
	}else{
		if(s_witch==0){
			t0=0;
			Itvacf=0;
			dtime = dt*Dyna_nsamp;
				for(int i =0;i<Dyn_TMAx;i++){
					r2t[i] = 0;
					r4t[i] = 0;
					nisf[i] = 0;
					alfa2[i] = 0.0;
            		ISF[i] = 0.0;
		            Qself[i] = 0.0;
		            Kai4_1self[i] = 0.0;			
				}
				Qreal = Dyn_q;
//       ====Set up wave vectors
		Qmodu = powl(round(Qreal*L[1]/2/PI),2);
		WaveVector_isf(Qmodu);	
		}
		else{
			 ofstream outputMSD,outputISF,outputalfa,outputDH;
             outputMSD.open("MSD.dat");
			 outputISF.open("ISF.dat");
			 outputalfa.open("alfa.dat");
			 outputDH.open("DH.dat");
			 vol = L[0]*L[1];
			 fact=vol/(N*N);
			 for(int i=1;i<(Dyn_TMAx+1);i++){
				 vtime = dtime*(i-1);
					 if(nisf[i]>10){
						 //=====output MSD
						 r2t[i] /= double(N*nisf[i]);
						 outputMSD<<vtime<<"    "<<r2t[i]<<endl;
						 //=====output alfa2
						 r4t[i] /= double(N*nisf[i]);
					    alfa2[i] = (3*r4t[i])/(5*r2t[i]*r2t[i])	- 1;	
						outputalfa<<vtime<<"    "<<alfa2[i]<<endl;
						 //=====output isf
						 ISF[i]/=(N*nisf[i]*Qcount1);
						 outputISF<<vtime<<"    "<<ISF[i]<<endl;
						 //=====output X4
			            rub = (Qself[i]/double(nisf[i]))*(Qself[i]/double(nisf[i]));
			            Kai4 = fact*(Kai4_1self[i]/double(nisf[i])-rub);
						outputDH<<vtime<<"    "<<Qself[i]/double(N*nisf[i])<<"   "<<Kai4<<endl;				 
					 }			 
			 }
			 outputMSD.close();
			 outputISF.close();
             outputalfa.close();
			 outputDH.close();	
		}	
	  }	
}
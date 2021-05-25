
TITLE transmitter release


INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX glurelDouble
	RANGE dur, cmax, T, Twait, Tinterval, Trise,dur1,dur2
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	(mM) = (milli/liter)
}

PARAMETER {
	dur1= 2000 (ms)
	dur2= 2000 (ms)
	
	Trise=0.15 (ms)
	cmax = 1 (mM)
	Twait = 10 (ms)
	Tinterval = 30 (ms)
}

ASSIGNED {
	T (mM)
}


INITIAL {
	T = 0
}

BREAKPOINT {
        if(t < Twait) {
                T = 0
        }
	    if ((t>=Twait) && (t<=Twait+Trise)){
		T=(cmax/0.15)*(t-Twait)
		}
        if ( (t >= Twait + Trise)&&(t <= (Twait + Trise + dur1))) {
		T = cmax
        }
		if ((t>=Twait + Trise + dur1) && (t<=Twait + dur1 + (2*Trise))){
		T=-((cmax/0.15)*(t-(Twait + Trise + dur1)))+cmax
		}
        
	  if (t > (Twait + dur1+ (2*Trise)) && t<(Twait+dur1+Tinterval+ (2*Trise))) {
		T = 0
	  }
	    if ( (t >= (Twait+dur1+Tinterval+ (2*Trise)))&&(t < (Twait+dur1+Tinterval+ (3*Trise)))) {
		T=(cmax/0.15)*(t-(Twait+dur1+Tinterval+ (2*Trise)))
		}
		if ( (t >= (Twait+dur1+Tinterval+ (3*Trise)))&&(t < (Twait+dur1+dur2+Tinterval+ (3*Trise)))) {
		T = cmax
		}
		if ( (t >= (Twait+dur1+dur2+Tinterval+ (3*Trise))&&(t < (Twait+dur1+dur2+Tinterval+ (4*Trise))))) {
		T=-(cmax/0.15)*(t-(Twait+dur1+dur2+Tinterval+ (3*Trise)))+cmax
		}
		
      if(t>=(Twait+dur1+dur2+Tinterval+ (4*Trise))){
	  T=0
	  }

}


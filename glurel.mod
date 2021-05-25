
TITLE transmitter release


INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX glurel
	RANGE dur, cmax, T, Twait, Tinterval, Trise
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	(mM) = (milli/liter)
}

PARAMETER {
	dur = 2000 (ms)
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
        if ( (t >= Twait + Trise)&&(t <= (Twait + Trise + dur))) {
		T = cmax
        }
		if ((t>=Twait + Trise + dur) && (t<=Twait + dur + (2*Trise))){
		T=-((cmax/0.15)*(t-(Twait + Trise + dur)))+cmax
		}
        
	  if (t > (Twait + dur+ (2*Trise)) && t<(Twait+dur+Tinterval+ (2*Trise))) {
		T = 0
	  }
	    if ( (t >= (Twait+dur+Tinterval+ (2*Trise)))&&(t < (Twait+dur+Tinterval+ (3*Trise)))) {
		T=(cmax/0.15)*(t-(Twait+dur+Tinterval+ (2*Trise)))
		}
		if ( (t >= (Twait+dur+Tinterval+ (3*Trise)))&&(t < (Twait+(2*dur)+Tinterval+ (3*Trise)))) {
		T = cmax
		}
		if ( (t >= (Twait+(2*dur)+Tinterval+ (3*Trise))&&(t < (Twait+(2*dur)+Tinterval+ (4*Trise))))) {
		T=-(cmax/0.15)*(t-(Twait+(2*dur)+Tinterval+ (3*Trise)))+cmax
		}
		
      if(t>=(Twait+(2*dur)+Tinterval+ (4*Trise))){
	  T=0
	  }

}


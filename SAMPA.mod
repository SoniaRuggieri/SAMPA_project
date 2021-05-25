TITLE Iamgonnadie
INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}
NEURON {
	POINT_PROCESS SAMPA
		POINTER glu
	NONSPECIFIC_CURRENT iampa
	RANGE Erev, RelProb 
	RANGE gampa, gbarampa
	RANGE k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, beta				:forwards
	RANGE kn1, kn2, kn3, kn4, kn5, kn6, kn7, kn8, kn9, kn10, alpha		:backwards
		}
UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(umho) = (micromho)
	(mM) = (milli/liter)
	(pS) = (picosiemens)
}


PARAMETER {	
	gbarampa	= 1200   (pS)
	Erev	= 0	(mV)
    RelProb=0.46	
	:kb    =0.28 (mM)  
	
	k1	= 13.66	(/mM /ms) 				
	k2	= 6.019	(/mM /ms)				
	k3	= 13.66	(/mM /ms)					
	k4	= 1.0	(/ms)			
    k5	= 1.8	(/ms)
	k6	= 0.0124 (/ms)
	k7	= 0.5	(/ms)
	k8	= 0.04	(/ms)
	k9	= 10.34	(/ms)
	k10	= 0.233	(/ms)
	alpha	= 3.734	(/ms)
	
	kn1	= 2.093	(/ms)		
	kn2	= 4.719	(/ms)	
	kn3	= 0.44623	(/ms)		
	kn4	= 0.06	(/ms)
    kn5 = 0.0045	(/ms)
	kn6 = 0.0015	(/ms)
	kn7 = 0.591	(/ms)
	kn8 = 0.421	(/ms)
	kn9 = 0.140	(/ms)
	kn10 = 0.0003242	(/ms)
	beta = 17.23	(/ms)
}


ASSIGNED {
	v		(mV) : postsynaptic voltage
	iampa 		(nA) : current = g*(v - Erev)
	gampa 		(pS) :	conductance
	glu 		(mM) :	pointer to glutamate concentration

	:rb		(/ms): binding
}


STATE {
	: Channel states (all fractions)
	CO		: unbound
	CA1		: single glu bound
	CA2		: double glu bound
 	O		: open state 2
	DA1		: single glu bound, desensitized
 	DA2a	: double glu bound, desensitized
	DA2b
	DA2c
	DA2d
}

INITIAL {
	CO=1
	CA1=0
	CA2=0
	DA1=0
	DA2a=0
	DA2b=0
	DA2c=0
	DA2d=0
	O=0
}
BREAKPOINT {
	SOLVE kstate METHOD sparse: derivimplicit
	gampa=gbarampa*O*RelProb
	iampa=(1e-6)*gampa*(v-Erev)
	}

KINETIC kstate{

	~CO		<->	CA1 (k1*glu,kn1)
	~CA1	<->	DA1 (k4,kn4)
	~CA1	<->	CA2	(k2*glu,kn2)
	~DA2a	<->	DA1	(kn3,k3*glu)
	~DA2a	<->	CA2	(kn5,k5)
	~DA2a	<->	DA2b(k8,kn8)
	~O		<->	CA2	(alpha,beta)
	~O		<->	DA2b(k6,kn6)
	~O		<->	DA2d(k7,kn7)
	~DA2c	<->	DA2d(kn10,k10)
	~DA2c	<->	DA2b(kn9,k9)
	
	CONSERVE CO+CA1+CA2+DA1+DA2a+DA2b+DA2c+O+DA2d=1
	:-(CA1+CA2+DA1+DA2a+DA2b+DA2c+O+DA2d)
	:CO=(1-(CA1+CA2+DA1+DA2a+DA2b+DA2c+O+DA2d))
	
}

COMMENT
----------------------------------------------------------------------------------

DERIVATIVE state {

	:CO'		= -(CO*k1*glu)+(CA1*k1)
	CA1'	= -(CA1*(kn1+k4+(k2*glu)))+((1-(CA1+CA2+DA1+DA2a+DA2b+DA2c+O+DA2d))*k1*glu)+(DA1*kn4)+(CA2*kn2)
	CA2'	= -(CA2*(kn2+k5+beta))+(CA1*k2*glu)+(DA2a*kn5)+(O*alpha)
	O'		= -(O*(alpha+k6+k7))+(CA2*beta)+(DA2b*kn6)+(DA2d*kn7)
	DA1'	= -(DA1*(kn4+(k3*glu)))+(DA2a*kn3)+(CA1*k4)
	DA2a'	= -(DA2a*(kn3+k8+kn5))+(DA1*k3*glu)+(DA2b*kn8)+(CA2*k5)
	DA2b'	= -(DA2b*(kn8+k9+kn6))+(DA2a*k8)+(O*k6)+(DA2c*kn9)
	DA2c'	= -(DA2c*(kn9+kn10))+(DA2b*k9)+(DA2d*k10)
	DA2d'	= -(DA2d*(kn7+k10))+(DA2c*kn10)+(O*k7)
	
}
----------------------------------------------
ENDCOMMENT
	

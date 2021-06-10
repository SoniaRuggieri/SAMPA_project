########## it works with SAMPAtemp1head08mar_ko_exp.hoc
######### SAMPAmorph08mar_exp.hoc

#rxd trial
from neuron import h,gui,rxd
from neuron.rxd import v
from neuron.rxd import rxdmath
#from matplotlib import pyplot
from matplotlib import pyplot, animation
from nrnutils import Mechanism, Section
from IPython.display import HTML
import matplotlib.gridspec as gridspec
import random
import numpy as np
from math import inf
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

h.load_file('stdrun.hoc')
import time

## dist 1.43, part 0.25, part2 5 and idea() works nicely. 

h.load_file("SAMPAtemp1head08mar_ko_exp.hoc")
rxd.nthread(4)
rxd.options.enable.extracellular=True
dist=1.76   #1.43 700um  #2 for 500nm distance, 2.19 for 465nm (kullman 1998),   1.76 569nm
part=0.25 #0.25
part2=5  #5
nt=10000
kh=10
print(h.nspinepre-1)

h.somaWT1[0].connect(h.somaWT(0),0)
h.somaWT1[1].connect(h.somaWT(0.5),0)
h.somaWT1[2].connect(h.somaWT(1),0)
h.somaWTbig.connect(h.somaWT(1),0)


h.PREwt1[0].connect(h.PREwt(0),0)
h.PREwt1[1].connect(h.PREwt(0.5),0)
h.PREwt1[2].connect(h.PREwt(1),0)


for i in range(3):
    for j in range(3):
        #print(int(2))
        h.headpre[(i*3)+j].connect(h.PREwt1[i]((j+1)/4),0)    #j/2
        h.head[(i*3)+j].connect(h.somaWT1[i]((j+1)/4),0)
        h.cWT[(i*3)+j].gbarampa=100#350  
        #170 ko no firing #200 spike ko 
        #200 wt no firing #
        #print(i)
        #print(j)
        #print((i*3)+j)

h.topology()

 
def exclude(x, y, z, diam, value_outside=inf, value_inside=1):
    """ Function returns value_outside if the (x,y,z) point is outside the
        diameter otherwise value_inside (defaults to inf)
    """
    
    if z>=h.lpre/2 and z<=(h.lpre/2)+0.02: #and x>=0 and x<=h.syndist*4:# :y>=-0.05 and y<=h.somadist*3
             return value_inside
    return value_outside
 


ecswt = rxd.Extracellular(-0.5, -0.5, -0.5, (h.syndist*4)+0.5, (h.somadist*3), h.lpre+0.02+h.lhead, dx=(0.05,0.05,0.005), volume_fraction=1, tortuosity=lambda x,y,z: exclude(x, y, z, 1))##tortuosity=1.05) #1.34
#print(tortuosity)
print(h.somadist*3)
print(ecswt)
#ecswt = rxd.Extracellular(-1, 4, 0, 21, 6, 2, dx=(0.1), volume_fraction=0.3, tortuosity=1.05) #1.34

#tortuosity 1.34 from kullman paper
#volume fraction 0.112 from kullman paper
xwt = rxd.Species(ecswt,d=1.14,name="xwt",charge=1,initial=0,ecs_boundary_conditions=0)#, initial=lambda nd: 1 if hasattr(nd, 'sec') and nd.segment in h.PREwt else 0)
#xwt = rxd.Species(ecswt,d=lambda x,y,z: exclude(x, y, z, 1.14),name="xwt",charge=1,initial=0,ecs_boundary_conditions=0)
Xwtecs=xwt[ecswt]

for i in range(3):
    for j in range(3):
        #h.head[(i*3)+j].connect(h.somaWT1[i]((j/2)),0)
        h.setpointer(xwt[ecswt].node_by_location((((i+1)/4)*h.syndist*4),j*h.somadist, ((h.lpre/2)+0.02))._ref_concentration,'glu',h.cWT[(i*3)+j])
        print(((i+1)/4)*h.syndist*4)
        print((i*3)+j)
     
    #h.setpointer(xwt[ecswt].node_by_location((i*h.somalength/(h.nspine*dist))+part2,5, (h.lpre/2)+0.02)._ref_concentration,'glu',h.cWT[i])

print(h.lpre) 
#h.setpointer(xwt[ecswt].node_by_location(((5*10/(h.nspine))),5.02, 0.02)._ref_concentration,'glu',h.cWT[5])

e = 1.60217662e-19
scale = 1e-14 / e
R = 1e3
U = 1e5

#wtexp = rxd.MultiCompartmentReaction(Xwtecs, Xwtcyt,  Xwtecs * scale, membrane=memwt,custom_dynamics=True)


####

t_vec = h.Vector()
t_vec.record(h._ref_t)
PREwt_X = h.Vector()
PREwt_X.record(h.headpre[0](0.5)._ref_T_rel)
PREwt_Xorg = h.Vector()
PREwt_Xorg.record(h.headpre[1](0.5)._ref_T_rel)

somaWT_X = h.Vector()
somaWT_X.record(h.somaWTbig(0)._ref_v)
somaWT_X1 = h.Vector()
somaWT_X1.record(h.head[1](0.5)._ref_v)
somaWT_Xorg = h.Vector()
somaWT_Xorg=h.Vector().record(Xwtecs.node_by_location(((0+1)/4)*h.syndist*4,0*h.somadist, (h.lpre/2)+0.02)._ref_concentration)
somaWT_Xorg2 = h.Vector()
somaWT_Xorg2=h.Vector().record(Xwtecs.node_by_location(((1+1)/4)*h.syndist*4,0*h.somadist, (h.lpre/2)+0.02)._ref_concentration)

#(-1, 2, 2, 11, 8, 5,
'''
xwtecs_vec0 = h.Vector()
xwtecs_vec0.record(Xwtecs.node_by_location(((1*h.somalength/(h.nspine*dist))+part2), 5, 0.5)._ref_value) # same as x[ecs].node_by_ijx(h.somalength,15,7)

# record the same node by it's index into stated3d
xwtecs_vec1 = h.Vector()
xwtecs_vec1.record(xwt[ecswt].node_by_location(((2*h.somalength/(h.nspine*dist))+part2), 5, 0.7)._ref_value) # same as x[ecs].node_by_location(50,0,0)

xwtecs_vec2 = h.Vector()
xwtecs_vec3 = h.Vector()
xwtecs_vec2.record(Xwtecs.node_by_location(((3*h.somalength/(h.nspine*dist))+part2),5, 1.00)._ref_value) # same as x[ecs].node_by_location(50,0,0)
xwtecs_vec3.record(Xwtecs.node_by_location(((4*h.somalength/(h.nspine*dist))+part2),5,1.02)._ref_value) # same as x[ecs].node_by_location(50,0,0)
'''
head1open_vec2 = h.Vector()
head2open_vec3 = h.Vector()
head1open_vec2.record(h.cWT[0]._ref_O) # same as x[ecs].node_by_location(50,0,0)
head2open_vec3.record(h.cWT[1]._ref_O) # same as x[ecs].node_by_location(50,0,0)
head3open = h.Vector()
head4open = h.Vector()
head3open.record(h.cWT[2]._ref_O) # same as x[ecs].node_by_location(50,0,0)
head4open.record(h.cWT[3]._ref_O) # same as x[ecs].node_by_location(50,0,0)
head5open = h.Vector()
head6open = h.Vector()
head5open.record(h.cWT[4]._ref_O) # same as x[ecs].node_by_location(50,0,0)
head6open.record(h.cWT[5]._ref_O) # same as x[ecs].node_by_location(50,0,0)
head7open = h.Vector()
head8open = h.Vector()
head7open.record(h.cWT[6]._ref_O) # same as x[ecs].node_by_location(50,0,0)
head8open.record(h.cWT[7]._ref_O) # same as x[ecs].node_by_location(50,0,0)
head9open = h.Vector()
head10open = h.Vector()
head9open.record(h.cWT[8]._ref_O) # same as x[ecs].node_by_location(50,0,0)
#head10open.record(h.cWT[9]._ref_O) # same as x[ecs].node_by_location(50,0,0)

headmean=(head1open_vec2+head2open_vec3+head3open+head4open+head5open+head6open+head7open+head8open+head9open)#+head10open)

ileak=h.Vector()
ileak.record(h.somaWT(0.5)._ref_i_pas)
ica=h.Vector()
ica.record(h.somaWT(0.5)._ref_i_cap)
ik=h.Vector()
ik.record(h.somaWT(0.5)._ref_ik)
ina=h.Vector()
ina.record(h.somaWT(0.5)._ref_ina)




#print(random.sample([1,2,3,4],3))
#pyplot.show()
print(list(range(0,int(h.nspinepre))))

def hi():
    global vv
    print(h.t)
    #vv=[0]
    vv=random.sample(list(range(0,int(h.nspinepre))),int(int(h.nspinepre)*0.3))   ##70% release probability @1st stimulus
    print(vv)
    for i in range(0,len(vv)):
        print(h.headpre[vv[i]](0.5).VA_rel)
        h.headpre[vv[i]](0.5).nt_rel=0
        h.headpre[vv[i]](0.5).kh_rel=0
        #print(h.headpre[vv[i]](0.5).nt_rel)
    
    #-(h.trainsWT.interval/2)
    return vv

def hi2():
    print(h.t)
    for i in range(0,len(vv)):
        #print(h.headpre[vv[i]](0.5).nt_rel)
        h.headpre[vv[i]](0.5).nt_rel=nt
        h.headpre[vv[i]](0.5).kh_rel=kh
    
def hi3():
    global vv1
    print(h.t)
    #vv=[0]
    vv1=random.sample(list(range(0,int(h.nspinepre))),int(int(h.nspinepre)*0.6))   ##70%*60% release probability @2nd stimulus
    print(vv1)
    for i in range(0,len(vv1)):
        #print(h.headpre[vv1[i]](0.5).nt_rel)
        h.headpre[vv1[i]](0.5).nt_rel=0
        h.headpre[vv1[i]](0.5).kh_rel=0
        
        #print(h.headpre[vv1[i]](0.5).nt_rel)
    
    #-(h.trainsWT.interval/2)
    return vv1

def hi4():
    print(h.t)
    for i in range(0,len(vv1)):
        #print(h.headpre[vv1[i]](0.5).nt_rel)
        h.headpre[vv1[i]](0.5).nt_rel=nt
        h.headpre[vv1[i]](0.5).kh_rel=kh
   

def init():
    h.t=0
    h.trainsWT.number=10
    h.trainsWT.interval=20
    h.trainsWT.start=50
    h.trainsWT.noise=0
    # run and plot the results
    h.finitialize(-70)   
    h.cvode.event(h.t+h.trainsWT.start-(h.trainsWT.interval/3),hi)
    h.cvode.event(h.t+h.trainsWT.start+(h.trainsWT.interval/3),hi2)
    
    
    #fih = h.FInitializeHandler(200, hi)
    for i in range(1,int(h.trainsWT.number)):
        h.cvode.event(h.t+h.trainsWT.start+(h.trainsWT.interval*i)-(h.trainsWT.interval/3),hi3)
        h.cvode.event(h.t+h.trainsWT.start+(h.trainsWT.interval*i)+(h.trainsWT.interval/3),hi4)

test= np.array([1,3,5,7])
def idea():
    h.trainsWT.number=10
    h.trainsWT.interval=20
    h.trainsWT.start=0
    for i in test:
        h.headpre[i](0.5).nt_rel=0
        h.headpre[i](0.5).kh_rel=0
        h.cWT[i].gbarampa=180
'''
    h.headpre[1](0.5).nt_rel=0
    h.headpre[1](0.5).kh_rel=0
    h.headpre[3](0.5).nt_rel=0
    h.headpre[3](0.5).kh_rel=0
    h.headpre[5](0.5).nt_rel=0
    h.headpre[5](0.5).kh_rel=0
    h.headpre[7](0.5).nt_rel=0
    h.headpre[7](0.5).kh_rel=0
    h.headpre[9](0.5).nt_rel=0
    h.headpre[9](0.5).kh_rel=0
    h.cWT[1].gbarampa=45
    h.cWT[3].gbarampa=45
    h.cWT[5].gbarampa=45
    h.cWT[7].gbarampa=45
    h.cWT[9].gbarampa=45
'''

init()
h.continuerun(300)


#h.finitialize(-70)
#idea()
#print(h.trainsWT.start)
#h.continuerun(150)


fig = pyplot.figure()

pyplot.subplot2grid((4, 3),(0,0))
pyplot.plot(t_vec,PREwt_X, label='T_Rel_headpre[0]')
pyplot.legend()
pyplot.xlabel('t (ms)')
pyplot.ylabel('mM')
#pyplot.ylim(0,2)

pyplot.subplot2grid((4, 3),(0,1))
pyplot.plot(t_vec,somaWT_Xorg, label='[Glu] @ headpost[0]')
pyplot.legend()
pyplot.xlabel('t (ms)')
pyplot.ylabel('mM')
#pyplot.yticks(np.arange(0,1,0.2))
#pyplot.yticks(np.arange(min(min(somaWT_Xorg),min(somaWT_Xorg2)), max(max(somaWT_Xorg),max(somaWT_Xorg2))+0.2, 0.2))
#pyplot.ylim(0,1)


pyplot.subplot2grid((4, 3),(0,2))
pyplot.plot(t_vec, head1open_vec2, label='Po headpost[0]')
pyplot.legend()
pyplot.xlabel('t (ms)')
#pyplot.yticks(np.arange(0,1,0.2))
pyplot.ylim(0,1)

pyplot.subplot2grid((4, 3),(1,0))
pyplot.plot(t_vec,PREwt_Xorg, label='T_rel_head[1]')
pyplot.legend()
pyplot.xlabel('t (ms)')
pyplot.ylabel('mM')
#pyplot.ylim(0,2)

pyplot.subplot2grid((4, 3),(1,1))
pyplot.plot(t_vec,somaWT_Xorg2, label='[Glu] @ headpost[1]')
pyplot.legend()
pyplot.xlabel('t (ms)')
pyplot.ylabel('mM')
#pyplot.yticks(np.arange(0,1,0.2))
#pyplot.yticks(np.arange(0,0.7,0.1))
#pyplot.ylim(0,1)

pyplot.subplot2grid((4, 3),(1,2))
pyplot.plot(t_vec, head2open_vec3, label='Po head[1]')
pyplot.legend()
#pyplot.yticks(np.arange(0,1,0.2))
#pyplot.yticks(np.arange(0,0.7,0.1))
pyplot.xlabel('t (ms)')
#pyplot.ylim(0,0.6)

pyplot.subplot2grid((4, 3),(2,0))#,colspan=3,rowspan=2)
pyplot.plot(t_vec,somaWT_X, label='ref_v_somaWT')
pyplot.legend()
pyplot.xlabel('t (ms)')
pyplot.ylabel('mV')
#pyplot.ylim(-70,-60)

pyplot.subplot2grid((4, 3),(2,1))
pyplot.imshow(xwt[ecswt].states3d.mean(2).T, extent=xwt[ecswt].extent('xy'), origin="lower",aspect='auto')
#pyplot.imshow(xwt[ecswt].states3d[:,:,100].T,extent=xwt[ecswt].extent('xy'),origin="lower",aspect='auto')

pyplot.colorbar()

pyplot.subplot2grid((4, 3),(2,2))
pyplot.plot(t_vec,(1/10)*(head1open_vec2+head2open_vec3+head3open+head4open+head5open+head6open+head7open+head8open+head9open))#+head10open))
#pyplot.yticks(np.arange(0,0.7,0.1))
pyplot.xlabel('t (ms)')
#pyplot.ylim(0,0.4)

pyplot.subplot2grid((4, 3),(3,1))
#pyplot.imshow(xwt[ecswt].states3d.mean(2).T, extent=xwt[ecswt].extent('xy'), origin="lower",aspect='auto')
#pyplot.imshow(xwt[ecswt].states3d[:,284,:].T,extent=xwt[ecswt].extent('xz'),origin="lower",aspect='auto')

#pyplot.colorbar()

#pyplot.subplot(4, 3, 8)
#pyplot.imshow(xko[ecsko].states3d.mean(2).T, extent=xko[ecsko].extent('xy'), origin="lower", aspect='equal')
#pyplot.legend()

fig.tight_layout()
pyplot.show()

##con 500 ms di simulazione e 5 stimuli, funge

h.dt=0.1

#init()

def runsim(species,ecs,  frames=3000): #min_conc, max_conc,
    fig = pyplot.figure()
    im = pyplot.imshow(species[ecs].states3d.mean(2).T, extent=species[ecs].extent('xy'), origin="lower",aspect='auto')#, vmin=0,vmax=0.6)#, vmin=min_conc, vmax=max_conc)
    #im = pyplot.imshow(species[ecs].states3d[:,:,1].T, origin="lower",aspect='auto')#, vmin=0,vmax=0.6)#, vmin=min_conc, vmax=max_conc)
    pyplot.axis('off')

    def init():
        im.set_data(species[ecs].states3d.mean(2).T)
        return [im]
    def animate(i):
        h.fadvance()
        im.set_data(species[ecs].states3d.mean(2).T)
        return [im]

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=30)
    ret =  HTML(anim.to_html5_video())
    pyplot.close()
    return ret

#runsim(xwt,ecswt)
#h.init()
#pyplot.imshow(xwt[ecswt].states3d.mean(2).T, extent=xwt[ecswt].extent('xy'), origin="lower",aspect='auto')
#h.run()
#pyplot.imshow(xwt[ecswt].states3d.mean(2).T, extent=xwt[ecswt].extent('xy'), origin="lower",aspect='auto')

#h.finitialize(-70)



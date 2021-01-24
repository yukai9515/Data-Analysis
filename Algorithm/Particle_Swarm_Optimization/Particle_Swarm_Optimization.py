# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 21:34:17 2021

@author: Kai
"""

import numpy as np
import math
import matplotlib.pyplot as plt 
import random

def fitness (x,y):
    fit = math.exp(-0.2*(pow(x,4)+pow(y,4)) ) +math.exp(math.cos(2*math.pi*x)+math.cos(2*math.pi*y))
    return fit

'--------------------parameter setting-------------------'
n_p =40                             #number of particle
n_d=2                                 #number of dimension [x,y]
c1=2                                  #self confidence factor
c2=2                                  #swarm confidence factor
w=0.8                                 #weight=0.8
v_max=0.3*3                           #vmax=k*X_max  k=0.3  X_max=3
b_r=0.8                               #boundary rate :limit X,Y
crazy_r=0.2                           #crazy rate : Maintain Diversity
n_iteration=200                       #number of iteration
particle= np.zeros((n_p,n_d))
velocity=np.zeros((n_p,n_d))
obj= np.zeros(n_p)
pbest=np.zeros((n_p,n_d+1))
gbest=np.zeros((1,n_d+1))
history=[]
maxg=0

'--------------------main-------------------'
'initialization'
for p in range(0,n_p):
    velocity[p,0]=round(random.uniform(-0.5,0.5),3)
    velocity[p,1]=round(random.uniform(-0.5,0.5),3)
    particle[p,0]=round(random.uniform(-1,2),3)       #-1<x<2  Constraint Handling
    particle[p,1]=round(random.uniform(-2,1),3)       #-2<y<1  Constraint Handling
    while particle[p,0]+particle[p,1] > 1:
        particle[p,0]=round(random.uniform(-1,2),3)   #   x+y<=1  Constraint Handling
        particle[p,1]=round(random.uniform(-2,1),3)
n_time=0
while n_time < n_iteration:
   for p in range (0,n_p):
       obj[p]=fitness(particle[p,0],particle[p,1])
       if pbest[p,2] < obj[p]:                        #updated pbest
            pbest[p,0] = particle[p,0]
            pbest[p,1] = particle[p,1]
            pbest[p,2] = obj[p] 
       if obj[p] > gbest[0,2]:                        #updated gbest
            gbest[0,0]=particle[p,0]
            gbest[0,1]=particle[p,1]
            gbest[0,2]=obj[p]
   r1=random.uniform(0,1)
   r2=random.uniform(0,1)
   for p in range(0,n_p):
       rand=random.uniform(0,1)
       if rand < crazy_r:                                   #Maintain Diversity:Craziness 
            velocity[p]=round(v_max*random.uniform(0,1),3)  #small than 0.2, go crazy(change velocity)
       else:
            velocity[p]=w*velocity[p]+r1*c1*(pbest[p,:2]-particle[p])+r2*c2*(gbest[len(gbest)-1,:2]-particle[p])
   for p in range(0,n_p):
        if abs(velocity[p,0])>v_max:                            #velocity limit:Damping limit for velocity
            velocity[p,0]=velocity[p,0]/abs(velocity[p,0])*v_max
        if abs(velocity[p,1])>v_max:                            #velocity limit:Damping limit for velocity
            velocity[p,1]=velocity[p,1]/abs(velocity[p,1])*v_max
        if particle[p,0]+particle[p,1]+velocity[p,0]+velocity[p,1]<=1 :  #x+y<=1  Constraint Handling
            particle[p]=particle[p]+velocity[p]                         #if violate then ,Velocity=0          
        if particle[p,0] > 2:                      #Constraint Handling:Bouncing strategy rate=0.8
            particle[p,0]=2-(particle[p,0]-2)*b_r  #Boundary=2       -1<x<2
        if particle[p,0] < -1:                     #Boundary=-1
            particle[p,0]=-1-(particle[p,0]+1)*b_r
        if particle[p,1] > 1:                      #Constraint Handling:Bouncing strategy rate=0.8
            particle[p,1]=1-(particle[p,1]-1)*b_r  #Boundary=1       -2<y<1
        if particle[p,1] < -2:                     #Boundary=-2
            particle[p,1]=-2-(particle[p,1]+2)*b_r
        particle[p,0]=round(particle[p,0],3) 
        particle[p,1]=round(particle[p,1],3)
   w= 0.8-(n_time/n_iteration)*0.8                     #Inertia weight upper bound=0.8 lower bound=0
   history.append(gbest[0,2])
   n_time=n_time+1
'display'
plt.plot(history)
print('x',gbest[0,0],'y',gbest[0,1],'fitness',gbest[0,2])
       



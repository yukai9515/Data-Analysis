# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 14:02:14 2021

@author: Kai
"""

import numpy as np
import math
import matplotlib.pyplot as plt 
import random

def fitness (e_x,e_y):
    fit = math.exp(-0.2*(pow(e_x,4)+pow(e_y,4))) +math.exp(math.cos(2*math.pi*e_x)+math.cos(2*math.pi*e_y))
    return fit

def select (cul_prob):
    rate_c=random.random()
    e=0
    for c in range(0,n_c):
        if rate_c < cul_prob[c]:
            break
        e=e+1  
    return e
    
def tr(chromosom):
    x=0
    y=0
    for i in range(0,round(n_d/2)):
        if chromosom[i] == 1:
            x=pow(2,round(n_d/2)-i-1)+x
    for i in range(0,round(n_d/2)):
        if chromosom[i+round(n_d/2)] == 1:
            y=pow(2,round(n_d/2)-i-1)+y
    return x,y

def evaluation(temp_chromosom):
    matrix_xy=np.zeros((1,2))
    x,y=tr(temp_chromosom)
    matrix_xy[0,0]=round((-1+x*3/(pow(2,round(n_d/2))-1)),nu)
    matrix_xy[0,1]=round((-2+y*3/(pow(2,round(n_d/2))-1)),nu)
    obj[c]=fitness(xy[c,0],xy[c,1])
    return matrix_xy

def penalty(matrix_xy,obj_penalty):
    matrix_xy=np.zeros((1,2))
    if matrix_xy[0,0]+matrix_xy[0,1]>1.75:
        obj_penalty=obj_penalty-(matrix_xy[0,0]+matrix_xy[0,1]-1)*2
    elif matrix_xy[0,0]+matrix_xy[0,1]>1.5:
        obj_penalty=obj_penalty-(matrix_xy[0,0]+matrix_xy[0,1]-1)*1
    elif matrix_xy[0,0]+matrix_xy[0,1]>1.25:
        obj_penalty=obj_penalty-(matrix_xy[0,0]+matrix_xy[0,1]-1)*0.5
    elif matrix_xy[0,0]+matrix_xy[0,1]>1:
        obj_penalty=obj_penalty-(matrix_xy[0,0]+matrix_xy[0,1]-1)*0.25
    return obj_penalty

def Roulette_wheel():
    tr_obj=np.zeros(n_c)            #Roulette wheel1
    for c in range (0,n_c):
        tr_obj[c]=obj[c]
        if obj[c] < -1 :
            tr_obj[c]=abs(1/obj[c])
    prob=tr_obj/sum(tr_obj)
    cprob[0]=prob[0]    
    for c in range(1,n_c):
        cprob[c]=prob[c]+cprob[c-1]
    'select parents1'
    e1=select(cprob)
    ch1=list(chromosom[e1])
    tr_obj=np.delete(tr_obj,e1,0)    #Roulette wheel2
    prob=tr_obj/sum(tr_obj)
    cprob[0]=prob[0]    
    for c in range(1,n_c-1):
        cprob[c]=prob[c]+cprob[c-1]
    'select parents2'
    e2=select(cprob)
    if e1<=e2:
        e2=e2+1
        ch2=list(chromosom[e2])
    if e1 > e2:
        ch2=list(chromosom[e2])
    return ch1,ch2


'--------------------parameter setting-------------------'
n_c = 80         #Number of chromosomes =100
n_d = 24         #24-bit chromosomes:12 bits for variable X and 12 bits for Y
generation= 200  #number of generations=200
CR= 0.8          #crossover rate=0.8
MR =0.3          #mutation rate=0.3
nu=3             #Round off to the 3rd decimal

chromosom = np.zeros((n_c,n_d))
ch_chromosom =np.zeros((n_c,n_d))
xy = np.zeros((n_c,2))
obj=np.zeros(n_c)
prob=np.zeros(n_c)
cprob=np.zeros(n_c)
max_obj=[]

'--------------------main-------------------'

'initialization    constraint  x+y<1 '
for c in range (0,n_c):
    chromosom[c]=np.random.randint(0,2,(1,n_d))
    xy[c]=evaluation(chromosom[c])
    obj[c]=fitness(xy[c,0],xy[c,1])
    while xy[c,0]+xy[c,1] > 1:
        xy[c]=evaluation(chromosom[c])
        obj[c]=fitness(xy[c,0],xy[c,1])
        break
g_time = 0     
while g_time < generation:
    for c in range (0,n_c):
        xy[c]=evaluation(chromosom[c])
        obj[c]=fitness(xy[c,0],xy[c,1])
        'penalty'
        obj[c]=penalty(xy[c],obj[c])         
    obj2=obj
    m1=0
    for c in range(0,n_c):
        if max(obj2)==obj2[c]:
            break
        m1=m1+1
    obj2=np.delete(obj,m1,0)
    m2=0
    for c in range(0,n_c-1):
        if max(obj2)==obj2[c]:
            break
        m2=m2+1
    if m1 <= m2:
        m2=m2+1
    ch_chromosom[0],ch_chromosom[1]=chromosom[m1],chromosom[m2]
    
    pair=2
    time=2
    while time < n_c:
        new_ch1=[]
        new_ch2=[]
        child1,child2=Roulette_wheel()
        'crossover'
        rate_cr=random.random()
        if rate_cr < CR:
            s_rate1 =random.random()  
            s_rate2 =random.random()
            c_location1 = math.ceil(s_rate1*(n_d/2-1))
            c_location2 = math.ceil(s_rate2*(n_d/2-1))+round(n_d/2) 
            new_ch1=child1[0:c_location1]+child2[c_location1:round((n_d/2))]+child1[round(n_d/2):c_location2]+child2[c_location2:n_d]
            new_ch2=child2[0:c_location1]+child1[c_location1:round((n_d/2))]+child2[round(n_d/2):c_location2]+child1[c_location2:n_d]
            'mutation'
            rate_mu1=random.random()
            if rate_mu1 < MR:
                rate_mu_l=random.random()
                if new_ch1[round(rate_mu_l*(n_d-1))] == 0.0:
                    new_ch1[round(rate_mu_l*(n_d-1))]=1.0
                else:
                    new_ch1[round(rate_mu_l*(n_d-1))]=0.0
            rate_mu2=random.random()
            if rate_mu2 < MR:
                rate_mu_l=random.random()
                if new_ch2[round(rate_mu_l*(n_d-1))] == 0.0:
                    new_ch2[round(rate_mu_l*(n_d-1))]=1.0
                else:
                    new_ch2[round(rate_mu_l*(n_d-1))]=0.0
            ch_chromosom[pair],ch_chromosom[pair+1]=new_ch1,new_ch2
            pair=pair+2
            time=time+2
    chromosom = ch_chromosom
    
    for c in range (0,n_c):
        xy[c]=evaluation(chromosom[c])
        obj[c]=fitness(xy[c,0],xy[c,1])
        obj[c]=penalty(xy[c],obj[c])  
    max_obj.append(max(obj))
    g_time=g_time+1 


'display'
plt.plot(max_obj)
for c in range(0,n_c):
    if obj[c]== max(obj):
        print('x',xy[c,0],'y',xy[c,1],'fitness',obj[c])
        break

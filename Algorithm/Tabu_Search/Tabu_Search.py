# -*- coding: utf-8 -*-
"""
Created on Mon May 27 12:13:26 2019
@author: user
"""
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import copy


def fitness(s):
    fit=0
    for i in range(0,n_node):
        x=int(s[i])
        y=int(s[i+1])
        fit=fit+data[x,y]                   #data is distance matrix
    return fit
'--------------------parameter setting-------------------'
tenure=4                                    #Tabu tenure =4
asp=5                                       #aspiration criterion 5
swap=10                                      #swap 7 times
n_node=9                                    #number of nodes =9
tabu=np.zeros([n_node,n_node])
solu=np.zeros((n_node+1))
a=np.zeros((n_node+1))
swap_l=np.zeros([swap,n_node+3])
iteration=200                           #number of iteraion times
min_obj=[]
best=[]
data = pd.read_csv('data.csv')
data=data.to_numpy()

'--------------------main-------------------'

"initialization "    
solu[0]=0
solu[n_node]=0
for i in range(1,n_node):
    solu[i]=random.random()
for i in range(1,n_node):
    k=1
    for j in range (1,n_node):
        if solu[i]>solu[j]:
            k=k+1
        if j == (n_node-1):
            a[i]=k
solu=a
'evaluation'
p_obj=fitness(solu)
for n in range(0,iteration):                        
    for i in range(0,n_node):                       #Tabu matrix
        for j in range(0,n_node):
            if i<j :           
                if tabu[i,j]>0:                     #Update Tabu matrix
                    tabu[i,j]=tabu[i,j]-1
    time=0
    sw_list=np.zeros([swap,2])
    while time < swap:                            #Generate n random swap moves 
        swap1=random.randint(1,n_node-1)
        swap2=random.randint(1,n_node-1)
        dummy=np.zeros(n_node+1)
        if swap1 != swap2:
            dummy=copy.copy(solu)
            e1=0
            e2=0
            for i in range (0,len(solu)):
                if dummy[i]==swap1:
                    e1=i
                if dummy[i]==swap2:
                    e2=i
            dummy[e1]=swap2
            dummy[e2]=swap1
            dummy=list(dummy)
            dummy.append(swap1)
            dummy.append(swap2)
            sw_list[time,0]=swap1
            sw_list[time,1]=swap2
            swap_l[time]=dummy
            time=time+1
    obj=np.zeros(swap)
    for i in range(0,swap):                 #evaluate Obj value of each candidate move
        obj[i]=fitness(swap_l[i])
    new_obj=np.zeros(swap)
    for i in range(0,swap):
        s1=int(sw_list[i,0])
        s2=int(sw_list[i,1])   
        if s1>s2:
            new_obj[i]=obj[i]+tabu[s1,s2]       #updaated obj value by frequency
            if tabu[s2,s1]>0:                   #in jeil
                new_obj[i]=new_obj[i]+asp       #aspiration 
        else:
            new_obj[i]=obj[i]+tabu[s2,s1]       #updaated obj value by frequency
            if tabu[s1,s2]>0:                   #in jeil
                new_obj[i]=new_obj[i]+asp       #aspiration
    for i in range(0,swap):
        if min(new_obj)==new_obj[i]:
            s1=int(sw_list[i,0])
            s2=int(sw_list[i,1])
            if s1>s2:
                tabu[s1,s2]=tabu[s1,s2]+1       #updaate frequency in Tabu matrix
                tabu[s2,s1]=tenure              #put it in the jeil
            if s2>s1:
                tabu[s2,s1]=tabu[s2,s1]+1       #updaate frequency in Tabu matrix
                tabu[s1,s2]=tenure              #put it in the jeil
            solu=swap_l[i,0:n_node+1]           #updaate Solution to be next iteration
            if p_obj > obj[i]:
                min_obj.append(obj[i])
                p_obj=obj[i]
                best=copy.copy(swap_l[i,0:n_node+1])
            if p_obj < obj[i]:
                min_obj.append(p_obj)
            break
'display'
print("The best solution",best)
print("The total distance of best solution",p_obj)
plt.plot(min_obj)

                
                
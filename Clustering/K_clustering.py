# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 12:25:23 2021

@author: Kai
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.metrics.classification import accuracy_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def initial(n_k):
    k_cluster = np.random.random(size=[n_k,dim])
    return k_cluster

def calculate_distance(x1,c1,use_Kmeans):
    distance=np.zeros((len(x1),len(c1)))
    if use_Kmeans == True:
        for i in range(len(c1)):  #k個
            for j in range(len(x1)):  #j 筆資料
                distance[j,i]=math.sqrt(np.sum((x1[j]-c1[i])**2))
    else:
        for i in range(len(c1)):  #k個
            for j in range(len(x1)):  #j 筆資料
                distance[j,i]=np.sum(abs(x1[j]-c1[i]))    
    return distance

def assigned_cluster(asg_dis):
    instances_cluster=np.zeros(len(X))
    for i in range (len(X)):
        for j in range(n_k):
            if min (asg_dis[i]) == asg_dis[i,j]:
                instances_cluster[i]=j
    return instances_cluster

def updata_centroid(la,use_Kmeans):
    new_centroid=np.zeros((n_k,dim))
    if use_Kmeans == True:
        for i in range(n_k): 
            n=0
            for j in range(len(X)):
                if la[j] == label[i]:
                    new_centroid[i]= X[j]+ new_centroid[i]
                    n=n+1
            new_centroid[i]=new_centroid[i]/n
    else:
        df=np.column_stack([X, la]).tolist()
        df=pd.DataFrame(df)
        d = {dim: 'lab'}
        df=df.rename(columns=d)
        for i in range(n_k):
            for j in range (dim):
                dummy=df.loc[df['lab'] == label[i]]
                new_centroid[i,j]=np.median(dummy[j])
    return new_centroid

def K_cluster(n,d,iteration,apply_Kmeans):
    
    global n_k , dim, label
    n_k=n
    use_Kmeans=apply_Kmeans
    it=iteration
    
    dim=d.shape[1]
    '''initial'''
    label =np.arange(0,n_k,1)
    old_centroid= initial(n_k)
    for i in range (it):
        dis=calculate_distance(X,old_centroid,use_Kmeans)
        res_label=assigned_cluster(dis)
        centroid=updata_centroid(res_label,use_Kmeans)
        col_mean = np.nanmean(centroid, axis=0)
        inds = np.where(np.isnan(centroid))
        centroid[inds] = np.take(col_mean, inds[1])
        if np.array_equal(old_centroid,centroid):
            break
        if i ==99:
            print("need more iteration")
        old_centroid=centroid
    score=0
    for i in range(dis.shape[0]):
        score=score+min(dis[i])
    score=score/dis.shape[0]
    return res_label,score

def Normalization(num):
    for i in range(num.shape[1]):
        num[:,i]=(num[:,i]-min(num[:,i]))/(max(num[:,i])-min(num[:,i]))
    return num



'''''''''''''''''''main'''''''''''''''''''
''' import data'''
data = pd.read_csv('C:/Users/kai/Desktop/META/iris_x.csv')
data=np.random.permutation(data) #random data
X=Normalization(data)

result=K_cluster(3,X,100,apply_Kmeans=False)


SSE=[]
K_range=list(range(2,8))
for i in range(2,8):
    res_SSE=K_cluster(i,X,100,apply_Kmeans=False)
    SSE.append(res_SSE[1])

#plot
lines=plt.plot(K_range,SSE)
plt.setp(lines,marker="o")
plt.show()

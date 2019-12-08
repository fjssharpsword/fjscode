# -*- coding: utf-8 -*-
'''
Created on 2019。12.08

@author: Jiansheng Fang   11949039@mail.sustech.edu.cn
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import warnings
warnings.filterwarnings("ignore")

    
def loaddata(path):
    '''
    input: path of txt file
    return: data:list
    '''
    data = []
    with open("data.txt", 'r') as fd:
        line = fd.readline()
        while line != None and line != '':
            arr = line.strip('\n').split(',')#get rid of line break and split
            data.append(arr)
            line = fd.readline()
    return data

#dataSet:聚类数据集
#k:指定的k个类（大佬）             
def kmeans(dataSet, k):
    '''
    input: dataSet:numpy.array, n*m
           k:int
    return: centroid:numpy.array
            cluster:numpy.mat
    '''
    row, col = dataSet.shape #the number of samples
    cluster = np.mat(np.zeros((row, 2))) #initializing a mat with row*2
    centroids = np.zeros((k, col)) #initializing a array with k*col
    
    for i in range(k):#generate the centorids by random
        index = int(np.random.uniform(0, row))
        centroids[i, :] = dataSet[index, :]
        
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        
        for i in range(row):#handle every sample
            minDist = np.sqrt(np.sum(np.power(centroids[0, :] - dataSet[i, :], 2))) #calculate the distance
            minIndex = 0
            for j in range(1,k):#distance between sample and centroid
                distance = np.sqrt(np.sum(np.power(centroids[j, :] - dataSet[i, :], 2)))
                if distance < minDist:
                    minDist  = distance
                    minIndex = j

            if cluster[i, 0] != minIndex: #not convergence
                clusterChanged = True
                cluster[i, :] = minIndex, minDist**2 #update
        #update centroid
        for j in range(k):
            pointsInCluster = dataSet[np.nonzero(cluster[:, 0].A == j)[0]] #all sample belongs to this centroid
            centroids[j, :] = np.mean(pointsInCluster, axis = 0)#update 

    return centroids, cluster
 

def elbowrule(data):
    '''
    input: data for training, m*n
    return: best K
    '''
    distortions=[]
    K = [1,2,3,4,5,6,7,8,9,10]
    for k in K:
        #kmeans=KMeansCluster(k=k)
        centroids, _ = kmeans(data, k)
        value=sum(np.min(cdist(data, centroids, 'euclidean'),axis=1))/data.shape[0]
        print('cluster k=%d <---> value of distortions = %f'%(k,value))
        distortions.append(value)

    cha = [distortions[i] - distortions[i + 1] for i in range(len(distortions) - 1)]
    a_v=distortions[cha.index(max(cha)) + 1]
    index=distortions.index(a_v)+1
    #print(max(cha), a_v,index)
    # Plot the elbow
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal k')
    plt.show()

    return index+1

def predict(X, centroids):
        """
        intpu: x: m*n, sample
        return: m*1, index of centroids
        """
        if not isinstance(X,np.ndarray):
            try:
                X = np.asarray(X)
            except:
                raise TypeError("numpy.ndarray required for X")
        
        m = X.shape[0]#
        preds = np.empty((m,))
        for i in range(m):#assign every sample to a centroid
            minDist = np.inf
            for j in range(centroids.shape[0]):
                #distJI = self._calEDist(centroids[j,:], X[i,:])
                distJI = np.sqrt(np.sum(np.power(centroids[j, :] - X[i, :], 2)))
                if distJI < minDist:
                    minDist = distJI
                    preds[i] = j
        return preds
    
def main():
    
    #1. load  data  and EDA
    df = pd.read_csv('data.txt', sep=',', header=None, dtype=np.float64, na_filter=False)
    print ('Dataset Statistics: row=%d, column=%d'%(df.shape[0],df.shape[1]))
    print (df[255].value_counts(bins=5))
    data = np.array(df)
    
    #2.Elbow rule
    best_k = elbowrule (data)
    print ('The best clusters is: %d'%best_k)
    
    #3. training
    centroids, cluster = kmeans(data, best_k)
    
    #4.predict
    preds = predict(data,centroids)
    #save the prediction of test
    preds =  preds + 1
    np.savetxt("index.txt", preds.astype(int), fmt='%i')
    key = np.unique(preds)
    result = {}
    for k in key:
        mask = (preds == k)
        y_new = preds[mask]
        v = y_new.size
        result[k] = v
    print('The distribution of cluster is:')
    print (result)
    
    #5.plot result
    row = data.shape[0]
    
    #mark = ['or', 'ob', 'og','oc','om','ok','ow','oy']
    mark = ['or', 'ob', 'og']
    for i in range(row):
        markIndex = int(cluster[i, 0])
        plt.plot(data[i, 0], data[i, 255], mark[markIndex])
    
    #mark = ['+r', '+b', '+g','+c','+m','+k','+w','+y']
    mark = ['+r', '+b', '+g']
    for i in range(best_k):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=12)
    
    plt.show()
      
if __name__ == "__main__":
    main()

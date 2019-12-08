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


class KMeansCluster():
    "K-means Cluster"
    
    def __init__(self, k=3, initCent='random', max_iter=200):
        
        self._k = k #cluster numbers
        self._initCent = initCent #first centroids random choose
        self._clusterAssment = None #quare error between sample and nearest centroid
        self._labels = None #sample belongs to centroid id
        self._max_iter = max_iter #epoches
        
    def _calEDist(self, arrA, arrB):
        """
        input: numpy.array arrA, arrB
        return: Euclidean distance calculation
        """
        return np.math.sqrt(sum(np.power(arrA-arrB, 2)))
    
    def _calMDist(self, arrA, arrB):
        """
        input: numpy.array arrA, arrB
        return: Manhattan distance calculation
        """
        return sum(np.abs(arrA-arrB))


    def _randCent(self, data_X, k):
        """
        intpu: data: m*n
               k: cluster nums
        return: centorids with random choice: k*n
        """
        n = data_X.shape[1] # features
        centroids = np.zeros((k,n)) # init with (0,0)....
        for i in range(n):
            dmin, dmax = np.min(data_X[:,i]), np.max(data_X[:,i])
            centroids[:,i] = dmin + (dmax - dmin) * np.random.rand(k)
        return centroids 
    
    def _converged(self, centroids1, centroids2):
        # if centroids not changed, we say 'converged'
        set1 = set([tuple(c) for c in centroids1])
        set2 = set([tuple(c) for c in centroids2])
        return (set1 == set2)
     
    def fit(self, data_X):
        """
        intpu: data: m*n
        Func: training data to update centroids
        """
        n = data_X.shape[0] # number of entries
        if self._initCent == 'random':
            self._centroids = self._randCent(data_X, self._k)
        self._labels = np.zeros(n,dtype=np.int) # track the nearest centroid
        self._clusterAssment = np.zeros(n) # for the assement of our model
        converged = False
        
        for _ in range(self._max_iter):
        #while not converged:
            old_centroids = np.copy(self._centroids)
            for i in range(n):
                # determine the nearest centroid and track it with label
                min_dist, min_index = np.inf, -1
                for j in range(self._k):
                    dist = self._calEDist(data_X[i],self._centroids[j])
                    if dist < min_dist:
                        min_dist, min_index = dist, j
                        self._labels[i] = j
                self._clusterAssment[i] = self._calEDist(data_X[i],self._centroids[self._labels[i]])**2
            
            # update centroid
            for m in range(self._k):
                self._centroids[m] = np.mean(data_X[self._labels==m],axis=0)
                
            #converge verificaiton
            converged = self._converged(old_centroids,self._centroids) 
            if converged:#condition of convergence
                break 
    
    def predict(self, X):
        """
        intpu: x: m*n, sample
        return: m*1, index of centroids
        """
        if not isinstance(X,np.ndarray):
            try:
                X = np.asarray(X)
            except:
                raise TypeError("numpy.ndarray required for X")
        
        m = X.shape[0]#m代表样本数量
        preds = np.empty((m,))
        for i in range(m):#将每个样本点分配到离它最近的质心所属的族
            minDist = np.inf
            for j in range(self._k):
                distJI = self._calEDist(self._centroids[j,:], X[i,:])
                if distJI < minDist:
                    minDist = distJI
                    preds[i] = j
        return preds
    
    
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
              

def elbowrule(data):
    '''
    input: data for training, m*n
    return: K
    '''
    distortions=[]
    for k in range(1,5):
        kmeans=KMeansCluster(k=k)
        kmeans.fit(data)
        value=sum(np.min(cdist(data, kmeans._centroids, 'euclidean'),axis=1))/data.shape[0]
        print('cluster k=%d <---> value of distortions = %f'%(k,value))
        distortions.append(value)

    cha = [distortions[i] - distortions[i + 1] for i in range(len(distortions) - 1)]
    a_v=distortions[cha.index(max(cha)) + 1]
    index=distortions.index(a_v)+1
    #print(max(cha), a_v,index)

    return index+1
 
def main():
    #1. load  data  and EDA
    df = pd.read_csv('data.txt', sep=',', header=None, dtype=np.float64, na_filter=False)
    print ('Dataset Statistics: row=%d, column=%d'%(df.shape[0],df.shape[1]))
    print (df[255].value_counts(bins=5))
    
    #2. choose the best clusters K based on Elbow rule
    best_k = elbowrule (np.array(df)) #3 or 4
    
    #3. training data with best_k
    kmeans=KMeansCluster(k=best_k)
    kmeans.fit(np.array(df))
    print ("The sum error of training is %f"%np.sum(kmeans._clusterAssment))
    
    #4. predict the label of samples
    preds = kmeans.predict(np.array(df))
    #save the prediction of test
    preds =  preds + 1
    np.savetxt("index.txt", preds.astype(int), fmt='%i')
    
    #5.result analysis
    key = np.unique(preds)
    result = {}
    for k in key:
        mask = (preds == k)
        y_new = preds[mask]
        v = y_new.size
        result[k] = v
    print(result)
      
if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
'''
Created on 2019。12.08

@author: Jiansheng Fang   11949039@mail.sustech.edu.cn
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings("ignore")


class KMeansCluster():
    "K-means Cluster"
    
    def __init__(self, k=3, initCent='random', max_iter=500 ):
        
        self._k = k #cluster numbers
        self._initCent = initCent #first centroids random choose
        self._max_iter = max_iter #epoches
        self._clusterAssment = None
        self._labels = None
        self._sse = None
        
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
        n = data_X.shape[1] #dimensions
        centroids = np.empty((k,n))  #generate a k*n matrix with zero
        for j in range(n):
            minJ = min(data_X[:, j])
            rangeJ  = float(max(data_X[:, j] - minJ))
            centroids[:, j] = (minJ + rangeJ * np.random.rand(k, 1)).flatten()#flatten
        return centroids 
    
    def fit(self, data_X):
        """
        intpu: data: m*n
        Func: training data to update centroids
        """
        if not isinstance(data_X, np.ndarray) or \
               isinstance(data_X, np.matrixlib.defmatrix.matrix):
            try:
                data_X = np.asarray(data_X)
            except:
                raise TypeError("numpy.ndarray resuired for data_X")
                
        m = data_X.shape[0]  #number of samples
        #m*2 matrix for save the cluster id of sample and square error between sample and centroids
        self._clusterAssment = np.zeros((m,2)) 
        
        if self._initCent == 'random':
            self._centroids = self._randCent(data_X, self._k)
            
        clusterChanged = True
        for _ in range(self._max_iter): 
            clusterChanged = False
            for i in range(m):   #assign the sample to the nearest centroid
                minDist = np.inf #initializing a infinity value
                minIndex = -1    #initializing the nearest centroid equal to -1
                for j in range(self._k): #iteration
                    arrA = self._centroids[j,:]
                    arrB = data_X[i,:]
                    distJI = self._calEDist(arrA, arrB) #calculate the error value
                    if distJI < minDist:
                        minDist = distJI
                        minIndex = j
                if self._clusterAssment[i, 0] != minIndex or self._clusterAssment[i, 1] > minDist**2:
                    clusterChanged = True
                    self._clusterAssment[i,:] = minIndex, minDist**2
            if not clusterChanged:#condition of convergence
                break
            for i in range(self._k):#update the centroid with mean
                index_all = self._clusterAssment[:,0] #index of sample
                value = np.nonzero(index_all==i) 
                ptsInClust = data_X[value[0]]   
                self._centroids[i,:] = np.mean(ptsInClust, axis=0) #mean
        
        self._labels = self._clusterAssment[:,0]
        self._sse = sum(self._clusterAssment[:,1])
    
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
    K = [1,2,3,4,5,6,7,8,9]
    for k in K:
        #kmeans=KMeansCluster(k=k)
        kmeans=KMeans(n_clusters=k)
        kmeans.fit(data)
        #value=sum(np.min(cdist(data, kmeans._centroids, 'euclidean'),axis=1))/data.shape[0]
        value=sum(np.min(cdist(data, kmeans.cluster_centers_, 'euclidean'),axis=1))/data.shape[0]
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


    return index
 
def main():
    #1. load  data  and EDA
    df = pd.read_csv('data.txt', sep=',', header=None, dtype=np.float64, na_filter=False)
    print ('Dataset Statistics: row=%d, column=%d'%(df.shape[0],df.shape[1]))
    print (df[255].value_counts(bins=5))
    
    #2. choose the best clusters K based on Elbow rule
    best_k = elbowrule (df)
    
    #3. training data with best_k
    kmeans=KMeans(n_clusters=best_k)
    kmeans.fit(np.array(df))
    
    #4. predict the label of samples
    preds = kmeans.predict(np.array(df))
    #save the prediction of test
    preds =  preds + 1
    np.savetxt("index.txt", preds.astype(int), fmt='%i')
    
    #5.plot the result
    colors = ['b','g','r','k','c','m','y','#e24fff','#524C90','#845868']
    preds =  preds - 1
    for i in range(best_k):
        index = np.nonzero(preds==i)[0]
        x0 = np.array(df)[index, 0]
        x1 = np.array(df)[index, 1]
        y_i = i
        for j in range(len(x0)):
            plt.text(x0[j], x1[j], str(y_i), color=colors[i],fontdict={'weight': 'bold', 'size': 6})
        plt.scatter(kmeans._centroids[i,0],kmeans._centroids[i,1],marker='x',color=colors[i],linewidths=7)
    plt.show()
   
if __name__ == "__main__":
    main()

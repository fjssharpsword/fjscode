# -*- coding: utf-8 -*-
'''
Created on 2019。11.26

@author: Jiansheng Fang   11949039@mail.sustech.edu.cn
'''

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from matplotlib import rcParams
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def loadDataset_as_List(filePath):
    dataset = []
    with open(filePath, 'r') as fd:
        line = fd.readline()
        while line != None and line != '':
            arr = line.strip('\n').split(' ')#Separator is space 
            strs = []
            for i in range(len(arr)):
                strs.append(arr[i])
            dataset.append(strs)
            line = fd.readline()
    return dataset
    

def main():
    #load train data and test data
    X_train = np.array(loadDataset_as_List('traindata.txt')).astype(float)
    print('Train Dataset Statistics: lines = %d, rows = %d'%(X_train.shape[0],X_train.shape[1]))
    Y_train = np.array(loadDataset_as_List('trainlabel.txt')).astype(int)
    print('Label1={} and Label2={}'.format(sum(Y_train==1),sum(Y_train==2)))
    X_test = np.array(loadDataset_as_List('testdata.txt')).astype(float)
    print('Test Dataset Statistics: lines = %d, rows = %d'%(X_test.shape[0],X_test.shape[1]))
    
    #EDA
    dt = pd.DataFrame(np.concatenate((X_train,Y_train),axis=1))
    #dt.columns = ['age', 'sex', 'chest_pain_type', 'resting_blood_pressure', 'cholesterol', 'fasting_blood_sugar', 'rest_ecg', 'max_heart_rate_achieved',
    #               'exercise_induced_angina', 'st_depression', 'st_slope', 'num_major_vessels', 'thalassemia','target']
    dt.columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13','target']
    dt.hist()
    plt.show()
    
    '''
    rcParams['figure.figsize'] = 20, 14
    plt.matshow(dt.corr())
    plt.yticks(np.arange(dt.shape[1]), dt.columns)
    plt.xticks(np.arange(dt.shape[1]), dt.columns)
    plt.colorbar()
    plt.show()
    '''
    
    '''
    print (pd.isnull(dt))
    print (pd.isna(dt))
    
    #observe discrete feature 
    print (dt.sex.value_counts()) 
    print (dt.chest_pain_type.value_counts())
    print (dt.fasting_blood_sugar.value_counts())
    print (dt.exercise_induced_angina.value_counts())
    print (dt.st_slope.value_counts())
    print (dt.num_major_vessels.value_counts())
    print (dt.thalassemia.value_counts())
    #show label distribution
    sns.countplot(x="target", data=dt, palette="bwr")
    plt.show()
    '''

    '''
    #normalize the data
    scaler = StandardScaler().fit(np.concatenate((X_train, X_test), axis=0))
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    Y_train = np.where(Y_train==1,0,1) #turn label to 0,1
    print('Label1={} and Label2={}'.format(sum(Y_train==0),sum(Y_train==1)))
    '''
    
   
if __name__ == "__main__":
    main()
    
'''
Attribute Information:
> 1. age
> 2. sex
> 3. chest pain type (4 values)
> 4. resting blood pressure
> 5. serum cholestoral in mg/dl
> 6. fasting blood sugar > 120 mg/dl
> 7. resting electrocardiographic results (values 0,1,2)
> 8. maximum heart rate achieved
> 9. exercise induced angina
> 10. oldpeak = ST depression induced by exercise relative to rest
> 11. the slope of the peak exercise ST segment
> 12. number of major vessels (0-3) colored by flourosopy
> 13. thal: 3 = normal; 6 = fixed defect; 7 = reversable defect
'''

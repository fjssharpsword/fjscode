# -*- coding: utf-8 -*-
'''
Created on 2019。11.26

@author: Jiansheng Fang   11949039@mail.sustech.edu.cn
'''

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
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
    #preprocess  data
    dt = pd.DataFrame(np.concatenate((X_train, X_test), axis=0))
    dt.columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    dt = pd.get_dummies(dt, columns = ['2', '3', '6', '7', '9', '11', '12', '13'])#onehot
    standardScaler = StandardScaler()
    columns_to_scale = ['1', '4', '5', '8', '10']
    dt[columns_to_scale] = standardScaler.fit_transform(dt[columns_to_scale])#normalize
    X_train = np.array(dt)[0:180]
    print(X_train.shape)
    X_test = np.array(dt)[180:]
    print (X_test.shape)
    #turn label to 0,1
    Y_train = np.where(Y_train==1,0,1) 
    print('Label1={} and Label2={}'.format(sum(Y_train==0),sum(Y_train==1)))
    #training with RandomForestClassifier
    accs = []
    models = []
    for epoch in range(1000): 
        x_train, x_val, y_train, y_val = train_test_split(X_train, Y_train, test_size = .2, random_state=0)
        model = RandomForestClassifier(max_depth=5)
        model.fit(x_train, y_train)
        models.append(model)
        y_predict = model.predict(x_val)
        acc = accuracy_score(y_val,y_predict)
        accs.append(acc)
        #print ('epoch:{} /200 ==> Accuracy:{}'.format(epoch,acc))
    #predict train dataset
    iMax =  accs.index(max(accs))
    print ('The best Accuracy is {} in epoch:{}'.format(max(accs),iMax))
    Y_pred = models[iMax].predict(X_train)
    print ('The accuracy of train dataset is {}'.format(accuracy_score(Y_train,Y_pred)))
    #predict test dataset
    Y_test = models[iMax].predict(X_test)#choose the best model to predict test label
    Y_test = np.where(Y_test==0,1,2)#turn 0,1 to label
    #save the prediction of test
    np.savetxt("testlabel_rf.txt", Y_test.astype(int), fmt='%i')
    
   
if __name__ == "__main__":
    main()

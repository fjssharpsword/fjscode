# -*- coding: utf-8 -*-
'''
Created on 2019。11.26

@author: Jiansheng Fang   11949039@mail.sustech.edu.cn
'''

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import sys
import tensorflow as tf
import warnings
warnings.filterwarnings("ignore")

def sigmoid(x):
    s = 1/(1+np.exp(-x)) 
    return s

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

class NNModel():
    
    def __init__(self,lr=0.01):
        self.lr = lr
        #set network structure
        self.add_placeholders()
        self.add_weight()
        self.add_model()
        self.add_loss()
        self.add_optimizer()
        self.init_sess()
    def add_placeholders(self):
        self.X_input = tf.placeholder(tf.float32)
        self.Y_input = tf.placeholder(tf.float32)
        
    def add_weight(self):
        self.weights = { #13->8->4->2
            'h1': tf.Variable(tf.random_normal([13, 8])),
            'h2': tf.Variable(tf.random_normal([8, 4])),
            'out': tf.Variable(tf.random_normal([4, 1]))}
        self.biases = {
            'b1': tf.Variable(tf.random_normal([8])),
            'b2': tf.Variable(tf.random_normal([4])),
            'out': tf.Variable(tf.random_normal([1]))}
    def add_model(self):
        # Hidden fully connected layer with 256 neurons
        layer_1 = tf.add(tf.matmul(self.X_input, self.weights['h1']), self.biases['b1'])
        # Hidden fully connected layer with 256 neurons
        layer_2 = tf.add(tf.matmul(layer_1, self.weights['h2']), self.biases['b2'])
        # Output fully connected layer with a neuron for each class
        self.Y_output = tf.matmul(layer_2, self.weights['out']) + self.biases['out']
    
    def add_loss(self):
        self.loss = tf.losses.sigmoid_cross_entropy( self.Y_input , self.Y_output ) 
        
    def add_optimizer(self):
        optimizer = tf.train.AdamOptimizer(self.lr)
        self.train_step = optimizer.minimize(self.loss)
        
    def init_sess(self):
        #self.config = tf.ConfigProto()
        #self.config.gpu_options.allow_growth = True
        #self.config.allow_soft_placement = True
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())
    

def main():
    #load train data and test data
    X_train = np.array(loadDataset_as_List('traindata.txt')).astype(float)
    print('Train Dataset Statistics: lines = %d, rows = %d'%(X_train.shape[0],X_train.shape[1]))
    Y_train = np.array(loadDataset_as_List('trainlabel.txt')).astype(int)
    print('Label1={} and Label2={}'.format(sum(Y_train==1),sum(Y_train==2)))
    X_test = np.array(loadDataset_as_List('testdata.txt')).astype(float)
    print('Test Dataset Statistics: lines = %d, rows = %d'%(X_test.shape[0],X_test.shape[1]))
    #normalize the data
    scaler = StandardScaler().fit(np.concatenate((X_train, X_test), axis=0))
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    Y_train = np.where(Y_train==1,0,1) #turn label to 0,1
    print('Class0={} and Class1={}'.format(sum(Y_train==0),sum(Y_train==1)))
    #training with DNN
    tf_model = NNModel() #bulid model
    batchSize=10
    num_batches = X_train.shape[0] // batchSize + 1 
    pre_loss = 0.0
    while True:#convergence
        losses = []
        for i in range(num_batches):
            min_idx = i * batchSize
            max_idx = np.min([X_train.shape[0], (i+1)*batchSize])
            X_batch = X_train[min_idx: max_idx]
            Y_batch = Y_train[min_idx: max_idx]
            _, tmp_loss = tf_model.sess.run([tf_model.train_step, tf_model.loss], 
                                             feed_dict={tf_model.X_input: X_batch,tf_model.Y_input: Y_batch})
            losses.append(tmp_loss)
            #if verbose and i % verbose == 0:
            #    sys.stdout.write('\r{} / {} : loss = {}'.format(i, num_batches, np.mean(losses[-verbose:])))
            #    sys.stdout.flush()
        sys.stdout.write("Mean loss in this epoch is: {}\n".format( np.mean(losses) ))
        sys.stdout.flush()
        #whether convergence
        if abs( np.mean(losses) - pre_loss)<0.001:
            break
        else:
            pre_loss = np.mean(losses)
    Y_pred = tf_model.sess.run(tf_model.Y_output, feed_dict={tf_model.X_input: X_train,tf_model.Y_input: Y_train})
    Y_pred = sigmoid(Y_pred)
    Y_pred = np.where(Y_pred>0.5,1,0)
    print ('The accuracy of train dataset is {}'.format(accuracy_score(Y_train,Y_pred)))
    #predict test dataset
    Y_test = tf_model.sess.run(tf_model.Y_output, feed_dict={tf_model.X_input: X_test})
    Y_test = sigmoid(Y_test)
    Y_test = np.where(Y_test>0.5,1,0)
    Y_test = np.where(Y_test==0,1,2)#turn 0,1 to label
    #save the prediction of test
    np.savetxt("testlabel_nn.txt", Y_test.astype(int), fmt='%i')
    
   
if __name__ == "__main__":
    main()
    

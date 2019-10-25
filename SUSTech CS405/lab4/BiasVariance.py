# coding:utf-8  
'''
Created on 2019年9月27日

@author: Jason.Fang   11949039@mail.sustech.edu.cn
'''
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge

'''
The bias-variance tradeoff is a central problem in supervised learning.
Ideally, one wants to choose a model that both accurately captures the regularities in its training data, 
but also generalizes well to unseen data.
Unfortunately, it is typically impossible to do both simultaneously.
High-variance learning methods may be able to represent their training set well, 
but are at risk of overfitting to noisy or unrepresentative training data.
In contrast, algorithms with high bias typically produce simpler models that don't tend to overfit, 
but may underfit their training data, failing to capture important regularities.
'''
if __name__ == "__main__":
    
    #load boston dataset
    boston = load_boston()
    X = boston.data #get the feature
    y = boston.target #get the target vector
    X = X[y<50.0]#leave out outliers
    y = y[y<50.0]#leave out outliers
    print('Train Dataset Statistics: line = %d, row = %d'%(X.shape[0],X.shape[1]))
    
    #split into train set and test set.
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2)
    
    #split into train set and validation set.
    _, X_val, _, y_val = train_test_split(X_train,y_train,test_size = 0.2)
    
    
    #training linear Regression
    lin_reg = LinearRegression()#default parameters
    lin_reg.fit(X_train, y_train)
    print("Validation set Score@LR:{}".format(lin_reg.score(X_val, y_val)))
    print("Test set Score@LR:{}".format(lin_reg.score(X_test, y_test)))
    
    ''' Overfitting <==> high-variance
    Validation set Score@LR:0.803489575756606
    Test set Score@LR:0.7016545286041725
    '''
    
    #training linear Regression with regularization
    ridge = Ridge(alpha=1.0)#default parameters
    ridge.fit(X_train, y_train)
    print("Validation set Score@LR:{}".format(ridge.score(X_val, y_val)))
    print("Test set Score@LR:{}".format(ridge.score(X_test, y_test)))
    ''' underfitting <==> high-bias
    Validation set Score@LR:0.7763393991398273
    Test set Score@LR:0.7510162722803512
    '''

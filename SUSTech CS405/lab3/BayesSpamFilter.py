# coding:utf-8  
'''
Created on 2019年9月23日

@author: Jason.Fang   11949039@mail.sustech.edu.cn
'''
import jieba
import os
from collections import Counter
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

#construct the dictionary for email
def make_Dictionary(train_dir):
    #Traverse all files under folders
    for _,_,files in os.walk(train_dir):
        emails = [os.path.join(train_dir,f) for f in files]
    all_words = []
    for mail in emails:
        with open(mail) as m:
            for i, line in enumerate(m):
                if i==2: #body of email is valid
                    words = line.split()
                    all_words += words
    dictionary = Counter(all_words)#dict, words:frequency
    #remove the non-words
    list_to_remove = list(dictionary.keys())
    for item in list_to_remove:
        if item.isalpha() ==False:
            del dictionary[item]
        elif len(item) ==1:
            del dictionary[item]
    dictionary = dictionary.most_common(3000)
    return dictionary

#Extracting the feature of mails, wordtovec
def extract_features(mail_dir,dictionary):
    for _,_,files in os.walk(mail_dir):
        emails = [os.path.join(mail_dir,f) for f in files]
    features_matrix = np.zeros((len(emails),3000))
    label_series = np.zeros(len(emails))
    docID=0
    for mail in emails:
        if 'spm' in os.path.basename(mail):#label the spam
            label_series[docID]=1
        with open(mail) as m:
            for i, line in enumerate(m):
                if i==2:
                    words = line.split()
                    for word in words:
                        wordID=0
                        for i, d in enumerate(dictionary):
                            if d[0] ==word:
                                wordID=i
                                features_matrix[docID,wordID]=1
            docID = docID+1
    return  features_matrix, label_series   
    
if __name__ == "__main__":
    
    #prepare dataset
    train_dir = 'ling-spam/train-mails'
    test_dir = 'ling-spam/test-mails'
    dictionary = make_Dictionary(train_dir)
    x_train, y_train = extract_features(train_dir, dictionary)#extract the features of train data
    print('Train Dataset Statistics: line = %d, row = %d'%(x_train.shape[0],x_train.shape[1]))
    assert(x_train.shape[0]==y_train.shape[0])
    x_test, y_test = extract_features(test_dir, dictionary)#extract the features of test data
    print('Train Dataset Statistics: line = %d, row = %d'%(x_test.shape[0],x_test.shape[1]))
    assert(x_test.shape[0]==y_test.shape[0])
    #training navie Bayes model
    mnb_count = MultinomialNB()
    mnb_count.fit(x_train, y_train)
    #performance metrics
    y_test_pred = mnb_count.predict(x_test)
    print (classification_report(y_test, y_test_pred))
    
    
    
'''
outcome:
Train Dataset Statistics: line = 702, row = 3000
Train Dataset Statistics: line = 260, row = 3000
              precision    recall  f1-score   support

         0.0       0.94      0.99      0.97       130
         1.0       0.99      0.94      0.96       130

   micro avg       0.97      0.97      0.97       260
   macro avg       0.97      0.97      0.97       260
weighted avg       0.97      0.97      0.97       260
'''
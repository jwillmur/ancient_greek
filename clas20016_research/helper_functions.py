'''
Define functions for CLAS20016 Research Code
'''

import numpy as np

from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2, f_classif, SelectKBest
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

def categorise_number(number):
    '''
    Convert number of ship to numbered categories
    '''
    if number=='s':
        return 1
    if number=='p':
        return 0

def categorise_case(case):
    '''
    Categorise case of ship to numbered categories
    '''
    if case=='n':
        return 0
    if case=='g':
        return 1
    if case=='d':
        return 2
    if case=='a':
        return 3


def chi_square(X_input, Y_input, test_input, k):
    '''
    Selects the k most significant features using the chi squared metric
    '''
    x2 = SelectKBest(chi2, k=k)
    x2.fit(X_input, Y_input)
    X_output = x2.fit_transform(X_input, Y_input)
    test_output = x2.transform(test_input)
    return X_output, test_output

def anova(X_input, Y_input, test_input):
    '''
    Selects the k most significant features using ANOVA
    '''
    anova = SelectKBest(f_classif, k=2)
    anova.fit(X_input, Y_input)
    X_output = anova.fit_transform(X_input, Y_input)
    test_output = anova.transform(test_input)
    return X_output, test_output

def tfidf_vector(train_in, test_in):
    '''
    Weights the vectors with their occurences
    '''
    tfidf_vectorizer = TfidfVectorizer()
    train_out = tfidf_vectorizer.fit_transform(train_in)
    test_out = tfidf_vectorizer.transform(test_in)
    return train_out, test_out

def model_features(X_train, X_test, y_train, y_test):
    '''
    Find the accuracy of three models
    '''
    ## baseline: zero_r
    zero_r = DummyClassifier(strategy='most_frequent')
    zero_r = zero_r.fit(X_train, y_train)
    print('Baseline 0-R:', cross_val_score(zero_r, X_test, y_test, scoring='f1_micro').mean())

    ## one_r
    one_r = DecisionTreeClassifier(max_depth=1)
    one_r = one_r.fit(X_train, y_train)
    print('One-R:', cross_val_score(one_r, X_test, y_test, scoring='f1_micro').mean())

    ## decision tree
    tree = DecisionTreeClassifier(max_depth=5)
    tree = tree.fit(X_train, y_train)
    print('Decision tree:', cross_val_score(tree, X_test, y_test, scoring='f1_micro').mean())

    ## logistic regression
    lgr = LogisticRegression(C=1, penalty='l1', solver='saga')
    lgr = lgr.fit(X_train, y_train)
    print('MLR:', cross_val_score(lgr, X_test, y_test, scoring='f1_micro').mean())

    return
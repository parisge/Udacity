"""
Created on Fri Jan 15 15:59:35 2016

@author: GEP
"""
#!/usr/bin/python
import os
import sys
import pickle
import random
import matplotlib
from matplotlib import pyplot
sys.path.append("../tools/")
import pandas as pd
import numpy as np
import pprint

from numpy import mean
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.preprocessing import MinMaxScaler
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn import tree
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi'] # You will need to use more features

### Load the dictionary containing the dataset
#data_dict = pickle.load(open("final_project_dataset.pkl", "r") )
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
df=pd.DataFrame(data_dict)

df.dtypes
df.info()
tdf = df.transpose()
tdf.head()

### Task 2: Remove outliers
num_data_points = len(data_dict)
num_data_features = len(data_dict[data_dict.keys()[0]])

     
num_poi = 0
for dic in data_dict.values():
	if dic['poi'] == 1: num_poi += 1

print "Data points: ", num_data_points
print "Features: ", num_data_features
print "POIs: ", num_poi
print data_dict['SKILLING JEFFREY K'].keys()

# graphical representation of salary & bonus
for dic in data_dict.values():
     matplotlib.pyplot.scatter( dic['salary'] , dic['bonus']  )

matplotlib.pyplot.xlabel("salary")
matplotlib.pyplot.ylabel("bonus")
matplotlib.pyplot.show()

for k, v in data_dict.items():
    if v['salary'] != 'NaN' and v['salary'] > 10000000: print k

# removal of the  TOTAL row salaries & bonuses 

del data_dict["TOTAL"]
del data_dict["THE TRAVEL AGENCY IN THE PARK"]

features = ["from_this_person_to_poi", "from_poi_to_this_person"]
poi_data = featureFormat(data_dict, features)

# graphical representation of communication from & to POIs
print poi_data.max()
for point in poi_data:
    from_this_person_to_poi = point[0]
    from_poi_to_this_person = point[1]
    matplotlib.pyplot.scatter( from_this_person_to_poi, from_poi_to_this_person )

matplotlib.pyplot.xlabel("from_this_person_to_poi")
matplotlib.pyplot.ylabel("from_poi_to_this_person")
matplotlib.pyplot.show()

from_outliers = []
for key in data_dict:
    val = data_dict[key]['from_poi_to_this_person']
    if val == 'NaN':
        continue
    from_outliers.append((key,int(val)))

print sorted(from_outliers,key=lambda x:x[1],reverse=True)[:3]

to_outliers = []
for key in data_dict:
    val = data_dict[key]['from_this_person_to_poi']
    if val == 'NaN':
        continue
    to_outliers.append((key,int(val)))

print sorted(to_outliers,key=lambda x:x[1],reverse=True)[:3]
print data_dict['DELAINEY DAVID W'].values()[3]

### Task 3: Create new feature(s) and change POIs
### Store to my_dataset for easy export below.
my_dataset = data_dict

my_dataset['LAVORATO JOHN J']['poi']=True
num_poi = 0
for dic in my_dataset.values():
	if dic['poi'] == 1: num_poi += 1

print "New Number of POIs: ", num_poi
     
## Custom features
## Fraction of POI communications
for item in my_dataset:
	person = my_dataset[item]
	if (all([	person['from_poi_to_this_person'] != 'NaN',
				person['from_this_person_to_poi'] != 'NaN',
				person['to_messages'] != 'NaN',
				person['from_messages'] != 'NaN'
			])):
	    fraction_from_poi = float(person["from_poi_to_this_person"]) / float(person["to_messages"])
	    person["fraction_from_poi"] = fraction_from_poi
	    fraction_to_poi = float(person["from_this_person_to_poi"]) / float(person["from_messages"])
	    person["fraction_to_poi"] = fraction_to_poi
	else:
	    person["fraction_from_poi"] = person["fraction_to_poi"] = 0

## Aggregate financial wealth
for item in my_dataset:
	person = my_dataset[item]
	if (all([	person['salary'] != 'NaN',
				person['total_stock_value'] != 'NaN',
				person['exercised_stock_options'] != 'NaN',
				person['bonus'] != 'NaN'
			])):
		person['wealth'] = sum([person[field] for field in ['salary',
														   'total_stock_value',
														   'exercised_stock_options',
														   'bonus']])
	else:
	    person['wealth'] = 'NaN'

my_features = features_list + ['fraction_from_poi',
                               'fraction_to_poi', 'wealth',
						   'salary', 'to_messages', 'deferral_payments', 
         'total_payments', 'exercised_stock_options', 'bonus', 'restricted_stock',
         'shared_receipt_with_poi', 'restricted_stock_deferred',
         'total_stock_value', 'expenses','loan_advances',
         'from_messages', 'other', 'from_this_person_to_poi',
         'director_fees','deferred_income', 'long_term_incentive',
         'from_poi_to_this_person']


### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, my_features, sort_keys = True)
labels, features = targetFeatureSplit(data)

print "Intuitive features:", my_features
scaler = MinMaxScaler()
features = scaler.fit_transform(features)

# Forest of Trees features
X = features
Y = labels
forest = ExtraTreesClassifier(n_estimators=250,random_state=0)
forest.fit(X, Y).transform(X)
importances = forest.feature_importances_
results_list= zip(importances, my_features[1:])
results_list= sorted(results_list, key=lambda x: x[0], reverse=True)
indices = np.argsort(importances)[::-1]
print "Forest of trees features:", results_list[0:10]

# K-best features
k_best = SelectKBest(f_regression, k=10)
k_best.fit(features, labels)
results_list = zip(k_best.get_support(), my_features[1:], k_best.scores_)
results_list = sorted(results_list, key=lambda x: x[2], reverse=True)
print "K-best features:", results_list[0:10]

#########################################################
## Iteration of Validation of Algorithms
def test_clf(grid_search, labels, features, parameters, iterations=50):
	precision, recall = [], []
	for iteration in range(iterations):
		features_train, features_test, labels_train, labels_test = train_test_split(features, labels, random_state=iteration)
		grid_search.fit(features_train, labels_train)
		predictions = grid_search.predict(features_test)
		precision = precision + [precision_score(labels_test, predictions)]
		recall = recall + [recall_score(labels_test, predictions)]
		if iteration % 10 == 0:
			sys.stdout.write('.')
	print '\nPrecision:', mean(precision)
	print 'Recall:', mean(recall)
	best_params = grid_search.best_estimator_.get_params()
	for param_name in sorted(parameters.keys()):
		print '%s=%r, ' % (param_name, best_params[param_name])
##############################################################  
### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
# Scale features 


## 5 best features chosen by SelectKBest
my_features = features_list + ['exercised_stock_options',
							   'total_stock_value',
							   'bonus',
							   'salary',
							   'fraction_to_poi',
                                     'wealth',
                                     'from_poi_to_this_person']

data = featureFormat(my_dataset, my_features, sort_keys = True)
labels, features = targetFeatureSplit(data)


clf = GaussianNB()
print clf.score
print clf
parameters = {}
grid_search = GridSearchCV(clf, parameters)
print '\nGaussianNB:'
test_clf(grid_search, labels, features, parameters)

clf = tree.DecisionTreeClassifier()

parameters = {'criterion': ['gini', 'entropy'],
               'min_samples_split': [2, 10, 20],
               'max_depth': [None, 2, 5, 10],
               'min_samples_leaf': [1, 5, 10],
               'max_leaf_nodes': [None, 5, 10, 20]}
grid_search = GridSearchCV(clf, parameters)
print '\nDecisionTree:'
test_clf(grid_search, labels, features, parameters)

clf = AdaBoostClassifier()
parameters = {'n_estimators': [10, 20, 30, 40, 50],
               'algorithm': ['SAMME', 'SAMME.R'],
               'learning_rate': [.5,.8, 1, 1.2, 1.5]}
grid_search = GridSearchCV(clf, parameters)
print '\nAdaBoost:'
test_clf(grid_search, labels, features, parameters)

## 5 best features chosen by Forest of Trees
my_features = features_list + ['bonus',
                                   'exercised_stock_options',
                                   'fraction_to_poi',
                                   'total_stock_value',
                                   'deferred_income',
                                   'expenses',
                                   'other'
                               ]

data = featureFormat(my_dataset, my_features, sort_keys = True)
labels, features = targetFeatureSplit(data)

clf = GaussianNB()
print clf.score
print clf
parameters = {}
grid_search = GridSearchCV(clf, parameters)
print '\nGaussianNB:'
test_clf(grid_search, labels, features,  parameters)

clf = tree.DecisionTreeClassifier()

parameters = {'criterion': ['gini', 'entropy'],
               'min_samples_split': [2, 10, 20],
               'max_depth': [None, 2, 5, 10],
               'min_samples_leaf': [1, 5, 10],
               'max_leaf_nodes': [None, 5, 10, 20]}
grid_search = GridSearchCV(clf, parameters)
print '\nDecisionTree:'
test_clf(grid_search, labels, features, parameters)

clf = AdaBoostClassifier()
parameters = {'n_estimators': [10, 20, 30, 40, 50],
               'algorithm': ['SAMME', 'SAMME.R'],
               'learning_rate': [.5,.8, 1, 1.2, 1.5]}
grid_search = GridSearchCV(clf, parameters)
print '\nAdaBoost:'
test_clf(grid_search, labels, features, parameters)

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.3, random_state=42)

from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, my_features)
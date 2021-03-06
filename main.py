import sys
import scipy
import numpy
import matplotlib
import pandas
import sklearn

'''1. Check the versions of libraries'''

# print('Python: {}'.format(sys.version))
# print('scipy: {}'.format(scipy.__version__))
# print('numpy: {}'.format(numpy.__version__))
# print('matplotlib: {}'.format(matplotlib.__version__))
# print('pandas: {}'.format(pandas.__version__))
# print('sklearn: {}'.format(sklearn.__version__))

'''2. Load libraries'''
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Load dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(url, names=names)

'''3. Summarize the Dataset'''
# # Dimensions of Dataset
# # shape
# print(dataset.shape)

# # Peek at the Data
# # head: the first 20 rows of the data

# print(dataset.head(20))
# # Statistical Summary
# # descriptions

# print(dataset.describe())

# # class distribution
# print(dataset.groupby('class').size())

'''4. Data Visualization'''
# Univariate Plots

# # box and whisker plots
# dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
# plt.show()

# # histograms
# dataset.hist()
# plt.show()

# Multivariate Plots

# # scatter plot matrix
# scatter_matrix(dataset)
# plt.show()

'''5. Evaluate Some Algorithms'''
# Create a Validation Dataset
# Split-out validation dataset
array = dataset.values
X = array[:,0:4]
Y = array[:,4]
validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

# Test Harness
# Test options and evaluation metric
seed = 7
scoring = 'accuracy'

# Build Models
# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))
# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = model_selection.KFold(n_splits=10, random_state=seed)
	cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
	results.append(cv_results)
	names.append(name)
	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
	print(msg)
print('\n'.join(map(str, results)))

# Select Best Model

# Compare Algorithms
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

'''6. Make Predictions'''
# Make predictions on validation dataset
knn = KNeighborsClassifier()
knn.fit(X_train, Y_train)
predictions = knn.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))

svc = SVC(gamma='auto')
svc.fit(X_train, Y_train)
predictions = svc.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))

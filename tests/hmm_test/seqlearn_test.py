from seqlearn.perceptron import StructuredPerceptron # it's like mini neural network.

# the lengths_train marked each individual sequence's length as an array.
import numpy as np
X_train = np.random.random((5,4)) # one-hot encoded? not? features=4
y_train = np.random.randint(0,5,(5,)) # the freaking label.

lengths_train = [1,1,2,1] # may i apologize. sum=5

classifier =  StructuredPerceptron()
classifier.fit(X_train, y_train, lengths_train)

from seqlearn.evaluation import bio_f_score
y_pred = clf.predict(X_train, lengths_test)
print(bio_f_score(y_test, y_pred))
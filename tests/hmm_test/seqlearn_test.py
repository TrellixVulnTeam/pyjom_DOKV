from seqlearn.perceptron import StructuredPerceptron

from seqlearn.datasets import load_conll
def features(sequence, i):
...     yield "word=" + sequence[i].lower()
...     if sequence[i].isupper():
...         yield "Uppercase"
clf = StructuredPerceptron()
clf.fit(X_train, y_train, lengths_train)
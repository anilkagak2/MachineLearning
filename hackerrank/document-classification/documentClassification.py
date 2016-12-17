import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
#from sklearn.cross_validation import train_test_split, GridSearchCV
from sklearn import metrics

# Gather training data
train_X, train_Y = [], []
with open("trainingdata.txt") as fp:
    lines = int( next(fp).strip() )

    for _ in range(0, lines):
        line = next(fp)
        vals = line.strip().split(' ', 1)
        if len(vals) != 2: continue
        
        train_X.append(vals[1])
        train_Y.append(int(vals[0]))

train_X, train_Y = np.array(train_X), np.array(train_Y)
#X_train, X_test, y_train, y_test = train_test_split(train_X, train_Y, test_size=0.25, random_state=42)

# Gather test data
T = int( raw_input() )
test_X = []
for _ in range(0, T):
    test_X.append(raw_input().strip())

test_X = np.array(test_X)

#print("Training..")
#text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB())])
text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, n_iter=5, random_state=42))])
text_clf.fit(train_X, train_Y)

#parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
#               'tfidf__use_idf': (True, False),
#               'clf__alpha': (1e-2, 1e-3),
#}

#gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
#text_clf.fit(X_train, y_train)

#print("Prediction..")
#predicted = text_clf.predict(X_test)
#print("Accuracy = " + str(np.mean(predicted == y_test)))
#print(metrics.classification_report(y_test, predicted))

## Test the classifier
predictions = text_clf.predict(test_X)
for category in predictions:
    print(category)
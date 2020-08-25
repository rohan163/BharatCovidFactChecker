import socket
import os
import warnings
warnings.simplefilter("ignore")
import csv
import nltk
from sklearn import metrics
import pandas as pd
import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import Counter
from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn import metrics
import itertools
from sklearn.metrics import precision_score,recall_score
from sklearn.metrics import confusion_matrix
training_set = pd.read_csv("train_covid.csv", sep=',')
training_set = training_set.drop("X1", axis=1)
training_set = training_set.drop("X2", axis=1)
training_set.title.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
training_set.text.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
training_set = training_set[(training_set.label == 'FAKE') | (training_set.label == 'REAL')]
training_set_labels = training_set.label 
training_set_data = training_set.drop("label", axis = 1)
training_set_data = training_set_data.drop("ID", axis = 1)
training_set_data["full_text"] = training_set_data["title"].map(str) + " " + training_set_data["text"]
training_data = training_set_data["full_text"]
stopwords = set(STOPWORDS)
training_labels = training_set_labels.tolist()
labels = [1 if x =='FAKE' else 0 for x in training_labels]
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stop_list = stopwords.words('english')
stemmer = PorterStemmer()
all_tokens_lower = [t.lower() for t in training_data]
tokens_normalised = [stemmer.stem(t) for t in all_tokens_lower
                                     if t not in stop_list]
X_train, X_test, y_train, y_test = train_test_split(tokens_normalised, labels,test_size = .3 , random_state = 42 )
X_train = np.asarray(X_train)
y_train = np.asarray(y_train)
X_test = np.asarray(X_test)
y_test = np.asarray(y_test)
text_clf = Pipeline([('vect', CountVectorizer(stop_words = "english")), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
parameters = {'vect__ngram_range': [(1, 1), (1, 2), (1, 3)], #test up to 3 n-grams
              'tfidf__use_idf': (True, False), 
              'tfidf__norm': ('l1', 'l2'), 
              'tfidf__sublinear_tf': (True, False), 
              'clf__alpha': (1e-2, 1e-3), 
              'clf__fit_prior':(True, False) }
gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1, cv=5)
model1 = gs_clf.fit(X_train, y_train)
#predicted = model1.predict(X_test)
#print(np.mean(predicted == y_test))

print("server on")

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        with open('news_file.csv', mode='w') as news_file:
            news_writer = csv.writer(news_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            news_writer.writerow([data])
        news_set = pd.read_csv("news_file.csv", sep=',')
        news_set_data = news_set
        stop_list = stopwords.words('english')
        stemmer = PorterStemmer()
        all_tokens_lower = [t.lower() for t in news_set_data]
        tokens_normalised1 = [stemmer.stem(t) for t in all_tokens_lower
                                       if t not in stop_list]
        final_testX = np.asarray(tokens_normalised1)
        predictedfinal = model1.predict(final_testX)
        results =  predictedfinal
        if results == 1:
            data = "Fake"
        else:
            data = "True"
        print(data)
        os.remove("news_file.csv")
        conn.send(data.encode())  # send data to the client

    #conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
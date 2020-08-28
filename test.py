import os
import sys
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
import pickle


with open('news_file.csv', mode='w') as news_file:
            filename = 'finalized_model.sav'
            data = "%s" % (sys.argv[1]) 
            loaded_model = pickle.load(open(filename, 'rb'))
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
predictedfinal = loaded_model.predict(final_testX)
results =  predictedfinal
if results == 1:
    data = "Fake"
else:
    data = "True"

if (data == "True"):
        sent="According To The Fact Checker The News Is:"
        sent2=""
else :
        sent="According To The Fact Checker The News Is:"
        sent2=". We Wont Recommend You Sharing This News Further. But We Would Still Request You To Cross Check The News From An Authentic News Channel."
print(sent + data + sent2) 
os.remove("news_file.csv")
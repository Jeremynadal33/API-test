import random

from fbapp.models import Content
from bs4 import BeautifulSoup
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer # Tfidf
import lightgbm
import numpy as np
import joblib
import re
import os

def find_content():
    contents = Content.query.all()
    print(contents)
    content = random.choice(contents)
    return content.title, content.body, content.tags

pos_from_tag = lambda tag: ('a' if tag[0].lower() == 'j' else tag[0].lower()) if tag[0].lower() in ['n', 'r', 'v'] else 'n'
def _nothing(x):
    return x
def handle_body(text,
                #tokenizer = nltk.RegexpTokenizer(r'\w+'),
                stop_words = nltk.corpus.stopwords.words("english"),
                lemmatizer = nltk.stem.WordNetLemmatizer()  ):

    POS_to_rm = ['RB','RBR','RBS','JJ','JJR','JJS','CD'] #Removing adverbs and adjectives and digits
    stop_words += ['.','€','$','?','\'s',',',':',';','=','+','-']

    soup = BeautifulSoup(text, 'html.parser')
    tokens = nltk.word_tokenize( soup.get_text().lower() )

    tokens = [re.sub('[.,?!)()<>:;\ \"\'\]\[+-=\{\}\|^*@&`’]','',token).replace('\\','').replace('?','') for token in tokens]
    tokens = [token for token in tokens if token != '']
    tags = nltk.pos_tag(tokens)

    tokens = [ tokens[i] for i in range(len(tokens)) if ( (not tokens[i] in stop_words) and (not tags[i][1] in POS_to_rm ) )]

    tags = nltk.pos_tag(tokens)

    result = [lemmatizer.lemmatize(tokens[i], pos=pos_from_tag(tags[i][1])) for i in range(len(tokens))]

    return result

def handle_title(text,
                 stop_words = nltk.corpus.stopwords.words("english"),
                 lemmatizer = nltk.stem.WordNetLemmatizer()  ):

    POS_to_rm = ['RB','RBR','RBS','JJ','JJR','JJS'] #Removing adverbs and adjectives
    stop_words += ['.','€','$','?','\'s',',',':',';','=','+','-']

    tokens = re.split(' ', text.lower())
    tokens = [re.sub('[.,?!)()<>:;\ \"\'\]\[=\{\}\|^*@&`’]','',token).replace('\\','').replace('?','') for token in tokens]

    tokens = [token for token in tokens if token != '']
    tags = nltk.pos_tag(tokens)

    tokens = [ tokens[i] for i in range(len(tokens)) if ( (not tokens[i] in stop_words) and (not tags[i][1] in POS_to_rm ) )]

    tags = nltk.pos_tag(tokens)

    result = [lemmatizer.lemmatize(tokens[i], pos=pos_from_tag(tags[i][1])) for i in range(len(tokens))]

    return result

def preprocess_text(body, title = None):
    body = handle_body(body)
    if title :
        title = handle_title(title)
        body = title + title + body
    return body


def predict_new_sentence(text, vectorizer, model, all_tags, title = None):
    all_tags = np.array(all_tags)
    text = np.array(preprocess_text(text, title=title)).reshape(1, -1)
    text = vectorizer.transform(text)
    pred = model.predict(text)

    assert pred[0].shape == all_tags.shape, 'the passed tags doesnot have same shape as model output'
    idx = [idx for idx in range(len(all_tags)) if pred[0][idx]==1]
    return all_tags[idx]

vectorizer = joblib.load('fbapp/vectorizer_tfidf.bin')
classifier = joblib.load('fbapp/lightgbm_tfidf.bin')
all_tags   = joblib.load('fbapp/unique_tags.bin')

def predict_tags(body, title= ""):
    result = predict_new_sentence(body,vectorizer, classifier, all_tags, title=title)
    return result

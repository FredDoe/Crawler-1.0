__author__:'Godfred Doe'
import pickle
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

data_path = 'C:/workspace/python/analitica_innovare/Crawler/src/models'
# load the dataset
df = pd.read_csv(data_path +'/parsed-news-data.csv')

# Loading the necessary data from the already trained classifier
# tfidf
with open(data_path+'/Pickles/tfidf.pickle', 'rb') as data:
    tfidf = pickle.load(data)

# X_train
with open(data_path+'/Pickles/X_train.pickle', 'rb') as data:
    X_train = pickle.load(data)

# X_test
with open(data_path+'/Pickles/X_test.pickle', 'rb') as data:
    X_test = pickle.load(data)

# y_train
with open(data_path+'/Pickles/y_train.pickle', 'rb') as data:
    y_train = pickle.load(data)

# y_test
with open(data_path+'/Pickles/y_test.pickle', 'rb') as data:
    y_test = pickle.load(data)

# SVM Model
with open(data_path+'/Models/best_svc.pickle', 'rb') as data:
    svc_model = pickle.load(data)

# Category mapping dictionary
category_codes = {
    'business': 0,
    'entertainment': 1,
    'politics': 2,
    'sport': 3,
    'tech': 4
}

category_names = {
    0: 'business',
    1: 'entertainment',
    2: 'politics',
    3: 'sport',
    4: 'tech'
}

punctuation_signs = list("?:!.,;")
stop_words = list(stopwords.words('english'))


def create_features_from_text(text):
    # Dataframe creation
    lemmatized_text_list = []
    dframe = pd.DataFrame(columns=['Content'])
    dframe.loc[0] = text
    dframe['Content_Parsed_1'] = dframe['Content'].str.replace("\r", " ")
    dframe['Content_Parsed_1'] = dframe['Content_Parsed_1'].str.replace("\n", " ")
    dframe['Content_Parsed_1'] = dframe['Content_Parsed_1'].str.replace("    ", " ")
    dframe['Content_Parsed_1'] = dframe['Content_Parsed_1'].str.replace('"', '')
    dframe['Content_Parsed_2'] = dframe['Content_Parsed_1'].str.lower()
    dframe['Content_Parsed_3'] = dframe['Content_Parsed_2']
    for punct_sign in punctuation_signs:
        dframe['Content_Parsed_3'] = dframe['Content_Parsed_3'].str.replace(punct_sign, '')
    dframe['Content_Parsed_4'] = dframe['Content_Parsed_3'].str.replace("'s", "")
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized_list = []
    text = dframe.loc[0]['Content_Parsed_4']
    text_words = text.split(" ")
    for word in text_words:
        lemmatized_list.append(wordnet_lemmatizer.lemmatize(word, pos="v"))
    lemmatized_text = " ".join(lemmatized_list)
    lemmatized_text_list.append(lemmatized_text)
    dframe['Content_Parsed_5'] = lemmatized_text_list
    dframe['Content_Parsed_6'] = dframe['Content_Parsed_5']
    for stop_word in stop_words:
        regex_stopword = r"\b" + stop_word + r"\b"
        dframe['Content_Parsed_6'] = dframe['Content_Parsed_6'].str.replace(regex_stopword, '')
    df = dframe['Content_Parsed_6']
    df = df.rename({'Content_Parsed_6': 'Parsed_Content'}, axis=1)

    # TF-IDF
    features = tfidf.transform(df).toarray()

    return features


def get_category_name(category_id):
    for category, id_ in category_codes.items():
        if id_ == category_id:
            return category


def predict_from_text(text):
    # Predict using the input model
    prediction_svc = svc_model.predict(create_features_from_text(text))[0]
    prediction_svc_proba = svc_model.predict_proba(create_features_from_text(text))[0]

    # Return result
    category_svc = get_category_name(prediction_svc)

    return category_svc, (prediction_svc_proba.max()*100)
    # print("The predicted category using the SVM model is %s." % (category_svc))
    # print("The conditional probability is: %a" % (prediction_svc_proba.max() * 100))

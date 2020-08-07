import re
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit

df = pd.read_csv('C:/HOBBY/python/analitica_innovare/Crawler/src/models/parsed-news-data.csv')

X_train, X_test, y_train, y_test = train_test_split(df['Parsed_Content'],
                                                    df['Category_Code'],
                                                    test_size=0.15,
                                                    random_state=8)

# Parameter selection
ngram_range = (1, 2)
min_df = 10
max_df = 1.
max_features = 300

tfidf = TfidfVectorizer(encoding='utf-8',
                        ngram_range=ngram_range,
                        stop_words=None,
                        lowercase=False,
                        max_df=max_df,
                        min_df=min_df,
                        max_features=max_features,
                        norm='l2',
                        sublinear_tf=True)

features_train = tfidf.fit_transform(X_train).toarray()
labels_train = y_train

features_test = tfidf.transform(X_test).toarray()
labels_test = y_test

# X_train
with open('Pickles/X_train.pickle', 'wb') as output:
    pickle.dump(X_train, output)

# X_test
with open('Pickles/X_test.pickle', 'wb') as output:
    pickle.dump(X_test, output)

# y_train
with open('Pickles/y_train.pickle', 'wb') as output:
    pickle.dump(y_train, output)

# y_test
with open('Pickles/y_test.pickle', 'wb') as output:
    pickle.dump(y_test, output)

# df
with open('Pickles/df.pickle', 'wb') as output:
    pickle.dump(df, output)

# features_train
with open('Pickles/features_train.pickle', 'wb') as output:
    pickle.dump(features_train, output)

# labels_train
with open('Pickles/labels_train.pickle', 'wb') as output:
    pickle.dump(labels_train, output)

# features_test
with open('Pickles/features_test.pickle', 'wb') as output:
    pickle.dump(features_test, output)

# labels_test
with open('Pickles/labels_test.pickle', 'wb') as output:
    pickle.dump(labels_test, output)

# TF-IDF object
with open('Pickles/tfidf.pickle', 'wb') as output:
    pickle.dump(tfidf, output)



#GridSearch
# Create the parameter grid based on the results of random search
C = [.0001, .001, .01, .1]
degree = [3, 4, 5]
gamma = [1, 10, 100]
probability = [True]

param_grid = [
  {'C': C, 'kernel':['linear'], 'probability':probability},
  {'C': C, 'kernel':['poly'], 'degree':degree, 'probability':probability},
  {'C': C, 'kernel':['rbf'], 'gamma':gamma, 'probability':probability}
]

# Create a base model
svc = svm.SVC(random_state=8)

# Manually create the splits in CV in order to be able to fix a random_state (GridSearchCV doesn't have that argument)
cv_sets = ShuffleSplit(n_splits = 3, test_size = .33, random_state = 8)

# Instantiate the grid search model
grid_search = GridSearchCV(estimator=svc,
                           param_grid=param_grid,
                           scoring='accuracy',
                           cv=cv_sets,
                           verbose=1)

# Fit the grid search to the data
grid_search.fit(features_train, labels_train)

best_svc = grid_search.best_estimator_
best_svc = best_svc.fit(features_train, labels_train)
with open('Models/best_svc.pickle', 'wb') as output:
    pickle.dump(best_svc, output)



# Loading the necessary data from the already trained classifier

#tfidf
with open('Pickles/tfidf.pickle', 'rb') as data:
    tfidf = pickle.load(data)

# X_train
with open('Pickles/X_train.pickle', 'rb') as data:
    X_train = pickle.load(data)

# X_test
with open('Pickles/X_test.pickle', 'rb') as data:
    X_test = pickle.load(data)

# y_train
with open('Pickles/y_train.pickle', 'rb') as data:
    y_train = pickle.load(data)

# y_test
with open('Pickles/y_test.pickle', 'rb') as data:
    y_test = pickle.load(data)

# SVM Model
with open('Models/best_svc.pickle', 'rb') as data:
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

    print("The predicted category using the SVM model is %s." % (category_svc))
    print("The conditional probability is: %a" % (prediction_svc_proba.max() * 100))


text0 = """
The center-right party Ciudadanos closed a deal on Wednesday with the support of the conservative Popular Party (PP) to take control of the speaker’s committee in the Andalusian parliament, paving the way for the regional PP leader, Juan Manuel Moreno, to stand as the candidate for premier of the southern Spanish region. The move would see the Socialist Party (PSOE) lose power in the Junta, as the regional government is known, for the first time in 36 years.

Talks in Andalusia have been ongoing since regional polls were held on December 2. The PSOE, led by incumbent premier Susana Díaz, had been expected to win the early elections, but in a shock result the party took the most seats in parliament, 33, but fell well short of a majority of 55. It was their worst result in the region since Spain returned to democracy. The PP came in second, with 26 seats, while Ciudadanos were third with 21. The major surprise was the strong performance of far-right group Vox, which won more than 391,000 votes (10.9%), giving it 12 deputies. The anti-immigration group is the first of its kind to win seats in a Spanish parliament since the end of the Francisco Franco dictatorship. It now holds the key to power in Andalusia, given that its votes, added to those of the PP and Ciudadanos, constitute an absolute majority.

The move would see the Socialist Party lose power in the region for the first time in 36 years

On Thursday, Marta Bosquet of Ciudadanos was voted in as the new speaker of the Andalusian parliament thanks to 59 votes from her party, the PP and Vox. The other candidate, Inmaculada Nieto of Adelante Andalucía, secured 50 votes – from her own party and 33 from the PSOE.

The speaker’s role in the parliament is key for the calling of an investiture vote and for the selection of the candidate for premier.

Officially, the talks as to the make up of a future government have yet to start, but in reality they are well advanced, according to sources from both the PP and Ciudadanos. The leader of the Andalusian PP is banking on being voted into power around January 16 and wants the majority of his Cabinet to be decided “five days before the investiture vote.”

The speaker’s role in the parliament is key for the calling of an investiture vote and for the selection of the candidate for premier

The PP, which was ousted from power by the PSOE in the national government in June, is keen to take the reins of power in Andalusia as soon as possible. The difficulties that Ciudadanos has faced to justify the necessary inclusion of Vox in the talks, has slowed down progress. Rather than align itself with the far right party, the group – which began life in Catalonia in response to the independence drive, but soon launched onto the national stage – had sought a deal with Adelante Andalucía.

Wednesday was a day of intense talks among the parties in a bid to find a solution that would keep everyone happy. But at 9pm last night, Adelante Andalucía announced that it would not be part of “any deal” and that would instead vote for its own candidates to the speaker’s committee in order to “face up to the right wing and the extreme right.”

The PSOE, meanwhile, argues that having won the elections with a seven-seat lead over the PP gives it the legitimacy to aspire to the control of the regional government and the parliament, and to maintain its positions on the speaker’s committee.

"""
predict_from_text(text0)


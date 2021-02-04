import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import re #regex applies a regular expression to a string and returns the matching substrings.
import nltk
import nltk.corpus
from nltk.corpus import stopwords

# Uncomment if you to download these datasets
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
import string
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize

"""
    Ce package contient des méthodes pour préparer les données textuelles
        Appeler **clean_dataframe** pour nettoyer vos données
"""

def clean_dataframe(df:pd.DataFrame, column="text", show_progress=False):
    """
        Nettoyer une colonne contenant du texte dans un df

        Params:
            * df: dataframe contenant les les données à modifier
            * column: colonne sur laquelle le traitement s"effectura
            * show_progress: afficher la progression du nettoyage des données.
        Returns:
            DataFrame avec des colonnes : [column, "text_clean"]
    """
    data = df.copy()
    columns = list(df.columns)
    _progress("unidecode", show_progress)
    data[column] = data[column].apply(lambda x: unidecode_text(x))
    
    _progress("clean_text", show_progress)
    data = clean_text(data, text_field=column)
    
    _progress("word_tokenize", show_progress)
    data = word_tokenize_text(data)
    
    _progress("word_stemmer", show_progress)
    data = word_stemmer_text(data)
    
    _progress("word_lemmatizer", show_progress)
    data = word_lemmatizer_text(data)
    
    _progress("remove_extra", show_progress)
    data = remove_extra(data)
    return data[columns+["text_clean"]]

def _progress(text, show_progress):
    """
        Afficher la progression lors du nettoyage des données
    """
    if show_progress:
        print(text)

# 1
def unidecode_text(text):
    return text.lower()

# 2
def clean_text(df:pd.DataFrame, text_field='text', new_text_field_name='text_clean'):
    """
        Nettoyer du texte. Extraire les mot et chiffres
    """
    df[new_text_field_name] = df[text_field].str.lower() #Convert strings in the Series/Index to lowercase.
    df[new_text_field_name] = df[new_text_field_name].apply(lambda elem: re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", elem)) 
    df[new_text_field_name] = df[new_text_field_name].apply(lambda elem: re.sub(r"\d+", "", elem))
    
    return df

# 3
def word_tokenize_text(data_clean:pd.DataFrame, text_field='text_clean', new_text_field_name='text_tokens'):
    data_clean[new_text_field_name] = data_clean[text_field].apply(lambda x: word_tokenize(x))
    return data_clean

# 4
def word_stemmer_text(data_clean:pd.DataFrame, text_field='text_tokens', new_text_field_name='text_tokens'):
    pstem = PorterStemmer()
    data_clean[new_text_field_name] = data_clean[text_field].apply(lambda x: [pstem.stem(i) for i in x])
    return data_clean

# 5
def word_lemmatizer_text(data_clean, text_field='text_tokens', new_text_field_name='text_tokens'):
    wlem = WordNetLemmatizer()
    data_clean[text_field] = data_clean[new_text_field_name].apply(lambda x: [wlem.lemmatize(i) for i in x])
    return data_clean

# 6
def _remove_extra(text):
    url = re.compile(r'https?://\S+|www\.\S+')
    text = url.sub(r'', text)
    
    html = re.compile(r'<.*?>')
    text = html.sub(r'',text)
    
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    
    table = str.maketrans('','',string.punctuation)
    return text.translate(table)

# 7
def remove_extra(data_clean, text_field='text_tokens', new_text_field_name='text_clean'):
    data_clean[new_text_field_name] = data_clean[text_field].apply(lambda x: " ".join(x))
    data_clean[new_text_field_name] = data_clean[new_text_field_name].apply(lambda x: _remove_extra(x))
    return data_clean
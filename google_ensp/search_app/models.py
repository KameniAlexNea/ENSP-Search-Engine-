# from django.db import models
import pandas as pd
import numpy as np
import os
import ml_models.tools.models as m
import glob
import requests
import pickle as pkl


# Create your models here.

class EngineModel():
    def __init__(self, model_folder="./ml_models/sauvegarde/"):
        self.headers = { 
            "apikey": "60e07650-2df1-11eb-96e2-bf23fa38d811"
        }
        self.params = None
        self.response = None
        self.base_url = 'https://app.zenserp.com/api/v2/'
        self.columns = ["url", "title", "description", "destination"]
        self.data = None
        self.data_clean = None
        self.lr = None
        self.xgb = None
        self.vectoriser = None
        self._read(model_folder)
    
    def _read(self, model_folder="./ml_models/sauvegarde/"):
        """
            Charger les modèles de machine de learning pour la classification
        """
        with open(model_folder+"model_lr.pkl", "rb") as file:
            self.lr = pkl.load(file) # Model Logistique
        with open(model_folder+"model_xgboost.pkl", "rb") as file:
            self.xgb = pkl.load(file) # Model XGBoost
        with open(model_folder+"tfidf.pkl", "rb") as file:
            self.vectoriser = pkl.load(file) # Model Vectoriser

    def clean_text(self, question:str, answers:pd.DataFrame, column="description"):
        """
            Nettoyer les données obtenues de la requête et de l'API de recherche
            Params:
                - question: requete envoyé par l'apprenant
                - answers: liste des résultats envoyés par la première couche (moteur de recherche)
                    - devrait contenir la colonne **column**: default snippet
            Return:
                res: pd.Series
                     Series de [requete & reponses] nettoyées dans 'text_clean'
        """
        reponses = pd.DataFrame(answers[column].values, columns=["text"])
        query = pd.DataFrame(np.array([question]), columns=["text"])
        self.data_clean = m.clean_dataframe(reponses)
        self.query = m.clean_dataframe(query)
        return self.data_clean.copy()
    
    def classify_base_on_bloom(self, query_clean, data_clean, column="text_clean"):
        """
            Classifier la requete ainsi que le jeu de données d'entrainement
        """
        query_vect = self.vectoriser.transform(query_clean[column])
        query_prob = (self.lr.predict_proba(query_vect)+self.xgb.predict_proba(query_vect))/2

        data_vect = data_clean[column].apply(lambda x: self.vectoriser.transform(x))
        data_prob = data_vect.apply(lambda x: (self.lr.predict_proba(x)+self.xgb.predict_proba(x))/2)
        return query_prob, data_prob
    

    
    def _fetch_exemples(self, path="./ml_models/exemple/queries.txt", save_to="./ml_models/exemple/", count=70):
        """
            Fouiller les résultats pertinents des requêtes contenues dans path
        """
        questions = None
        with open(path, 'rb') as file:
            questions = file.readlines()
        for i, question in enumerate(questions):
            _, data = self._fetch_data(question)
            data.to_csv(save_to+"query{}.csv".format(i), index=False, header=True)

    def _fetch_data(self, query=None, count=70):
        """
            Chercher du contenu éducatif sur internet
            Params:
                - query: requête à transmettre au moteur de recherche
            Return:
                question, answers
                    - question: str
                    - answers: pd.DataFrame: ["url", "title", "description", "destination"]
        """
        if query is None:
            return self._fetch_data_offline()
        self.params = (
            ("q", query),
            ("num", str(count)),
        )
        self.query = query
        self.response = requests.get(self.base_url+"search", headers=self.headers, params=self.params)
        self.data = pd.DataFrame(self.response.json()["organic"])
        return query, self.data[self.columns].copy()

    def _fetch_data_offline(self, path='./ml_models/exemple/query*.csv', queries_path='./ml_models/exemple/queries.txt'):
        """
            Appliquer les différents modèles sur des données en local
            Params:
                path: chemin contenant les différents fichier .csv
                le choix d'une des requêtes du fichier se fait aléatoirement
            Returns:
                DataFrame de resultat ainsi que la requête transmise
                question, answers
                    - question: str
                    - answers: pd.DataFrame: [link, title, snippet]
        """
        np.random.seed()
        exemples = glob.glob(path)
        if len(exemples) == 0:
            raise Exception("No queries examples found in {}".format(path))
        path_queries_index = np.random.choice(range(len(exemples)))
        self.data = pd.read_csv(exemples[path_queries_index])
        with open(queries_path, 'rb') as file:
            self.query = file.readlines()[path_queries_index]
        return self.query, self.data.copy()


class Result(models.Model):

    def __init__(self, row, link, title, summary, bloom_type, score, query_class):
        self.link = link
        self.title = title
        self.summary = summary
        self.bloom_type = bloom_type
        self.score = score
        self.query_class = query_class
        self.row = row

    def __str__(self):
        return self.title

    @classmethod
    def fromEngineResult(cls, row, data):
        return cls(row, data[0], data[1], data[2], data[3], data[4], data[5])

    @staticmethod
    def createResults(df: pd.DataFrame):
        results = np.array([
            Result.fromEngineResult(row, data) for row, data in df.iterrows()
        ])
        return results

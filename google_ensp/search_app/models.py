from django.db import models
import pandas as pd
import numpy as np
import os
from search_app.ml_models.tools import models as m
import glob
import requests
import pickle as pkl


# Create your models here.

class EngineModel():
    def __init__(self, model_folder="./search_app/ml_models/sauvegarde/"):
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
    
    def _read(self, model_folder="./search_app/search_app/search_app/ml_models/sauvegarde/"):
        """
            Charger les modèles de machine de learning pour la classification
        """
        with open(model_folder+"linear_reg.pkl", "rb") as file:
            self.lr = pkl.load(file) # Model Logistique
        with open(model_folder+"xgboost.pkl", "rb") as file:
            self.xgb = pkl.load(file) # Model XGBoost
        with open(model_folder+"tfid2.pkl", "rb") as file:
            self.vectoriser = pkl.load(file) # Model Vectoriser
    
    def search(self, query, count=70, local=True):
        if local:
            qr, dt = self._fetch_data_offline()
        else:
            qr, dt = self._fetch_data(query, count)
        qr_cl, dt_cl = self._clean_text(query, dt)
        qr_pb, dt_pb = self._classify_base_on_bloom(qr_cl, dt_cl)
        return (qr, dt), (qr_pb, dt_pb), self.lr.classes_


    def _clean_text(self, question:str, answers:pd.DataFrame, column="description"):
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
        return self.query, self.data_clean.copy()
    
    def _classify_base_on_bloom(self, query_clean, data_clean, column="text_clean"):
        """
            Classifier la requete ainsi que le jeu de données d'entrainement
        """
        query_vect = self.vectoriser.transform(query_clean[column].values)
        query_prob = (self.lr.predict_proba(query_vect)+self.xgb.predict_proba(query_vect))/2
        query_prob = pd.DataFrame(query_prob, columns=self.lr.classes_)

        data_vect = self.vectoriser.transform(data_clean[column].values)
        data_prob = (self.lr.predict_proba(data_vect) + self.xgb.predict_proba(data_vect))/2
        data_prob = pd.DataFrame(np.array(data_prob.reshape(-1, 6)), columns=self.lr.classes_)
        print('Shape', data_prob.shape)
        return query_prob, data_prob
    

    
    def _fetch_exemples(self, path="./search_app/ml_models/exemple/queries.txt", save_to="./search_app/ml_models/exemple/", count=70):
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

    def _fetch_data_offline(self, path='./search_app/ml_models/exemple/query*.csv', queries_path='./search_app/ml_models/exemple/queries.txt'):
        """
            Appliquer les différents modèles sur des données en local
            Params:
                path: chemin contenant les différents fichier .csv
                le choix d'une des requêtes du fichier se fait aléatoirement
            Returns:
                DataFrame de resultat ainsi que la requête transmise
                question, answers
                    - question: str
                    - answers: pd.DataFrame: ["url", "title", "description", "destination"]
        """
        np.random.seed()
        exemples = glob.glob(path)
        if len(exemples) == 0:
            self._fetch_exemples()
            exemples = glob.glob(path)
            # raise Exception("No queries examples found in {}".format(path))
        path_queries_index = np.random.choice(range(len(exemples)))
        self.data = pd.read_csv(exemples[path_queries_index])
        with open(queries_path, 'rb') as file:
            self.query = file.readlines()[path_queries_index]
        return self.query, self.data.copy()


class Result(models.Model):

    def __init__(self, row, url, title, description, destination, bloom_type):
        self.row = row
        self.url = url
        self.title = title
        self.description = description
        self.destination = destination

        self.bloom_type = bloom_type

    def __str__(self):
        return self.title

    @classmethod
    def fromEngineResult(cls, row, data):
        """
            ["url", "title", "description", "destination"]
        """
        return cls(row, data["url"], data["title"], data["description"], data["destination"], " ".join(np.array(data["bloom"], dtype=np.str)))

    @staticmethod
    def createResults(df: pd.DataFrame):
        results = np.array([
            Result.fromEngineResult(row, data) for row, data in df.iterrows()
        ])
        return results

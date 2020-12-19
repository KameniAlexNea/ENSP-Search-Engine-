# from django.db import models
import pandas as pd
import numpy as np
import os
import ml_models.tools.models as m
import glob
import requests



# Create your models here.

class EngineModel():
    def __init__(self,):
        self.headers = { 
            "apikey": "60e07650-2df1-11eb-96e2-bf23fa38d811"
        }
        self.params = None
        self.response = None
        self.base_url = 'https://app.zenserp.com/api/v2/'
        self.columns = ["url", "title", "description", "destination"]

    def clean_text(self, question:str, answers:pd.DataFrame, column="snippet"):
        """
            Nettoyer les données obtenues de la requête et de l'API de recherche
            Params:
                - question: requete envoyé par l'apprenant
                - answers: liste des résultats envoyés par la première couche (moteur de recherche)
                    - devrait contenir la colonne **column**: default snippet
            Return:
                res: pd.Series
                     Series de [requete & reponses] nettoyées
        """
        data = pd.DataFrame(np.append([question], answers[column].values), columns=["text"])
        data = m.clean_dataframe(data)
        return data
    
    def _fetch_exemples(self, path="./ml_models/exemple/queries.txt", save_to="./ml_models/exemple/", count=70):
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




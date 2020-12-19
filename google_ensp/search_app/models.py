# from django.db import models
import pandas as pd
import numpy as np
import os
import ml_models.tools.models as m
import glob

# Create your models here.

class EngineModel():
    def __init__(self,):
        pass

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

    def _fetch_data(self, query):
        """
            Chercher du contenu éducatif sur internet
            Params:
                - query: requête à transmettre au moteur de recherche
            Return:
                question, answers
                    - question: str
                    - answers: pd.DataFrame: [link, title, snippet]
        """
        pass

    def _fetch_data_offline(self, path='./ml_models/exemple/*.csv'):
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
        choice = np.random.choice(exemples)
        data = pd.read_csv(choice)
        return data




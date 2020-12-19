# ENSP-Search-Engine

## Compréhension des tâches de l'utilisateur

Projet Django de compréhension des taches de l'utilisateur

Il est construit tel que suit
* **Module notebook**: ce module contient les différents résultats des modèles machines Learning utilisés lors de la modélisation de la compréhension d'un utilisateur

* **Module output**: contient les sorties d'exécution des modèles machine Learning
    * verbs/: contient les différents verbes de la taxonomie de Bloom's
    * queries_df.csv: contient une liste de requêtes chacune classée dans un niveau. Contient environ 190.000 requêtes

* **Module sauvegarde**: liste des modèles machine learning pertients sauvegardé
* **Module tools**: contient les différents helpers pour l'élaboration des modèles machine Learning

## Installation et initialisation du projet
Ici on suppose que vous disposez de la version complète de Anaconda sur votre machine. Les étapes ci après partent de là

* Créer un environnement virtuel python sur votre machine: (pensez à ajouter conda à votre variable d'environnement) 
> conda create django 
* Activer l'environnement crée: 
> conda activate django
* Installer les différents packages listés dans le fichier : requirements.txt. Bon nombre de ces packages sont contenus dans l'installation de conda:
> conda install requirements.txt

ou 
> pip install requirements.txt
* Installer le dataset de nltk
> nltk.download()


## Lancer le projet

> python manage.py runserver

Entrer l'adresse qui s'affiche dans votre console, dans votre navigateur en ajoutant **search_app/**


**Note** consulter gitignore pour savoir quels sont les fichiers exclus du projet en ligne. M'envoyer un message à mon adresse pour avoir ses fichiers

**Bonne navigation**
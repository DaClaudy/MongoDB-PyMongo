# MongoDB-PyMongo

Base de données NoSQL : Interroger MongoDB avec PyMongo

## Description (`mongo_manager.py`)

Ce projet utilise MongoDB pour gérer les données et se connecte à une instance MongoDB via la bibliothèque PyMongo. Il vous permet de gérer des bases de données, des collections et d'effectuer des opérations courantes sur MongoDB.

### Fonctionnalités

- Connexion sécurisée à MongoDB Atlas via PyMongo.
- Liste des bases de données disponibles.
- Liste des collections dans une base de données spécifique.
- Sélection et manipulation de collections.
- Fermeture de la connexion à la base de données.

## Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/DaClaudy/MongoDB-PyMongo.git
   cd MongoDB-PyMongo
   ```

2. **Créer et activer un environnement virtuel** (facultatif mais recommandé) :
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Créez un fichier `.env` à la racine du projet contenant votre URI MongoDB Atlas :
```env
MONGODB_URI="your_mongodb_connection_string"
```

## Technologies

- **Python** : 3.11.5
- **MongoDB Atlas** : hébergement cloud
- **MongoDB Compass** : interface graphique pour visualiser les données
- **PyMongo** : client Python officiel pour MongoDB
- **dotenv** : pour sécuriser la chaîne de connexion

---

## Exercices réalisés

### Exercice 1 - Insertion de documents

- Insertion de livres dans une collection `livre`.
- Utilisation de la méthode `insert_many`.

### Exercice 2 - Requêtes simples

- Trouver tous les livres d'un auteur.
- Rechercher par année ou par genre.
- Trier les livres selon l’année ou le titre.
- Supprimer un document par titre.

### Exercice 3 - Contraintes et index

- Création d’un index unique sur le champ `titre`.
- Gestion des doublons avec `BulkWriteError`.

### Exercice 4 - Modification de documents

- Mise à jour du nom et des coordonnées d’une ville.
- Ajout de champs (`population`, etc.).
- Modification et suppression d’éléments dans des tableaux (`tags`).

### Exercice 5 - Requêtes avancées

- Filtrage par note, date de création, nombre de votes.
- Recherche de magasins par catégories ou produits spécifiques.
- Recherche géospatiale : trouver le magasin le plus proche.

### Exercice 6 - Création de vues

- Création d’une vue filtrée sur les magasins ayant une note ≥ 75.
- Affichage des résultats de cette vue.

### Exercice 7 - Agrégations

**Agrégation 1 :**
- Filtrage par catégorie (`Fruit`), regroupement par couleur, tri et limite des résultats.

**Agrégation 2 :**
- Sélection des documents selon le prix, regroupement par catégorie, somme des quantités et moyenne des prix.

**Agrégation 3 :**
- Calcul de la moyenne des prix par catégorie.
- Mise à jour des documents avec un champ `prix_moyen`.

---

## Structure du projet

```
MongoDB-PyMongo/
│
├── mongo_manager.py
├── exercices.py
├── .env
├── requirements.txt
└── README.md
```

---

## Auteur

Damigou BOUNDJA  
Étudiante en Data Science & IA


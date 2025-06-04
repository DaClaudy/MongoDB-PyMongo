from mongo_manager import MongoManager
from dotenv import load_dotenv
from pymongo.errors import BulkWriteError
import os

load_dotenv()

uri = os.getenv("MONGO_URI")

# Connexion
mongo_manager = MongoManager(uri)
mongo_manager.db = "exercice"

# --------------------------------------------------------
# Exercice 1 : Composition de requêtes simples
# --------------------------------------------------------

def exercice_1(collection_name):
    collection = mongo_manager.db[collection_name]

    # 2. Afficher les jeux 3DS sortis
    games_3ds = collection.read_many_documents({"Platform": "3DS"})
    print("\nJeux 3DS :", games_3ds)

    # 3. Afficher les jeux 3DS sortis en 2011
    games_3ds_2011 = collection.read_many_documents({
        "Platform": "3DS",
        "Year": "2011"
    })
    print("\nJeux 3DS sortis en 2011 :", games_3ds_2011)

    # 4. Afficher le nom et le global_sales des jeux 3DS sortis en 2011
    games_3ds_2011_projection = collection.find(
        {"Platform": "3DS", "Year": "2011"},
        {"_id": 0, "Name": 1, "Global_Sales": 1}
    ).limit(5)
    print("\nNom + ventes globales (3DS - 2011) :", list(games_3ds_2011_projection))

    # 5. Afficher le nom et le global_sales des 3 jeux les plus vendus sur 3DS en 2011
    top3_sales_3ds_2011 = collection.find(
        {"Platform": "3DS", "Year": "2011"},
        {"_id": 0, "Name": 1, "Global_Sales": 1}
    ).sort("Global_Sales", -1).limit(3)
    print("\nTop 3 ventes globales (3DS - 2011) :", list(top3_sales_3ds_2011))


# --------------------------------------------------------
# Exercice 2 : Insertion et validation des données
# --------------------------------------------------------

def exercice_2(collection_name):
    collection = mongo_manager.db[collection_name]

    livres = [
        {"titre": "Harry Potter à l'école des sorciers", "auteur": "J. K. Rowling", "annee": 2001, "genre": "Fantasy"},
        {"titre": "Harry Potter et la chambre des secrets", "auteur": "J. K. Rowling", "annee": 2002, "genre": "Fantasy"},
        {"titre": "Livre vieux", "auteur": "Auteur inconnu", "annee": 1800},  # insertion invalide car annee < 1901
        {"titre": "Harry Potter à l'école des sorciers", "auteur": "Copycat", "annee": 2012, "genre": "Fantasy"}  # Doublon (index unique)
    ]

    try:
        collection.insert_many(livres, ordered=False)  # insérer les lignes valides
        print("\nInsertion réussie")
    except Exception as e:
        print("\nErreur lors de l'insertion des documents :")
        print(e)

# --------------------------------------------------------
# Exercice 3 : Scénario avec insertions et suppressions
# --------------------------------------------------------

def exercice_3(collection_name):
    collection = mongo_manager.db[collection_name]

    # 1. Insérer plusieurs livres
    livres = [
        {"titre": "Harry Potter à l'école des sorciers", "auteur": "J. K. Rowling", "annee": 2001, "genre": "Fantasy"},
        {"titre": "Harry Potter et la chambre des secrets", "auteur": "J. K. Rowling", "annee": 2002, "genre": "Fantasy"},
        {"titre": "Le Seigneur des Anneaux", "auteur": "J. R. R. Tolkien", "annee": 1954, "genre": "Fantasy"},
        {"titre": "1984", "auteur": "George Orwell", "annee": 1949, "genre": "Dystopie"},
        {"titre": "Livre test à supprimer", "auteur": "Test Auteur", "annee": 2005}
    ]
    try:
        collection.insert_many(livres, ordered=False)
        print("Livres insérés avec succès.")
    except BulkWriteError as bwe:
        print("Certains documents existent déjà (erreurs ignorées) :")
        for error in bwe.details["writeErrors"]:
            print(f"- {error['errmsg']}")


    # 2. Supprimer un livre spécifique par son titre
    delete_result = collection.delete_one({"titre": "Livre test à supprimer"})
    print(f"{delete_result.deleted_count} livre supprimé par titre.")

    # 3. Supprimer tous les livres de J. K. Rowling
    delete_jkr = collection.delete_many({"auteur": "J. K. Rowling"})
    print(f"{delete_jkr.deleted_count} livres de J. K. Rowling supprimés.")

# --------------------------------------------------------
# Exercice 4 : Modification de tableaux
# --------------------------------------------------------

def exercice_4(collection_name):
    collection = mongo_manager.db[collection_name]

    # --------------------------
    # Question 1 - Modifications simples
    # --------------------------

    # 1. Modifier le nom d'une ville
    result_update_name = collection.update_one(
        {"city_name": "Bourges"},
        {"$set": {"city_name": "Bourges-sur-Cher"}}
    )
    print(f"{result_update_name.modified_count} document modifié (nom de ville).")

    # 2. Ajuster les coordonnées de Lyon
    result_update_coords = collection.update_one(
        {"city_name": "Lyon"},
        {"$set": {"coordinates": [4.8357, 45.7640]}}
    )
    print(f"{result_update_coords.modified_count} document modifié (coordonnées de Lyon).")

    # 3. Ajouter le champ population à Lyon
    result_add_population = collection.update_one(
        {"city_name": "Lyon"},
        {"$set": {"population": 522000}}
    )
    print(f"{result_add_population.modified_count} document modifié (population de Lyon).")

    # --------------------------
    # Question 2 - Manipulation de tableaux
    # --------------------------

    # 4. Ajouter plusieurs éléments aux tags de tous les documents
    result_add_tags = collection.update_many(
        {},
        {"$addToSet": {"tags": {"$each": ["historique", "touristique"]}}}
    )
    print(f"{result_add_tags.modified_count} documents mis à jour (ajout tags).")

    # 5. Supprimer un élément spécifique de tous les tags
    result_remove_tag = collection.update_many(
        {},
        {"$pull": {"tags": "ancien"}}
    )
    print(f"{result_remove_tag.modified_count} documents mis à jour (suppression tag 'ancien').")

    # 6. Supprimer le premier élément des tags pour Bourges
    result_pop_first_tag = collection.update_one(
        {"city_name": "Bourges-sur-Cher"},
        {"$pop": {"tags": -1}}  # -1 = début du tableau, 1 = fin
    )
    print(f"{result_pop_first_tag.modified_count} document modifié (pop premier tag de Bourges).")

    # 7. Supprimer tous les tags d’un document (ex : Lyon)
    result_unset_tags = collection.update_one(
        {"city_name": "Lyon"},
        {"$unset": {"tags": ""}}
    )
    print(f"{result_unset_tags.modified_count} document modifié (tags supprimés pour Lyon).")

# --------------------------------------------------------
# Exercice 5 : Composition de requêtes avancées
# --------------------------------------------------------

def exercice_5(collection_name):
    collection = mongo_manager.db[collection_name]

    print("\n--- Partie 1 ---")

    # 1. Le magasin le moins bien noté
    worst_shop = collection.find_one(sort=[("rate", 1)])
    print("Magasin le moins bien noté :", worst_shop)

    # 2. Le magasin le plus ancien
    oldest_shop = collection.find_one(sort=[("createdAt", 1)])
    print("Magasin le plus ancien :", oldest_shop)

    # 3. Magasins avec une note entre 50 et 80 inclus
    shops_50_80 = list(collection.find({"rate": {"$gte": 50, "$lte": 80}}))
    print(f"{len(shops_50_80)} magasins ont une note entre 50 et 80.")

    # 4. Magasins créés en 2023
    shops_2023 = list(collection.find({
        "createdAt": {
            "$gte": "2023-01-01",
            "$lt": "2024-01-01"
        }
    }))
    print(f"{len(shops_2023)} magasins créés en 2023.")

    print("\n--- Partie 2 ---")

    # 5. Magasins sans catégorie
    shops_no_category = list(collection.find({
        "$or": [{"category": {"$exists": False}}, {"category": None}]
    }))
    print(f"{len(shops_no_category)} magasins sans catégorie.")

    # 6. Magasins avec une note > 75
    shops_gt_75 = list(collection.find({"rate": {"$gt": 75}}))
    print(f"{len(shops_gt_75)} magasins avec une note > 75.")

    # 7. Magasins avec plus de 50 votes et une note > 60
    shops_votes_note = list(collection.find({
        "votes": {"$gt": 50},
        "rate": {"$gt": 60}
    }))
    print(f"{len(shops_votes_note)} magasins avec votes >50 et rate >60.")

    print("\n--- Défi ---")

    # 8. Magasins avec 'Google' dans le nom
    shops_google = list(collection.find({"name": {"$regex": "google", "$options": "i"}}))
    print(f"{len(shops_google)} magasins liés à Google.")

    # 9. Magasin le plus proche d’un point
    user_point = [50.12, 10.45]

    # S'assurer que l’index géospatial est bien créé
    collection.create_index([("location", "2dsphere")])

    closest_shop = collection.find_one({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": user_point
                }
            }
        }
    })
    print("Magasin le plus proche :", closest_shop)

# --------------------------------------------------------
# Exercice 6 : Création d'une vue
# --------------------------------------------------------

def exercice_6():
    db = mongo_manager.db

    # Supprimer la vue si elle existe déjà
    db.drop_collection("magasins_bien_notes")

    # Création de la vue
    db.command({
        "create": "magasins_bien_notes",
        "viewOn": "magasins",
        "pipeline": [
            {"$match": {"rate": {"$gte": 75}}}
        ]
    })
    print("Vue 'magasins_bien_notes' créée.")

    # Affichage des documents de la vue
    view_docs = list(db["magasins_bien_notes"].find())
    print(f"Magasins notés à 75 ou plus ({len(view_docs)} résultats) :")
    for magasin in view_docs:
        print(magasin)

# --------------------------------------------------------
# Exercice 7 : Exercice d'aggregation
# --------------------------------------------------------

def aggregation_exercice_1():
    collection = mongo_manager.db["fruits_vegetables"]

    pipeline = [
        {"$match": {"category": "Fruit"}},
        {"$group": {"_id": "$color", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]

    results = list(collection.aggregate(pipeline))
    print("Top 5 couleurs de fruits :")
    for r in results:
        print(r)

def aggregation_exercice_2():
    collection = mongo_manager.db["fruits_vegetables"]

    pipeline = [
        {"$match": {"price": {"$gte": 1.00}}},
        {"$group": {
            "_id": "$category",
            "total_quantity": {"$sum": "$quantity"},
            "avg_price": {"$avg": "$price"}
        }},
        {"$sort": {"total_quantity": -1}}
    ]

    results = list(collection.aggregate(pipeline))
    print("Statistiques par catégorie (prix ≥ 1 €) :")
    for r in results:
        print(r)

def aggregation_exercice_3():
    collection = mongo_manager.db["fruits_vegetables"]

    # Calculer la moyenne des prix par catégorie
    moyennes = list(collection.aggregate([
        {"$group": {"_id": "$category", "avg_price": {"$avg": "$price"}}}
    ]))

    # Mise à jour des documents avec le champ 'avg_price'
    for m in moyennes:
        collection.update_many(
            {"category": m["_id"]},
            {"$set": {"avg_price": round(m["avg_price"], 2)}}
        )

    print("Mise à jour avec 'avg_price' réussie.")
   



if __name__ == "__main__":
    #exercice_1("console_games")
    #exercice_2("livre")
    #exercice_3("livre")
    #exercice_4("city")
    #exercice_5("magasins")
    #exercice_6()
    #aggregation_exercice_1()
    #aggregation_exercice_2()
    aggregation_exercice_3()

    mongo_manager.close_connection()
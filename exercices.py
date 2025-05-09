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

   



if __name__ == "__main__":
    #exercice_1("console_games")
    #exercice_2("livre")
    exercice_3("livre")

    mongo_manager.close_connection()
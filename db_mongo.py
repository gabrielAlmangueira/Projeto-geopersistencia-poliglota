from pymongo import MongoClient

def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["geodatabase"]
    return db

def create_collection():
    db = connect_mongo()
    if "locais" not in db.list_collection_names():
        db.create_collection("locais")

def insert_local(nome_local, cidade, latitude, longitude, descricao):
    db = connect_mongo()
    local = {
        "nome_local": nome_local,
        "cidade": cidade,
        "coordenadas": {
            "latitude": latitude,
            "longitude": longitude
        },
        "descricao": descricao
    }
    db.locais.insert_one(local)

def query_locais():
    db = connect_mongo()
    return list(db.locais.find())
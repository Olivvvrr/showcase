import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime

# Carregar variáveis do arquivo .env
load_dotenv()

# Conectar ao MongoDB usando a URI do .env
mongo_uri = os.getenv("MONGO_URI")

def connect_mongo():
    try:
        # Conectar ao MongoDB
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # Timeout de 5 segundos
        db = client["UserAnalyticsCluster"]
        if db is not None:
            return db
        else:
            raise Exception("Conexão com o MongoDB falhou.")
        
    except PyMongoError as err:
        print(f"Erro ao conectar ao MongoDB: {err}")
        return None
    
# função para registrar uma interação no MongoDB
def log_interation(button_clicked): 
    db = connect_mongo()
    if db is not None:
        interactions_collection = db["interactions"] # nome da coleção
        
        # dados da interação
        interaction = {
            "button": button_clicked,
            "timestamp": datetime.now(),
            "user_ip": "127.0.0.1" # tentar capturar o UF mais tarde
        }
        
        # inserir a interação no MongoDB
        result = interactions_collection.insert_one(interaction)
        print(f"Interação registrada com sucesso! ID da interação: {result.inserted_id}")
    else:
        print("Não foi possivel registrar a interação devido a erro na conexão.")
        
# testar o registro de uma interação

if __name__ == "__main__":
    button = input("Digite o nome do botão clicado: ")
    log_interation(button)
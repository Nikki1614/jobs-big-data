import pandas as pd
from pymongo import MongoClient
import json

MONGO_URI = "mongodb+srv://nikkiawa:VxgtPCustn1YzcHP@cluster0.8uier.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "kaggle"
COLLECTION_NAME = "trabajos"


df = pd.read_csv("eda_dataset.csv")

# Columna innecesaria
df.drop(columns=["Unnamed: 0"], inplace=True)

# Convertir binarios a booleanos
binary_cols = ["python_yn", "R_yn", "spark", "aws", "excel", "same_state"]
for col in binary_cols:
    df[col] = df[col].astype(bool)


df = df.where(pd.notnull(df), None)
df.head()
records = df.to_dict(orient='records')

# MONGO
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Eliminar documentos anteriores
    collection.delete_many({})
    collection.insert_many(records)

    print(f"{len(records)} registros insertados en MongoDB Atlas.")
except Exception as e:
    print(f"Error al conectar o insertar: {e}")


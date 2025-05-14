import streamlit as st
import pandas as pd
from pymongo import MongoClient

# MONGO 
MONGO_URI = "mongodb+srv://nikkiawa:VxgtPCustn1YzcHP@cluster0.8uier.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "kaggle"
COLLECTION_NAME = "trabajos"



@st.cache_data
def cargar_datos():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    data = list(collection.find({}, {"_id": 0}))  # Excluir el campo _id
    return pd.DataFrame(data)

# DASHBOARD 
st.title("Empleos Glassdoor")

df = cargar_datos()
st.sidebar.header("Filtros")
estado = st.sidebar.selectbox("Filtrar por estado", ["Todos"] + sorted(df["job_state"].dropna().unique().tolist()))
seniority = st.sidebar.selectbox("Filtrar por seniority", ["Todos"] + sorted(df["seniority"].dropna().unique().tolist()))

if estado != "Todos":
    df = df[df["job_state"] == estado]

if seniority != "Todos":
    df = df[df["seniority"] == seniority]


st.metric("Promedio Salarial", f"${df['avg_salary'].mean():,.2f}")
st.metric("Cantidad de trabajos", len(df))

#Graficos
st.subheader("Distribución de salarios")
st.bar_chart(df["avg_salary"])

st.subheader("Frecuencia por rol simplificado")
st.bar_chart(df["job_simp"].value_counts())

st.subheader("Herramientas más requeridas")
tools = {
    "Python": df["python_yn"].sum(),
    "R": df["R_yn"].sum(),
    "Spark": df["spark"].sum(),
    "AWS": df["aws"].sum(),
    "Excel": df["excel"].sum()
}
st.bar_chart(pd.Series(tools))


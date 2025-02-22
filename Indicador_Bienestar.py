import streamlit as st
import pandas as pd
import sqlite3
import requests

# URL del archivo SQL en GitHub
GITHUB_SQL_URL = "https://raw.githubusercontent.com/JuanMIRANDA796/INDICADOR_BIENESTAR/main/mi_base_de_datos.sql"

# Descargar el archivo SQL
response = requests.get(GITHUB_SQL_URL)
with open('mi_base_de_datos.sql', 'wb') as file:
    file.write(response.content)

# Conectar a la base de datos SQLite
conn = sqlite3.connect('mi_base_de_datos.db')
cursor = conn.cursor()

# Ejecutar el script SQL para crear la base de datos y las tablas
with open('mi_base_de_datos.sql', 'r', encoding='utf-8') as sql_file:
    sql_script = sql_file.read()
cursor.executescript(sql_script)
conn.commit()

# Leer los datos de la tabla SQL
df = pd.read_sql_query("SELECT * FROM mi_tabla", conn)

# Mostrar el DataFrame en Streamlit
st.write(df)

# Cerrar la conexión
conn.close()


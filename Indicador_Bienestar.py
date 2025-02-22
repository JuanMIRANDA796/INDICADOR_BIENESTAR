import streamlit as st
import pandas as pd
import sqlite3
import requests

# URL del archivo SQL en GitHub
GITHUB_SQL_URL = "https://raw.githubusercontent.com/JuanMIRANDA796/INDICADOR_BIENESTAR/main/mi_base_de_datos.sql"

# Función para descargar y guardar el archivo SQL
def descargar_sql(url, filename="database.sql"):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        return filename
    else:
        st.error("⚠️ Error al descargar el archivo SQL desde GitHub.")
        return None

# Descargar el archivo SQL
sql_file = descargar_sql(GITHUB_SQL_URL)

# Crear la base de datos SQLite en memoria
if sql_file:
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    try:
        # Leer el contenido del archivo SQL con manejo de errores de codificación
        with open(sql_file, "r", encoding="utf-8", errors="ignore") as file:
            sql_script = file.read()
    except UnicodeDecodeError:
        st.error("⚠️ Error al decodificar el archivo SQL. Asegúrate de que esté en formato UTF-8.")
    else:
        # Depurar y ejecutar cada sentencia SQL individualmente
        for statement in sql_script.split(';'):
            try:
                cursor.execute(statement)
            except sqlite3.Error as e:
                st.error(f"⚠️ Error al ejecutar la sentencia SQL: {e}")
                st.error(f"Sentencia SQL con error: {statement}")
                break
        conn.commit()

        # Obtener nombres de las tablas
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
        st.write("### 📌 Tablas disponibles en la base de datos:")
        st.write(tables)

        # Selección de tabla para visualizar
        table_name = st.selectbox("Selecciona una tabla para ver los datos:", tables["name"])

        if table_name:
            # Cargar los datos en un DataFrame
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            st.write(f"### 📊 Datos de la tabla `{table_name}`")
            st.dataframe(df)

            # Opción para descargar los datos en CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Descargar CSV", csv, "datos.csv", "text/csv")

    # Cerrar la conexión
    conn.close()

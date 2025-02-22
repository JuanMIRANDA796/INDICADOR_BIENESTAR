import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import requests

# URL del archivo de base de datos SQLite en GitHub
GITHUB_DB_URL = "https://raw.githubusercontent.com/JuanMIRANDA796/INDICADOR_BIENESTAR/main/mi_base_de_datos.db"

# Función para descargar y guardar el archivo de base de datos
def descargar_db(url, filename="mi_base_de_datos.db"):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        return filename
    else:
        st.error("⚠️ Error al descargar el archivo de base de datos desde GitHub.")
        return None

# Descargar el archivo de base de datos
db_file = descargar_db(GITHUB_DB_URL)

# Conectar a la base de datos SQLite
if db_file:
    conn = sqlite3.connect(db_file)

    # Obtener nombres de las tablas
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
    st.sidebar.write("### 📌 Tablas disponibles en la base de datos:")
    st.sidebar.write(tables)

    # Selección de tabla para visualizar
    table_name = st.sidebar.selectbox("Selecciona una tabla para ver los datos:", tables["name"])

    if table_name:
        # Cargar los datos en un DataFrame
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        st.write(f"### 📊 Datos de la tabla `{table_name}`")
        st.dataframe(df)

        # Crear el gráfico de líneas
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df['año'], df['Variacion_Porcentual_IPC'], marker='o', label='Variación Porcentual IPC')
        ax.plot(df['año'], df['variacion porcentual anual'], marker='s', label='Variación Porcentual Anual')
        ax.plot(df['año'], df['Tasa de Crecimiento Anual KW/h'], marker='x', label='Tasa de Crecimiento Anual KW/h')
        ax.plot(df['año'], df['indicador_bienestar'], marker='^', label='Indicador de Bienestar')  # Plot indicador_bienestar

        ax.set_xlabel('Año')
        ax.set_ylabel('Porcentaje / Tasa / Indicador')  # Updated y-axis label
        ax.set_title('Comparación de Variables a lo Largo del Tiempo')
        ax.legend()
        ax.grid(True)
        ax.set_xticks(df['año'])

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)

        # Opción para descargar los datos en CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar CSV", csv, "datos.csv", "text/csv")

    # Cerrar la conexión
    conn.close()

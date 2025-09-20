# src/utils.py

# =========================
# 1️⃣ Librerías core
# =========================
import pandas as pd
import numpy as np
import re
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from word2number import w2n  # Para convertir strings numéricos a números

# =========================
# 2️⃣ Configuración de pandas
# =========================
pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
# pd.set_option('display.float_format', '{:,.0f}'.format)  # Formato sin notación científica

# =========================
# 3️⃣ Configuración de gráficos
# =========================
sns.set(style="whitegrid")           # Estilo de Seaborn
sns.set_palette("Set2")              # Paleta de colores
plt.rcParams["figure.figsize"] = (10,6)
plt.rcParams["axes.titlesize"] = 16
plt.rcParams["axes.labelsize"] = 14
plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12

# =========================
# 4️⃣ Configuración general
# =========================
import warnings
warnings.filterwarnings("ignore")  # Ocultar warnings innecesarios

# =========================
# 5️⃣ Funciones
# =========================

def carga_eda(csv):
    """ 
    Función para leer csv, convertir a df y hacer una primera exploración.
    Igualar a variable con el nombre que quieres dar a DataFrame
    """
    
    try:
        # Convertir el csv a DataFrame
        df = pd.read_csv(f"../data/{csv}.csv")        

        # Muestro las primeras filas
        display(df.head())

        # Muestro las últimas filas
        display(df.tail())

        # Muestro las dimensiones del dataframe
        print(f"-----\n\nEl DataFrame tiene {df.shape[0]} filas y {df.shape[1]} columnas.\n-----")

        # Consulto si hay filas duplicadas
        print(f"\nEl número de filas duplicadas es {df.duplicated().sum()}\n-----")

        # Muestro el tipo de dato y si hay nulos por cada columna
        print("\nInformación del DataFrame:")
        df.info()

        # Muestro el porcentaje de nulos por variable
        print("\nPorcentaje de nulos:")
        display(round(df.isnull().mean() * 100, 2))

        # Muestro las estadísticas de columnas numéricas
        print("-----\n\nEstadísticas descriptivas:")
        display(df.describe(include="all").T)

        # Me devuelve un df que tendré que igualar a una variable
        return df  
                

    # Excepciones en caso de no encontrar el archivo o de que haya un error
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '../data/{csv}.csv'.")
        return None  
    
    except Exception as e:
        print(f"Error: {e}")
        return None 
    

def text_to_num(year):
    """
    Limpiar y convertir a números str sin errores ortográficos ni de puntuación: 
        - Si el valor es un str, lo normaliza dejando todo en minusculas y quitando espacios en los extremos.
        - Después lo convierte a número con la librería w2n, método word_to_num
        - Si no puede devuelve el valor ya normalizado
        - Si no es un str, devuelve el valor original
    """
    # Si es str
    if isinstance(year, str):

        # Normalizamos el str
        year_limpio = year.strip().lower()

        try:
            return w2n.word_to_num(year_limpio)
        
        except ValueError:
            
            # Si no puede leer los números en str devuelve NaN
            return np.nan
        
        except Exception as e:

            # Por si hay cualquier otro tipo de error
            print(f"⚠️ Error inesperado con '{year}': {e}")
            return np.nan
        
    # Si no es str, devuelve el mismo valor   
    else: 
        return year
    

def clean_budget(num):
        # Quitar espacios al inicio/final
        num = num.strip() 

        # Buscar si hay "M" o "m":
        if re.search(r"[Mm]", num):

            # Quitar "M" o "m" y convertir a int y millones
            clean_num = re.sub(r"[^\d\.]", "", num)
            try:
                return int(clean_num) * 1_000_000
            except:
                return np.nan

        # Buscar si hay "K" o "k":
        if re.search(r"[Kk]", num):

            # Quitar "K" o "k" y convertir a int y miles
            clean_num = re.sub(r"[^\d\.]", "", num)
            try:
                return int(clean_num) * 1_000
            except:
                return np.nan   
            
        # Si no encuentra solo convierte a Int
        else:
            
            try:
                return int(num)
            except:
                return np.nan
            

def fill_omdb(row, columns_to_fill=["IMDB_Rating", "Revenue", "Genre"]):
    """
    Toma una fila de un DataFrame, comprueba si tiene NaN en las columnas especificadas,
    y si es así consulta OMDb por el título y devuelve la fila con los valores rellenados.
    """
    # Si no falta nada, devuelve la fila tal cual
    if not row[columns_to_fill].isnull().any():
        return row

    title = row["Title"]

    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data.get("Response") == "True":
            if pd.isna(row["IMDB_Rating"]) and "imdbRating" in data:
                if data["imdbRating"] != "N/A":
                    row["IMDB_Rating"] = data["imdbRating"]
                    print(f"{title} -> IMDB_Rating: {row["IMDB_Rating"]}")
                else:
                    row["IMDB_Rating"] = np.nan

            if pd.isna(row["Revenue"]) and "BoxOffice" in data:
                if data["BoxOffice"] != "N/A":
                    row["Revenue"] = data["BoxOffice"]
                    print(f"{title} -> Revenue: {row["Revenue"]}")
                else:
                    row["Revenue"] = np.nan

            if pd.isna(row["Genre"]) and "Genre" in data:
                if data["Genre"] != "N/A":
                    row["Genre"] = data["Genre"].split(",")[0].strip()
                    print(f"{title} -> Genre: {row["Genre"]}")
                else:
                    row["Genre"] = np.nan

        else:
            print(f"No encontrado en OMDb: {title}")
            
    else:
        print(f"Error con la API para {title}: {response.status_code}")

    return row



# Adopta Un Junior Challenge: Movies Dataset Analysis

Exploratory analysis and visualization of a movie dataset as part of the **Adopta un Junior** data challenge.  
This project gave me the opportunity to be selected and become part of the **Adopta un Junior** initiative.

## Initial Setup

The following libraries were imported for data manipulation (`pandas`, `numpy`, `re`, `requests`), string-to-number conversion (`word2number`), and visualization (`matplotlib`, `seaborn`).

Configuration steps:
- Pandas adjusted to show all columns and disable scientific notation (optional).  
- Seaborn and Matplotlib configured for a consistent visual style, color palette, and label sizes.  
- Unnecessary warnings were ignored to keep the Notebook clean.

This setup ensures a consistent and professional environment for data exploration, cleaning, and visualization.

---

## 1. Introduction
This project analyzes a movie dataset containing information such as year, genre, budget, revenue, and IMDB rating.  
The goal was to clean, explore, and fill missing data to extract insights and prepare a reliable dataset for further analysis — while keeping in mind potential scalability, as this dataset is quite small.

---

## 2. Dataset
- **Source**: CSV file provided by the "Adopta un Junior" challenge.  
- **Main columns**:
  - `Title`: Movie title  
  - `Genre`: Genre  
  - `Year`: Release year  
  - `Budget`: Production budget  
  - `Revenue`: Box office revenue  
  - `IMDB_Rating`: IMDB rating  

> Size: 22 rows  

---

## 3. Exploratory Data Analysis (EDA)

A preliminary analysis was performed using the `carga_eda()` function to understand data distribution and detect possible issues.  
Checks performed:
- `value_counts()` for categorical variables  
- `describe()` for numerical variables  
- Null value detection  
- Duplicate detection  

### Pre-cleaning exploratory visualizations:

| Chart | Insight |
|--------|----------|
| ![Year distribution](images/histplot_years1.png) | Some values were strings ("Two Thousand") and converted to numeric years. The year with the most movies is **2020**. |
| ![Scatter Budget vs Revenue](images/scatter_budget_revenue1.png) | Budget values were inconsistent and mixed-format. Planned normalization (thousands, millions) for proper analysis. |
| ![Boxplot Budget](images/boxplot_budget1.png) | Mixed-format values ("80M") were detected and required cleaning. |
| ![Histplot Rating](images/histplot_ratings1.png) | Most movies have mid-range IMDB ratings, with few extreme values. |
| ![Scatter Rating vs Revenue](images/scatter_rating_revenue1.png) | No clear correlation between IMDB_Rating and Revenue; to be rechecked post-cleaning. |

---

## 4. Duplicates, Cleaning, and Transformations

### 4.1 Duplicates
Two duplicate rows were detected during the EDA.

- `value_counts()` was run on the `Title` column (unique identifier).  
- Duplicates confirmed using `df_movies.duplicated(keep=False).sort_values("Title")`.  
- Removed via `df_movies.drop_duplicates(inplace=True)`.  
- Verified with `.shape` to ensure proper application.

---

### 4.2 Year
- Converted strings to numbers using the `text_to_num()` function (`word2number` library).  
- Converted to datetime and extracted the year (`dt.year`) for accurate temporal analysis.

### 4.3 Budget
- Cleaned using `clean_budget()` function.  
- Regex used to detect letters `M/m` and `K/k` and convert to integers (millions and thousands).  
- Unconvertible values replaced with `NaN`.

### 4.5 OMDb API
Missing values were identified in the columns `IMDB_Rating`, `Revenue`, and `Genre`.

- Created a function `fill_omdb()` that:
  1. Iterates through rows with missing values.  
  2. Queries the OMDb API using the movie title.  
  3. Fills only the empty fields found in the API response.  
  4. Keeps `NaN` if the movie is not found.  
  5. Prints a message in case of errors or missing movies.  

- The percentage of null values was reviewed before and after applying the function.

**Note:** For small datasets, retrieved information is limited, but the function is designed for scalability.

---

## 5. Final Missing Value Imputation

| Column | Imputation Strategy | Visualization |
|---------|--------------------|---------------|
| **Genre** | Filled with API data or labeled as `"Unknown"` if not found | ![alt text](images/barplot_rating_genre1.png) <br> ![alt text](reports/media_rating_per_genre1.png) |
| **Revenue** | Imputed using the median based on the Budget/Revenue ratio | ![Null Scatterplot](images/null_scatter_budget_revenue1.png) <br> ![Non-null Scatterplot](images/no_null_scatter_budget_revenue1.png) |
| **IMDB_Rating** | Imputed with the global median (for larger datasets, imputation by genre is recommended) | ![Null Histplot](images/histplot_rating1.png) <br> ![Non-null Histplot](images/no_null_histplot_rating1.png) |

---

## 6. Final Visualizations and Conclusions

Below are the main insights obtained after data cleaning and visualization.

⚠️ **Note:** The dataset is small, so results should be interpreted cautiously. Larger datasets could yield different insights.

---

### 6.1 Budget and Revenue Over Time
- **Downward trend** in both budget and revenue between 2000 and 2022.  
- Confirms the **positive correlation** identified in the correlation matrix.

|  |  |
|--------------|---------------|
|![Year-Budget Relationship](reports/relacion_año_budget1.png)|![Year-Revenue Relationship](reports/relacion_año_revenue1.png)|

![Budget-Revenue Relationship](reports/relacion_budget_revenue1.png)

---

### 6.2 Top 5 Movies
- **60% overlap** between the Top 5 highest-budget and highest-revenue movies (correlation 0.58).  
- **No clear relationship** between IMDB rating and revenue.

|  |  |
|--------------|---------------|
|![Top 5 Budget/Revenue](reports/top5_budget_revenue1.png)|![Top 5 Revenue/Rating](reports/top5_revenue_rating1.png)|

---

### 6.3 Genres
- **Drama, Comedy, and Thriller** have the most movies and the highest absolute revenue.  
- **Documentary, Action, and Comedy** show the highest average ratings.

|  |  |
|--------------|---------------|
|![Movies per Genre](reports/film_per_genre1.png)|![Top 3 Revenue by Genre](reports/top3_genre_revenue1.png)|

![Top Rated Genres](reports/media_rating_per_genre1.png)

---

### 6.4 IMDb Rating
- **Most active year:** 2020.  
- **Highest average rating:** 2003 (8.2), followed by 2016 and 2007 (7.2).  
- **Lowest average rating:** 2019 (3.9).  
- **Global average rating:** 5.77.  
- Most movies are in the mid-range ratings (4.8–5.8), with few extremes.

|  |  |
|--------------|---------------|
|![Movies per Year](reports/distribucion_per_year1.png)|![Alternative Year Distribution](reports/distribucion_per_year2.png)|

![Average Rating per Year](reports/media_rating_per_year1.png)  
![Rating Distribution](reports/distribucion_rating1.png)

---

## 7. Next Steps
- Identify movies by their IMDb code for better referencing.  
- Expand the analysis using a larger dataset to validate insights.  
- Build a **Tableau dashboard** summarizing key findings.

---

## 8. How to Run the Project
1. Clone the repository  
2. Install dependencies: `pip install -r requirements.txt`  
3. Set up the API Key:
   - Obtain an OMDb API Key (free for basic use).  
   - Request one at http://www.omdbapi.com/apikey.aspx  
   - Insert your key into the `API_KEY` variable in the code before running the notebooks (`02_limpieza_nulos.ipynb`).  
4. Run notebooks in this order:
   - `01_eda.ipynb`  
   - `02_limpieza_y_nulos.ipynb`  
   - `03_visualizaciones_y_conclusiones.ipynb`  

> During execution, generated images are saved automatically in:
- `./images/` → exploratory and EDA plots  
- `./reports/` → final visualizations used in conclusions




---


# Reto Adopta Un Junior: Análisis Movies Dataset
Análisis exploratorio y visualización de un dataset de películas como parte del reto de datos de Adopta un Junior.

## Configuración inicial

Se importan las librerías necesarias para manipulación de datos (`pandas`, `numpy`, `re`, `requests`), conversión de strings a números (`word2number`) y visualización (`matplotlib`, `seaborn`).

Se configuran:  
- Pandas para mostrar todas las columnas y evitar notación científica (opcional).  
- Seaborn y Matplotlib para un estilo uniforme, paleta de colores y tamaños de títulos/etiquetas.  
- Ignorar warnings innecesarios para mantener el Notebook limpio.

Esta configuración asegura un entorno consistente y profesional para el análisis exploratorio, limpieza y visualización de los datos.


## 1. Introducción
Este proyecto consiste en analizar un dataset de películas con información sobre años, género, budget, revenue y valoración en IMDB.  
El objetivo es limpiar, explorar y completar los datos faltantes para extraer insights y preparar un dataset listo para análisis posteriores, sin perder de vista la posible escalabilidad del proyecto, teniendo en cuenta que este dataset es reducido.

---

## 2. Dataset
- Fuente: CSV proporcionado por el reto "Adopta un Junior".
- Columnas principales:
  - `Title`: Título de la película
  - `Genre`: Género
  - `Year`: Año de lanzamiento
  - `Budget`: Presupuesto
  - `Revenue`: Ingresos generados
  - `IMDB_Rating`: Valoración en IMDB

> Tamaño: 22 filas 

---

## 3. Análisis Exploratorio (EDA)

Se realizó un análisis preliminar con la función `carga_eda()`para entender la distribución de los datos y detectar posibles problemas.  
- Revisiones realizadas:
  - `value_counts()` para variables categóricas
  - `describe()` para variables numéricas
  - Detección de valores nulos
  - Detección de duplicados

---
### Visualizaciones exploratorias realizadas previa limpieza:

| Gráfico | Insight |
|---------|---------|
| ![Distribución por año](images/histplot_years1.png) | Algunos valores estaban en formato string ("Two Thousand") y se convirtieron a años. El año con más películas es **2020**. |
| ![Scatter Budget vs Revenue](images/scatter_budget_revenue1.png) | Los valores de Budget estaban desordenados y en formatos mixtos. Se planificó normalizar unidades (miles, millones) para analizar la relación. |
| ![Boxplot Budget](images/boxplot_budget1.png) | Se detectan valores en formato mixto ("80M") que hay que limpiar. |
| ![Histplot Rating](images/histplot_ratings1.png) | Se observa la distribución de IMDB_Rating. La mayoría de películas se concentran en valores medios, con pocas películas con valoraciones extremas. |
| ![Scatterplot Rating/Revenue](images/scatter_rating_revenue1.png) | No se observa una relación clara entre IMDB_Rating y Revenue; se volverá a comprobar una vez los datos estén limpios. |


## 4. Duplicados, Limpieza y Transformaciones

### 4.1 Duplicados
Durante el EDA se detectaron **2 filas duplicadas** en el dataset.

- Se realizó un `value_counts()` sobre la columna `Title` (identificador único).  
- Se confirmaron los duplicados usando `df_movies.duplicated(keep=False).sort_values("Title")`.  
- Se eliminaron con `df_movies.drop_duplicates(inplace=True)`.  
- Se verificó con `.shape` que los cambios se aplicaron correctamente.

---

### 4.2 Year
- Conversión de strings a números usando la función `text_to_num()` (librería `word2number`).  
- Transformación a tipo datetime y extracción del año (`dt.year`) para análisis correcto.

### 4.3 Budget
- Limpieza con la función `clean_budget()`.  
- Detecta las letras `M/m` y `K/k` con Regex y convierte los valores a int (millones y miles).  
- Valores no convertibles se transforman en `NaN`.

### 4.5 OMDb API
Se identificaron valores nulos en las columnas: `IMDB_Rating`, `Revenue` y `Genre`.

- Se creó la función `fill_omdb()` que:  
  1. Itera sobre filas con nulos.  
  2. Consulta la API de OMDb por el título de la película.  
  3. Rellena únicamente los datos vacíos que existen en la respuesta.  
  4. Mantiene `NaN` si la API no devuelve información.  
  5. Imprime un aviso si la película no se encuentra o si hay error de conexión.  

- Se revisó el porcentaje de nulos antes y después de aplicar la función.

**Nota:** En datasets pequeños, la cantidad de información obtenida es limitada, pero la función está pensada para escalabilidad.

---

## 5. Imputación final de Nulos

| Columna | Estrategia de imputación | Visualización |
|---------|--------------------------|---------------|
| **Genre** | Valores nulos completados con la API o mantenidos como `NaN` si no se encontraron, luego se etiquetan como `"Unknown"` | ![alt text](images/barplot_rating_genre1.png) <br> ![alt text](reports/media_rating_per_genre1.png)|
| **Revenue** | Imputación por mediana usando la relación con Budget (`ratio`) | ![Scatterplot Nulos](images/null_scatter_budget_revenue1.png) <br> ![Scatterplot Sin Nulos](images/no_null_scatter_budget_revenue1.png) |
| **IMDB_Rating** | Imputación por mediana global (en datasets grandes se recomienda por género) | ![Histplot Nulos](images/histplot_rating1.png) <br> ![Histplot Sin Nulos](images/no_null_histplot_rating1.png) |

---


## 6. Visualizaciones y Conclusiones finales

A continuación se muestran los principales insights obtenidos tras el análisis exploratorio de los datos y las visualizaciones.

⚠️ **Nota**: El dataset es reducido, por lo que los resultados deben interpretarse con cautela. Con un conjunto de datos más completo, los insights podrían variar significativamente.

---

### 6.1 Evolución de Budget y Revenue por año
- **Tendencia decreciente** de presupuesto y recaudación entre 2000 y 2022.
- Confirma la **relación positiva** identificada en la matriz de correlación.

|  |  |
| -------------- | --------------- |
|![Relación Año-Budget](reports/relacion_año_budget1.png)|![Relación Año-Revenue](reports/relacion_año_revenue1.png)|

![alt text](reports/relacion_budget_revenue1.png)

---

### 6.2 Top 5 películas
- **60% de coincidencia** entre Top 5 de mayor presupuesto y Top 5 de mayor recaudación (correlación 0.58).  
- **No existe relación** clara entre valoración IMDb y recaudación.

|  |  |
| -------------- | --------------- |
|![Top 5 Budget/Revenue](reports/top5_budget_revenue1.png)|![Top 5 Revenue/Rating](reports/top5_revenue_rating1.png)|

---

### 6.3 Géneros
- **Drama, Comedy y Thriller** son los géneros con más películas y mayor recaudación absoluta.  
- **Documentary, Action y Comedy** presentan las valoraciones promedio más altas.

|  |  |
| -------------- | --------------- |
|![Géneros con más películas](reports/film_per_genre1.png)|![Top 3 ingresos por género](reports/top3_genre_revenue1.png)|

![Géneros mejor valorados](reports/media_rating_per_genre1.png)

---

### 6.4 IMDb Rating
- **Año con más películas**: 2020.  
- **Mejor valoración media**: 2003 (8.2), seguida de 2016 y 2007 (7.2).  
- **Peor valoración media**: 2019 (3.9).  
- **Valoración media global**: 5.77.  
- La mayoría de películas tienen valoraciones medias (4.8 a 5.8), pocas tienen valoraciones extremas.

|  |  |
| -------------- | --------------- |
|![Distribución de películas por año](reports/distribucion_per_year1.png)|![Distribución alternativa por año](reports/distribucion_per_year2.png)|

![Valoración media por años](reports/media_rating_per_year1.png)  
![Distribución de la valoración](reports/distribucion_rating1.png)


## 7. Next Steps
- Identificar las películas con su código IMDb para facilitar referencias y consultas externas.
- Ampliar el análisis con un dataset más grande para validar los insights.
- Crear un dashboard en Tableau que resuma los hallazgos principales.

---

## 8. Cómo ejecutar el proyecto
1. Clonar el repositorio  
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar API Key:
- Es necesario obtener una API Key de OMDb (gratuita para uso básico).
- Puedes solicitarla en http://www.omdbapi.com/apikey.aspx
- Una vez obtenida, introduce tu API Key en la variable API_KEY dentro del código antes de ejecutar los notebooks (`02_limpieza_nulos.ipynb`).
4. Ejecutar notebooks en el orden:
   - `01_eda.ipynb`  
   - `02_limpieza_y_nulos.ipynb`  
   - `03_visualizaciones_y_conclusiones.ipynb`

> Durante la ejecución, las imágenes generadas se guardan automáticamente en las carpetas:
- `./images/` → visualizaciones exploratorias y gráficas del EDA.
- `./reports/` → visualizaciones finales utilizadas en las conclusiones.


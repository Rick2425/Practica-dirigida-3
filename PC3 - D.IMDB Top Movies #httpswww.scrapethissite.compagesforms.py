# ==========================================
# LIBRERÍAS NECESARIAS
# ==========================================
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
# ==========================================


## Parte 1: Programas en Red
# 1. Definir la URL objetivo
url = "https://www.scrapethissite.com/pages/forms/"

try:
    # 2. Realizar la petición HTTP GET
    respuesta_servidor = requests.get(url)
    
    # Levantar una excepción si hubo un error en la petición HTTP (códigos 4xx o 5xx)
    respuesta_servidor.raise_for_status()
    
    print("--- DATOS DE CONEXIÓN ---")
    
    # 3. Mostrar el status_code
    print(f"Status Code: {response.status_code}")
    
    # 4. Mostrar la URL consultada
    print(f"URL Consultada: {response.url}")
    
    # 5. Mostrar el Content-Type
    print(f"Content-Type: {response.headers.get('Content-Type')}")

except requests.exceptions.RequestException as e:
    print(f"Error al intentar conectar con la página: {e}")

# ==========================================
# PARTE II. RECUPERACIÓN DE DATOS
# ==========================================

# Página web asignada
url = "https://www.scrapethissite.com/pages/forms/"

# Encabezado para simular una petición desde navegador
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Obtener el contenido HTML de la página
response = requests.get(url, headers=headers)
response.raise_for_status()

# Analizar el HTML
soup = BeautifulSoup(response.text, "html.parser")

# Buscar las filas de la tabla
filas = soup.select("tr.team")

# Lista donde se guardarán los registros extraídos
registros = []

# Obtener al menos 15 registros
for fila in filas[:20]:

    # Texto completo de la fila
    texto_fila = fila.get_text(" ", strip=True)

    # Expresión regular para extraer un año de 4 dígitos
    patron_anio = re.search(r"\b(19|20)\d{2}\b", texto_fila)

    # Extraer atributos relevantes
    equipo = fila.select_one(".name").get_text(strip=True)
    anio = patron_anio.group() if patron_anio else None
    victorias = fila.select_one(".wins").get_text(strip=True)
    derrotas = fila.select_one(".losses").get_text(strip=True)
    porcentaje_victoria = fila.select_one(".pct").get_text(strip=True)

    # Guardar cada registro como diccionario
    registros.append({
        "equipo": equipo,
        "anio": anio,
        "victorias": victorias,
        "derrotas": derrotas,
        "porcentaje_victoria": porcentaje_victoria
    })

print("PARTE II - Registros recuperados:")

# ==========================================
# PARTE III. PROCESAMIENTO Y ANÁLISIS
# ==========================================

# Crear un DataFrame con pandas
df = pd.DataFrame(registros)

# Limpieza y transformación de datos
df["equipo"] = df["equipo"].str.strip()
df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
df["victorias"] = pd.to_numeric(df["victorias"], errors="coerce")
df["derrotas"] = pd.to_numeric(df["derrotas"], errors="coerce")
df["porcentaje_victoria"] = pd.to_numeric(df["porcentaje_victoria"], errors="coerce")

# Eliminar registros con datos vacíos importantes
df = df.dropna(subset=["equipo", "anio", "victorias", "derrotas", "porcentaje_victoria"])

# Crear una nueva columna transformada
df["total_partidos"] = df["victorias"] + df["derrotas"]

print("\nPARTE III - DataFrame procesado:")
print(df)

# Obtener tres estadísticas descriptivas relevantes
promedio_victorias = df["victorias"].mean()
promedio_derrotas = df["derrotas"].mean()
maximo_porcentaje_victoria = df["porcentaje_victoria"].max()

print("\nEstadísticas descriptivas:")
print("Promedio de victorias:", round(promedio_victorias, 2))
print("Promedio de derrotas:", round(promedio_derrotas, 2))
print("Máximo porcentaje de victoria:", round(maximo_porcentaje_victoria, 3))

# Explicación en dos líneas
print("\nInterpretación:")
print("Los resultados permiten conocer el rendimiento promedio de los equipos según sus victorias y derrotas.")
print("Además, el porcentaje máximo de victoria identifica al equipo con mejor desempeño dentro de los registros analizados.")

# Guardar el DataFrame en un archivo CSV
df.to_csv("registros_hockey_procesados.csv", index=False, encoding="utf-8-sig")
print(registros)
print("Cantidad de registros obtenidos:", len(registros))


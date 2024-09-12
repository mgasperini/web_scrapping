from bs4 import BeautifulSoup as bs
import requests
import sqlite3
# from urllib.parse import urlparse, parse_qs
from random import randint
from tqdm import tqdm

import random
import datetime
import time
import re
import json

import os
from dotenv import load_dotenv


# import pandas as pd
# import numpy as np

# from selenium_stealth import stealth
from urllib.parse import urlencode
from seleniumwire import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.proxy import Proxy, ProxyType
# from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

fecha = datetime.date.today()

# Función para crear una conexión a la base de datos
def crear_conexion(nombre_bd):
    try:
        conexion = sqlite3.connect(nombre_bd)
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

NOMBRE_BBDD = 'mercado_inmobiliario.db'

# Definir constantes para las claves
CLAVES_INMUEBLE = [
    'id_inmueble', 'Nombre', 'Precio', 'Precio_anterior', 'Direccion', 'Barrio', 'Distrito', 'Ciudad',
    'Comarca', 'Provincia', 'tipo_propiedad', 'plantas', 'metros_construidos_m2', 'habitaciones', 'baños',
    'parcela_m2', 'garaje', 'estado', 'año_construcción', 'calefaccion', 'Piscina', 'Jardin', 'Consumo',
    'Emisiones', 'fecha_actualizacion', 'planta_n', 'ascensor', 'orientacion', 'fecha_creacion', 'datos_ubicacion'
]

# Crear o conectar a la base de datos
conn = sqlite3.connect(f'{NOMBRE_BBDD}')
cursor = conn.cursor()


def crear_bbdd(cursor):
    # Crear la tabla inmuebles si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inmuebles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_inmueble TEXT,
            Nombre TEXT,
            Precio INTEGER,
            Precio_anterior INTEGER,
            Direccion TEXT,
            Barrio TEXT,
            Distrito TEXT,
            Ciudad TEXT,
            Comarca TEXT,
            Provincia TEXT,
            tipo_propiedad TEXT,
            plantas INTEGER,
            metros_construidos_m2 INTEGER,
            habitaciones INTEGER,
            baños INTEGER,
            parcela_m2 INTEGER,
            garaje BOOLEAN,
            estado TEXT,
            año_construcción INTEGER,
            calefaccion TEXT,
            Piscina BOOLEAN,
            Jardin TEXT,
            Consumo REAL,
            Emisiones REAL,
            datos_ubicacion TEXT,
            fecha_actualizacion DATE,
            planta_n INTEGER,
            ascensor BOOLEAN,
            orientacion TEXT
        )
    ''')

    # Crear la tabla modificaciones_valor_inmuebles si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modificaciones_valor_inmuebles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_inmueble TEXT,  -- Relacionado con la tabla inmuebles
        precio_actual INT,
        precio_anterior INT,
        fecha_actualizacion DATE,
        FOREIGN KEY (id_inmueble) REFERENCES inmuebles (id_inmueble)  -- Crear relación con la tabla inmuebles
        )
    ''')

crear_bbdd(cursor)

# Función para insertar un diccionario en la tabla
def insertar_inmueble(diccionario, nombre_bd='mercado_inmobiliario.db'):
    # Obtener las claves y valores del diccionario
    valores = [diccionario.get(clave, None) for clave in CLAVES_INMUEBLE]
    
    # Convertir la lista de datos_ubicacion a una cadena JSON para almacenarla en la base de datos
    
    valores[-1] = json.dumps(valores[-1])  # Convertir 'datos_ubicacion' a JSON
    
    # Crear la consulta SQL de inserción
    consulta = f'''
        INSERT INTO inmuebles ({", ".join(CLAVES_INMUEBLE)})
        VALUES ({", ".join(["?" for _ in CLAVES_INMUEBLE])})
    '''

    
    # Realizar la inserción en la base de datos
    with crear_conexion(nombre_bd) as conexion:
        if conexion is not None:
            try:
                cursor = conexion.cursor()
                # Ejecutar la consulta con los valores proporcionados
                cursor.execute(consulta, valores)
                conexion.commit()
                print("Inmueble insertado correctamente.")
            except sqlite3.Error as e:
                print(f"Error al insertar inmueble: {e}")

def ejecutar_consulta(query, database='mercado_inmobiliario.db'):
    with crear_conexion(database) as conexion:
        if conexion is not None:
            try:
                cursor = conexion.cursor()
                cursor.execute(query)
                conexion.commit()
                return cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Error al ejecutar la consulta: {e}")


def actualizar_valor_inmueble(id_inmueble, nuevo_valor, valor_anterior, fecha, nombre_bd=NOMBRE_BBDD):
    # Crear la consulta SQL de inserción en la tabla modificaciones_valor_inmuebles
    consulta_insercion = '''
        INSERT INTO modificaciones_valor_inmuebles (id_inmueble, precio_actual, precio_anterior, fecha_actualizacion)
        VALUES (?, ?, ?, ?)
    '''
    
    # Ejecutar la inserción y actualizar la tabla inmuebles
    with crear_conexion(nombre_bd) as conexion:
        if conexion is not None:
            try:
                cursor = conexion.cursor()
                # Insertar registro de modificación
                cursor.execute(consulta_insercion, (id_inmueble, nuevo_valor, valor_anterior, fecha))
                # Confirmar la inserción
                conexion.commit()
                print(f"Registro de modificación insertado para el inmueble ID: {id_inmueble}")

            except sqlite3.Error as e:
                print(f"Error al insertar el registro de modificación: {e}")


def parsear_ubicacion(lista_datos):

    match len(lista_datos):
        case 6:
            if len(lista_datos[-1].strip()) > 1:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Barrio': lista_datos[2].strip() + ", " + lista_datos[1].strip(),
                    'Distrito': lista_datos[3].strip(),
                    'Ciudad': lista_datos[4].strip(),
                    'Comarca': lista_datos[5].split(',')[0].strip(),
                    'Provincia': lista_datos[5].split(',')[1].strip()
                }
            else:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Barrio': lista_datos[1].strip(),
                    'Distrito': lista_datos[2].strip(),
                    'Ciudad': lista_datos[3].strip(),
                    'Provincia': lista_datos[4].split(',')[0].strip()
                }
        case 5:
            if len(lista_datos[-1].strip()) > 1:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Barrio': lista_datos[1].strip(),
                    'Distrito': lista_datos[2].strip(),
                    'Ciudad': lista_datos[3].strip(),
                    'Comarca': lista_datos[4].split(',')[0].strip(),
                    'Provincia': lista_datos[4].split(',')[1].strip()
                }
            else:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Barrio': lista_datos[1].strip(),
                    'Distrito': lista_datos[2].strip(),
                    'Ciudad': lista_datos[3].strip(),
                    'Provincia': lista_datos[4].split(',')[0].strip()
                }
        case 4:
            if len(lista_datos[-1].strip()) > 1:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Distrito': lista_datos[1].strip(),
                    'Ciudad': lista_datos[2].strip(),
                    'Comarca': lista_datos[3].split(',')[0].strip(),
                    'Provincia': lista_datos[3].split(',')[1].strip()
                }
            else:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Distrito': lista_datos[1].strip(),
                    'Ciudad': lista_datos[2].strip(),
                    'Provincia': lista_datos[3].split(',')[0].strip()
                }
        case 3:
            if len(lista_datos[-1].strip()) > 1:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Ciudad': lista_datos[1].strip(),
                    'Comarca': lista_datos[2].split(',')[0].strip(),
                    'Provincia': lista_datos[2].split(',')[1].strip()
                }
            else:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Ciudad': lista_datos[1].strip(),
                    'Provincia': lista_datos[2].split(',')[0].strip()
                }
        case 1:
            if len(lista_datos[-1].strip()) > 1:
                return {
                    'Comarca': lista_datos[0].split(',')[0].strip(),
                    'Provincia': lista_datos[0].split(',')[1].strip()
                }
            else:
                return {
                    'Provincia': lista_datos[0].split(',')[0].strip()
                }
        case _:
            return {
                'datos_ubicacion': lista_datos
            }


load_dotenv()

SCRAPE_OPS_API_KEY = os.getenv('SCRAPE_OPS_API_KEY')
SCRAPE_OPS_EMAIL = os.getenv('SCRAPE_OPS_EMAIL')
# Intentos ante falla
NUM_RETRIES = 3


def get_user_agent_list():
  response = requests.get('http://headers.scrapeops.io/v1/user-agents?api_key=' + SCRAPE_OPS_API_KEY)
  json_response = response.json()
  return json_response.get('result', [])

def get_random_user_agent(user_agent_list):
  random_index = randint(0, len(user_agent_list) - 1)
  return user_agent_list[random_index]

user_agent_list = get_user_agent_list()
     

from scrapeops_python_requests.scrapeops_requests import ScrapeOpsRequests


## Initialize the ScrapeOps Logger
scrapeops_logger = ScrapeOpsRequests(
    scrapeops_api_key=SCRAPE_OPS_API_KEY, 
    spider_name='Prueba',
    )


## Initialize the ScrapeOps Python Requests Wrapper
requests = scrapeops_logger.RequestsWrapper() 


def get_request(url):

    URL_PROXY = 'https://proxy.scrapeops.io/v1/'
    PARAMS_PROXY = {
        'api_key': SCRAPE_OPS_API_KEY,
        'url': url,
    }
    headers = {'User-Agent': get_random_user_agent(user_agent_list)}
    try:
        response = requests.get(
            URL_PROXY,
            params=PARAMS_PROXY,
            headers= headers,
            timeout= 120,
        )
        print(response.status_code)
        return response.content
    except:
        return None

def obtener_ids_inmuebles(url_listado):
    # Direcciona el navegador a la URL
    driver = get_request(url_listado)

    # Extrae el html de la página
    html = driver

    ## Scrapear páginas de resultados (ID y Precio)

    # Parsea el html
    soup = bs(html,'lxml')

    # Diccionario para obtener los datos
    datos_id_precio = {}

    # Obtiene los artículos donde se puede obtener la información de ID y Precio
    
    articles = soup.find_all('article',{'class':'item'})

    # Itera en cada artículo para obtener los datos necesarios
    for article_info in articles:
        try:
            #ID
            id_inmueble = article_info.get('data-element-id')
            # Precio
            precio_inmueble = int(article_info.find('span',{'class':'item-price'}).text.replace('.','').replace('€',''))

            #Guarda los datos en el diccionario
            datos_id_precio[id_inmueble] = precio_inmueble
        except Exception as e:
            print(f"Error con id {id_inmueble}:", e)

    return datos_id_precio

def clasificar_y_parsear_caracteristicas(lista_caracteristicas):
    # Diccionario para guardar todas las características
    caracteristicas = {
        "tipo_propiedad": None,
        "plantas": None,
        "metros_construidos_m2": None,
        "habitaciones": None,
        "baños": None,
        "parcela_m2": None,
        "garaje": None,
        "estado": None,
        "año_construcción": None,
        "calefaccion": None,
        "orientacion": None,
        "Piscina": None,
        "Jardin": None,
        "Consumo": None,
        "Emisiones": None,
        "planta_n": None,
        "ascensor": None,
    }

    # Expresiones regulares para cada tipo de característica
    regex_patterns = {
        "tipo_propiedad": r"(casa|chalet|apartamento|piso|ático|independiente)",
        "plantas": r"(\d+)\s*plantas?",
        "metros_construidos_m2": r"(\d+[\.\d+]*)\s*m²\s*construidos?",
        "habitaciones": r"(\d+)\s*habitaciones?",
        "baños": r"(\d+)\s*baños?",
        "parcela_m2": r"parcela de\s*(\d+[\.\d+]*)\s*m²",
        "garaje": r"plaza de garaje",
        "estado": r"(segunda mano|buen estado|nuevo|reformado)",
        "año_construcción": r"construido en\s*(\d{4})",
        "calefaccion": r"calefacción\s*(\w+)?(?:\s*:\s*(\w+))?",
        "orientacion": r"(orientación|orientacion)\s+(\w+)",
        "Piscina": r"Piscina",
        "Jardin": r"(Jardín|Jardin)",
        "Consumo": r"Consumo:\s*([\d\.]+)",
        "Emisiones": r"Emisiones:\s*([\d\.]+)",
        "planta_n": r"^Planta\s*(\d+)(?:[a-zA-Z]*)",
        "ascensor": r"\b(Con|Sin)\sascensor\b",
    }

    # Iterar sobre los elementos de la lista y clasificar
    for item in lista_caracteristicas:
        for key, pattern in regex_patterns.items():
            match = re.search(pattern, item, re.IGNORECASE)
            if match:
                # Procesar el valor según la característica
                if key in ["metros_construidos_m2", "parcela_m2"]:
                    # Extraer solo el número y convertirlo a entero
                    number = re.search(r"(\d+[\.\d+]*)", match.group(0))
                    if number:
                        caracteristicas[key] = int(float(number.group(1).replace(',', '')))
                elif key in ["plantas", "habitaciones", "baños", "año_construcción"]:
                    # Extraer solo el número y convertirlo a entero
                    number = re.search(r"(\d+)", match.group(0))
                    if number:
                        caracteristicas[key] = int(number.group(1))
                elif key == "calefaccion":
                    # Extraer el tipo de calefacción
                    calefaccion = re.findall(r"(\w+)", match.group(0))[-1]
                    if calefaccion and calefaccion != 'calefacción':
                        caracteristicas[key] = calefaccion
                elif key == "garaje":
                    # Indicar si tiene plaza de garaje
                    caracteristicas[key] = True
                elif key in ["Piscina", "Jardin"]:
                    # Indicar si tiene piscina o jardín
                    caracteristicas[key] = True
                elif key in ["Consumo", "Emisiones"]:
                    # Convertir el valor a float
                    caracteristicas[key] = float(match.group(1))
                elif key == "orientacion":
                    # Extraer orientación
                    orientacion = re.findall(r"(\w+)", match.group(0))[-1]
                    if orientacion:
                        caracteristicas[key] = orientacion
                elif key == 'ascensor':
                    ascensor = match.group(1).lower() == "con"
                    if ascensor:
                        caracteristicas[key] = ascensor
                elif key == 'planta_n':
                    n_planta = match.group(1)
                    if n_planta:
                        caracteristicas[key] = n_planta
                else:
                    # Para otros casos, solo almacenar el valor encontrado
                    caracteristicas[key] = match.group(0)
                break

    return caracteristicas

def obtener_listado_bbdd():
    query = """SELECT id_inmueble, precio FROM inmuebles"""
    return  dict(ejecutar_consulta(query))

# Hago query en SQLite para obtener todos los ids y su precio
inmuebles_en_bbdd = obtener_listado_bbdd()

print(inmuebles_en_bbdd)

### Our Helper Functions ###
def get_page_url_status_code(url, driver):
    page_url_status_code = 500

    # Access requests via the `requests` attribute
    for request in driver.requests:

        if request.response:
            #show all urls that are requested per page load
            print(
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type']
            )


        if request.url == url:
            page_url_status_code = request.response.status_code

    return page_url_status_code


def interceptor(request):
    # stopping images from being requested
    # in case any are not blocked by imagesEnabled=false in the webdriver options above 
    if request.path.endswith(('.png', '.jpg', '.gif')):
        request.abort()

    # stopping css from being requested
    if request.path.endswith(('.css')):
        request.abort()

    # stopping fonts from being requested
    if 'fonts.' in request.path: #eg fonts.googleapis.com or fonts.gstatic.com
        request.abort()

### End Of Helper Functions ###

paginas_a_scrapear = 10
offset = 0
for pagina in tqdm(range(1 + offset, paginas_a_scrapear + 1 + offset, 1)):
    url = f"https://www.idealista.com/venta-viviendas/valencia-provincia/pagina-{pagina}.htm?ordenado-por=fecha-publicacion-desc"

    dic_inmuebles = obtener_ids_inmuebles(url)

    inmuebles_en_bbdd = obtener_listado_bbdd()
    try:
        # Agrego Loop para iterar sobre los id's de la lista
        for inmueble in tqdm(dic_inmuebles):
            id_inmueble = inmueble
            if id_inmueble in inmuebles_en_bbdd:
                # ID existe en ambos diccionarios
                if dic_inmuebles[id_inmueble] == inmuebles_en_bbdd[
                        id_inmueble]:
                    # ID existe con el mismo valor --> Continua al siguiente inmueble
                    continue
                else:
                    # Valor es diferente, actualizar el valor del inmueble
                    actualizar_valor_inmueble(
                        id_inmueble,
                        valor_anterior=inmuebles_en_bbdd[id_inmueble],
                        nuevo_valor=dic_inmuebles[id_inmueble],
                        fecha=fecha)
                    continue
            else:
                # ID no existe en el segundo diccionario, crear un nuevo inmueble
                url_inmueble = f'https://www.idealista.com/inmueble/{id_inmueble}/'

                for _ in range(NUM_RETRIES):
                    try:
                        # Direcciona el navegador a la URL
                        driver = get_request(url=url_inmueble)
                        if driver:
                            # Extrae el html de la página
                            html = driver

                            ## Scrapear páginas de resultados (ID y Precio)

                            # Parsea el html
                            soup = bs(html, 'lxml')

                            # Nombre
                            nombre_inmueble = soup.find(
                                'span', {
                                    'class': 'main-info__title-main'
                                }).text.strip()

                            # Ubicación
                            lista_datos_ubicacion = []
                            info_ubicacion = soup.find('div', {
                                'id': 'headerMap'
                            }).find_all('li', {'class': 'header-map-list'})
                            for info in info_ubicacion:
                                lista_datos_ubicacion.append(info.text.strip())

                            dic_ubicacion = parsear_ubicacion(
                                lista_datos_ubicacion)

                            # Precio
                            precio = int(
                                soup.find('span', {
                                    'class': 'info-data-price'
                                }).text.replace('.', '').replace('€',
                                                                 '').strip())

                            # Precio Anterior
                            try:
                                precio_anterior = int(
                                    soup.find('span', {
                                        'class': 'pricedown_price'
                                    }).text.replace('.', '').replace('€', ''))
                            except:
                                precio_anterior = None

                            # Características básicas

                            lista_caracteristicas_basicas = []

                            info_caracteristicas_basicas = soup.find(
                                'div',
                                {'class', 'details-property'}).find_all('li')
                            for caract in info_caracteristicas_basicas:
                                lista_caracteristicas_basicas.append(
                                    caract.text.strip().replace("\n", ""))

                            # Parsear los resultados
                            caracteristicas_principales = clasificar_y_parsear_caracteristicas(
                                lista_caracteristicas_basicas)

                            # Unifica los datos obtenidos
                            dic_datos_inmueble = {
                                "id_inmueble": id_inmueble
                            } | {
                                "Nombre": nombre_inmueble
                            } | {
                                "Precio": precio
                            } | {
                                "Precio_anterior": precio_anterior
                            } | dic_ubicacion | caracteristicas_principales | {
                                "fecha_creacion": fecha
                            }

                            #Agrega el inmueble a la base de datos
                            insertar_inmueble(dic_datos_inmueble)
                            # time.sleep(random.randint(10, 12))
                            break
                    except Exception as e:
                        print("error", e)
    except Exception as e:
        print("Error:", e)
    finally:
        # Cerrar la conexión
        conn.close()

conn.close()


# Importación de librerías
from bs4 import BeautifulSoup as bs
import sqlite3

import random
import datetime
import time
import re
import json

import undetected_chromedriver as uc

## Configuración de BBDD
bbdd = 'mercado_inmobiliario.db'

# Crear o conectar a la base de datos
conn = sqlite3.connect(f'{bbdd}')
cursor = conn.cursor()

## Tabla Inmuebles
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

## Crear registro inmueble
# Función para insertar un diccionario en la tabla
def insertar_inmueble(diccionario):
    # Obtener las claves y valores del diccionario
    claves = [
        'id_inmueble', 'Nombre', 'Precio', 'Precio_anterior', 'Direccion', 'Barrio', 'Distrito', 'Ciudad',
        'Comarca', 'Provincia', 'tipo_propiedad',
        'plantas', 'metros_construidos_m2', 'habitaciones', 'baños', 'parcela_m2',
        'garaje', 'estado', 'año_construcción', 'calefaccion', 'Piscina',
        'Jardin', 'Consumo', 'Emisiones', 'fecha_actualizacion', 'planta_n', 'ascensor', 'orientacion', 'fecha_creacion' , 'datos_ubicacion'
    ]
    valores = [diccionario.get(clave, None) for clave in claves]
    
    # Convertir la lista de datos_ubicacion a una cadena JSON para almacenarla en la base de datos
    
    valores[-1] = json.dumps(valores[-1])  # Convertir 'datos_ubicacion' a JSON
    
    # Crear la consulta SQL de inserción
    consulta = '''
        INSERT INTO inmuebles (
            id_inmueble, Nombre, Precio, Precio_anterior, Direccion, Barrio, Distrito, Ciudad, Comarca,
            Provincia, tipo_propiedad, plantas,
            metros_construidos_m2, habitaciones, baños, parcela_m2, garaje, estado,
            año_construcción, calefaccion, Piscina, Jardin, Consumo, Emisiones,
            fecha_actualizacion, planta_n, ascensor, orientacion, fecha_creacion , datos_ubicacion
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # Ejecutar la consulta con los valores proporcionados
    cursor.execute(consulta, valores)
    conn.commit()

    ## Consulta BBDD

def ejecutar_consulta(query,database = bbdd, tabla = 'inmuebles', parametros=None):
    """
    Ejecuta una consulta SQL en una base de datos SQLite específica y devuelve el resultado.
    :param database: Nombre o ruta de la base de datos SQLite.
    :param tabla: Nombre de la tabla de la cual se quieren obtener los datos.
    :param query: Consulta SQL a ejecutar.
    :param parametros: Tupla de parámetros a usar en la consulta (opcional).
    :return: Resultado de la consulta.
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Ejecutar la consulta
        if parametros:
            cursor.execute(query, parametros)
        else:
            cursor.execute(query)

        # Obtener todos los resultados
        resultado = cursor.fetchall()

        return resultado

    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    finally:
        # Cerrar la conexión
        conn.close()

## Tabla modificiones_valor_inmuebles

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

## Actualiza valor del inmueble

def actualizar_valor_inmueble(id_inmueble, nuevo_valor, valor_anterior, fecha):
    # Conectar a la base de datos SQLite
    conexion = sqlite3.connect('nombre_base_datos.db')
    cursor = conexion.cursor()
    
    try:
        # Insertar los datos en la tabla modificaciones_valor_inmuebles
        cursor.execute('''
            INSERT INTO modificaciones_valor_inmuebles (id_inmueble, precio_actual, precio_anterior, fecha_actualizacion)
            VALUES (?, ?, ?, ?)
        ''', (id_inmueble, nuevo_valor, valor_anterior, fecha))

        # Confirmar los cambios
        conexion.commit()
        print(f"Datos insertados correctamente para el inmueble ID: {id_inmueble}")

    except sqlite3.Error as e:
        print(f"Error al insertar datos: {e}")
    finally:
        # Cerrar la conexión
        conexion.close()

## Scrapping
def parsear_ubicacion(lista_datos):
    # parsed_url = urlparse(info_coordenadas)
    # query_params = parse_qs(parsed_url.query)
    # # Extraer el parámetro 'center'
    # center_param = query_params.get('center', [''])[0]

    # # Dividir el 'center' para obtener latitud y longitud
    # latitud, longitud = center_param.split(',')
    match len(lista_datos):
        case 5:
            if len(lista_datos[-1].strip()) > 1:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Barrio': lista_datos[1].strip(),
                    'Distrito': lista_datos[2].strip(),
                    'Ciudad': lista_datos[3].strip(),
                    'Comarca': lista_datos[4].split(',')[0],
                    'Provincia': lista_datos[4].split(',')[1]
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
                    'Comarca': lista_datos[3].split(',')[0],
                    'Provincia': lista_datos[3].split(',')[1]
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

def obtener_ids_inmuebles(browser,url_listado):
    # Direcciona el navegador a la URL
    browser.get(url=url_listado)
    try:
        time.sleep(1)
        # Selecciona "Aceptar y continuar" en cookies de Idealista
        browser.find_element('xpath','//*[@id="didomi-notice-agree-button"]').click()
    except:
        pass

    # Extrae el html de la página
    html = browser.page_source

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
        "calefaccion": r"calefacción\s*central\s*:\s*(\w+)",
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
                    if calefaccion:
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

# Hago query en SQLite para obtener todos los ids y su precio
query = """SELECT id_inmueble, precio FROM inmuebles"""
inmuebles_en_bbdd = dict(ejecutar_consulta(query))

fecha = datetime.date.today()

# Abre el navegador
browser = uc.Chrome()

paginas_a_scrapear = input("Páginas a scrapear:\n")

while not paginas_a_scrapear.isdigit():
    print('Introducir un número de páginas')
    paginas_a_scrapear = input("Páginas a scrapear:\n")
    next

try:
    for pagina in range(1,paginas_a_scrapear+1,1):
        url = f"https://www.idealista.com/venta-viviendas/valencia-provincia/pagina-{pagina}.htm?ordenado-por=fecha-publicacion-desc"

        dic_inmuebles = obtener_ids_inmuebles(browser, url)


        # Agrego Loop para iterar sobre los id's de la lista
        for inmueble in dic_inmuebles:
            id_inmueble = inmueble
            if id_inmueble in inmuebles_en_bbdd:
                # ID existe en ambos diccionarios
                if dic_inmuebles[id_inmueble] == inmuebles_en_bbdd[id_inmueble]:
                    # ID existe con el mismo valor --> Continua al siguiente inmueble
                    continue
                else:
                    # Valor es diferente, actualizar el valor del inmueble
                    actualizar_valor_inmueble(
                        id_inmueble,
                        valor_anterior=inmuebles_en_bbdd[id_inmueble],
                        nuevo_valor=dic_inmuebles[id_inmueble],
                        fecha=fecha)
            else:
                # ID no existe en el segundo diccionario, crear un nuevo inmueble
                url_inmueble = f'https://www.idealista.com/inmueble/{id_inmueble}/'

                # Direcciona el navegador a la URL
                browser.get(url=url_inmueble)
                try:
                    time.sleep(4)
                    # Selecciona "Aceptar y continuar" en cookies de Idealista
                    browser.find_element(
                        'xpath', '//*[@id="didomi-notice-agree-button"]').click()
                except:
                    pass

                # Extrae el html de la página
                html = browser.page_source

                ## Scrapear páginas de resultados (ID y Precio)

                # Parsea el html
                soup = bs(html, 'lxml')

                # Nombre
                nombre_inmueble = soup.find('span', {
                    'class': 'main-info__title-main'
                }).text.strip()

                # Ubicación
                lista_datos_ubicacion = []
                info_ubicacion = soup.find('div', {
                    'id': 'headerMap'
                }).find_all('li', {'class': 'header-map-list'})
                for info in info_ubicacion:
                    lista_datos_ubicacion.append(info.text.strip())

                dic_ubicacion = parsear_ubicacion(lista_datos_ubicacion)

                # Precio
                precio = int(
                    soup.find('span', {
                        'class': 'info-data-price'
                    }).text.replace('.', '').replace('€', '').strip())

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
                    'div', {'class', 'details-property'}).find_all('li')
                for caract in info_caracteristicas_basicas:
                    lista_caracteristicas_basicas.append(caract.text.strip().replace(
                        "\n", ""))

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
                time.sleep(random.randint(10, 12))
except Exception as e:
    print("Error:",e)
finally:
    # Cerrar la conexión
    conn.close()


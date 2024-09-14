from bs4 import BeautifulSoup as bs
from scrapping.parser import parsear_ubicacion, clasificar_y_parsear_caracteristicas
from scrapping.helpers import get_request
from datetime import date
import os

def obtener_ids_inmuebles(url_listado):
    """
    Obtiene los IDs y precios de los inmuebles a partir de una lista de URL de listado de inmuebles.

    Parámetros:
    - url_listado (str): URL del listado de inmuebles.

    Retorna:
    - dict: Un diccionario con los IDs de los inmuebles como claves y los precios como valores.
    """
    html = get_request(url_listado)
    soup = bs(html, 'lxml')
    datos_id_precio = {}

    # Busca todos los artículos que representan inmuebles
    articles = soup.find_all('article', {'class': 'item'})
    for article_info in articles:
        try:
            # Obtiene el ID del inmueble
            id_inmueble = article_info.get('data-element-id')
            # Obtiene el precio del inmueble, eliminando puntos y el símbolo del euro
            precio_inmueble = int(
                article_info.find('span', {'class': 'item-price'}).text
                .replace('.', '').replace('€', '')
            )
            datos_id_precio[id_inmueble] = precio_inmueble
        except Exception as e:
            print(f"Error con id {id_inmueble}:", e)

    return datos_id_precio

def obtener_datos_inmueble_codigo_fuente(html, url_inmueble=None):
    soup = bs(html, 'lxml')

    # Obtiene el nombre del inmueble
    nombre_inmueble = soup.find('span', {'class': 'main-info__title-main'}).text.strip()

    # Obtiene la lista de datos de ubicación
    lista_datos_ubicacion = [
        info.text.strip() for info in soup.find('div', {'id': 'headerMap'}).find_all('li', {'class': 'header-map-list'})
    ]
    dic_ubicacion = parsear_ubicacion(lista_datos_ubicacion)

    # Obtiene el precio del inmueble
    precio = int(
        soup.find('span', {'class': 'info-data-price'}).text
        .replace('.', '').replace('€', '').strip()
    )

    # Obtiene el precio anterior, si está disponible
    try:
        precio_anterior = int(
            soup.find('span', {'class': 'pricedown_price'}).text
            .replace('.', '').replace('€', '')
        )
    except:
        precio_anterior = None

    # Obtiene y clasifica las características básicas del inmueble
    lista_caracteristicas_basicas = [
        caract.text.strip().replace("\n", "") for caract in soup.find('div', {'class': 'details-property'}).find_all('li')
    ]
    caracteristicas_principales = clasificar_y_parsear_caracteristicas(lista_caracteristicas_basicas, nombre_inmueble)

    if not url_inmueble:
        id_inmueble = soup.find('link',{'rel':'canonical'}).get('href').replace('https://www.idealista.com/inmueble/','').replace('/','')
        return {
            "id_inmueble": id_inmueble, 
            "Nombre": nombre_inmueble,
            "Precio": precio,
            "Precio_anterior": precio_anterior,
            **dic_ubicacion,
            **caracteristicas_principales,
            "fecha_creacion": date.today()  # Fecha actual de creación del registro
        }
    else:
        return {
            "id_inmueble": url_inmueble.split('/')[-2],  # Extrae el ID del inmueble de la URL
            "Nombre": nombre_inmueble,
            "Precio": precio,
            "Precio_anterior": precio_anterior,
            **dic_ubicacion,
            **caracteristicas_principales,
            "fecha_creacion": date.today()  # Fecha actual de creación del registro
        }

def obtener_datos_inmueble(url_inmueble):
    """
    Obtiene los datos detallados de un inmueble a partir de su URL.

    Parámetros:
    - url_inmueble (str): URL del inmueble.

    Retorna:
    - dict o None: Un diccionario con los datos del inmueble si la solicitud es exitosa, o None si falla.
    """
    html = get_request(url_inmueble)
    if not html:
        return None

    return obtener_datos_inmueble_codigo_fuente(html=html,url_inmueble=url_inmueble)
    
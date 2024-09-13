from bs4 import BeautifulSoup as bs
from scrapping.parser import parsear_ubicacion, clasificar_y_parsear_caracteristicas
from scrapping.helpers import get_request
from datetime import date


def obtener_ids_inmuebles(url_listado):
    html = get_request(url_listado)
    soup = bs(html, 'lxml')
    datos_id_precio = {}

    articles = soup.find_all('article', {'class': 'item'})
    for article_info in articles:
        try:
            id_inmueble = article_info.get('data-element-id')
            precio_inmueble = int(
                article_info.find('span', {
                    'class': 'item-price'
                }).text.replace('.', '').replace('€', ''))
            datos_id_precio[id_inmueble] = precio_inmueble
        except Exception as e:
            print(f"Error con id {id_inmueble}:", e)

    return datos_id_precio


def obtener_datos_inmueble(url_inmueble):
    html = get_request(url_inmueble)
    if not html:
        return None

    soup = bs(html, 'lxml')

    nombre_inmueble = soup.find('span', {
        'class': 'main-info__title-main'
    }).text.strip()

    lista_datos_ubicacion = [
        info.text.strip() for info in soup.find('div', {
            'id': 'headerMap'
        }).find_all('li', {'class': 'header-map-list'})
    ]
    dic_ubicacion = parsear_ubicacion(lista_datos_ubicacion)

    precio = int(
        soup.find('span', {
            'class': 'info-data-price'
        }).text.replace('.', '').replace('€', '').strip())

    try:
        precio_anterior = int(
            soup.find('span', {
                'class': 'pricedown_price'
            }).text.replace('.', '').replace('€', ''))
    except:
        precio_anterior = None

    lista_caracteristicas_basicas = [
        caract.text.strip().replace("\n", "")
        for caract in soup.find('div', {
            'class': 'details-property'
        }).find_all('li')
    ]
    caracteristicas_principales = clasificar_y_parsear_caracteristicas(
        lista_caracteristicas_basicas)

    return {
        "id_inmueble": url_inmueble.split('/')[-2],
        "Nombre": nombre_inmueble,
        "Precio": precio,
        "Precio_anterior": precio_anterior,
        **dic_ubicacion,
        **caracteristicas_principales, "fecha_creacion": date.today()
    }


from utils.user_agents import get_random_user_agent
import os
from config import requests

def get_request(url):
    """
    Realiza una solicitud GET a través de un proxy para obtener el contenido de una página web.

    Parámetros:
    - url (str): La URL de la página que se quiere obtener.

    Variables utilizadas:
    - SCRAPE_OPS_API_KEY (str): Clave API obtenida del entorno para autenticar el uso del proxy.
    - URL_PROXY (str): URL del servicio de proxy que se usará para realizar la solicitud.
    - PARAMS_PROXY (dict): Parámetros necesarios para el proxy, que incluyen la clave API y la URL de destino.
    - headers (dict): Cabeceras HTTP, en este caso contiene un 'User-Agent' generado aleatoriamente.

    Retorna:
    - (bytes): El contenido de la respuesta en caso de éxito.
    - None: Si la solicitud falla.
    """
    SCRAPE_OPS_API_KEY = os.getenv('SCRAPE_OPS_API_KEY')  # Obtiene la clave API del entorno
    URL_PROXY = 'https://proxy.scrapeops.io/v1/'
    PARAMS_PROXY = {
        'api_key': SCRAPE_OPS_API_KEY,  # Clave API para el proxy
        'url': url,                     # URL de destino a la que se apunta
    }
    headers = {'User-Agent': get_random_user_agent()}  # Cabecera con un 'User-Agent' aleatorio
    try:
        response = requests.get(
            URL_PROXY,
            params=PARAMS_PROXY,
            headers=headers,
            timeout=120,  # Tiempo máximo de espera de 120 segundos
        )
        print(response.status_code)  # Imprime el código de estado de la respuesta
        return response.content  # Devuelve el contenido de la respuesta
    except:
        return None  # Si hay un error, retorna None


def get_page_url_status_code(url, driver):
    """
    Obtiene el código de estado HTTP de una URL específica utilizando un navegador controlado por Selenium.

    Parámetros:
    - url (str): La URL de la página cuyo código de estado se quiere obtener.
    - driver (Selenium WebDriver): El objeto del navegador Selenium que realiza la navegación.

    Variables utilizadas:
    - request (Selenium Request): Cada solicitud realizada por el navegador que contiene la URL, respuesta, y otros datos.

    Retorna:
    - (int): El código de estado HTTP de la URL proporcionada.
    - 500: Si no encuentra la URL o no hay respuesta, devuelve 500 (error del servidor).
    """
    for request in driver.requests:  # Itera sobre todas las solicitudes realizadas por el navegador
        if request.response:
            # Imprime la URL, código de estado y el tipo de contenido de la respuesta
            print(request.url, request.response.status_code, request.response.headers['Content-Type'])
        if request.url == url:  # Si la URL de la solicitud coincide con la que buscamos
            return request.response.status_code  # Devuelve el código de estado de la respuesta
    return 500  # Si no se encuentra la URL, devuelve 500 (error interno del servidor)


def interceptor(request):
    """
    Interceptor que aborta las solicitudes no necesarias para optimizar la carga.

    Parámetros:
    - request (Selenium Request): Objeto de solicitud interceptada por Selenium.

    Función:
    - Si la solicitud es para recursos estáticos como imágenes, hojas de estilo o fuentes, se aborta para mejorar el rendimiento.
    """
    if request.path.endswith(('.png', '.jpg', '.gif', '.css')) or 'fonts.' in request.path:
        request.abort()  # Aborta la solicitud si es de imagen, CSS o fuente

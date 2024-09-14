import os

# Define el nombre de la base de datos
NOMBRE_BBDD = 'mercado_inmobiliario.db'

# Define el número de reintentos para operaciones de red o similares
NUM_RETRIES = 3

def inicializar_scrapeops():
    from scrapeops_python_requests.scrapeops_requests import ScrapeOpsRequests
    global requests

    SCRAPE_OPS_API_KEY = os.getenv('SCRAPE_OPS_API_KEY')
    scrapeops_logger = ScrapeOpsRequests(
        scrapeops_api_key=SCRAPE_OPS_API_KEY,
        spider_name='Idealista',
    )
    requests = scrapeops_logger.RequestsWrapper()

# Inicialmente, 'requests' no está definido
requests = None
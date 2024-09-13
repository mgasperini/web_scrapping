import sys
import os

# Añade el directorio raíz del proyecto al sys.path para importar módulos correctamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from tqdm import tqdm
from database.connection import crear_conexion
from database.operations import obtener_listado_bbdd, actualizar_valor_inmueble, insertar_inmueble
from scrapping.scraper import obtener_ids_inmuebles, obtener_datos_inmueble
from config import NOMBRE_BBDD, NUM_RETRIES

# Carga las variables de entorno desde el archivo .env
load_dotenv()


def main():
    try:
        # Crea una conexión a la base de datos
        conn = crear_conexion(NOMBRE_BBDD)

        # Obtiene el listado de inmuebles existentes en la base de datos
        inmuebles_en_bbdd = obtener_listado_bbdd(conn)

        PAGINAS_A_SCRAPEAR = -1
        OFFSET = -1

        # Solicita al usuario el número de página de inicio y valida la entrada
        while not str(OFFSET).isdigit():
            OFFSET = int(input("Empezar desde la página:\n"))
        OFFSET -= 1

        # Solicita al usuario el número de páginas a scrapear y valida la entrada
        while not str(
                PAGINAS_A_SCRAPEAR).isdigit() and PAGINAS_A_SCRAPEAR != 0:
            PAGINAS_A_SCRAPEAR = int(
                input("Páginas a scrapear (ingresar un número positivo):\n"))

        # Itera sobre el rango de páginas a scrapear
        for pagina in tqdm(range(1 + OFFSET, PAGINAS_A_SCRAPEAR + 1 + OFFSET)):
            # Construye la URL de la página a scrapear
            url = f"https://www.idealista.com/venta-viviendas/valencia-provincia/pagina-{pagina}.htm?ordenado-por=fecha-publicacion-desc"
            # Obtiene los IDs y precios de los inmuebles en la página
            dic_inmuebles = obtener_ids_inmuebles(url)
            for id_inmueble, precio in tqdm(dic_inmuebles.items()):
                # Verifica si el inmueble ya existe en la base de datos
                if id_inmueble in inmuebles_en_bbdd:
                    # Actualiza el valor del inmueble si ha cambiado
                    if precio != inmuebles_en_bbdd[id_inmueble]:
                        actualizar_valor_inmueble(
                            conn, id_inmueble, inmuebles_en_bbdd[id_inmueble],
                            precio)
                else:
                    # Obtiene la URL del inmueble y scrapea los datos
                    url_inmueble = f'https://www.idealista.com/inmueble/{id_inmueble}/'
                    for _ in range(NUM_RETRIES):
                        datos_inmueble = obtener_datos_inmueble(url_inmueble)
                        if datos_inmueble:
                            # Inserta los datos del nuevo inmueble en la base de datos
                            insertar_inmueble(conn, datos_inmueble)
                            break
    except Exception as e:
        # Maneja cualquier excepción y muestra un mensaje de error
        print(f"Error en el proceso de scraping: {e}")
    finally:
        # Cierra la conexión a la base de datos
        conn.close()


# Ejecuta la función main si el script se ejecuta directamente
if __name__ == "__main__":
    main()

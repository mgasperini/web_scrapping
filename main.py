import sys
import os

# Añade el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from tqdm import tqdm
from database.connection import crear_conexion
from database.operations import obtener_listado_bbdd, actualizar_valor_inmueble, insertar_inmueble
from scrapping.scraper import obtener_ids_inmuebles, obtener_datos_inmueble
from config import NOMBRE_BBDD, NUM_RETRIES


load_dotenv()


def main():
    
    try:
        conn = crear_conexion(NOMBRE_BBDD)
        inmuebles_en_bbdd = obtener_listado_bbdd(conn)

        PAGINAS_A_SCRAPEAR = -1
        OFFSET = -1

        
        while (not str(OFFSET).isdigit()):
            OFFSET = int(input("Empezar desde la página:\n"))
            next 
        OFFSET -= 1
        while (not str(PAGINAS_A_SCRAPEAR).isdigit()) and (PAGINAS_A_SCRAPEAR != 0) :
            PAGINAS_A_SCRAPEAR = int(input("Páginas a scrapear (ingresar un número positivo):\n"))
            next 
        print(OFFSET, PAGINAS_A_SCRAPEAR,range(1 + OFFSET, PAGINAS_A_SCRAPEAR + 1 + OFFSET))
    
        for pagina in tqdm(range(1 + OFFSET, PAGINAS_A_SCRAPEAR + 1 + OFFSET)):
            url = f"https://www.idealista.com/venta-viviendas/valencia-provincia/pagina-{pagina}.htm?ordenado-por=fecha-publicacion-desc"
            dic_inmuebles = obtener_ids_inmuebles(url)
            for id_inmueble, precio in tqdm(dic_inmuebles.items()):
                if id_inmueble in inmuebles_en_bbdd:
                    if precio != inmuebles_en_bbdd[id_inmueble]:
                        actualizar_valor_inmueble(
                            conn, id_inmueble, inmuebles_en_bbdd[id_inmueble],
                            precio)
                else:
                    url_inmueble = f'https://www.idealista.com/inmueble/{id_inmueble}/'
                    for _ in range(NUM_RETRIES):
                        datos_inmueble = obtener_datos_inmueble(url_inmueble)
                        if datos_inmueble:
                            insertar_inmueble(conn, datos_inmueble)
                            break
    except Exception as e:
        print(f"Error en el proceso de scraping: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

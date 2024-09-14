import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from tqdm import tqdm
from database.connection import crear_conexion
from database.operations import obtener_listado_bbdd, actualizar_valor_inmueble, insertar_inmueble
from scrapping.scraper import obtener_ids_inmuebles, obtener_datos_inmueble, obtener_datos_inmueble_codigo_fuente

from config import NOMBRE_BBDD, NUM_RETRIES

load_dotenv()

def inicializar_scrapeops():
    from config import inicializar_scrapeops
    inicializar_scrapeops()

def scrapear_paginas(conn, inmuebles_en_bbdd, offset, paginas_a_scrapear):
    for pagina in tqdm(range(1 + offset, paginas_a_scrapear + 1 + offset)):
        url = f"https://www.idealista.com/venta-viviendas/valencia-provincia/pagina-{pagina}.htm?ordenado-por=fecha-publicacion-desc"
        dic_inmuebles = obtener_ids_inmuebles(url)
        for id_inmueble, precio in tqdm(dic_inmuebles.items()):
            if id_inmueble in inmuebles_en_bbdd:
                if precio != inmuebles_en_bbdd[id_inmueble]:
                    actualizar_valor_inmueble(conn, id_inmueble, inmuebles_en_bbdd[id_inmueble], precio)
            else:
                url_inmueble = f'https://www.idealista.com/inmueble/{id_inmueble}/'
                for _ in range(NUM_RETRIES):
                    datos_inmueble = obtener_datos_inmueble(url_inmueble)
                    if datos_inmueble:
                        insertar_inmueble(conn, datos_inmueble)
                        break

def scrapear_manualmente(conn):
    archivo_path = "./Auxiliar/datos_pagina_web.txt"
    
    # Asegurarse de que el directorio existe
    os.makedirs(os.path.dirname(archivo_path), exist_ok=True)
    
    # Borrar el contenido del archivo si existe, o crear uno nuevo
    with open(archivo_path, 'w') as file:
        pass  # Esto crea un archivo vacío o borra el contenido si ya existe
    
    print(f"Se ha creado/vaciado el archivo {archivo_path}")
    print("Por favor, pegue el código fuente HTML de la página del inmueble en el archivo.")
    input("Presione Enter cuando haya terminado...")
    
    # Leer el contenido del archivo
    with open(archivo_path, 'r', encoding='utf-8') as file:
        html = file.read()
    
    if not html.strip():
        print("El archivo está vacío. No se puede procesar.")
        return
    
    # id_inmueble = input("Ingrese el ID del inmueble:\n")
    datos_inmueble = obtener_datos_inmueble_codigo_fuente(html)#, id_inmueble)
    
    if datos_inmueble:
        insertar_inmueble(conn, datos_inmueble)

def menu_principal():
    while True:
        print("\nMenú principal:")
        print("1. Scrapear automáticamente (ScrapeOps)")
        print("2. Scrapear Manualmente")
        print("3. Salir")
        opcion = input("Seleccionar una opción: ")
        
        if opcion == "1":
            return "automatico"
        elif opcion == "2":
            return "manual"
        elif opcion == "3":
            return "salir"
        else:
            print("Opción no válida. Por favor, intentar de nuevo.")

def main():
    try:
        conn = crear_conexion(NOMBRE_BBDD)
        inmuebles_en_bbdd = obtener_listado_bbdd(conn)

        while True:
            modo = menu_principal()
            
            if modo == "automatico":
                if not scrapeops_inicializado:
                    inicializar_scrapeops()
                    scrapeops_inicializado = True
                offset = -1
                paginas_a_scrapear = -1

                while not str(offset).isdigit():
                    offset = int(input("Empezar desde la página:\n"))
                offset -= 1

                while not str(paginas_a_scrapear).isdigit() and paginas_a_scrapear != 0:
                    paginas_a_scrapear = int(input("Páginas a scrapear (ingresar un número positivo):\n"))

                scrapear_paginas(conn, inmuebles_en_bbdd, offset, paginas_a_scrapear)
            elif modo == "manual":
                scrapear_manualmente(conn)
            elif modo == "salir":
                break

    except Exception as e:
        print(f"Error en el proceso de scraping: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
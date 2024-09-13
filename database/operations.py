import json
import sqlite3
from datetime import date

def obtener_listado_bbdd(conn):
    """
    Obtiene un listado de inmuebles y sus precios desde la base de datos.

    Parámetros:
    - conn (sqlite3.Connection): Objeto de conexión a la base de datos.

    Retorna:
    - dict: Diccionario con ID de inmueble como clave y precio como valor.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id_inmueble, precio FROM inmuebles")
    return dict(cursor.fetchall())

def actualizar_valor_inmueble(conn, id_inmueble, valor_anterior, nuevo_valor):
    """
    Actualiza el valor de un inmueble en la tabla de modificaciones de valor.

    Parámetros:
    - conn (sqlite3.Connection): Objeto de conexión a la base de datos.
    - id_inmueble (str): ID del inmueble.
    - valor_anterior (int): Valor anterior del inmueble.
    - nuevo_valor (int): Nuevo valor del inmueble.

    Ejecuta:
    - Comando SQL para insertar un registro en la tabla 'modificaciones_valor_inmuebles'.
    """
    cursor = conn.cursor()
    fecha = date.today()
    cursor.execute(
        '''
        INSERT INTO modificaciones_valor_inmuebles 
        (id_inmueble, precio_actual, precio_anterior, fecha_actualizacion)
        VALUES (?, ?, ?, ?)
    ''', (id_inmueble, nuevo_valor, valor_anterior, fecha))
    conn.commit()

def insertar_inmueble(conn, diccionario):
    """
    Inserta un nuevo inmueble en la tabla 'inmuebles'.

    Parámetros:
    - conn (sqlite3.Connection): Objeto de conexión a la base de datos.
    - diccionario (dict): Diccionario con los datos del inmueble.

    Ejecuta:
    - Comando SQL para insertar un nuevo inmueble en la tabla 'inmuebles'.
    """
    cursor = conn.cursor()
    claves = list(diccionario.keys())
    valores = list(diccionario.values())

    # Convertir la lista de datos_ubicacion a una cadena JSON
    if 'datos_ubicacion' in diccionario:
        valores[claves.index('datos_ubicacion')] = json.dumps(
            diccionario['datos_ubicacion'])

    placeholders = ', '.join(['?' for _ in claves])
    consulta = f"INSERT INTO inmuebles ({', '.join(claves)}) VALUES ({placeholders})"

    try:
        cursor.execute(consulta, valores)
        conn.commit()
        print("Inmueble insertado correctamente.")
    except sqlite3.Error as e:
        print(f"Error al insertar inmueble: {e}")

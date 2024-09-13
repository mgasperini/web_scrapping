import json
import sqlite3
from datetime import date


def obtener_listado_bbdd(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id_inmueble, precio FROM inmuebles")
    return dict(cursor.fetchall())


def actualizar_valor_inmueble(conn, id_inmueble, valor_anterior, nuevo_valor):
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

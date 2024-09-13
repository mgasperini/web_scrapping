import sqlite3

def crear_conexion(nombre_bd):
    """
    Crea una conexión a la base de datos SQLite con el nombre dado.

    Parámetros:
    - nombre_bd (str): Nombre del archivo de la base de datos.

    Retorna:
    - conexion (sqlite3.Connection) o None: Objeto de conexión si la conexión es exitosa, o None si ocurre un error.
    """
    try:
        conexion = sqlite3.connect(nombre_bd)  # Establece la conexión con la base de datos
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")  # Imprime el error si ocurre
        return None

def crear_bbdd(cursor):
    """
    Crea las tablas necesarias en la base de datos si no existen.

    Parámetros:
    - cursor (sqlite3.Cursor): Objeto cursor para ejecutar comandos SQL.

    Ejecuta:
    - Comando SQL para crear la tabla 'inmuebles' si no existe.
    - Comando SQL para crear la tabla 'modificaciones_valor_inmuebles' si no existe.
    """
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

    # Crear la tabla modificaciones_valor_inmuebles si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modificaciones_valor_inmuebles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_inmueble TEXT,
            precio_actual INT,
            precio_anterior INT,
            fecha_actualizacion DATE,
            FOREIGN KEY (id_inmueble) REFERENCES inmuebles (id_inmueble)
        )
    ''')

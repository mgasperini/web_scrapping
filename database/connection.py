import sqlite3


def crear_conexion(nombre_bd):
    try:
        conexion = sqlite3.connect(nombre_bd)
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None


def crear_bbdd(cursor):
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

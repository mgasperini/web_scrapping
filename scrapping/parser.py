import re

def parsear_ubicacion(lista_datos):
    """
    Parsea una lista de datos de ubicación y devuelve un diccionario con las claves correspondientes.

    Parámetros:
    - lista_datos (list of str): Lista de cadenas que representan diferentes niveles de ubicación.

    Retorna:
    - dict: Un diccionario con las claves 'Direccion', 'Barrio', 'Distrito', 'Ciudad', 'Comarca', 'Provincia', 
            dependiendo de la longitud de `lista_datos` y la presencia de comas en los datos.
    """
    match len(lista_datos):
        case 6:
            if len(lista_datos[-1].strip()) > 1:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Barrio': lista_datos[2].strip() + ", " + lista_datos[1].strip(),
                    'Distrito': lista_datos[3].strip(),
                    'Ciudad': lista_datos[4].strip(),
                    'Comarca': lista_datos[5].split(',')[0].strip(),
                    'Provincia': lista_datos[5].split(',')[1].strip()
                }
            else:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Barrio': lista_datos[1].strip(),
                    'Distrito': lista_datos[2].strip(),
                    'Ciudad': lista_datos[3].strip(),
                    'Provincia': lista_datos[4].split(',')[0].strip()
                }
        case 5:
            if len(lista_datos[-1].strip()) > 1:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Barrio': lista_datos[1].strip(),
                    'Distrito': lista_datos[2].strip(),
                    'Ciudad': lista_datos[3].strip(),
                    'Comarca': lista_datos[4].split(',')[0].strip(),
                    'Provincia': lista_datos[4].split(',')[1].strip()
                }
            else:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Barrio': lista_datos[1].strip(),
                    'Distrito': lista_datos[2].strip(),
                    'Ciudad': lista_datos[3].strip(),
                    'Provincia': lista_datos[4].split(',')[0].strip()
                }
        case 4:
            if len(lista_datos[-1].strip()) > 1:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Distrito': lista_datos[1].strip(),
                    'Ciudad': lista_datos[2].strip(),
                    'Comarca': lista_datos[3].split(',')[0].strip(),
                    'Provincia': lista_datos[3].split(',')[1].strip()
                }
            else:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Distrito': lista_datos[1].strip(),
                    'Ciudad': lista_datos[2].strip(),
                    'Provincia': lista_datos[3].split(',')[0].strip()
                }
        case 3:
            if len(lista_datos[-1].strip()) > 1:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Ciudad': lista_datos[1].strip(),
                    'Comarca': lista_datos[2].split(',')[0].strip(),
                    'Provincia': lista_datos[2].split(',')[1].strip()
                }
            else:
                return {
                    'Direccion': lista_datos[0].strip(),
                    'Ciudad': lista_datos[1].strip(),
                    'Provincia': lista_datos[2].split(',')[0].strip()
                }
        case 1:
            if len(lista_datos[-1].strip()) > 1:
                return {
                    'Comarca': lista_datos[0].split(',')[0].strip(),
                    'Provincia': lista_datos[0].split(',')[1].strip()
                }
            else:
                return {'Provincia': lista_datos[0].split(',')[0].strip()}
        case _:
            return {'datos_ubicacion': lista_datos}

def clasificar_y_parsear_caracteristicas(lista_caracteristicas, nombre_inmueble):
    """
    Clasifica y parsea una lista de características de una propiedad en un diccionario con claves estandarizadas.

    Parámetros:
    - lista_caracteristicas (list of str): Lista de características de la propiedad en formato de texto.

    Retorna:
    - dict: Un diccionario con las claves de características estandarizadas y sus valores extraídos de `lista_caracteristicas`.
    """
    # Diccionario para guardar todas las características
    caracteristicas = {
        "tipo_propiedad": None,
        "plantas": None,
        "metros_construidos_m2": None,
        "habitaciones": None,
        "baños": None,
        "parcela_m2": None,
        "garaje": None,
        "estado": None,
        "año_construcción": None,
        "calefaccion": None,
        "orientacion": None,
        "Piscina": None,
        "Jardin": None,
        "Consumo": None,
        "Emisiones": None,
        "planta_n": None,
        "ascensor": None,
    }

    # Expresiones regulares para cada tipo de característica
    regex_patterns = {
        "tipo_propiedad": r"(casa|chalet|apartamento|piso|ático|independiente|finca rústica|dúplex|estudio|torre})",
        "plantas": r"(\d+)\s*plantas?",
        "metros_construidos_m2": r"(\d+[\.\d+]*)\s*m²\s*construidos?",
        "habitaciones": r"(\d+)\s*habitaciones?",
        "baños": r"(\d+)\s*baños?",
        "parcela_m2": r"parcela de\s*(\d+[\.\d+]*)\s*m²",
        "garaje": r"plaza de garaje",
        "estado": r"(segunda mano|buen estado|nuevo|reformado)",
        "año_construcción": r"construido en\s*(\d{4})",
        "calefaccion": r"calefacción\s*(\w+)?(?:\s*:\s*(\w+))?",
        "orientacion": r"(orientación|orientacion)\s+(\w+)",
        "Piscina": r"Piscina",
        "Jardin": r"(Jardín|Jardin)",
        "Consumo": r"Consumo:\s*([\d\.]+)",
        "Emisiones": r"Emisiones:\s*([\d\.]+)",
        "planta_n": r"^Planta\s*(\d+)(?:[a-zA-Z]*)",
        "ascensor": r"\b(Con|Sin)\sascensor\b",
    }

    # Itera sobre los elementos de la lista y clasificar
    for item in lista_caracteristicas:
        for key, pattern in regex_patterns.items():
            match = re.search(pattern, item, re.IGNORECASE)
            if match:
                # Procesa el valor según la característica
                if key in ["metros_construidos_m2", "parcela_m2"]:
                    # Extrae solo el número y lo convierte a entero
                    number = re.search(r"(\d+[\.\d+]*)", match.group(0))
                    if number:
                        caracteristicas[key] = int(float(number.group(1).replace(',', '')))
                elif key in ["plantas", "habitaciones", "baños", "año_construcción"]:
                    # Extrae solo el número y lo convierte a entero
                    number = re.search(r"(\d+)", match.group(0))
                    if number:
                        caracteristicas[key] = int(number.group(1))
                elif key == "calefaccion":
                    # Extrae el tipo de calefacción
                    calefaccion = re.findall(r"(\w+)", match.group(0))[-1]
                    if (calefaccion) and (calefaccion != 'calefacción'):
                        caracteristicas[key] = calefaccion
                elif key == "garaje":
                    # Indica si tiene plaza de garaje
                    caracteristicas[key] = True
                elif key in ["Piscina", "Jardin"]:
                    # Indica si tiene piscina o jardín
                    caracteristicas[key] = True
                elif key in ["Consumo", "Emisiones"]:
                    # Convierte el valor a float
                    caracteristicas[key] = float(match.group(1))
                elif key == "orientacion":
                    # Extrae orientación
                    orientacion = re.findall(r"(\w+)", match.group(0))[-1]
                    if orientacion:
                        caracteristicas[key] = orientacion
                elif key == 'ascensor':
                    # Indica si tiene ascensor
                    ascensor = match.group(1).lower() == "con"
                    if ascensor:
                        caracteristicas[key] = ascensor
                elif key == 'planta_n':
                    # Extrae el número de planta
                    n_planta = match.group(1)
                    if n_planta:
                        caracteristicas[key] = n_planta
                else:
                    # Para otros casos, solo almacenar el valor encontrado
                    caracteristicas[key] = match.group(0)
                break
        if not caracteristicas['tipo_propiedad']:
            try:
                caracteristicas['tipo_propiedad'] = re.search(regex_patterns['tipo_propiedad'],nombre_inmueble,re.IGNORECASE)[0]
            except:
                pass
    return caracteristicas

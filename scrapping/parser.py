import re


def parsear_ubicacion(lista_datos):
    match len(lista_datos):
        case 6:
            if len(lista_datos[-1].strip()) > 1:
                return {
                    'Direccion':
                    lista_datos[0].strip(),
                    'Barrio':
                    lista_datos[2].strip() + ", " + lista_datos[1].strip(),
                    'Distrito':
                    lista_datos[3].strip(),
                    'Ciudad':
                    lista_datos[4].strip(),
                    'Comarca':
                    lista_datos[5].split(',')[0].strip(),
                    'Provincia':
                    lista_datos[5].split(',')[1].strip()
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


def clasificar_y_parsear_caracteristicas(lista_caracteristicas):
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
        "tipo_propiedad":
        r"(casa|chalet|apartamento|piso|ático|independiente)",
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

    # Iterar sobre los elementos de la lista y clasificar
    for item in lista_caracteristicas:
        for key, pattern in regex_patterns.items():
            match = re.search(pattern, item, re.IGNORECASE)
            if match:
                # Procesar el valor según la característica
                if key in ["metros_construidos_m2", "parcela_m2"]:
                    # Extraer solo el número y convertirlo a entero
                    number = re.search(r"(\d+[\.\d+]*)", match.group(0))
                    if number:
                        caracteristicas[key] = int(
                            float(number.group(1).replace(',', '')))
                elif key in [
                        "plantas", "habitaciones", "baños", "año_construcción"
                ]:
                    # Extraer solo el número y convertirlo a entero
                    number = re.search(r"(\d+)", match.group(0))
                    if number:
                        caracteristicas[key] = int(number.group(1))
                elif key == "calefaccion":
                    # Extraer el tipo de calefacción
                    calefaccion = re.findall(r"(\w+)", match.group(0))[-1]
                    if calefaccion:
                        caracteristicas[key] = calefaccion
                elif key == "garaje":
                    # Indicar si tiene plaza de garaje
                    caracteristicas[key] = True
                elif key in ["Piscina", "Jardin"]:
                    # Indicar si tiene piscina o jardín
                    caracteristicas[key] = True
                elif key in ["Consumo", "Emisiones"]:
                    # Convertir el valor a float
                    caracteristicas[key] = float(match.group(1))
                elif key == "orientacion":
                    # Extraer orientación
                    orientacion = re.findall(r"(\w+)", match.group(0))[-1]
                    if orientacion:
                        caracteristicas[key] = orientacion
                elif key == 'ascensor':
                    ascensor = match.group(1).lower() == "con"
                    if ascensor:
                        caracteristicas[key] = ascensor
                elif key == 'planta_n':
                    n_planta = match.group(1)
                    if n_planta:
                        caracteristicas[key] = n_planta
                else:
                    # Para otros casos, solo almacenar el valor encontrado
                    caracteristicas[key] = match.group(0)
                break

    return caracteristicas

def eliminacion_mejora(text):
    # ? Función que me verifica si el tipo de dato parametrizado es el que ingresa a la función
    if isinstance(text, str) and text[21] == '5':
        cadena = text[:21] + '000000000'
        return cadena 
    else:
        return None  # Devuelve None si el valor no es un string
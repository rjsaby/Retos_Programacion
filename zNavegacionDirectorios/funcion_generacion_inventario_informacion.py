import os, sys
import pandas as pd
from pathlib import Path
import datetime

def generacion_inventario_informacion(ruta_base, ruta_salida_xlsx, nombre_xlsx):

    # TODO: Añadir el directorio A al sys.path, esto para llamar a una función contenida en otro directorio, ambas dentro de la misma carpeta raiz
    sys.path.append(os.path.abspath('../zReporteRadicados'))

    # ** Importar Librerías Propias
    from funcion_personalizacion_tablas import personalizacion_tablas

    ruta_base = ruta_base
    ruta_salida_xlsx = ruta_salida_xlsx
    nombre_xlsx = nombre_xlsx

    ruta_archivo = []
    nomArchivo = []
    extensionArchivo = []
    pesoArchivoMbs = []
    fechaCreacionArchivo = []
    fuenteArchivo = []

    extensiones = ['.shp','.xls','.xlsx','.csv','.txt','.doc','.docx','.dwg','.dxf','.pdf', '.geojson', '.json', '.xtf', '.ili', '.jpg','.mp4','.jpeg','.png','.pptx,','.html','.py','.sql'
        '.SHP','.XLS','.XLSX','.CSV','.TXT','.DOC','.DOCX','.DWG','.DXF','.PDF', '.GEOJSON', '.JSON', '.XTF', '.ILI', '.JPG','.MP4','.JPEG','.PNG','.PPTX','.HTML','.PY','.SQL']
    
    columnas = ['ruta_archivo','nomArchivo','extensionArchivo','pesoArchivoMbs','fechaCreacionArchivo','fuenteArchivo']

    for ruta, directorio, archivo in os.walk(ruta_base):
        for nombre_archivo in archivo:        
            ruta_archivos = os.path.join(ruta, nombre_archivo)
            rArchivos = Path(ruta_archivos)
            extensionArchivos = rArchivos.suffix
            for extBase in extensiones:
                if extBase == rArchivos.suffix:
                    ruta_archivo.append(ruta_archivos)
                    nomArchivo.append(rArchivos.stem)
                    fuenteArchivo.append(ruta_archivos.split('\\')[2])                
                    extensionArchivo.append(rArchivos.suffix)
                    pesoArchivoMbs.append((os.path.getsize(rArchivos))/1000000)
                    # ** DE UT a Formato Fecha
                    marca_tiempo_creacion = os.path.getctime(rArchivos)
                    fecha_creacion = datetime.datetime.fromtimestamp(marca_tiempo_creacion)
                    fecha_formateada = fecha_creacion.strftime('%Y-%m-%d')
                    fechaCreacionArchivo.append(fecha_formateada)
                    print("Se documenta {0}".format(rArchivos.name))

    for ruta, directorios, archivo in os.walk(ruta_base):
        for nombre_directorio in directorios:        
            ruta_directorios = os.path.join(ruta, nombre_directorio)
            rDirectorios = Path(ruta_directorios)
            if rDirectorios.suffix == '.gdb':
                    ruta_archivo.append(ruta_directorios)                
                    nomArchivo.append(rDirectorios.stem)
                    fuenteArchivo.append(ruta_directorios.split('\\')[2])
                    extensionArchivo.append(rDirectorios.suffix)
                    pesoArchivoMbs.append((os.path.getsize(rDirectorios))/1000000)
                    # ** DE UT a Formato Fecha
                    marca_tiempo_creacion = os.path.getctime(rDirectorios)
                    fecha_creacion = datetime.datetime.fromtimestamp(marca_tiempo_creacion)
                    fecha_formateada = fecha_creacion.strftime('%Y-%m-%d')
                    fechaCreacionArchivo.append(fecha_formateada)
                    print("Se documenta {0}".format(rDirectorios.name))    

    lista_archivos_recibidos = list(zip(ruta_archivo, nomArchivo, extensionArchivo, pesoArchivoMbs, fechaCreacionArchivo, fuenteArchivo))
    df_lista_archivos_recibidos = pd.DataFrame(lista_archivos_recibidos, columns = columnas)
    df_lista_archivos_recibidos.head(50)

    df_lista_archivos_recibidos["tipoInsumo"] = None

    # ** Documental
    df_lista_archivos_recibidos.loc[(df_lista_archivos_recibidos['tipoInsumo'].isnull()) & 
                                    ((df_lista_archivos_recibidos['extensionArchivo'] == '.pdf') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.PDF') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.doc') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.pptx') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.PPTX') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.DOC') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.docx') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.DOCX')), 'tipoInsumo'] = 'Documental'

    # ** Geográfica
    df_lista_archivos_recibidos.loc[(df_lista_archivos_recibidos['tipoInsumo'].isnull()) & 
                                    ((df_lista_archivos_recibidos['extensionArchivo'] == '.gdb') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.GDB') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.shp') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.SHP') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.geojson') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.GEOJSON')), 'tipoInsumo'] = 'Geografica'

    # ** Alfanumérica
    df_lista_archivos_recibidos.loc[(df_lista_archivos_recibidos['tipoInsumo'].isnull()) & 
                                    ((df_lista_archivos_recibidos['extensionArchivo'] == '.xlsx') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.XLSX') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.xls') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.XLS') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.json') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.JSON') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.xtf') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.XTF') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.ili') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.ILI') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.txt') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.TXT') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.csv') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.CSV') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.dwg') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.DWG') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.dxf') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.DXF')), 'tipoInsumo'] = 'Alfanumerica'
    
    # ** Multimedia
    df_lista_archivos_recibidos.loc[(df_lista_archivos_recibidos['tipoInsumo'].isnull()) & 
                                    ((df_lista_archivos_recibidos['extensionArchivo'] == '.jpg') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.JPG') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.mp4') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.MP4') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.JPEG') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.PNG') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.png') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.HTML') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.html') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.jpeg')), 'tipoInsumo'] = 'Multimedia'
    
    # ** Desarrollo
    df_lista_archivos_recibidos.loc[(df_lista_archivos_recibidos['tipoInsumo'].isnull()) & 
                                    ((df_lista_archivos_recibidos['extensionArchivo'] == '.py') |
                                    (df_lista_archivos_recibidos['extensionArchivo'] == '.sql')), 'tipoInsumo'] = 'Desarrollo'
    
    df_lista_archivos_recibidos.to_excel(os.path.join(ruta_salida_xlsx,nombre_xlsx))

    # TODO: Ejecución de la función que personaliza la tabla de salida
    personalizacion_tablas(os.path.join(ruta_salida_xlsx,nombre_xlsx))
    
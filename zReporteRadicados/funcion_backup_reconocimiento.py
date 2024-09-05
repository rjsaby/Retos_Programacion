# ? Se usa para determina la fecha de ejecución del proceso dentro del export de los resultados estadísticos
from datetime import datetime as dt

import os, sys
import zipfile

from pathlib import Path

import shutil

def generacion_backup(ruta_origen:str):

    fecha_actual = dt.now()
    fecha_directorio = str(fecha_actual.strftime("%Y%m%d"))

    # * Añadir el directorio A al sys.path, esto para llamar a una función contenida en otro directorio, ambas dentro de la misma carpeta raiz
    sys.path.append(os.path.abspath('../zNavegacionDirectorios'))

    # ** Importar Librerías Propias
    from funcion_generacion_inventario_informacion import generacion_inventario_informacion

    # TODO: Proceso de Copia Nube a Local
    R = Path(ruta_origen)
    ruta_destino = r"C:\BUp"
    directorio_destino = r"C:\BUp"
    ruta_destino = os.path.join(directorio_destino, R.name)

    try:
        shutil.copytree(src = ruta_origen, dst = ruta_destino)
        print(f"Se Copia de Local {ruta_origen} a Nube {ruta_destino}")
    except OSError as e:
        print(f"Se presente el siguiente error {e}")

    # TODO: Proceso de Compresión a ruta Local (1)
    ruta_origen = os.path.join(directorio_destino, R.name)
    nombre_directorio_bUP = ((R.name).replace(' ','_'))

    # *** TODO: Generación Inventario ***
    nombre_xlsx = fecha_directorio+'_'+nombre_directorio_bUP+'_'+'Inventario_Informacion.xlsx'
    generacion_inventario_informacion(ruta_origen, ruta_origen, nombre_xlsx)
    print("Se genera inventario")     

    # TODO: Proceso de Compresión a ruta Local (2)
    nombre_directorio_origen_comprimido = fecha_directorio+'_'+nombre_directorio_bUP+'.zip'
    ruta_compresion = os.path.join(directorio_destino, nombre_directorio_origen_comprimido)

    with zipfile.ZipFile(ruta_compresion, 'w') as zipf:
        for raiz, _, archivos in os.walk(ruta_origen):          
            for archivo in archivos:
                ruta_completa = os.path.join(raiz, archivo)
                # * Ruta completa, directorio origen
                ruta_en_zip = os.path.relpath(ruta_completa, ruta_origen)
                zipf.write(ruta_completa, ruta_en_zip)

    # TODO: Proceso de Copia a Nube
    ruta_origen = ruta_compresion
    ruta_destino = r"G:\Mi unidad\Equipo_Consolidacion\Hitos\BackUP" + '\\' + nombre_directorio_origen_comprimido
    shutil.copy(src = ruta_origen, dst = ruta_destino)
    print(f"Se Copia de Local {ruta_origen} a Nube {ruta_destino}")

    # TODO: Borrar el archivo
    E = Path(ruta_origen)    
    if E.exists():
        E.unlink()
        print(f"Archivo {E.name} eliminado.")
    else:
        print("El archivo no existe.")

    ruta_origen = os.path.join(directorio_destino, R.name)

    # TODO: Borrar el archivo
    E = Path(ruta_origen)    
    if E.exists():
        shutil.rmtree(E)
        print(f"Directorio {E.name} eliminado.")
    else:
        print("El archivo no existe.")
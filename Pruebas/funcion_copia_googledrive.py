import pandas as pd
import os
import seaborn as sns
import shutil

os.environ["CRYPTOGRAPHY_OPENSSL_NO_LEGACY"] = "yes"

# ? Se usa para generar gráficos
import matplotlib.pyplot as plt

# ? Se usa para determina la fecha de ejecución del proceso dentro del export de los resultados estadísticos
from datetime import datetime

# ? Conexión a BD Postgres. Se usa dado que pandas no acepta sino este paquete para la conexión.
from sqlalchemy import create_engine, text

from datetime  import datetime as dt

from arcgis.features import GeoAccessor, GeoSeriesAccessor
import arcpy

from pathlib import Path

def migracion_googledrive(dLocal, dGoogleDrive):
    for rutas, directorios, archivos in os.walk(dLocal):
        for nombre_directorio in directorios:
            ruta_archivos_origen = os.path.join(rutas, nombre_directorio)        
            rDirectorios = Path(ruta_archivos_origen)        
            if rDirectorios.suffix == '.gdb':
                parte_deseada = rDirectorios.relative_to(rDirectorios.parent.parent)
                ruta_salida = os.path.join(dGoogleDrive, parte_deseada)

                # * Se elimina el directorio de destino si ya existe
                if os.path.exists(ruta_salida):
                    shutil.rmtree(ruta_salida)

                arcpy.env.workspace = str(rDirectorios.parent)
                arcpy.Copy_management(rDirectorios.name, ruta_salida)
                print(f"Se copia BD {rDirectorios.name}")

                arcpy.ClearWorkspaceCache_management()

    for rutas, directorios, archivos in os.walk(dLocal):
        for nombre_archivo in archivos:
            ruta_archivos_origen = os.path.join(rutas, nombre_archivo)        
            rDirectorios = Path(ruta_archivos_origen)
            if rDirectorios.suffix == '.pdf':
                parte_deseada = rDirectorios.relative_to(rDirectorios.parent.parent)
                ruta_salida = os.path.join(dGoogleDrive, parte_deseada)
                shutil.copy(src=rDirectorios,dst=ruta_salida)
                print(f"Se copia archivo PDF {rDirectorios.name}")
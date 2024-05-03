# Rodian Jasef Saby Sanabria
# 2024-04-30

print("CONTINUA PROCESO")

"""
    Importación de Librerías
"""

import pandas as pd, os, arcpy, zipfile, shutil
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from datetime import datetime

print("1. Se exportan Librerías")

"""
    Variables Globales
"""

arcpy.env.overwriteOutput = True

fecha_actual = datetime.now()
fecha_archivo = str(fecha_actual.strftime("%Y-%m-%d"))

RUTA_SHP = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\zApoyo_A_Equipos\zApoyoEquipoSIG\1.Geo_Gestion_Cambios\zShps"
RUTA_GESTION = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\zApoyo_A_Equipos\zApoyoEquipoSIG\1.Geo_Gestion_Cambios"
RUTA_BDCONSOLIDADA = r"C:\Users\rodian.saby\OneDrive\Documentos\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E1_Alistamiento_Diagnostico\3_Disposicion\1.BD_Consolidada\BD_Consolidada_Lote4.gdb"
# ** Se define la ruta del proyecto de PRO (extensión .aprx)
RUTA_PROYECTO_PRO = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\1.GIS\1.2.PRO\RAISS_Lote_4\RAISS_Lote_4.aprx"

print("2. Se parametrizan variables globales")

"""
    Export de Layout
"""

# ** Ruta de exportación del JPEG

NOMBRE = ' Gestión Cambios - Equipo SIG'

nombre_jpeg = str(fecha_archivo) + NOMBRE

# ** Se establece en el entorno de trabajo
arcpy.env.workspace = RUTA_PROYECTO_PRO

# ** Se accede por código al proyecto .aprx del proyecto, se crea un objeto de tipo proyecto
aprx = arcpy.mp.ArcGISProject(RUTA_PROYECTO_PRO)

# ** Se listan los Layouts generados en el proyecto
for i in aprx.listLayouts():
    print(f'Nombre Layout: {i.name}')
    if i.name == "Gestión Cambios - Equipo SIG":
        layout = i
        print(f"Se almacena en variable el layout {layout.name}")

ruta_salida_jpeg = os.path.join(RUTA_GESTION, nombre_jpeg)

# ** Parametrización de la resolución
resolution = 300

layout.exportToJPEG(ruta_salida_jpeg, resolution = resolution, jpeg_quality = 100)
print(f"Se exporta JPEG {nombre_jpeg}")

print("4. Se exporta layout")

"""
    Compresión SHP
"""
print("inicia")

NOMBRE_ARCHIVO_ZIP = "Progreso_Gestion_Cambios.zip"

directorio_archivo_compresion = os.path.join(RUTA_GESTION, NOMBRE_ARCHIVO_ZIP)

with zipfile.ZipFile(directorio_archivo_compresion, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(RUTA_SHP):
        for file in files:
            ruta_completa = os.path.join(root, file)
            rel_path = os.path.relpath(ruta_completa, RUTA_SHP)
            zipf.write(ruta_completa, rel_path)
            print(f"Se comprime exitosamente el directorio {file}")

print("5. Se comprime SHP")

"""
    Copia resultados a Google Drive
"""
ruta_destino_archivo = r"G:\Mi unidad\Equipo_Consolidacion\Hitos\zApoyo_A_Equipos\zApoyoEquipoSIG\1.Geo_Gestion_Cambios"

try:
    def copia_google_drive(a: str, b: str):

        NOMBRE_ARCHIVO_ORIGEN = a
        EXTENSION = b

        if EXTENSION == 'zip':
            
            archivo_origen = NOMBRE_ARCHIVO_ORIGEN
            archivo_destino = NOMBRE_ARCHIVO_ORIGEN

            directorio_origen = os.path.join(RUTA_GESTION, archivo_origen)
            directorio_destino = os.path.join(ruta_destino_archivo, archivo_destino)            

            shutil.copy(src = directorio_origen, dst = directorio_destino)
        elif EXTENSION == 'jpg':

            archivo_origen = str(fecha_archivo) + NOMBRE_ARCHIVO_ORIGEN
            archivo_destino = str(fecha_archivo) + NOMBRE_ARCHIVO_ORIGEN

            directorio_origen = os.path.join(RUTA_GESTION, archivo_origen)
            directorio_destino = os.path.join(ruta_destino_archivo, archivo_destino)

            shutil.copy(src = directorio_origen, dst = directorio_destino)
        else:
            print("No existe correspondencia con la extensión de archivo")
except Exception as e:
    # **Mensaje general de error
    print("Se ha producido un error:", e)
finally:
    print("El proceso termina sin contratiempos")

archivo_jpeg = " Gestión Cambios - Equipo SIG.jpg"
archivo_zip = "Progreso_Gestion_Cambios.zip"

extension_jpg = "jpg"
extension_zip = "zip"

copia_google_drive(archivo_jpeg, extension_jpg)
copia_google_drive(archivo_zip, extension_zip)
print("Se ejecuta correctamente la función")

print("6. Se copia en Nube Google")

print("FINALIZA PROCESO")
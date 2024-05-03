# Rodian Jasef Saby Sanabria
# 2024-04-30

print("INICIA PROCESO")

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
    Lectura de Sheet
"""

# ? **** Lectura de Sheet y transformación a DataFrame
sheet_name = 'CONTROL_DE_CAMBIOS'
sheet_id = '1n_t9qtwLeIklH5UFoH9iDPiAa6uN4HZeR1-atsKTYeU'

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

control_cambios_esig_original = pd.read_csv(url)
columnas_seleccion = ['terreno_codigo', 
    'Nombre', 
    'EDICION',
    'POSIBLE SERVIDUMBRE', 
    'FECHA EDITOR',
    'OBSERVACIONES EDITOR',
    'REVISADO',
    'FECHA REVISOR',
    'OBSERVACIONES REVISOR',
    'ESTADO DE EDICION']

control_cambios_esig_filtro = control_cambios_esig_original[columnas_seleccion]

# ? **** Edición de dominios dentro del DataFrame, dominios asociados a la Edición SIG

control_cambios_esig_filtro.loc[control_cambios_esig_filtro['EDICION'] == 'REQUIERE VISITA DE CAMPO', 'EDICION'] = 'Requiere visita campo'
control_cambios_esig_filtro.loc[control_cambios_esig_filtro['EDICION'] == 'SI, (EDICION GEOGRAFICA)', 'EDICION'] = 'Con edición geo'
control_cambios_esig_filtro.loc[control_cambios_esig_filtro['EDICION'] == 'NO, (NO REQUIERE AJUSTE GEOGRAFICO)', 'EDICION'] = 'No requiere ajuste geo'

# ? **** Generación de DataFrame Espacial y cruce con información de Gestión de Cambios SIG

CAPA_TERRENOS_R = 'Analitica_UT_Consolidada\R_TERRENO'
CAPA_TERRENOS_U = 'Analitica_UT_Consolidada\\U_TERRENO'
SHP = '_Gestion_Cambios_SIG.shp'

nombre_shp = str(fecha_archivo) + SHP

capa_terrenos_rurales = os.path.join(RUTA_BDCONSOLIDADA, CAPA_TERRENOS_R)
capa_terrenos_urbanos = os.path.join(RUTA_BDCONSOLIDADA, CAPA_TERRENOS_U)

# ** Terrenos Rurales
df_terreno_rural = pd.DataFrame.spatial.from_featureclass(capa_terrenos_rurales)
df_terreno_rural.head()
# ** Terrenos Urbanos
df_terreno_urbano = pd.DataFrame.spatial.from_featureclass(capa_terrenos_urbanos)

# ** Selección de columnas
columnas_selecciones = ['CODIGO',
                        'CODIGO_ANTERIOR',
                        'SHAPE']

# ** DF Terrenos Rurales, Urbanos
df_terreno_rural_reducido = df_terreno_rural[columnas_selecciones]
df_terreno_urbano_reducido = df_terreno_urbano[columnas_selecciones]

# ** Concatenación de dataframes
df_terrenos = pd.concat([df_terreno_rural_reducido, df_terreno_urbano_reducido])

# ** Terrenos Gestionados SIG Espacializados
df_terrenos_gestion_sig = pd.merge(df_terrenos, control_cambios_esig_filtro, left_on='CODIGO', right_on='terreno_codigo', how='inner')

# ? **** Exportación de resultados tanto a FileGDB como a SHP

NOMBRE_CAPA_SALIDA = f"Analitica_UT_Consolidada\\{'terrenos_con_control_de_cambios_esig'.upper()}"
ruta_salida_terrenos_contro_cambios = os.path.join(RUTA_BDCONSOLIDADA, NOMBRE_CAPA_SALIDA)

df_terrenos_gestion_sig.spatial.to_featureclass(location=ruta_salida_terrenos_contro_cambios)
print(f"Se exporta la capa {NOMBRE_CAPA_SALIDA}")

ruta_salida_shp = os.path.join(RUTA_SHP, nombre_shp)
df_terrenos_gestion_sig.spatial.to_featureclass(location=ruta_salida_shp, overwrite=True)
print(f"Se exporta la capa {nombre_shp}")

print("3. Se migra de Sheet a DataFrame")

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
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
RUTA_BDCONSOLIDADA = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E1_Alistamiento_Diagnostico\3_Disposicion\1.BD_Consolidada\BD_Consolidada_Lote4.gdb"
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

# ? **** Código para evitar el Slice
control_cambios_esig_filtro = control_cambios_esig_filtro.copy()

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


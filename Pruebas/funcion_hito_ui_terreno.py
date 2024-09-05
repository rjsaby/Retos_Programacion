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

# ** Librerías propias

def hito_ui_terreno():
    estandarizacion_columnas_terrenos = ['codigo', 'zona_predio', 'area_ha_cmt12','SHAPE']
estandarizacion_columnas_terreno_hito = ['codigo','ID_UI','Zona_UI','Departamento_UI','Municipio_UI','Meta_Hito']

df_rel_terrenos_ui = pd.DataFrame.spatial.from_table(RUTA_REL_TERRENOS_UI)
df_ui = pd.DataFrame.spatial.from_featureclass(RUTA_UI)

df_terrenos = pd.DataFrame.spatial.from_featureclass(RUTA_CAPA_TERRENOS)

# TODO: Generacion Campo Zona
df_terrenos = df_terrenos.copy()

df_terrenos['codigo_zona'] = df_terrenos['codigo'].str[5:7]
df_terrenos['zona_predio'] = None

df_terrenos.loc[df_terrenos['codigo_zona'] == '01', 'zona_predio'] = 'Urbano'
df_terrenos.loc[df_terrenos['codigo_zona'] == '00', 'zona_predio'] = 'Rural'
df_terrenos.loc[(df_terrenos['codigo_zona'] != '00') & (df_terrenos['codigo_zona'] != '01'), 'zona_predio'] = 'Corregimientos Urbanos'

df_terrenos = df_terrenos[estandarizacion_columnas_terrenos]

pd_terreno_hito = pd.merge(left=df_rel_terrenos_ui,
    right=df_ui,
    left_on='id_ui',
    right_on='ID_UI',
    how='left')

df_terreno_hito = pd_terreno_hito[estandarizacion_columnas_terreno_hito]

df_estadistico_terreno_hito =pd.merge(left=df_terreno_hito,
    right=df_terrenos,
    on='codigo',
    how='inner')

return df_estadistico_terreno_hito
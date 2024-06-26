import pandas as pd
import os
import seaborn as sns

os.environ["CRYPTOGRAPHY_OPENSSL_NO_LEGACY"] = "yes"

# ? Se usa para generar gráficos
import matplotlib.pyplot as plt

import shutil

# ? Se usa para determina la fecha de ejecución del proceso dentro del export de los resultados estadísticos
from datetime import datetime as dt

# ? Conexión a BD Postgres. Se usa dado que pandas no acepta sino este paquete para la conexión.
from sqlalchemy import create_engine, text

from datetime import datetime as dt

from arcgis.features import GeoAccessor, GeoSeriesAccessor
import arcpy

from pathlib import Path

import pandas as pd

# ** Librerías propias

def xlsx_avance_edicion_gis():
    fecha_actual = dt.now()
    fecha_estandarizada = str(fecha_actual.strftime("%Y%m%d"))


    XLSX_ESTADISTICOS = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\O_Apoyo_Construccion_UIntervencion\UI_Finales\Estadisticos\indicadores_base_ui_lote_4.xlsx"

    DIRECTORIO_XLSX = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_6_Indicador_Edicion_Geografica\zReportes\Seguimiento_Diario"
    ARCHIVO_XLSX = fecha_estandarizada+'_avance_edicios_GIS.xlsx'
    RUTA_XLSX = os.path.join(DIRECTORIO_XLSX, ARCHIVO_XLSX)

    dict_rutas_estadisticos = {'ESTADISTICOS_MARIA':r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_6_Indicador_Edicion_Geografica\zReportes\seguimiento_edicionGeo_MariaLaBaja.xlsx",
        'ESTADISTICOS_REPELON':r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_6_Indicador_Edicion_Geografica\zReportes\seguimiento_edicionGeo_Repelon.xlsx",
        'ESTADISTICOS_BARANOA':r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_6_Indicador_Edicion_Geografica\zReportes\seguimiento_edicionGeo_Baranoa.xlsx"}

    columnas_estadisticos = ['Hito','Area_Ha_CMT12','Area_Ha_Contractual']
    columnas_ordenadas = ['Hito',
        'Area_Ha_CTM12',
        'Area_Ha_Contractual',
        'area_editada_MariaLaBaja',
        '%_avance_MariaLaBaja',
        'area_editada_Repelon',
        '%_avance_Repelon',
        'area_editada_Baranoa',
        '%_avance_Baranoa']

    nSheet_estadisticoXHito = 'Area_Editada_X_Hito'

    df_estadisticos = pd.read_excel(XLSX_ESTADISTICOS, sheet_name="hitos_por_asignacion")
    df_estadisticos = df_estadisticos[columnas_estadisticos].rename(columns={'Area_Ha_CMT12':'Area_Ha_CTM12'})

    dataframe = {}

    for llave, valor in dict_rutas_estadisticos.items():
        df = pd.read_excel(valor, sheet_name=nSheet_estadisticoXHito)
        dataframe[llave] = df

    for dframe, df in dataframe.items():
        df_estadisticos = pd.merge(left=df_estadisticos, right=df, left_on="Hito", right_on="Meta_Hito", how="left", suffixes=('', f'_{dframe}'))

    columnas_unificacion = ['Hito','Area_Ha_CTM12',
                            'Area_Ha_Contractual',
                            'area_editada_MariaLaBaja',
                            'area_editada_Repelon',
                            'area_editada_Baranoa']

    df_estadisticos_estandarizados = df_estadisticos[columnas_unificacion]
    df_estadisticos_estandarizados = df_estadisticos_estandarizados.fillna(0)

    df_estadisticos_estandarizados['%_avance_MariaLaBaja'] = (df_estadisticos_estandarizados['area_editada_MariaLaBaja']/df_estadisticos_estandarizados['Area_Ha_CTM12']*100).round(2)
    df_estadisticos_estandarizados['%_avance_Repelon'] = (df_estadisticos_estandarizados['area_editada_Repelon']/df_estadisticos_estandarizados['Area_Ha_CTM12']*100).round(2)
    df_estadisticos_estandarizados['%_avance_Baranoa'] = (df_estadisticos_estandarizados['area_editada_Baranoa']/df_estadisticos_estandarizados['Area_Ha_CTM12']*100).round(2)

    df_estadisticos_ordenados = df_estadisticos_estandarizados[columnas_ordenadas]

    df_estadisticos_ordenados.to_excel(RUTA_XLSX, sheet_name='Avance_SIG')
    print(f"Se genera XLSX {ARCHIVO_XLSX}")
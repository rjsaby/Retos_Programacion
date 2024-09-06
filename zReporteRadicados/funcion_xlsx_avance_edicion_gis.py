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

from arcgis.features import GeoAccessor, GeoSeriesAccessor
import arcpy

from pathlib import Path

import pandas as pd

# ** Librerías propias
import funcion_personalizacion_tablas

def xlsx_avance_edicion_gis():

    fecha_actual = dt.now()
    fecha_estandarizada = str(fecha_actual.strftime("%Y%m%d"))

    # TODO: Estadisticos Contractuales del Lote 4
    XLSX_ESTADISTICOS = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\O_Apoyo_Construccion_UIntervencion\UI_Finales\Estadisticos\indicadores_base_ui_lote_4.xlsx"

    # TODO: Directorio donde se alojará los reportes estadísticos diarios
    DIRECTORIO_XLSX = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_6_Indicador_Edicion_Geografica\zReportes\Seguimiento_Diario"
    ARCHIVO_XLSX = fecha_estandarizada+'_avance_edicios_GIS.xlsx'
    RUTA_XLSX = os.path.join(DIRECTORIO_XLSX, ARCHIVO_XLSX)

    # TODO: Actualización del Reporte de Seguimiento
    DIRECTORIO_SALIDA_XLSX = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_2_Rendimientos_Reconocimiento"
    NOMBRE_XLSX = fecha_estandarizada + "_RendimientoEquipoReconocimiento_BCGS.xlsx"
    RUTA_SALIDA_XLSX = os.path.join(DIRECTORIO_SALIDA_XLSX, NOMBRE_XLSX)
    NOMBRE_HOJA = 'Avance_Edicion_SIG'

    # TODO: Diccionario con las rutas de estadisticos que se generan al ejecutar la función [edicion_sig_municipio]
    dict_rutas_estadisticos = {'ESTADISTICOS_MARIA':r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_6_Indicador_Edicion_Geografica\zReportes\seguimiento_edicionGeo_MariaLaBaja.xlsx",
        'ESTADISTICOS_REPELON':r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_6_Indicador_Edicion_Geografica\zReportes\seguimiento_edicionGeo_Repelon.xlsx",
        'ESTADISTICOS_BARANOA':r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_6_Indicador_Edicion_Geografica\zReportes\seguimiento_edicionGeo_Baranoa.xlsx",
        'ESTADISTICOS_SABANAGRANDE':r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_6_Indicador_Edicion_Geografica\zReportes\seguimiento_edicionGeo_Sabanagrande.xlsx"
        }

    # TODO: Copia a Google Drive de los resultados
    DIRECTORIO_DESTINO = r"G:\Mi unidad\Equipo_Consolidacion\Hitos\E2_Informes_Id_FisicoJuridica\2_2_6_Indicador_Edicion_Geografica\zReportes\Seguimiento_Diario"
    NOMBRE_ARCHIVO_DESTINO = fecha_estandarizada+'_avance_edicios_GIS.xlsx'
    ruta_destino = os.path.join(DIRECTORIO_DESTINO, NOMBRE_ARCHIVO_DESTINO)

    nSheet_estadisticoXHito = 'Area_Editada_X_Hito'

    df_estadisticos = pd.read_excel(XLSX_ESTADISTICOS, sheet_name="areas_ha_hito.xlsx")

    # TODO: Se crea dataframe por hoja de excel (diccionario -dict_rutas_estadisticos-)
    dataframe = {}
    for llave, valor in dict_rutas_estadisticos.items():
        df = pd.read_excel(valor, sheet_name=nSheet_estadisticoXHito)
        dataframe[llave] = df

    # TODO: Se unifican los DF creados anteriormente con la base de estadísticos.
    for dframe, df in dataframe.items():
        df_estadisticos = pd.merge(left=df_estadisticos, right=df, left_on="ID_UI", right_on="id_ui", how="left", suffixes=('', f'_{dframe}'))

    # TODO: Estandarización de resultados
    columnas_unificacion = ['Meta_Hito',
        'ID_UI',
        'Area_Ha_CTM12',
        'area_editada_MariaLaBaja',
        'area_editada_Repelon',
        'area_editada_Baranoa',
        'area_editada_Sabanagrande'
        ]
    df_estadisticos_estandarizados = df_estadisticos[columnas_unificacion]
    df_estadisticos_estandarizados = df_estadisticos_estandarizados.fillna(0)

    # TODO: Se unifica el total de áreas editadas sumando la de los municipios analizados
    df_estadisticos_estandarizados['area_editada'] = df_estadisticos_estandarizados['area_editada_MariaLaBaja'] + df_estadisticos_estandarizados['area_editada_Repelon'] + df_estadisticos_estandarizados['area_editada_Baranoa'] + df_estadisticos_estandarizados['area_editada_Sabanagrande']

    # TODO: Se calcula la Edición por UI
    df_estadisticos_hitos = df_estadisticos_estandarizados.groupby(['Meta_Hito','ID_UI'])[['Area_Ha_CTM12','area_editada']].sum()
    df_estadisticos_hitos = df_estadisticos_hitos.reset_index()

    # TODO: Se calcula el porcentaje de avance
    df_estadisticos_estandarizados['%_avance'] = (df_estadisticos_estandarizados['area_editada']/df_estadisticos_estandarizados['Area_Ha_CTM12']*100).round(2)

    # TODO: Se exporta y se lleva a Google Drive
    df_estadisticos_estandarizados.to_excel(RUTA_XLSX, sheet_name='Avance_SIG')
    print(f"Se genera XLSX {ARCHIVO_XLSX}")

    # TODO: Se actualiza el reporte de rendimientos
    with pd.ExcelWriter(RUTA_SALIDA_XLSX, engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
        df_estadisticos_estandarizados.to_excel(writer, sheet_name=NOMBRE_HOJA, index=False)

    # TODO: Copia a ruta del indicador
    shutil.copy(RUTA_XLSX, ruta_destino)
    print(f"Se copia a Google Drive")



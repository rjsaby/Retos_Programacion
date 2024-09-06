import pandas as pd
import os
import seaborn as sns

os.environ["CRYPTOGRAPHY_OPENSSL_NO_LEGACY"] = "yes"

# ? Se usa para generar gráficos
import matplotlib.pyplot as plt

# ? Se usa para determina la fecha de ejecución del proceso dentro del export de los resultados estadísticos
from datetime import datetime

# ? Conexión a BD Postgres. Se usa dado que pandas no acepta sino este paquete para la conexión.
from sqlalchemy import create_engine, text

from datetime import datetime as df

from arcgis.features import GeoAccessor, GeoSeriesAccessor
import arcpy

from pathlib import Path

# ** Importación Funciones Propias
import funcion_dataframe_terrenos

def edicion_sig_municipio(sheet_name, sheet_id, municipio):

    sheet_name = sheet_name
    sheet_id = sheet_id

    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

<<<<<<< HEAD
    # TODO: Ruta para la generación de reportes.
=======
    columnas_seleccion = ['Codigo terreno','Editor SIG','Ajuste Geografico']
    columnas_seleccion_ui = ['codigo','id_ui','Meta_Hito']
    columnas_filtrado_cambio_ui = ['Codigo terreno','Editor SIG','Ajuste Geografico','area_ha_cmt12','id_ui','Meta_Hito']
    # columnas_estadisticos = ['Hito','Area_Ha_CMT12','Area_Ha_Contractual']
    columnas_parametrizacion = ['Codigo terreno','Editor SIG','Ajuste Geografico','codigo','codigo_anterior','area_ha_cmt12','SHAPE']

    ruta_relacion_terreno_ui = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E1_Alistamiento_Diagnostico\3_Disposicion\1.BD_Consolidada\BD_Consolidada_Lote4.gdb\relacion_terreno_ui"
    ui = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\O_Apoyo_Construccion_UIntervencion\UI_Finales\UI_Finales.gdb\UI_Unificadas\UI_Unificadas"

    municipio = municipio

>>>>>>> 1de0162e9ad4e7a9df62aadbca46c2194b3914e9
    DIRECTORIO_RESULTADOS = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_6_Indicador_Edicion_Geografica\zReportes"
    NOMBRE_XLSX = 'seguimiento_edicionGeo_'+municipio+'.xlsx'
    ruta_edicion_xlsx = os.path.join(DIRECTORIO_RESULTADOS,NOMBRE_XLSX)

<<<<<<< HEAD
    # TODO: Ruta donde se almacenará las geometrías de los terrenos con alguna labor de edición.
=======
>>>>>>> 1de0162e9ad4e7a9df62aadbca46c2194b3914e9
    DIRECTORIO_BD_2_2_6 = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_6_Indicador_Edicion_Geografica\Base_Datos\2_2_6.gdb"
    NOMBRE_FC = 'terrenos_editados_'+municipio
    ruta_fc_estadistico = os.path.join(DIRECTORIO_BD_2_2_6, NOMBRE_FC)

<<<<<<< HEAD
    # TODO: LLamada a la capa de Terrenos Final
    terrenosXhito = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E1_Alistamiento_Diagnostico\3_Disposicion\1.BD_Consolidada\BD_Consolidada_Lote4.gdb\Analitica_UT_Consolidada\TERRENO_POR_HITO"
    df_terrenos = pd.DataFrame.spatial.from_featureclass(terrenosXhito)

    control_cambios_esig_original = pd.read_csv(url)

    # TODO: Se estandariza el DataFrame construido a partir del Sheet
    columnas_seleccion = ['Codigo terreno','Editor SIG','Ajuste Geografico']
    control_cambios_esig_filtro = control_cambios_esig_original[columnas_seleccion]

    # TODO: Se filtran todas las columnas editadas (no tienen en cuenta las en blanco, que se entienden no revisadas por SIG)
    control_cambios_esig_ajustados = control_cambios_esig_filtro[(control_cambios_esig_filtro['Ajuste Geografico'].notna()|
        control_cambios_esig_filtro['Ajuste Geografico'].notnull())]

    # TODO: A la capa del Sheet se le lleva las geometrías de Terrenos Finales
    df_cambios_terrenos = pd.merge(left=control_cambios_esig_ajustados, 
        right=df_terrenos, 
        left_on="Codigo terreno", 
        right_on="codigo",
        how="left"
        )

    print(f"Registros NO espacializados: {(df_cambios_terrenos[df_cambios_terrenos['SHAPE'].isnull()]).shape[0]}")

    # TODO: Parametrización de columnas Terrenos Finales con Cambios SIG
    columnas_parametrizacion = ['codigo','codigo_anterior','Editor SIG','Ajuste Geografico','nombre_municipio','id_ui','meta_hito','area_ha_cmt12','SHAPE']
    df_cambios_terrenos = df_cambios_terrenos[columnas_parametrizacion]

    # TODO: Se exporta la capa geográfica con todos los datos espacializados cargados en el Sheet y con procesos de Edición SIG
    df_cambios_terrenos.spatial.to_featureclass(location=ruta_fc_estadistico)
    print(f"Se genera FC asociado a terrenos editados, para el municipio {municipio}")

    # TODO: Cálculo de estadísticos, municipio, meta_hito y con la sumatoria de las áreas.
    df_estadistico_cambio_x_ui = (pd.DataFrame(df_cambios_terrenos.groupby(['nombre_municipio','meta_hito','id_ui'])['area_ha_cmt12'].sum()).reset_index()).rename(columns={'area_ha_cmt12':'area_editada_'+municipio})
    df_estadistico_cambio_x_ui['area_editada_'+municipio] = df_estadistico_cambio_x_ui['area_editada_'+municipio].round(3)

    with pd.ExcelWriter(ruta_edicion_xlsx, engine='xlsxwriter') as writer:
        df_estadistico_cambio_x_ui.to_excel(writer, sheet_name='Area_Editada_X_Hito')
=======
    resultado = funcion_dataframe_terrenos.dataframe_terrenos()
    df_terrenos = resultado[0]

    control_cambios_esig_original = pd.read_csv(url)

    control_cambios_esig_filtro = control_cambios_esig_original[columnas_seleccion]
    control_cambios_esig_filtro = control_cambios_esig_filtro.copy()
    control_cambios_esig_ajustados = control_cambios_esig_filtro[(control_cambios_esig_filtro['Ajuste Geografico']=='Ajuste Geográfico') | 
                                                                 (control_cambios_esig_filtro['Ajuste Geografico']=='AJUSTE GEOGRAFICO')]

    df_cambios_terrenos = pd.merge(left=control_cambios_esig_ajustados, 
    right=df_terrenos, 
    left_on="Codigo terreno", 
    right_on="codigo", how="left")

    print(f"Registros NO espacializados: {(df_cambios_terrenos[df_cambios_terrenos['SHAPE'].isnull()]).shape[0]}")

    df_cambios_terrenos = df_cambios_terrenos[columnas_parametrizacion]

    df_cambios_terrenos.spatial.to_featureclass(location=ruta_fc_estadistico)
    print(f"Se genera FC asociado a terrenos editados, para el municipio {municipio}")

    df_relacion_terreno_ui = pd.DataFrame.spatial.from_table(ruta_relacion_terreno_ui)
    df_ui = pd.DataFrame.spatial.from_featureclass(ui)

    df_relacionUiTerreno_ui = pd.merge(left=df_relacion_terreno_ui, 
    right=df_ui, 
    left_on="id_ui", 
    right_on="ID_UI", 
    how="left")

    df_relacionUiTerreno_ui = df_relacionUiTerreno_ui[columnas_seleccion_ui]
    df_relacionUiTerreno_ui

    df_cambio_w_ui = pd.merge(left=df_cambios_terrenos, 
    right=df_relacionUiTerreno_ui, 
    left_on="Codigo terreno", 
    right_on="codigo", 
    how="left")

    df_cambio_w_ui = df_cambio_w_ui[columnas_filtrado_cambio_ui]

    df_estadistico_cambio_x_hito = (pd.DataFrame(df_cambio_w_ui.groupby(['Meta_Hito'])['area_ha_cmt12'].sum()).reset_index()).rename(columns={'area_ha_cmt12':'area_editada_'+municipio})
    df_estadistico_cambio_x_hito['area_editada_'+municipio] = df_estadistico_cambio_x_hito['area_editada_'+municipio].round(3)

    df_estadistico_cambio_x_ui = (pd.DataFrame(df_cambio_w_ui.groupby(['Meta_Hito','id_ui'])['area_ha_cmt12'].sum()).reset_index()).rename(columns={'area_ha_cmt12':'area_editada_'+municipio})
    df_estadistico_cambio_x_ui['area_editada_'+municipio] = df_estadistico_cambio_x_ui['area_editada_'+municipio].round(3)

    with pd.ExcelWriter(ruta_edicion_xlsx, engine='xlsxwriter') as writer:
        df_estadistico_cambio_x_hito.to_excel(writer, sheet_name='Area_Editada_X_Hito')
        df_estadistico_cambio_x_ui.to_excel(writer, sheet_name='Area_Editada_X_UI')
>>>>>>> 1de0162e9ad4e7a9df62aadbca46c2194b3914e9
    print(f"Se genera el excel para el municipio de {municipio}")
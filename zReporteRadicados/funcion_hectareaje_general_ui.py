import os
import pandas as pd

os.environ["CRYPTOGRAPHY_OPENSSL_NO_LEGACY"] = "yes"

# import numpy as np
from arcgis.features import GeoAccessor, GeoSeriesAccessor
import arcpy

def funcion_hectareaje_general_hito(ruta_fcUI):
    ruta_fcUI = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\O_Apoyo_Construccion_UIntervencion\UI_Finales\UI_Finales.gdb"
    RUTA_XLSX = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\O_Apoyo_Construccion_UIntervencion\UI_Finales\Estadisticos"
    NOMBRE_XLSX = 'indicadores_base_ui_lote_4.xlsx'
    DIRECTORIO_XLSX = os.path.join(RUTA_XLSX, NOMBRE_XLSX)

    DIFERENCIA_AREAS_UT_CONTRATO = 'hitos_por_asignacion.xlsx'
    AREA_INDIVUALIZADA = 'areas_ha_hito.xlsx'

    h2_contractual = 16243.92
    h3_contractual = 54146.40
    h4_contractual = 81219.60
    h5_contractual = 108292.80

    arcpy.env.workspace = ruta_fcUI

    for dataset in arcpy.ListDatasets():
        for capa in arcpy.ListFeatureClasses(feature_dataset=dataset):
            ruta = os.path.join(arcpy.env.workspace,dataset,capa)
            df_unidades_intervencion = pd.DataFrame.spatial.from_featureclass(ruta)
            print(f"Se crea dataset de capa {capa}")
        
    query_2 = "Meta_Hito == 'Hito 2'"
    query_3 = "(Meta_Hito == 'Hito 2') or (Meta_Hito == 'Hito 3')"
    query_4 = "(Meta_Hito == 'Hito 2') or (Meta_Hito == 'Hito 3') or (Meta_Hito == 'Hito 4')"
    query_5 = "(Meta_Hito == 'Hito 2') or (Meta_Hito == 'Hito 3') or (Meta_Hito == 'Hito 4') or (Meta_Hito == 'Hito 5')"

    query_hito_2 =df_unidades_intervencion.query(query_2)
    # ! Corregir luego de modificar el nombre de la columna
    ha_hito_2 = query_hito_2['Area_Ha_CMT12'].sum().round(2)

    query_hito_3 =df_unidades_intervencion.query(query_3)
    # ! Corregir luego de modificar el nombre de la columna
    ha_hito_3 = query_hito_3['Area_Ha_CMT12'].sum().round(2)

    query_hito_4 =df_unidades_intervencion.query(query_4)
    # ! Corregir luego de modificar el nombre de la columna
    ha_hito_4 = query_hito_4['Area_Ha_CMT12'].sum().round(2)

    query_hito_5 =df_unidades_intervencion.query(query_5)
    # ! Corregir luego de modificar el nombre de la columna
    ha_hito_5 = query_hito_5['Area_Ha_CMT12'].sum().round(2)

    diccionario_hitos = {
    'Hito': ['Hito 2','Hito 3','Hito 4','Hito 5'],
    'Area_Ha_CMT12': [ha_hito_2, ha_hito_3, ha_hito_4, ha_hito_5],
    'Area_Ha_Contractual': [h2_contractual, h3_contractual, h4_contractual, h5_contractual]
    }

    df_hitos_ut = pd.DataFrame(diccionario_hitos)

    df_hitos_ut['Diferencia_AreaUT_Vs_Contrato'] = df_hitos_ut['Area_Ha_CMT12'] - df_hitos_ut['Area_Ha_Contractual']
    df_hitos_ut = df_hitos_ut.rename(columns={'Area_Ha_CMT12':'Area_Ha_CTM12'})

    df_unidades_intervencion_hitos = pd.DataFrame(df_unidades_intervencion[['ID_UI', 'Zona_UI', 'Municipio_UI', 'Meta_Hito','Area_Ha_CMT12']]).rename(columns={'Area_Ha_CMT12':'Area_Ha_CTM12'})

    # ** Usar ExcelWriter para guardar múltiples dataframes en diferentes hojas
    with pd.ExcelWriter(DIRECTORIO_XLSX, engine='xlsxwriter') as writer:
        df_unidades_intervencion_hitos.to_excel(writer, sheet_name=AREA_INDIVUALIZADA, index=False)
        df_hitos_ut.to_excel(writer, sheet_name=DIFERENCIA_AREAS_UT_CONTRATO, index=False)

    print(f"Se exporta {DIRECTORIO_XLSX}")

    print("FINALIZA PROCESO")

    return df_hitos_ut, df_unidades_intervencion_hitos
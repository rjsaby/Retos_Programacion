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
import funcion_parametrizacion_variables

def terrenos_bcgs_geo():

    resultados = funcion_parametrizacion_variables.parametrizacion_variables()
    dict_capa_version = resultados[15]

    arcpy.env.overwriteOutput = True

    # TODO: Base de Datos Corporativa
    bcgs_bdsde = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\1.GIS\1.2.PRO\RAISS_Lote_4\PostgreSQL-44-bcgs_geo(rodian_consulta).sde"
    bd_local = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_10_TerrenosBCGS\2_2_10_TerrenosBCGS.gdb"

    arcpy.env.workspace = bcgs_bdsde

    for llave, valor in dict_capa_version.items():
        for dataset in arcpy.ListDatasets():
            if dataset == 'bcgs_geo.'+valor[0]+'.Areas_Catastrales':
                for capa in arcpy.ListFeatureClasses(feature_dataset=dataset):
                    if capa == valor[1]:
                        # TODO: La función de cambio de versión exige un layer_feature
                        try:
                            arcpy.MakeFeatureLayer_management(in_features=capa, out_layer='ly_'+capa)
                            # TODO: Se hace el cambio de versión
                            arcpy.management.ChangeVersion('ly_'+capa, version_type='TRANSACTIONAL', version_name=llave)

                            # TODO: Se reemplaza los puntos para que permita copiar la capa                            
                            renombre_capa = capa.replace('.','_')

                            # TODO: Se parametriza la bd local donde se copiaran las capas asociadas a las versiones
                            ruta_destino = os.path.join(bd_local,renombre_capa)
                            
                            # TODO: Se copian los datos
                            arcpy.CopyFeatures_management(in_features='ly_'+capa, out_feature_class=ruta_destino)

                            print(f"Capa {capa} exportada correctamente a {ruta_destino}")
                        except arcpy.ExecuteError as e:
                            print(f"Error al exportar la capa {capa}: {e}")

    arcpy.env.workspace = bd_local

    # TODO: Trucado Capa Objetivo (Target)
    capa_objetivo = 'bcgs_lc_terreno'
    for capa in arcpy.ListFeatureClasses(wild_card=capa_objetivo):
        arcpy.TruncateTable_management(capa)

    for capa in arcpy.ListFeatureClasses():
        if capa != capa_objetivo:
            try:
                arcpy.Append_management(inputs=capa,target=capa_objetivo,schema_type='TEST')
                ruta_df_terrenos_bcgs = os.path.join(arcpy.env.workspace, capa_objetivo)
                print(f"Se unifica {capa} en -{capa_objetivo}-")
            except arcpy.ExecuteError as e:
                print(f"Error al exportar la capa {capa}: {e}")
                
    return ruta_df_terrenos_bcgs
                        






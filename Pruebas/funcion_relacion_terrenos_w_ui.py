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

from arcgis.features import GeoAccessor, GeoSeriesAccessor
import arcpy

from pathlib import Path

def funcion_terreno_w_ui(ruta_fcTerrenos, ruta_gdbScrach, rutafcUI):

    arcpy.env.overwriteOutput = True

    camposABorrarTerrenoJoinUI = ['Join_Count',
    'TARGET_FID',
    'codigo_anterior',
    'area_ha_cmt12'
    ]
    
    camposABorrarfcTerrenoUI = ['Join_Count',
    'TARGET_FID',
    'ORIG_FID',
    'codigo_1',
    'Area_Ha_CMT12_1',
    'Zona_UI',
    'Departamento_UI',
    'Municipio_UI',
    'Nombre_UI',
    'Codigo_DANE_UI',
    'Area_Ha_CMT12',
    'Meta_Hito']

    df_columnas_estandarizacion = ['codigo',
    'ID_UI']

    ruta_bdConsolidada = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E1_Alistamiento_Diagnostico\3_Disposicion\1.BD_Consolidada\BD_Consolidada_Lote4.gdb"

    rPathBDScrach = Path(ruta_gdbScrach)
    rPathBDConsolidada = Path(ruta_bdConsolidada)

    capa_centroides_terrenos = 'fcTerrenosCentroides'
    ruta_salida_centroidesTerrenos = os.path.join(ruta_gdbScrach,capa_centroides_terrenos)
    arcpy.management.FeatureToPoint(ruta_fcTerrenos, out_feature_class = ruta_salida_centroidesTerrenos, point_location = 'INSIDE')
    print(f"1. Se genera centroides de Terrenos, capa {capa_centroides_terrenos}, base de datos {rPathBDScrach.name}")

    capa_fccentroidesTerrenosWJoinUI = 'capa_fccentroidesTerrenosWJoinUI'
    arcpy.analysis.SpatialJoin(target_features = ruta_salida_centroidesTerrenos, 
                               join_features = rutafcUI, 
                               out_feature_class = os.path.join(ruta_gdbScrach, capa_fccentroidesTerrenosWJoinUI), 
                               match_option = 'INTERSECT')
    print(f"2. Se genera Join Terrenos Centroides W UI, capa {capa_fccentroidesTerrenosWJoinUI}, base de datos {rPathBDScrach.name}")

    arcpy.management.DeleteField(in_table = os.path.join(ruta_gdbScrach, capa_fccentroidesTerrenosWJoinUI), 
                                 drop_field = camposABorrarTerrenoJoinUI,
                                 method = 'DELETE_FIELDS')
    print(f"3. Se borran campos en Terrenos Centroides W UI, capa {capa_fccentroidesTerrenosWJoinUI}, base de datos {rPathBDScrach.name}")

    capa_fcTerrenosUI = 'fcTerrenosUI'
    arcpy.analysis.SpatialJoin(target_features = ruta_fcTerrenos, 
                               join_features = os.path.join(ruta_gdbScrach, capa_fccentroidesTerrenosWJoinUI), 
                               out_feature_class = os.path.join(ruta_gdbScrach, capa_fcTerrenosUI), 
                               match_option = 'INTERSECT')
    print(f"4. Se genera Join Terrenos Centroides W Terrenos Originales, capa {capa_fcTerrenosUI}, base de datos {rPathBDScrach.name}")

    arcpy.management.DeleteField(in_table = os.path.join(ruta_gdbScrach, capa_fcTerrenosUI), 
                                 drop_field = camposABorrarfcTerrenoUI,
                                 method = 'DELETE_FIELDS')
    print(f"5. Se borran campos en Terrenos W UI, capa {capa_fcTerrenosUI}, base de datos {rPathBDScrach.name}")

    df_terrenosUI = pd.DataFrame.spatial.from_featureclass(os.path.join(ruta_gdbScrach, capa_fcTerrenosUI))
    df_terrenosUI_estandarizado = df_terrenosUI[df_columnas_estandarizacion]
    tbl_terreno_vista = 'relacion_terreno_ui'
    df_terrenosUI_estandarizado.spatial.to_table(location=os.path.join(ruta_gdbScrach,tbl_terreno_vista))
    print(f"6.1. Se genera tabla {tbl_terreno_vista} que relaciona Terrenos con UI, base de datos {rPathBDScrach.name}")
    df_terrenosUI_estandarizado.spatial.to_table(location=os.path.join(ruta_bdConsolidada,tbl_terreno_vista))
    print(f"6.2. Se genera tabla {tbl_terreno_vista} que relaciona Terrenos con UI, base de datos {rPathBDConsolidada.name}")

    print("FINALIZA PROCESO")
    
    return os.path.join(ruta_bdConsolidada,tbl_terreno_vista)
    
    
    
    
    
    








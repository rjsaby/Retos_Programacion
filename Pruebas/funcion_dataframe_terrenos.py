from arcgis.features import GeoAccessor, GeoSeriesAccessor
import arcpy, pandas as pd, os

os.environ["CRYPTOGRAPHY_OPENSSL_NO_LEGACY"] = "yes"

def dataframe_terrenos():

    try:
        RUTA_BD_CONSOLIDADA = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E1_Alistamiento_Diagnostico\3_Disposicion\1.BD_Consolidada\BD_Consolidada_Lote4.gdb"

        CAPA_TERRENOS_R = 'Analitica_UT_Consolidada\R_TERRENO'
        CAPA_TERRENOS_U = 'Analitica_UT_Consolidada\\U_TERRENO'

        NOMBRE_FC_TERRENOS_UNIFICADOS = 'Analitica_UT_Consolidada\\TERRENO_UNIFICADO'

        capa_terrenos_rurales = os.path.join(RUTA_BD_CONSOLIDADA, CAPA_TERRENOS_R)
        capa_terrenos_urbanos = os.path.join(RUTA_BD_CONSOLIDADA, CAPA_TERRENOS_U)

        # ** Terrenos Rurales
        df_terreno_rural = pd.DataFrame.spatial.from_featureclass(capa_terrenos_rurales)
        # ** Terrenos Urbanos
        df_terreno_urbano = pd.DataFrame.spatial.from_featureclass(capa_terrenos_urbanos)

        # ** Selección de columnas
        columnas_selecciones = ['CODIGO',
            'CODIGO_ANTERIOR',
            'Area_ha_cmt12',
            'SHAPE']

        # ** DF Terrenos Rurales, Urbanos
        df_terreno_rural_reducido = df_terreno_rural[columnas_selecciones]
        df_terreno_urbano_reducido = df_terreno_urbano[columnas_selecciones]

        # ** Concatenación en DF
        df_terrenos_unificados = pd.concat([df_terreno_rural_reducido, df_terreno_urbano_reducido])

        # ** Generación de FC Físico
        df_terrenos_unificados.spatial.to_featureclass(location=os.path.join(RUTA_BD_CONSOLIDADA, NOMBRE_FC_TERRENOS_UNIFICADOS))
        
        arcpy.management.DeleteIdentical(os.path.join(RUTA_BD_CONSOLIDADA, NOMBRE_FC_TERRENOS_UNIFICADOS), fields = ['SHAPE','codigo', 'codigo_anterior','area_ha_cmt12'])
        df_terrenos_no_repetidos = pd.DataFrame.spatial.from_featureclass(os.path.join(RUTA_BD_CONSOLIDADA, NOMBRE_FC_TERRENOS_UNIFICADOS))

        print(f"De la capa original de Terrenos con {df_terrenos_unificados.shape[0]} registros se elimanan repetidos, obteniendose {df_terrenos_no_repetidos.shape[0]}")
        
        return df_terrenos_no_repetidos, os.path.join(RUTA_BD_CONSOLIDADA, NOMBRE_FC_TERRENOS_UNIFICADOS)
        
    except Exception as e:
        print(f"Error generado durante la ejecución de la función: {e}")
    finally:
        print(f"Concluye el proceso")
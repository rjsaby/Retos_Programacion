from arcgis.features import GeoAccessor, GeoSeriesAccessor
import arcpy, pandas as pd, os

def dataframe_terrenos():

    try:
        RUTA_BD_CONSOLIDADA = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E1_Alistamiento_Diagnostico\3_Disposicion\1.BD_Consolidada\BD_Consolidada_Lote4.gdb"

        CAPA_TERRENOS_R = 'Analitica_UT_Consolidada\R_TERRENO'
        CAPA_TERRENOS_U = 'Analitica_UT_Consolidada\\U_TERRENO'

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

        # ** Concatenación de dataframes
        return pd.concat([df_terreno_rural_reducido, df_terreno_urbano_reducido])

    except Exception as e:
        print(f"Error generado durante la ejecución de la función: {e}")
    finally:
        print(f"Concluye el proceso")
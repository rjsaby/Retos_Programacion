from arcgis.features import GeoAccessor, GeoSeriesAccessor
import arcpy, pandas as pd, os

os.environ["CRYPTOGRAPHY_OPENSSL_NO_LEGACY"] = "yes"

arcpy.env.overwriteOutput = True

def dataframe_terrenos():

    try:
        RUTA_BD_CONSOLIDADA = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E1_Alistamiento_Diagnostico\3_Disposicion\1.BD_Consolidada\BD_Consolidada_Lote4.gdb"

        CAPA_TERRENOS_R = 'Analitica_UT_Consolidada\R_TERRENO'
        CAPA_TERRENOS_U = 'Analitica_UT_Consolidada\\U_TERRENO'

        NOMBRE_FC_TERRENOS_UNIFICADOS = 'Analitica_UT_Consolidada\\TERRENO_UNIFICADO'

        # ! *************  Unificación Registros GIS ***************

        RUTA_BD_CONSOLIDADA_NUBE = r"C:\Users\rodian.saby\OneDrive\Documentos\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E1_Alistamiento_Diagnostico\3_Disposicion\1.BD_Consolidada\BD_Consolidada_Lote4.gdb\Consolidacion_ES\_con_r_lc_terreno"
        RUTA_TERRENOS_GC = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E1_Alistamiento_Diagnostico\3_Disposicion\1.BD_Consolidada\BD_Consolidada_Lote4.gdb\Analitica_UT_Consolidada\TERRENO_UNIFICADO"

        BD_CONSOLIDADA_LOCAL = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E1_Alistamiento_Diagnostico\3_Disposicion\1.BD_Consolidada\BD_Consolidada_Lote4.gdb\Analitica_UT_Consolidada"
        CAPA_TERRENOS_W_GIS = 'TERRENO_UNIFICADO_w_GIS'
        ruta_fc_terrenos_w_gis = os.path.join(BD_CONSOLIDADA_LOCAL,CAPA_TERRENOS_W_GIS)

        columna_creacion_terrenos_gis = {'codigo_anterior':None}

        columnas_seleccion_terrenos_gis = ['terreno_codigo',
            'codigo_anterior',
            'created_user',
            'last_edited_user',
            'last_edited_date',
            'globalid',
            'Area_ha_cmt12',
            'SHAPE'
            ]

        renombre_columnas_terrenos_gis = {
            'terreno_codigo':'codigo',
            'created_user':'sig_creador',
            'last_edited_user':'sig_ultima_edicion',
            'last_edited_date':'fecha_ultima_edicion',
            'Area_ha_cmt12':'area_ha_cmt12'
            }

        creacion_columnas_no_editado = {
            'sig_creador':None,
            'sig_ultima_edicion':None,
            'fecha_ultima_edicion':None,
            'globalid':None,
            }

        columnas_normalizacion_terreno_no_editado = ['codigo',
            'codigo_anterior',
            'area_ha_cmt12',
            'SHAPE_x'
            ]

        columnas_reorganizacion_no_editado = ['codigo',
            'codigo_anterior',
            'sig_creador',
            'sig_ultima_edicion',
            'fecha_ultima_edicion',
            'globalid',
            'area_ha_cmt12',
            'SHAPE_x'
            ]
        
        columna_renombre_no_editado = {'SHAPE_x':'SHAPE'}
        
        # ! *************  Unificación Registros GIS ***************

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
        
        # ! *************  Unificación Registros GIS ***************

        df_terrenos_gis = pd.DataFrame.spatial.from_featureclass(RUTA_BD_CONSOLIDADA_NUBE)
        df_terrenos_gc = pd.DataFrame.spatial.from_featureclass(RUTA_TERRENOS_GC)

        df_merge_terrenos_gc_gis = pd.merge(left=df_terrenos_gc,right=df_terrenos_gis,left_on="codigo",right_on="terreno_codigo",how="left")
        print(f"{df_merge_terrenos_gc_gis.shape[0]}")

        df_terrenos_no_editados = df_merge_terrenos_gc_gis[df_merge_terrenos_gc_gis['terreno_codigo'].isnull()]
        print(f"{df_terrenos_no_editados.shape[0]}")

        for llave, valor in columna_creacion_terrenos_gis.items():
            df_terrenos_gis[llave] = valor

        df_terrenos_gis = df_terrenos_gis[columnas_seleccion_terrenos_gis]
        df_terrenos_gis = df_terrenos_gis.rename(columns=renombre_columnas_terrenos_gis)

        df_terrenos_no_editados = df_terrenos_no_editados[columnas_normalizacion_terreno_no_editado]

        df_terrenos_no_editados = df_terrenos_no_editados.copy()

        for llave, valor in creacion_columnas_no_editado.items():
            df_terrenos_no_editados[llave] = valor

        df_terrenos_no_editados = df_terrenos_no_editados[columnas_reorganizacion_no_editado]

        df_terrenos_no_editados = df_terrenos_no_editados.rename(columns=columna_renombre_no_editado)

        df_terrenos_unificado = pd.concat([df_terrenos_gis, df_terrenos_no_editados])

        df_terrenos_unificado.spatial.to_featureclass(location = ruta_fc_terrenos_w_gis)
        print(f"Se crea la capa {CAPA_TERRENOS_W_GIS} en BD \n {BD_CONSOLIDADA_LOCAL}")

        arcpy.env.workspace = BD_CONSOLIDADA_LOCAL

        for capa in arcpy.ListFeatureClasses(wild_card='TERRENO_UNIFICADO_w_GIS'):
            for campo in arcpy.ListFields(dataset=capa, wild_card='area_ha_cmt12'):
                arcpy.management.CalculateGeometryAttributes(in_features = capa, geometry_property = [[campo.name,'AREA']], area_unit='HECTARES')
                print(f"Se actualiza el campo de hectareaje")

        df_terrenos_unificado_gis = pd.DataFrame.spatial.from_featureclass(ruta_fc_terrenos_w_gis)

        # ! *************  Unificación Registros GIS ***************

        return df_terrenos_unificado_gis, ruta_fc_terrenos_w_gis
        
    except Exception as e:
        print(f"Error generado durante la ejecución de la función: {e}")
    finally:
        print(f"Concluye el proceso")
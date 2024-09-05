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

from datetime import datetime

from arcgis.features import GeoAccessor, GeoSeriesAccessor
import arcpy

from pathlib import Path

# ** Librerías propias
import funcion_dataframe_terrenos
import funcion_SQL_a_DataFrame
import funcion_parametrizacionPredioMatriz_X_NPN

arcpy.env.overwriteOutput = True

# ! Asignación de Variables Globales
DIRECTORIO_REPORTE = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_0_Identificacion_Predial_Total_Ha_Actualizadas\zReportes"
RUTA_BD_LOCAL = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_0_Identificacion_Predial_Total_Ha_Actualizadas\Base_Datos\_2_2_0.gdb"
RUTA_BD_CONSOLIDADA = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E1_Alistamiento_Diagnostico\3_Disposicion\1.BD_Consolidada\BD_Consolidada_Lote4.gdb"
NOMBRE_CAPA_HAXESTADO = 'TERRENOS_RECONOCIMIENTO_TRAMITES_ATENCION_SHEET'

def calculo_rendimientos_indicadorSheet(nMunicipio, nSheet, idSheet):
    nombre_reporte_hasheet = 'Reporte_Ha_FuenteSheet_' + str(nMunicipio) + '.xlsx'
    nombre_capa_haXEstado = 'TERRENOS_VISITADOS_' + str(nMunicipio)

    # ! Migración de Sheet
    sheet_name = nSheet
    sheet_id = idSheet

    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    df_reporte_reconocimiento = pd.read_csv(url)
    columnas_seleccion = ['MUNICIPIO', 
        'ZONA', 
        'CODIGO',
        'Area terreno_Ha',
        'CODIGO_MUN', 
        'COORDINADOR',
        'RECONOCEDOR',
        'PROGRAMACION',
        'Visitado',
        'Nº Radicado BCGS']
    
    dict_campos_npn_matriz = {'npn_matriz':str,
                              'informalidades_visitadas':int,
                              'codigo':str,
                              'codigo_anterior':str,
                              'area_ha_cmt12':float
                              }
    
    dict_campos_conGeo = {'MUNICIPIO':str,
                         'ZONA':str,
                         'CODIGO':str,
                         'Area terreno_Ha':str,
                         'CODIGO_MUN':str,
                         'COORDINADOR':str,
                         'RECONOCEDOR':str,
                         'PROGRAMACION':str,
                         'Visitado':str,
                         'Nº Radicado BCGS':str,
                         'codigo_anterior':str,
                         'area_ha_cmt12':float
                         }

    columnas_salida_conGeo = ['MUNICIPIO',
                              'ZONA',
                              'CODIGO',
                              'Area terreno_Ha',
                              'CODIGO_MUN',
                              'COORDINADOR',
                              'RECONOCEDOR',
                              'PROGRAMACION',
                              'Visitado',
                              'Nº Radicado BCGS',
                              'codigo_anterior',
                              'area_ha_cmt12',
                              'SHAPE'
                              ]
    
    
    columnas_salida_sinGeo = ['npn_matriz',
                              'informalidades_visitadas',
                              'codigo',
                              'codigo_anterior',
                              'area_ha_cmt12',
                              'SHAPE',
                              ]

    df_reporte_reconocimiento = df_reporte_reconocimiento[columnas_seleccion]

    df_reporte_reconocimiento = df_reporte_reconocimiento.copy()

    total_registros = df_reporte_reconocimiento.shape[0]
    print(f"El total de registros analizados es de {total_registros}")

    # ! Filtro de Visitados
    df_reporte_reconocimiento = df_reporte_reconocimiento[(df_reporte_reconocimiento['Visitado'] == 'SI')]

    # ! Ejecución de función, espacialización de Terrenos
    df_terrenos, ruta_terrenos = funcion_dataframe_terrenos.dataframe_terrenos()

    # ! Espacialización de Rendimientos Reconocimiento
    # ** Left para verificar posteriormente cuales terrenos son posibles informalidades
    df_terrenos_reporteReconocimiento = pd.merge(left=df_reporte_reconocimiento, right=df_terrenos, left_on="CODIGO", right_on="codigo", how="left")
    print(f"{df_terrenos_reporteReconocimiento.shape[0]}")

    # ! Análisis de Terrenos Visitados sin Geometrías
    df_terrenos_reporteReconocimiento_sinGeo =  df_terrenos_reporteReconocimiento[df_terrenos_reporteReconocimiento['SHAPE'].isnull()]
    terrenos_posiblesInformalidades = df_terrenos_reporteReconocimiento_sinGeo.shape[0]
    print(f"Predios sin geometrías, posibles informalidades: {df_terrenos_reporteReconocimiento_sinGeo.shape[0]}")

    # ! Busqueda de predio matriz a partir de NPN
    # ** Aplica la función a cada elemento de la columna npn y asigna el resultado a npn_parametrizado
    df_terrenos_reporteReconocimiento_sinGeo = df_terrenos_reporteReconocimiento_sinGeo.copy()
    df_terrenos_reporteReconocimiento_sinGeo['npn_matriz'] = df_terrenos_reporteReconocimiento_sinGeo['CODIGO'].apply(funcion_parametrizacionPredioMatriz_X_NPN.eliminacion_mejora)

    df_terrenos_reporteReconocimiento_sinGeo_sinMatriz = df_terrenos_reporteReconocimiento_sinGeo[df_terrenos_reporteReconocimiento_sinGeo['npn_matriz'].isnull()]
    df_terrenos_reporteReconocimiento_sinGeo_conMatriz = df_terrenos_reporteReconocimiento_sinGeo[df_terrenos_reporteReconocimiento_sinGeo['npn_matriz'].notnull()]

    print(f"Terrenos por verificar desde Reconocimiento: {df_terrenos_reporteReconocimiento_sinGeo_sinMatriz}")

    # ! Espacialización de posibles matrices
    reporteReconocimiento_sinGeo_conMatriz_Unicos = pd.DataFrame(df_terrenos_reporteReconocimiento_sinGeo_conMatriz['npn_matriz'].value_counts()).rename(columns={'count':'informalidades_visitadas'}).reset_index()
    predios_matrices = reporteReconocimiento_sinGeo_conMatriz_Unicos.shape[0]
    print(f"Total de posibles Matrices: {reporteReconocimiento_sinGeo_conMatriz_Unicos.shape[0]}")

    reporteReconocimiento_sinGeo_conMatriz_Unicos_Geo = pd.merge(left=reporteReconocimiento_sinGeo_conMatriz_Unicos, right=df_terrenos, left_on="npn_matriz", right_on="codigo", how="inner")
    print(f"Matrices espacializados: {reporteReconocimiento_sinGeo_conMatriz_Unicos_Geo}")

    # ! Calculo de Ha Posibles Matrices (del tratamiento de informalidades)
    total_ha_matrices = reporteReconocimiento_sinGeo_conMatriz_Unicos_Geo['area_ha_cmt12'].sum().round(2)
    print(f"Total Ha Predios Matrices: {total_ha_matrices} Ha")

    # ! Análisis de Terrenos Visitados con Geometrías
    df_terrenos_reporteReconocimiento_conGeo =  df_terrenos_reporteReconocimiento[df_terrenos_reporteReconocimiento['SHAPE'].notnull()]
    terrenos_formales = df_terrenos_reporteReconocimiento_conGeo.shape[0]
    print(f"Predios con geometrías: {df_terrenos_reporteReconocimiento_conGeo.shape[0]}")

    total_ha_conGeo = df_terrenos_reporteReconocimiento_conGeo['area_ha_cmt12'].sum().round(2)
    print(f"Total Ha Predios Con Geometría: {total_ha_conGeo} Ha")
    print(df_terrenos_reporteReconocimiento_conGeo)
    
    # ** Actualización de la Zona
    df_terrenos_reporteReconocimiento_conGeo['codigo_zona'] = df_terrenos_reporteReconocimiento_conGeo['CODIGO'].str[5:7]

    df_terrenos_reporteReconocimiento_conGeo.loc[df_terrenos_reporteReconocimiento_conGeo['codigo_zona'] == '01', 'ZONA'] = 'Urbano'
    df_terrenos_reporteReconocimiento_conGeo.loc[df_terrenos_reporteReconocimiento_conGeo['codigo_zona'] == '00', 'ZONA'] = 'Rural'
    df_terrenos_reporteReconocimiento_conGeo.loc[(df_terrenos_reporteReconocimiento_conGeo['codigo_zona'] != '00') & (df_terrenos_reporteReconocimiento_conGeo['codigo_zona'] != '01'), 'ZONA'] = 'Corregimientos Urbanos'

    # ** Se parametrizan las columnas de salida
    reporteReconocimiento_sinGeo_conMatriz_Unicos_Geo = reporteReconocimiento_sinGeo_conMatriz_Unicos_Geo[columnas_salida_sinGeo]
    df_terrenos_reporteReconocimiento_conGeo = df_terrenos_reporteReconocimiento_conGeo[columnas_salida_conGeo]

    df_resumen_ha = pd.DataFrame([[nMunicipio, terrenos_posiblesInformalidades, predios_matrices, total_ha_matrices, terrenos_formales, total_ha_conGeo]], columns=['municipio', 'posibles_informalidades', 'terrenos_matrices', 'total_ha_posiblesinformalidades','predios_formales', 'total_ha_prediosformales'])
    df_resumen_ha['total_ha'] = df_resumen_ha['total_ha_posiblesinformalidades'] + df_resumen_ha['total_ha_prediosformales']

    # ! Generación Capas Espaciales
    reporteReconocimiento_sinGeo_conMatriz_Unicos_Geo = reporteReconocimiento_sinGeo_conMatriz_Unicos_Geo.copy()
    reporteReconocimiento_sinGeo_conMatriz_Unicos_Geo = reporteReconocimiento_sinGeo_conMatriz_Unicos_Geo.astype(dict_campos_npn_matriz)

    df_terrenos_reporteReconocimiento_conGeo = df_terrenos_reporteReconocimiento_conGeo.copy()
    df_terrenos_reporteReconocimiento_conGeo = df_terrenos_reporteReconocimiento_conGeo.astype(dict_campos_conGeo)
    df_terrenos_reporteReconocimiento_conGeo = df_terrenos_reporteReconocimiento_conGeo.rename(columns={'Nº Radicado BCGS':'Num_Radicado_BCGS'})

    # **** BD CONSOLIDADA  ****
    # TODO: Informalidades
    # ** Exportación a BD Consolidada`
    if reporteReconocimiento_sinGeo_conMatriz_Unicos_Geo.shape[0] != 0:
        NOMBRE_CAPA_SALIDA = f"Analitica_UT_Consolidada\\{str(nombre_capa_haXEstado) + '_INFORMAL'.upper()}"
        ruta_salida_terrenos_reconocimiento_matrices = os.path.join(RUTA_BD_CONSOLIDADA, NOMBRE_CAPA_SALIDA)

        reporteReconocimiento_sinGeo_conMatriz_Unicos_Geo.spatial.to_featureclass(location=ruta_salida_terrenos_reconocimiento_matrices)
        print(f"Se exporta la capa {NOMBRE_CAPA_SALIDA} a BD Consolidada")
    else:
        print("No se exporta por no tener registros")

    # TODO: Formales
    # ** Exportación a BD Consolidada
    NOMBRE_CAPA_SALIDA = f"Analitica_UT_Consolidada\\{str(nombre_capa_haXEstado) + '_FORMAL'.upper()}"
    ruta_salida_terrenos_reconocimiento_formales = os.path.join(RUTA_BD_CONSOLIDADA, NOMBRE_CAPA_SALIDA)

    df_terrenos_reporteReconocimiento_conGeo.spatial.to_featureclass(location=ruta_salida_terrenos_reconocimiento_formales)
    print(f"Se exporta la capa {NOMBRE_CAPA_SALIDA} a BD Consolidada")

    # **** BD LOCAL  ****
    # TODO: Informalidades
    # ** Exportación a Local
    if reporteReconocimiento_sinGeo_conMatriz_Unicos_Geo.shape[0] != 0:
        NOMBRE_CAPA_SALIDA = f"{str(nombre_capa_haXEstado) + '_INFORMAL'.upper()}"
        ruta_salida_terrenos_reconocimiento_matrices = os.path.join(RUTA_BD_LOCAL, NOMBRE_CAPA_SALIDA)

        reporteReconocimiento_sinGeo_conMatriz_Unicos_Geo.spatial.to_featureclass(location=ruta_salida_terrenos_reconocimiento_matrices)
        print(f"Se exporta la capa {NOMBRE_CAPA_SALIDA} a Local")
    else:
        print("No se exporta por no tener registros")

    # TODO: Formales
    # ** Exportación a Local
    NOMBRE_CAPA_SALIDA = f"{str(nombre_capa_haXEstado) + '_FORMAL'.upper()}"
    ruta_salida_terrenos_reconocimiento_formales = os.path.join(RUTA_BD_LOCAL, NOMBRE_CAPA_SALIDA)

    df_terrenos_reporteReconocimiento_conGeo.spatial.to_featureclass(location=ruta_salida_terrenos_reconocimiento_formales)
    print(f"Se exporta la capa {NOMBRE_CAPA_SALIDA} a Local")

    # ! Reporte Alfanumérico
    df_resumen_ha.to_excel(os.path.join(DIRECTORIO_REPORTE, nombre_reporte_hasheet))
import os
from datetime import datetime as dt
import shutil

def reporte_a_googleDrive():
    
    # ** Librerías propias
    import funcion_personalizacion_tablas

    # TODO: Preparación Fecha
    fecha_actual = dt.now()
    fecha_estandarizada = str(fecha_actual.strftime("%Y%m%d"))

    #TODO: Ruta Origen
    DIRECTORIO_SALIDA_XLSX = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_2_Rendimientos_Reconocimiento"
    NOMBRE_XLSX = fecha_estandarizada + "_RendimientoEquipoReconocimiento_BCGS.xlsx"
    RUTA_ORIGEN = os.path.join(DIRECTORIO_SALIDA_XLSX,NOMBRE_XLSX)

    # TODO: Ruta Destino
    DIRECTORIO_ONEDRIVE = r"G:\Mi unidad\Equipo_Consolidacion\Hitos\E2_Informes_Id_FisicoJuridica\2_2_2_Rendimientos_Reconocimiento"
    RUTA_SALIDA = os.path.join(DIRECTORIO_ONEDRIVE, NOMBRE_XLSX)

    # TODO: Se aplica el formateo a la tabla de seguimiento, para ello se llama la respectiva función -funcion_personalizacion_tablas-
    funcion_personalizacion_tablas.personalizacion_tablas(os.path.join(DIRECTORIO_SALIDA_XLSX, NOMBRE_XLSX))

    # TODO: Se copia a Google Drive
    shutil.copy(RUTA_ORIGEN, RUTA_SALIDA)
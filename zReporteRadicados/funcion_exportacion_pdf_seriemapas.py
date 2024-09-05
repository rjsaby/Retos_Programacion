import os, arcpy
from datetime import datetime as dt

def exportacion_salida_grafica(nLayout, rutaPDF):
    # TODO: Parametrización de Variables

    # ? Configuración del acceso al proyecto PRO.

    # ** Se define la ruta del proyecto de PRO (extensión .aprx)
    RUTA_PROYECTO_PRO = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\1.GIS\1.2.PRO\RAISS_Lote_4\RAISS_Lote_4.aprx"

    # ** Se establece en el entorno de trabajo
    arcpy.env.workspace = RUTA_PROYECTO_PRO

    # ** Se accede por código al proyecto .aprx del proyecto, se crea un objeto de tipo proyecto
    proyecto = arcpy.mp.ArcGISProject(arcpy.env.workspace)

    # ** Ruta de exportación del PDF
    ruta_pdf = rutaPDF

    fecha = dt.now()
    fecha_pdf = str(fecha.strftime("%Y%m%d"))

    ruta_salida_pdf = os.path.join(ruta_pdf, fecha_pdf)

    resolution = 300
    page_range_type = 'ALL'
    multiple_files = 'PDF_MULTIPLE_FILES_PAGE_NAME'
    image_quality = 'BEST'

    # TODO: Acceso a los Layouts y selección del indicador para exportar
    # ** Se listan los Layouts generados en el proyecto
    for i in proyecto.listLayouts():        
        if i.name == nLayout:
            mapSerie = i.mapSeries
            if isinstance(mapSerie, arcpy._mp.MapSeries):
                if mapSerie.enabled:
                    print(f'Nombre Layout: {i.name}')
                    mapSerie.refresh()
                    mapSerie.exportToPDF(ruta_salida_pdf, 
                                        resolution = resolution,
                                        page_range_type = page_range_type,
                                        multiple_files = multiple_files,
                                        image_quality = image_quality)
                    print(f"Se exporta a PDF {i.name}")


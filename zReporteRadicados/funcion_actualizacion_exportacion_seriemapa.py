import arcpy, os
from datetime import datetime as dt

def actualizacion_exportacion_mapa(nMapa, nomCapa, nomFieldSimbologia, nLayout):
    
    RUTA_PROYECTO_PRO = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\1.GIS\1.2.PRO\RAISS_Lote_4\RAISS_Lote_4.aprx"
    RUTA_SALIDA_PDF = r"C:\docsProyectos\5.RAISS\2024.0.RAISS_Lote_4\6.Hitos\E2_Informes_Id_FisicoJuridica\2_2_0_Identificacion_Predial_Total_Ha_Actualizadas\Salidas_Graficas\2.BCGS"
    arcpy.env.workspace = RUTA_PROYECTO_PRO
    proyecto = arcpy.mp.ArcGISProject(arcpy.env.workspace)

    fecha = dt.now()
    fecha_jpeg = str(fecha.strftime("%Y%m%d"))
    ruta_salida_pdf = os.path.join(RUTA_SALIDA_PDF, fecha_jpeg)

    resolution = 300
    page_range_type = 'ALL'
    multiple_files = 'PDF_MULTIPLE_FILES_PAGE_NAME'
    image_quality = 'BEST'    
    
    m = proyecto.listMaps(nMapa)[0]
    l = m.listLayers(nomCapa)[0]
    sym = l.symbology
    sym.updateRenderer('UniqueValueRenderer')
    sym.renderer.fields = [nomFieldSimbologia]
    colorRamp = proyecto.listColorRamps("Basic Random")[0]
    sym.renderer.colorRamp = colorRamp
    l.symbology = sym 
    proyecto.save()

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

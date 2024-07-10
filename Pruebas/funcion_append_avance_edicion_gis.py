import arcpy, os

def append_terrenos_avance_edicion_gis(rutaSalidaCapas):
    
    arcpy.env.workspace = rutaSalidaCapas
    for capa in arcpy.ListFeatureClasses():
        if capa == 'terrenos_editados':
            arcpy.TruncateTable_management(capa)
            print(f"* Se completa el truncado de las tabla objetivo: {capa}")
    print(f"1. Se completa el truncado de las tablas objetivo")

    lista_rutas_append = []
    for capa in arcpy.ListFeatureClasses():
        if capa != 'terrenos_editados':
            ruta_fc_append = os.path.join(arcpy.env.workspace,capa)
            lista_rutas_append.append(ruta_fc_append)

    for capa in arcpy.ListFeatureClasses():
        if capa == 'terrenos_editados':
            arcpy.management.Append(inputs = lista_rutas_append, target = capa, schema_type='TEST')
    
    print(f"2. Se anexan capas a BD")
            
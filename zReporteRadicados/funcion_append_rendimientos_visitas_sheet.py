import arcpy, os

def append_terrenos_visitas(rutaSalidaCapas):
    arcpy.env.workspace = rutaSalidaCapas

    dict_capas_input_target = {1:['TERRENOS_VISITADOS_FORMAL','TERRENOS_VISITADOS_MARIA_LA_BAJA_FORMAL','TERRENOS_VISITADOS_REPELON_FORMAL'],
    2:['TERRENOS_VISITADOS_INFORMAL','TERRENOS_VISITADOS_MARIA_LA_BAJA_INFORMAL','TERRENOS_VISITADOS_REPELON_INFORMAL']
    }

    for capa in arcpy.ListFeatureClasses():
        for llave, valor in dict_capas_input_target.items():
            if capa == valor[0]:
                arcpy.TruncateTable_management(capa)
                print(f"* Se completa el truncado de las tabla objetivo: {valor[0]}")
    print(f"1. Se completa el truncado de las tablas objetivo")

    for capa in arcpy.ListFeatureClasses():
        for llave, valor in dict_capas_input_target.items():
            if capa == valor[0] and llave == 1:
                arcpy.Append_management(inputs=[os.path.join(arcpy.env.workspace, valor[1]), os.path.join(arcpy.env.workspace, valor[2])], target=capa, schema_type='TEST')
                print(f"Se migran {valor[1]} - {valor[2]} a {capa}")
            if capa == valor[0] and llave == 2 and (arcpy.Exists(valor[2]) == False):
                arcpy.Append_management(inputs=[os.path.join(arcpy.env.workspace, valor[1])], target=capa, schema_type='TEST')
                print(f"Se migran {valor[1]} a {capa}")
            if capa == valor[0] and llave == 2 and (arcpy.Exists(valor[2]) == True):
                arcpy.Append_management(inputs=[os.path.join(arcpy.env.workspace, valor[1]), os.path.join(arcpy.env.workspace, valor[2])], target=capa, schema_type='TEST')
                print(f"Se migran {valor[1]} - {valor[2]} a {capa}")
    print(f"2. Se completa la unificación de las tablas municipio")
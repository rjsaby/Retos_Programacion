import os
from pathlib import Path
from Clases import total_tipo_archivos_por_directorio

directorio_principal = r"C:\docsInvestigacion\Python\Retos_Programacion\rutas"
directorio_salida_resultados = r"C:\docsInvestigacion\Python"

rutas_directorios = []
for ruta, directorio, archivo in os.walk(directorio_principal):
   for nombre in directorio:
      rutas_directorios.append(ruta)
      rutas_directorios.append(os.path.join(ruta, nombre))

# ** Listar todos los directorios con el módulo Path y la función iterdir()      
for i in rutas_directorios:
   p = Path(i)
   resultado = total_tipo_archivos_por_directorio.total_archivos_por_directorio(p)
   resultado.calculo_total_tipo_archivos_por_directorio()

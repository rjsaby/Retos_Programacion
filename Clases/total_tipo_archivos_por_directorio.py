import csv

class total_archivos_por_directorio:
    def __init__(self
        ,ruta_directorio
        ):
        
        self.ruta_directorio = ruta_directorio
        # self.ruta_salida = ruta_salida
    
    def calculo_total_tipo_archivos_por_directorio(self):
        lista_archivos = [i.suffix for i in self.ruta_directorio.iterdir() if i.is_file()]
        conteo = {}
        reporte_final = {}
        for j in lista_archivos:
            if lista_archivos.count(j) >=1:
                conteo[j] = lista_archivos.count(j)
                reporte_final[self.ruta_directorio] = conteo
        
        nombre_directorio = []
        tipos_arhivo = []
        conteo_archivo = []
        for llave, value in reporte_final.items():   
            for key, values in value.items():
                nombre_directorio.append(str(llave))
                tipos_arhivo.append(str(key))
                conteo_archivo.append(int(values))

        lista_reporte_salida = [i for i in zip(nombre_directorio, tipos_arhivo, conteo_archivo)]
        
        # ** Nombre del archivo CSV
        nombre_archivo = 'reporte_conteo_archivos.csv'

        # ** Escribir en el archivo CSV
        with open(nombre_archivo, 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerows(lista_reporte_salida)

        print(f'Se ha creado el archivo CSV: {nombre_archivo}')
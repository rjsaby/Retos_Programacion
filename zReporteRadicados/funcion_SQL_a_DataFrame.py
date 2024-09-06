from sqlalchemy import create_engine, text
import pandas as pd
import time
from sqlalchemy.exc import OperationalError

# Parámetros de conexión
host = 'bcgs-multiproposito-rds-alfa-replica.c108sqqsuwz4.us-east-1.rds.amazonaws.com'
database = 'bcgs'
user = 'vigente'
password = 'tDL!cg!ZhKRRE2iC9U6Z2#nY'
port = '5432'
schema = 'bpmcat'

def sql_a_dataframe(consulta_usuario: str):

    retry_attempts = 10  # Número de reintentos
    retry_delay = 10  # Tiempo de espera en segundos antes de reintentar

    for attempt in range(retry_attempts):  # Reintenta hasta 10 veces
        try:
            print("Inicio de la conexión")
            
            # Configuración de la conexión
            url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
            engine = create_engine(url, pool_size=50, echo=False)

            # Establecer la conexión
            with engine.connect() as conexion_sqlalq:
                # Establecer el nivel de aislamiento de la transacción
                conexion_sqlalq.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")

                # Establecer el esquema en la conexión
                conexion_sqlalq.execute(text(f'SET search_path TO {schema}'))

                # Ejecutar la consulta y crear el DataFrame
                consulta_sql = pd.read_sql_query(consulta_usuario, conexion_sqlalq)

                print("Conexión exitosa ...")
                
                # Devolver el DataFrame
                return pd.DataFrame(consulta_sql)

        except OperationalError as e:
            if "conflict with recovery" in str(e):
                if attempt < retry_attempts - 1:  # Si no es el último intento
                    print(f"Conflicto detectado, reintentando en {retry_delay} segundos...")
                    time.sleep(retry_delay)  # Espera 10 segundos antes de reintentar
                else:
                    raise  # Relanza el error si ya no hay más reintentos
            else:
                raise  # Relanza si es otro tipo de error

        except Exception as e:
            print(f"Error durante la conexión o ejecución de la consulta: {e}")
            consulta_sql = None
            break  # Salir del bucle si es un error general no relacionado con OperationalError

    # Si la consulta no se ejecutó con éxito
    if consulta_sql is None:
        print("La consulta no se pudo ejecutar y la variable consulta_sql no se definió.")



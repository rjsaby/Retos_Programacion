# ? Conexión a BD Postgres. Se usa dado que pandas no acepta sino este paquete para la conexión.
from sqlalchemy import create_engine, text
import pandas as pd

# ? Función dedicada a construir DataFrames a partir de consultas.
# ? Las consultas las genera el usuario y las debe registrar como parámetros de la función

# ? Se parametrizan las variables a usar en la función de conexión (connect)
host = 'bcgs-multiproposito-rds-alfa-replica.c108sqqsuwz4.us-east-1.rds.amazonaws.com'
database = 'bcgs'
user = 'vigente'
password = 'tDL!cg!ZhKRRE2iC9U6Z2#nY'
port = '5432'
schema = 'bpmcat'

def sql_a_dataframe(consulta_usuario:str):

    try:
        print("Inicio de la conexión")
        
        # ? Se asigna a una variable los resultados de leer una consulta SQL con una conexión previamente generada
        # ? Parámetros de conexión desde sqlalchemy
        url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(url, pool_size=50, echo=False)

        # ? Asignnación de una conexión a una variable
        conexion_sqlalq = engine.connect()

        # ? Establecer el esquema en la conexión
        conexion_sqlalq.execute(text(f'SET search_path TO {schema}'))

        # ? Generación de Dataframe por medio de consulta en sql. Función read_sql_query.
        consulta_sql = pd.read_sql_query(consulta_usuario, conexion_sqlalq)

        # ? Se construye el dataframe a partir de la lectura de la consulta (usando la función read_sql_query)
        return pd.DataFrame(consulta_sql) 

        print("Conexión exitosa ...")
        
        # Cierre de la conexión
        conexion_sqlalq.close()

    except Exception as e:
        print(f"Error durante la conexión o ejecución de la consulta: {e}")
        consulta_sql = None

    # Verificar si consulta_sql_3 se definió correctamente
    if consulta_sql is not None:
        print(consulta_sql)
    else:
        print("La consulta no se pudo ejecutar y la variable consulta_sql no se definió.")


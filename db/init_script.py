import pandas as pd
import pyodbc

# Configuración de la conexión a SQL Server
server = 'localhost'
database = 'DeaceroDB'
username = 'SA'
password = 'YourStrong@Passw0rd!'
driver = '{ODBC Driver 18 for SQL Server}'

# Conectar a la base de datos
try:
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;'
    )
    cursor = conn.cursor()
    print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit(1)

# Función para obtener las columnas de la tabla en la base de datos
def obtener_columnas_tabla(tabla_destino):
    query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tabla_destino}'"
    cursor.execute(query)
    columnas = [row[0] for row in cursor.fetchall()]
    return columnas

# Función para verificar si un pasajero existe en la tabla
def existe_pasajero(pasajero_id):
    query = "SELECT 1 FROM Pasajeros WHERE ID_Pasajero = ?"
    cursor.execute(query, pasajero_id)
    return cursor.fetchone() is not None

# Función para verificar si una línea aérea existe en la tabla
def existe_linea_aerea(code):
    query = "SELECT 1 FROM CatLineasAereas WHERE Code = ?"
    cursor.execute(query, code)
    return cursor.fetchone() is not None

# Función para verificar si un vuelo existe en la tabla
def existe_vuelo(cve_la, viaje, cve_cliente):
    query = "SELECT 1 FROM Vuelos WHERE Cve_LA = ? AND Viaje = ? AND Cve_Cliente = ?"
    cursor.execute(query, cve_la, viaje, cve_cliente)
    return cursor.fetchone() is not None

# Función para cargar datos desde un CSV a una tabla de SQL Server con validación de duplicados
def cargar_datos(csv_path, tabla_destino):
    try:
        # Leer el archivo CSV en un DataFrame de pandas
        df = pd.read_csv(csv_path)
        
        # Obtener columnas válidas de la tabla de destino
        columnas_validas = obtener_columnas_tabla(tabla_destino)
        
        # Filtrar el DataFrame para incluir solo las columnas que están en la tabla de destino
        df = df[columnas_validas]

        # Insertar cada fila del DataFrame en la tabla correspondiente
        for index, row in df.iterrows():
            # Validar existencia antes de insertar
            if tabla_destino == 'Pasajeros':
                if not existe_pasajero(row['ID_Pasajero']):
                    placeholders = ', '.join(['?'] * len(row))
                    columns = ', '.join(row.index)
                    sql = f"INSERT INTO {tabla_destino} ({columns}) VALUES ({placeholders})"
                    cursor.execute(sql, tuple(row))
                else:
                    print(f"Pasajero con ID {row['ID_Pasajero']} ya existe. Saltando inserción.")
            elif tabla_destino == 'CatLineasAereas':
                if not existe_linea_aerea(row['Code']):
                    placeholders = ', '.join(['?'] * len(row))
                    columns = ', '.join(row.index)
                    sql = f"INSERT INTO {tabla_destino} ({columns}) VALUES ({placeholders})"
                    cursor.execute(sql, tuple(row))
                else:
                    print(f"Línea aérea con código {row['Code']} ya existe. Saltando inserción.")
            elif tabla_destino == 'Vuelos':
                # Verificar si la línea aérea existe en la tabla CatLineasAereas antes de insertar en Vuelos
                if existe_linea_aerea(row['Cve_LA']):
                    if not existe_vuelo(row['Cve_LA'], row['Viaje'], row['Cve_Cliente']):
                        placeholders = ', '.join(['?'] * len(row))
                        columns = ', '.join(row.index)
                        sql = f"INSERT INTO {tabla_destino} ({columns}) VALUES ({placeholders})"
                        cursor.execute(sql, tuple(row))
                    else:
                        print(f"Vuelo con Cve_LA {row['Cve_LA']}, Viaje {row['Viaje']}, y Cliente {row['Cve_Cliente']} ya existe. Saltando inserción.")
                else:
                    print(f"Línea aérea con código {row['Cve_LA']} no existe en CatLineasAereas. Saltando inserción de vuelo en índice {index}.")
        
        # Confirmar la transacción
        conn.commit()
        print(f"Datos insertados correctamente en la tabla {tabla_destino}")
    except Exception as e:
        print(f"Error al insertar datos en la tabla {tabla_destino}: {e}")

# Cargar datos en la tabla CatLineasAereas primero
cargar_datos('/var/opt/mssql/data/csv/central/CatLineasAereas.csv', 'CatLineasAereas')

# Luego cargar los datos en las tablas Pasajeros
cargar_datos('/var/opt/mssql/data/csv/sucursal1/Pasajeros.csv', 'Pasajeros')
cargar_datos('/var/opt/mssql/data/csv/sucursal2/Pasajeros.csv', 'Pasajeros')

# Finalmente cargar los datos en la tabla Vuelos
cargar_datos('/var/opt/mssql/data/csv/sucursal1/Vuelos.csv', 'Vuelos')
cargar_datos('/var/opt/mssql/data/csv/sucursal2/Vuelos.csv', 'Vuelos')

# Cerrar la conexión
cursor.close()
conn.close()

import pyodbc

# Parámetros de conexión
server = 'DESKTOP-N84VS82'
database = 'base2'  # Cambia por el nombre de tu base de datos
driver = '{ODBC Driver 17 for SQL Server}'

# Si usas autenticación de Windows:
connection_string = (
    f'DRIVER={driver};SERVER={server};DATABASE={database};'
    'Trusted_Connection=yes;TrustServerCertificate=yes;'
)

try:
    conn = pyodbc.connect(connection_string)
    print("Conexión exitosa a SQL Server.")
    conn.close()
except Exception as ex:
    print(f"Error de conexión: {ex}")
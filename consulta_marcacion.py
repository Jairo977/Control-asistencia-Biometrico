import sys
from reportes.db_utils import get_db_connection

if len(sys.argv) < 2:
    print("Uso: python consulta_marcacion.py <id_usuario>")
    sys.exit(1)

id_usuario = sys.argv[1]

query = '''
    SELECT TOP 1
        CAST(t.punch_time AS DATE) AS fecha,
        CAST(t.punch_time AS TIME(0)) AS hora
    FROM iclock_transaction t
    WHERE RTRIM(LTRIM(t.emp_code)) = RTRIM(LTRIM(?))
    ORDER BY t.punch_time DESC
'''

conn = get_db_connection()
if not conn:
    print("No se pudo conectar a la base de datos.")
    sys.exit(1)

try:
    with conn.cursor() as cur:
        cur.execute(query, [str(id_usuario).strip()])
        row = cur.fetchone()
        if row:
            print(f"Última marcación para usuario {id_usuario}: Fecha: {row.fecha}, Hora: {row.hora}")
        else:
            print(f"No se encontró marcación para usuario: {id_usuario}")
finally:
    conn.close()

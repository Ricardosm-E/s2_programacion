import pyodbc

try:
    conn = pyodbc.connect(
    "DRIVER={MySQL ODBC 9.2 ANSI Driver};" #"DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=BibliotecaDB;"
    "USER=root;"
    "PASSWORD=root;"
    )
    print("Conexión exitosa a MySQL")
    conn.close()
except Exception as e:
    print("Error de conexión:", e)

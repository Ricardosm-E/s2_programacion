import pyodbc

def obtener_conexion():
    return pyodbc.connect(
        "DRIVER={MySQL ODBC 9.2 ANSI Driver};" 
        "SERVER=localhost;"
        "DATABASE=BibliotecaDB;"
        "USER=root;"
        "PASSWORD=root;"
    )

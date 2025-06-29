import tkinter as tk
from tkinter import ttk
from conexion import obtener_conexion

def ventana_consultas():
    consulta = tk.Toplevel()
    consulta.title("Consultas SQL de Biblioteca")
    consulta.geometry("850x500")

    conn = obtener_conexion()
    cursor = conn.cursor()

    opciones = [
        "Top 3 usuarios con más préstamos",
        "Libros más demandados",
        "Préstamos entre enero y mayo",
        "Libros que nunca han sido prestados"
    ]

    combo = ttk.Combobox(consulta, values=opciones, state="readonly", width=60)
    combo.pack(pady=10)
    combo.set(opciones[0])

    tree = ttk.Treeview(consulta, show="headings")
    tree.pack(pady=10, fill="both", expand=True)

    def ejecutar_consulta():
        for item in tree.get_children():
            tree.delete(item)

        seleccion = combo.get()

        if seleccion == "Top 3 usuarios con más préstamos":
            tree["columns"] = ("ID", "Nombre", "Apellido", "Cantidad de Préstamos")
            for col in tree["columns"]:
                tree.heading(col, text=col)

            cursor.execute("""
                SELECT u.ID_Usuario, u.Nombre, u.Apellido, COUNT(p.ID_Prestamo) AS TotalPrestamos
                FROM Usuario u
                JOIN Prestamo p ON u.ID_Usuario = p.ID_Usuario
                GROUP BY u.ID_Usuario
                ORDER BY TotalPrestamos DESC
                LIMIT 3
            """)


        elif seleccion == "Libros más demandados":
            tree["columns"] = ("ISBN", "Título", "Veces Prestado")
            for col in tree["columns"]:
                tree.heading(col, text=col)
            cursor.execute("""
                           SELECT l.ISBN, l.Titulo, COUNT(p.ID_Prestamo) AS VecesPrestado
                           FROM Libro l
                                    JOIN Prestamo p ON l.ISBN = p.ISBN
                           GROUP BY l.ISBN, l.Titulo
                           ORDER BY VecesPrestado DESC
                           """)
            resultados = cursor.fetchall()

            for fila in resultados:
                fila_limpia = tuple(str(col).strip().replace("'", "") for col in fila)

                tree.insert("", tk.END, values=fila_limpia)




        elif seleccion == "Préstamos entre enero y mayo":
            tree["columns"] = ("ID_Prestamo", "Usuario", "Libro", "Fecha_Prestamo")
            for col in tree["columns"]:
                tree.heading(col, text=col)

            cursor.execute("""
                SELECT p.ID_Prestamo, CONCAT(u.Nombre, ' ', u.Apellido) AS Usuario, l.Titulo, p.Fecha_Prestamo
                FROM Prestamo p
                JOIN Usuario u ON p.ID_Usuario = u.ID_Usuario
                JOIN Libro l ON p.ISBN = l.ISBN
                WHERE MONTH(p.Fecha_Prestamo) BETWEEN 1 AND 5
            """)

            resultados = cursor.fetchall()

            for fila in resultados:
                fila_limpia = tuple(str(col).strip().replace("'", "") for col in fila)
                tree.insert("", tk.END, values=fila_limpia)



        elif seleccion == "Libros que nunca han sido prestados":
            tree["columns"] = ("ISBN", "Título", "Estado")
            for col in tree["columns"]:
                tree.heading(col, text=col)

            cursor.execute("""
                SELECT l.ISBN, l.Titulo, l.Estado
                FROM Libro l
                LEFT JOIN Prestamo p ON l.ISBN = p.ISBN
                WHERE p.ID_Prestamo IS NULL
            """)

            resultados = cursor.fetchall()

            for fila in resultados:
                fila_limpia = tuple(str(col).strip().replace("'", "") for col in fila)
                tree.insert("", tk.END, values=fila_limpia)


    tk.Button(consulta, text="Ejecutar Consulta", command=ejecutar_consulta).pack(pady=5)

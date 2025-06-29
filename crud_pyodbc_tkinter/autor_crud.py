import tkinter as tk
from tkinter import ttk
from conexion import obtener_conexion

def ventana_autores():
    conn = obtener_conexion()
    cursor = conn.cursor()

    def mostrar():
        for i in tree.get_children():
            tree.delete(i)
        cursor.execute("SELECT ID_Autor, Nombre_Autor, Nacionalidad FROM Autor WHERE Estado != 'Inactivo'")
        for fila in cursor.fetchall():
            id_autor = str(fila[0])
            nombre = fila[1]
            nacionalidad_val = fila[2]
            tree.insert("", tk.END, values=(id_autor, nombre, nacionalidad_val))

    def insertar():
        datos = (nombre_autor.get(), nacionalidad.get())
        cursor.execute("INSERT INTO Autor (Nombre_Autor, Nacionalidad, Estado) VALUES (?, ?, 'Activo')", datos)
        conn.commit()
        mostrar()
        nombre_autor.delete(0, tk.END)
        nacionalidad.delete(0, tk.END)

    def actualizar():
        item = tree.focus()
        if not item:
            return
        id_autor = tree.item(item, "values")[0]
        datos = (nombre_autor.get(), nacionalidad.get(), id_autor)
        cursor.execute("UPDATE Autor SET Nombre_Autor=?, Nacionalidad=? WHERE ID_Autor=?", datos)
        conn.commit()
        mostrar()
        nombre_autor.delete(0, tk.END)
        nacionalidad.delete(0, tk.END)
    def eliminar():
        item = tree.focus()
        if not item:
            return
        id_autor = tree.item(item, "values")[0]
        cursor.execute("UPDATE Autor SET Estado='Inactivo' WHERE ID_Autor=?", (id_autor,))
        conn.commit()
        mostrar()
        nombre_autor.delete(0, tk.END)
        nacionalidad.delete(0, tk.END)

    def cargar_datos(event):
        item = tree.focus()
        if item:
            datos = tree.item(item, "values")
            nombre_autor.delete(0, tk.END)
            nacionalidad.delete(0, tk.END)
            nombre_autor.insert(0, datos[1])
            nacionalidad.insert(0, datos[2])

    ventana = tk.Toplevel()
    ventana.title("Gestión de Autores")
    ventana.geometry("600x300")

    tk.Label(ventana, text="Nombre del Autor").grid(row=0, column=0)
    nombre_autor = tk.Entry(ventana)
    nombre_autor.grid(row=0, column=1)

    tk.Label(ventana, text="Nacionalidad").grid(row=1, column=0)
    nacionalidad = tk.Entry(ventana)
    nacionalidad.grid(row=1, column=1)

    tk.Button(ventana, text="Insertar", command=insertar).grid(row=0, column=2)
    tk.Button(ventana, text="Actualizar", command=actualizar).grid(row=1, column=2)
    tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=2, column=2)

    tree = ttk.Treeview(ventana, columns=("ID", "Nombre_Autor", "Nacionalidad"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre_Autor", text="Nombre Autor")
    tree.heading("Nacionalidad", text="Nacionalidad")
    tree.grid(row=4, column=0, columnspan=3)
    tree.bind("<<TreeviewSelect>>", cargar_datos)

    mostrar()
    ventana.mainloop()

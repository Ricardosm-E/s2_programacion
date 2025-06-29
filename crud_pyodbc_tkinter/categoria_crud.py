import tkinter as tk
from tkinter import ttk
from conexion import obtener_conexion

def ventana_categorias():
    conn = obtener_conexion()
    cursor = conn.cursor()

    def mostrar():
        for i in tree.get_children():
            tree.delete(i)
        cursor.execute("SELECT ID_Categoria, Nombre_Categoria, Estado FROM Categoria WHERE Estado = 'Activo'")
        for fila in cursor.fetchall():
            id_categoria = fila[0]
            nombre_categoria = fila[1].strip("'")  # Limpieza de comillas si existen
            estado = fila[2]
            tree.insert("", tk.END, values=(id_categoria, nombre_categoria, estado))

    def insertar():
        nombre_categoria_val = nombre_categoria.get().strip()
        cursor.execute("INSERT INTO Categoria (Nombre_Categoria) VALUES (?)", (nombre_categoria_val,))
        conn.commit()
        mostrar()

    def actualizar():
        item = tree.focus()
        if not item:
            return
        id_categoria = tree.item(item, "values")[0]
        cursor.execute("UPDATE Categoria SET Nombre_Categoria=? WHERE ID_Categoria=?", (nombre_categoria.get(), id_categoria))
        conn.commit()
        mostrar()

    def eliminar():
        item = tree.focus()
        if not item:
            return
        id_categoria = tree.item(item, "values")[0]
        cursor.execute("UPDATE Categoria SET Estado='Inactivo' WHERE ID_Categoria=?", (id_categoria,))
        conn.commit()
        mostrar()

    def cargar_datos(event):
        item = tree.focus()
        if item:
            datos = tree.item(item, "values")
            nombre_categoria.delete(0, tk.END)
            nombre_categoria.insert(0, datos[1])

    ventana = tk.Toplevel()
    ventana.title("Gestión de Categorías")
    ventana.geometry("600x300")

    tk.Label(ventana, text="Nombre de Categoría").grid(row=0, column=0)
    nombre_categoria = tk.Entry(ventana)
    nombre_categoria.grid(row=0, column=1)

    tk.Button(ventana, text="Insertar", command=insertar).grid(row=0, column=2)
    tk.Button(ventana, text="Actualizar", command=actualizar).grid(row=1, column=2)
    tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=2, column=2)

    tree = ttk.Treeview(ventana, columns=("ID", "Nombre_Categoria", "Estado"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre_Categoria", text="Nombre Categoría")
    tree.heading("Estado", text="Estado")
    tree.grid(row=4, column=0, columnspan=3)
    tree.bind("<<TreeviewSelect>>", cargar_datos)

    mostrar()
    ventana.mainloop()

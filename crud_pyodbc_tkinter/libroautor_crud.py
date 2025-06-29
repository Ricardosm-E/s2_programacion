import tkinter as tk
from tkinter import ttk
from conexion import obtener_conexion

def ventana_libroautor():
    conn = obtener_conexion()
    cursor = conn.cursor()

    def cargar_libros_autores():
        cursor.execute("SELECT ISBN, Titulo FROM Libro")
        libros.clear()
        for row in cursor.fetchall():
            libros[row[1]] = row[0]
        combo_libro['values'] = list(libros.keys())

        cursor.execute("SELECT ID_Autor, Nombre_Autor FROM Autor")
        autores.clear()
        for row in cursor.fetchall():
            autores[row[1]] = row[0]
        combo_autor['values'] = list(autores.keys())

    def mostrar():
        for i in tree.get_children():
            tree.delete(i)
        cursor.execute("SELECT ID_Libro, ID_Autor FROM LibroAutor")
        for fila in cursor.fetchall():
            tree.insert("", tk.END, values=fila)

    def insertar():
        datos = (libros[combo_libro.get()], autores[combo_autor.get()])
        cursor.execute("INSERT INTO LibroAutor (ID_Libro, ID_Autor) VALUES (?, ?)", datos)
        conn.commit()
        mostrar()

    def eliminar():
        item = tree.focus()
        if not item:
            return
        libro_id, autor_id = tree.item(item, "values")
        cursor.execute("DELETE FROM LibroAutor WHERE ID_Libro=? AND ID_Autor=?", (libro_id, autor_id))
        conn.commit()
        mostrar()

    ventana = tk.Toplevel()
    ventana.title("Gestión de Libro-Autor")
    ventana.geometry("600x300")

    libros = {}
    autores = {}

    tk.Label(ventana, text="Libro").grid(row=0, column=0)
    combo_libro = ttk.Combobox(ventana)
    combo_libro.grid(row=0, column=1)

    tk.Label(ventana, text="Autor").grid(row=1, column=0)
    combo_autor = ttk.Combobox(ventana)
    combo_autor.grid(row=1, column=1)

    tk.Button(ventana, text="Insertar", command=insertar).grid(row=0, column=2)
    tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=1, column=2)

    tree = ttk.Treeview(ventana, columns=("ID_Libro", "ID_Autor"), show="headings")
    tree.heading("ID_Libro", text="ID Libro")
    tree.heading("ID_Autor", text="ID Autor")
    tree.grid(row=3, column=0, columnspan=3)

    cargar_libros_autores()
    mostrar()
    ventana.mainloop()

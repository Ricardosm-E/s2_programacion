import tkinter as tk
from tkinter import ttk
from conexion import obtener_conexion

def ventana_libros():
    conn = obtener_conexion()
    cursor = conn.cursor()

    def cargar_categorias():
        cursor.execute("SELECT ID_Categoria, Nombre_Categoria FROM Categoria WHERE Estado = 'Activo'")
        categorias.clear()
        for row in cursor.fetchall():
            categorias[row[1]] = row[0]
        combo_categoria['values'] = list(categorias.keys())

    def mostrar():
        for i in tree.get_children():
            tree.delete(i)
        cursor.execute(
            "SELECT ISBN, Titulo, Año_Publicacion, Editorial, Estado, ID_Categoria FROM Libro WHERE Estado != 'Eliminar'")
        for fila in cursor.fetchall():
            isbn_val = str(fila[0])
            titulo_val = fila[1]
            año_val = str(fila[2])
            editorial_val = fila[3]
            estado_val = fila[4]
            id_categoria_val = str(fila[5])
            tree.insert("", tk.END,
                        values=(isbn_val, titulo_val, año_val, editorial_val, estado_val, id_categoria_val))

    def insertar():
        datos = (
            isbn.get(), titulo.get(), año.get(), editorial.get(), estado.get(), categorias[combo_categoria.get()]
        )
        cursor.execute("""
            INSERT INTO Libro (ISBN, Titulo, Año_Publicacion, Editorial, Estado, ID_Categoria)
            VALUES (?, ?, ?, ?, ?, ?)
        """, datos)
        conn.commit()
        mostrar()

    def actualizar():
        item = tree.focus()
        if not item:
            return
        categoria_seleccionada = combo_categoria.get()
        if not categoria_seleccionada or categoria_seleccionada not in categorias:
            tk.messagebox.showwarning("Advertencia", "Seleccione una categoría válida antes de actualizar.")
            return
        datos = (
            titulo.get(), año.get(), editorial.get(), estado.get(), categorias[categoria_seleccionada], isbn.get()
        )
        cursor.execute("""
                       UPDATE Libro
                       SET Titulo=?,
                           Año_Publicacion=?,
                           Editorial=?,
                           Estado=?,
                           ID_Categoria=?
                       WHERE ISBN = ?
                       """, datos)
        conn.commit()
        mostrar()
        isbn.delete(0, tk.END)
        titulo.delete(0, tk.END)
        año.delete(0, tk.END)
        editorial.delete(0, tk.END)
        estado.delete(0, tk.END)
        combo_categoria.delete(0, tk.END)

    def eliminar():
        item = tree.focus()
        if not item:
            return
        codigo = tree.item(item, "values")[0]
        cursor.execute("UPDATE Libro SET Estado='Eliminar' WHERE ISBN=?", (codigo,))
        conn.commit()
        mostrar()

    def cargar_datos(event):
        item = tree.focus()
        if item:
            datos = tree.item(item, "values")
            isbn.delete(0, tk.END)
            titulo.delete(0, tk.END)
            año.delete(0, tk.END)
            editorial.delete(0, tk.END)
            estado.set(datos[4])

            isbn.insert(0, datos[0])
            titulo.insert(0, datos[1])
            año.insert(0, datos[2])
            editorial.insert(0, datos[3])
            for nombre, id_categoria in categorias.items():
                if id_categoria == datos[5]:
                    combo_categoria.set(nombre)
                    break

    ventana = tk.Toplevel()
    ventana.title("Gestión de Libros")
    ventana.geometry("900x400")

    categorias = {}

    tk.Label(ventana, text="ISBN").grid(row=0, column=0)
    isbn = tk.Entry(ventana)
    isbn.grid(row=0, column=1)

    tk.Label(ventana, text="Título").grid(row=1, column=0)
    titulo = tk.Entry(ventana)
    titulo.grid(row=1, column=1)

    tk.Label(ventana, text="Año Publicación").grid(row=2, column=0)
    año= tk.Entry(ventana)
    año.grid(row=2, column=1)

    tk.Label(ventana, text="Editorial").grid(row=3, column=0)
    editorial = tk.Entry(ventana)
    editorial.grid(row=3, column=1)

    tk.Label(ventana, text="Estado").grid(row=4, column=0)
    estado = ttk.Combobox(ventana, values=["Disponible", "Prestado"])
    estado.grid(row=4, column=1)

    tk.Label(ventana, text="Categoría").grid(row=5, column=0)
    combo_categoria = ttk.Combobox(ventana)
    combo_categoria.grid(row=5, column=1)

    tk.Button(ventana, text="Insertar", command=insertar).grid(row=0, column=2)
    tk.Button(ventana, text="Actualizar", command=actualizar).grid(row=1, column=2)
    tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=2, column=2)

    tree = ttk.Treeview(ventana, columns=("ISBN", "Titulo", "Año", "Editorial", "Estado", "ID_Categoria"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.grid(row=7, column=0, columnspan=3)
    tree.bind("<<TreeviewSelect>>", cargar_datos)

    cargar_categorias()
    mostrar()
    ventana.mainloop()

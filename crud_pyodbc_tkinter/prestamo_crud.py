import tkinter as tk
from tkinter import ttk
from conexion import obtener_conexion
from datetime import date
def ventana_prestamos():
    conn = obtener_conexion()
    cursor = conn.cursor()

    def cargar_usuarios_libros():
        cursor.execute("SELECT ID_Usuario, Nombre FROM Usuario")
        usuarios.clear()
        for row in cursor.fetchall():
            usuarios[row[1]] = row[0]
        combo_usuario['values'] = list(usuarios.keys())

        cursor.execute("SELECT ISBN, Titulo FROM Libro")
        libros.clear()
        for row in cursor.fetchall():
            libros[row[1]] = row[0]
        combo_libro['values'] = list(libros.keys())

    def mostrar():
        for i in tree.get_children():
            tree.delete(i)
        cursor.execute("SELECT * FROM Prestamo WHERE Estado != 'Eliminar'")
        for fila in cursor.fetchall():
            id_prestamo = fila[0]
            fecha_prestamo_str = fila[1].strftime("%Y-%m-%d") if isinstance(fila[1], date) else fila[1]
            fecha_devolucion_str = fila[2].strftime("%Y-%m-%d") if isinstance(fila[2], date) else fila[2]
            fecha_renovacion_str = fila[3].strftime("%Y-%m-%d") if isinstance(fila[3], date) else fila[3]
            estado_val = fila[4]
            id_usuario = fila[5]
            isbn = fila[6]

            tree.insert("", tk.END,
                        values=(id_prestamo, fecha_prestamo_str, fecha_devolucion_str, fecha_renovacion_str, estado_val,
                                id_usuario, isbn))
            tree.update_idletasks()

    def insertar():
        datos = (
            fecha_prestamo.get(), fecha_devolucion.get(), fecha_renovacion.get(), estado.get(),
            usuarios[combo_usuario.get()], libros[combo_libro.get()]
        )
        cursor.execute("""
            INSERT INTO Prestamo (Fecha_Prestamo, Fecha_Devolucion, Fecha_Renovacion, Estado, ID_Usuario, ISBN)
            VALUES (?, ?, ?, ?, ?, ?)
        """, datos)
        conn.commit()
        mostrar()

    def actualizar():
        item = tree.focus()
        if not item:
            return

        try:
            id_prestamo = tree.item(item, "values")[0]

            datos = (
                fecha_prestamo.get(),
                fecha_devolucion.get(),
                fecha_renovacion.get(),
                estado.get(),
                usuarios[combo_usuario.get()],
                libros[combo_libro.get()],
                id_prestamo
            )

            cursor.execute("""
                           UPDATE Prestamo
                           SET Fecha_Prestamo   = ?,
                               Fecha_Devolucion = ?,
                               Fecha_Renovacion = ?,
                               Estado           = ?,
                               ID_Usuario       = ?,
                               ISBN             = ?
                           WHERE ID_Prestamo = ?
                           """, datos)

            conn.commit()
            mostrar()

        except Exception as e:
            print("Error al actualizar:", e)

    def actualizar():
        item = tree.focus()
        if not item:
            return

        try:
            id_prestamo = tree.item(item, "values")[0]

            datos = (
                fecha_prestamo.get(),
                fecha_devolucion.get(),
                fecha_renovacion.get(),
                estado.get(),
                usuarios.get(combo_usuario.get(), None),
                libros.get(combo_libro.get(), None),
                id_prestamo
            )

            if None in datos:
                print("Error: Usuario o libro no seleccionado correctamente")
                return

            cursor.execute("""
                           UPDATE Prestamo
                           SET Fecha_Prestamo   = ?,
                               Fecha_Devolucion = ?,
                               Fecha_Renovacion = ?,
                               Estado           = ?,
                               ID_Usuario       = ?,
                               ISBN             = ?
                           WHERE ID_Prestamo = ?
                           """, datos)

            conn.commit()
            mostrar()

        except Exception as e:
            print("Error al actualizar:", e)
        fecha_prestamo.delete(0, tk.END)
        fecha_devolucion.delete(0, tk.END)
        fecha_renovacion.delete(0, tk.END)
        estado.set("")
        combo_usuario.set("")
        combo_libro.set("")

    def eliminar():
        item = tree.focus()
        if not item:
            return
        id_prestamo = tree.item(item, "values")[0]

        # Eliminado lógico:
        cursor.execute("UPDATE Prestamo SET Estado = ? WHERE ID_Prestamo = ?", ("Eliminar", id_prestamo))
        conn.commit()
        mostrar()

    def cargar_datos(event):
        item = tree.focus()
        if item:
            datos = tree.item(item, "values")
            fecha_prestamo.delete(0, tk.END)
            fecha_devolucion.delete(0, tk.END)
            fecha_renovacion.delete(0, tk.END)
            estado.set(datos[4])

            fecha_prestamo.insert(0, datos[1])
            fecha_devolucion.insert(0, datos[2])
            fecha_renovacion.insert(0, datos[3])

            for nombre, id_valor in usuarios.items():
                if id_valor == datos[5]:
                    combo_usuario.set(nombre)
                    break
            for titulo, isbn_val in libros.items():
                if isbn_val == datos[6]:
                    combo_libro.set(titulo)
                    break

    ventana = tk.Toplevel()
    ventana.title("Gestión de Préstamos")
    ventana.geometry("900x400")

    usuarios = {}
    libros = {}

    tk.Label(ventana, text="Fecha Préstamo (YYYY-MM-DD)").grid(row=0, column=0)
    fecha_prestamo = tk.Entry(ventana)
    fecha_prestamo.grid(row=0, column=1)

    tk.Label(ventana, text="Fecha Devolución (YYYY-MM-DD)").grid(row=1, column=0)
    fecha_devolucion = tk.Entry(ventana)
    fecha_devolucion.grid(row=1, column=1)

    tk.Label(ventana, text="Fecha Renovación (YYYY-MM-DD)").grid(row=2, column=0)
    fecha_renovacion = tk.Entry(ventana)
    fecha_renovacion.grid(row=2, column=1)

    tk.Label(ventana, text="Estado").grid(row=3, column=0)
    estado = ttk.Combobox(ventana, values=["Activo", "Devuelto", "Renovado"])
    estado.grid(row=3, column=1)

    tk.Label(ventana, text="Usuario").grid(row=4, column=0)
    combo_usuario = ttk.Combobox(ventana)
    combo_usuario.grid(row=4, column=1)

    tk.Label(ventana, text="Libro").grid(row=5, column=0)
    combo_libro = ttk.Combobox(ventana)
    combo_libro.grid(row=5, column=1)

    tk.Button(ventana, text="Insertar", command=insertar).grid(row=0, column=2)
    tk.Button(ventana, text="Actualizar", command=actualizar).grid(row=1, column=2)
    tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=2, column=2)

    tree = ttk.Treeview(ventana, columns=("ID", "Fecha_Prestamo", "Fecha_Devolucion", "Fecha_Renovacion", "Estado", "ID_Usuario", "ISBN"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.grid(row=8, column=0, columnspan=3)
    tree.bind("<<TreeviewSelect>>", cargar_datos)

    cargar_usuarios_libros()
    mostrar()
    ventana.mainloop()

import tkinter as tk
from tkinter import ttk
from conexion import obtener_conexion

def ventana_usuarios():
    conn = obtener_conexion()
    cursor = conn.cursor()

    def mostrar():
        for i in tree.get_children():
            tree.delete(i)
        cursor.execute("SELECT * FROM Usuario WHERE Estado != 'Eliminar'")
        for fila in cursor.fetchall():
            id_usuario = str(fila[0])
            nombre = fila[1]
            apellido = fila[2]
            direccion = fila[3]
            correo = fila[4]
            telefono = fila[5]
            tree.insert("", tk.END, values=(id_usuario, nombre, apellido, direccion, correo, telefono))


    def insertar():
        datos = (
            nombre.get(), apellido.get(), direccion.get(), correo.get(), telefono.get()
        )
        cursor.execute("""
            INSERT INTO Usuario (Nombre, Apellido, Direccion, Correo_Electronico, Telefono)
            VALUES (?, ?, ?, ?, ?)
        """, datos)
        conn.commit()
        mostrar()

    def actualizar():
        item = tree.focus()
        if not item:
            return
        id_usuario = tree.item(item, "values")[0]
        datos = (
            nombre.get(), apellido.get(), direccion.get(), correo.get(), telefono.get(), id_usuario
        )
        cursor.execute("""
            UPDATE Usuario
            SET Nombre=?, Apellido=?, Direccion=?, Correo_Electronico=?, Telefono=?
            WHERE ID_Usuario=?
        """, datos)
        conn.commit()
        mostrar()
        nombre.delete(0, tk.END)
        apellido.delete(0, tk.END)
        direccion.delete(0, tk.END)
        correo.delete(0, tk.END)
        telefono.delete(0, tk.END)
        id_usuario.set("")


    def eliminar():
        item = tree.focus()
        if not item:
            return
        id_usuario = tree.item(item, "values")[0]

        # Eliminado lógico: cambiamos el estado a 'Eliminar'
        cursor.execute("UPDATE Usuario SET Estado = ? WHERE ID_Usuario = ?", ("Eliminar", id_usuario))
        conn.commit()
        mostrar()

    def cargar_datos(event):
        item = tree.focus()
        if item:
            datos = tree.item(item, "values")
            nombre.delete(0, tk.END)
            apellido.delete(0, tk.END)
            direccion.delete(0, tk.END)
            correo.delete(0, tk.END)
            telefono.delete(0, tk.END)
            nombre.insert(0, datos[1])
            apellido.insert(0, datos[2])
            direccion.insert(0, datos[3])
            correo.insert(0, datos[4])
            telefono.insert(0, datos[5])

    ventana = tk.Toplevel()
    ventana.title("Gestión de Usuarios")
    ventana.geometry("800x400")

    etiquetas = ["Nombre", "Apellido", "Dirección", "Correo", "Teléfono"]
    entradas = []
    for i, texto in enumerate(etiquetas):
        tk.Label(ventana, text=texto).grid(row=i, column=0)
        entrada = tk.Entry(ventana)
        entrada.grid(row=i, column=1)
        entradas.append(entrada)

    nombre, apellido, direccion, correo, telefono = entradas

    tk.Button(ventana, text="Insertar", command=insertar).grid(row=0, column=2)
    tk.Button(ventana, text="Actualizar", command=actualizar).grid(row=1, column=2)
    tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=2, column=2)

    tree = ttk.Treeview(ventana, columns=("ID", "Nombre", "Apellido", "Direccion", "Correo", "Telefono"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.grid(row=6, column=0, columnspan=3)
    tree.bind("<<TreeviewSelect>>", cargar_datos)

    mostrar()
    ventana.mainloop()

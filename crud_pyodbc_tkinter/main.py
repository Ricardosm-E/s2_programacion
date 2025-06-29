import tkinter as tk
from usuario_crud import ventana_usuarios
from categoria_crud import ventana_categorias
from libro_crud import ventana_libros
from autor_crud import ventana_autores
from prestamo_crud import ventana_prestamos
from consultas import ventana_consultas  # <--- NUEVO

def main_menu():
    root = tk.Tk()
    root.title("Sistema de Biblioteca - Menú Principal")
    root.geometry("400x450")

    tk.Label(root, text="Sistema de Biblioteca", font=("Arial", 16)).pack(pady=20)

    tk.Button(root, text="Gestionar Usuarios", command=ventana_usuarios, width=30).pack(pady=5)
    tk.Button(root, text="Gestionar Categorías", command=ventana_categorias, width=30).pack(pady=5)
    tk.Button(root, text="Gestionar Libros", command=ventana_libros, width=30).pack(pady=5)
    tk.Button(root, text="Gestionar Autores", command=ventana_autores, width=30).pack(pady=5)
    tk.Button(root, text="Gestionar Préstamos", command=ventana_prestamos, width=30).pack(pady=5)
    tk.Button(root, text="Consultas", command=ventana_consultas, width=30).pack(pady=5)  # <--- NUEVO

    tk.Button(root, text="Salir", command=root.quit, width=30).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main_menu()

from tkinter import ttk
from tkinter import *
import sqlite3


class Product:
    db = 'database/product.db'

    def db_query(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def __init__(self, root):
        self.windows = root
        self.windows.title("App Gestor de Productos")  # Título de la ventana
        self.windows.resizable(1, 1)  # Activar la redimensión de la ventana. Para desactivarla: (0,0)
        self.windows.wm_iconbitmap('recursos/icon.ico')

        # Creación del contenedor Frame principal
        frame = LabelFrame(self.windows, text='Registro de un nuevo Producto')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text='Nombre: ')
        self.etiqueta_nombre.grid(row=1, column=0)
        # Entry Nombre
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text='precio: ')
        self.etiqueta_precio.grid(row=2, column=0)
        # Entry Precio
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # Botón añadir Producto
        self.boton_add = ttk.Button(frame, text='Guardar Producto')
        self.boton_add.grid(row=3, columnspan=2, sticky=W + E)

        # Tabla Productos

        # Estructura de la tabla
        self.tabla = ttk.Treeview(frame, height=20, columns=2)
        self.tabla.grid(row=4, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)
        self.tabla.heading('#1', text='Precio', anchor=CENTER)



if __name__ == '__main__':
    root = Tk()  # instalación de la ventana principal
    app = Product(root)  # Se envía a la clase Product el control sobre la ventana root
    root.mainloop()  # Comenzamos el bucle de aplicación, es como un while True

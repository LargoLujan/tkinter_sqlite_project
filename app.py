from tkinter import ttk
from tkinter import *
import sqlite3


class Product:

    def __init__(self, root):
        self.windows = root
        self.windows.title("App Gestor de Productos")  # Título de la ventana
        self.windows.resizable(1,1)  # Activar la redimensión de la ventana. Para desactivarla: (0,0)
        self.windows.wm_iconbitmap('recursos/icon.ico')


if __name__ == '__main__':
    root = Tk()  # instalación de la ventana principal
    app = Product(root)  # Se envía a la clase Product el control sobre la ventana root
    root.mainloop()  # Comenzamos el bucle de aplicación, es como un while True

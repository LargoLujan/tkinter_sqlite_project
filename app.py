from tkinter import ttk, messagebox
from tkinter import *
from ttkthemes import ThemedStyle # Importa ThemedTk desde ttkthemes
import sqlite3


class Product:
    db = 'database/products.db'

    def __init__(self, root):
        self.windows = root
        self.windows.title("App Gestor de Productos")  # Título de la ventana
        self.windows.resizable(1, 1)  # Activar el redimensionamiento de la ventana. Para desactivarla: (0,0)
        self.windows.wm_iconbitmap('recursos/icon.ico')
        style = ThemedStyle(self.windows) # Aplica el tema 'vista' de ttkthemes
        style.set_theme('clam')

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
        self.etiqueta_precio = Label(frame, text='Precio: ')
        self.etiqueta_precio.grid(row=2, column=0)
        # Entry Precio
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # Label Categoría
        self.etiqueta_categoria = Label(frame, text='Categoría: ')
        self.etiqueta_categoria.grid(row=3, column=0)
        # Entry Categoría
        self.categoria = Entry(frame)
        self.categoria.grid(row=3, column=1)

        # Label Stock
        self.etiqueta_stock = Label(frame, text='Stock: ')
        self.etiqueta_stock.grid(row=4, column=0)
        # Entry Stock
        self.stock = Entry(frame)
        self.stock.grid(row=4, column=1)

        # Botón añadir Producto
        self.boton_add = ttk.Button(frame, text='Guardar Producto', command=self.add_product)
        self.boton_add.grid(row=5, columnspan=2, sticky=W + E)

        # Tabla Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.TreeView", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.TreeView.Heading",
                        font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.TreeView", [('mystyle.TreeView.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes

        # Crear una etiqueta en el estilo personalizado
        style.map("mystyle.TreeView", background=[('selected', 'blue')], foreground=[('selected', 'white')])

        # Estructura de la tabla
        self.tabla = ttk.Treeview(frame, height=20, columns=("Precio", "Categoría", "Stock"), style='mystyle.TreeView')  # Añade una columna para Categoría
        self.tabla.grid(row=6, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)  # Cabeceras de la tabla
        self.tabla.heading('#1', text='Precio', anchor=CENTER)
        self.tabla.heading('#2', text='Categoría', anchor=CENTER)
        self.tabla.heading('#3', text='Stock', anchor=CENTER)

        # Asociamos la función 'on_select' al evento de selección de la tabla
        self.tabla.bind('<<TreeviewSelect>>', self.on_select)

        # Mensaje
        self.mensaje = Label(frame, text='')
        self.mensaje.grid(row=8, columnspan=2)

        # Botones de eliminar y editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))

        boton_eliminar = ttk.Button(text="Eliminar", style='my.TButton', command=self.del_producto)
        boton_eliminar.grid(row=6, column=0, columnspan=3, sticky=W + E)
        boton_editar = ttk.Button(text="Editar", style='my.TButton', command=self.edit_producto)
        boton_editar.grid(row=7, column=0, columnspan=3, sticky=W + E)

        self.get_products()

    def on_select(self, event):
        # Obtenemos el elemento seleccionado
        item = self.tabla.selection()[0]
        # Marcamos el elemento seleccionado
        self.tabla.item(item, tags=('selected',))

    def db_query(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_products(self):

        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = "SELECT * FROM product ORDER BY name DESC"
        registros = self.db_query(query)

        for fila in registros:
            print(fila)
            self.tabla.insert("", 0, text=fila[1], values=(fila[2], fila[3], fila[4]))

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):

        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def validacion_categoria(self):

        categoria_introducido_por_usuario = self.categoria.get()
        return len(categoria_introducido_por_usuario) != 0

    def validacion_stock(self):

        stock_introducido_por_usuario = self.stock.get()
        return len(stock_introducido_por_usuario) != 0

    def add_product(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock():
            query = "INSERT INTO product VALUES(NULL, ?, ?, ?, ?)"
            messagebox.showinfo("Información",
                                "Producto: " + self.nombre.get() + "\n" + "Precio: " + self.precio.get() + " €" + "\n" + "Categoria: " + self.categoria.get()+ "\n" + "Stock: " + self.stock.get())
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get())
            self.db_query(query, parametros)
            # Para debug
            # print(self.nombre.get())
            # print(self.precio.get())
        elif self.validacion_nombre() and self.validacion_precio() == False:
            messagebox.showerror("Error", "El precio es obligatorio")
        elif self.validacion_precio() and self.validacion_nombre() == False:
            messagebox.showerror("Error", "El nombre es obligatorio")
        elif not self.validacion_categoria():
            messagebox.showerror("Error", "La categoría es obligatoria")
        elif not self.validacion_stock():
            messagebox.showerror("Error", "El stock es obligatorio")
        else:
            messagebox.showerror("Error", "El nombre, el precio, la categoría y el stock son obligatorios")
        # elif self.validacion_nombre() and self.validacion_precio() == False:
        #     messagebox.showerror("Error", "El precio es obligatorio")
        # elif self.validacion_precio() and self.validacion_nombre() == False:
        #     messagebox.showerror("Error", "El nombre es obligatorio")
        # else:
        #     messagebox.showerror("Error", "El nombre y el precio son obligatorios")
        self.get_products()

    def del_producto(self):
        try:
            # obtener el nombre del producto seleccionado
            nombre = self.tabla.item(self.tabla.selection())['text']
            # ejecutar una consulta SQL para eliminar el producto de la base de datos
            query = "DELETE FROM product WHERE name = ?"
            self.db_query(query, (nombre,))
            # eliminar el elemento seleccionado de la tabla
            self.tabla.delete(self.tabla.selection())
            # mostrar un mensaje de éxito
            self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        except IndexError:
            # mostrar un mensaje de error si no hay ningún elemento seleccionado en la tabla
            self.mensaje['text'] = 'Por favor, seleccione un producto'

    def edit_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacío

        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
            old_precio = self.tabla.item(self.tabla.selection())['values'][
                0]  # El precio se encuentra dentro de una lista
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        # Crear una ventana por delante de la principal
        self.ventana_editar = Toplevel()
        # Titulo de la ventana
        self.ventana_editar.title = "Editar Producto"
        # Activar la redimension de la ventana. Para desactivarla: (0,0)
        self.ventana_editar.resizable(1, 1)
        # Icono de la ventana
        self.ventana_editar.wm_iconbitmap('recursos/icon.ico')


if __name__ == '__main__':
    root = Tk()  # instalación de la ventana principal
    app = Product(root)  # Se envía a la clase Product el control sobre la ventana root
    root.mainloop()  # Comenzamos el bucle de aplicación, es como un while True

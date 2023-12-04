import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import pandas as pd
from PIL import Image, ImageTk


class AplicacionInventario:
    def __init__(self, master):
        self.master = master
        self.master.title('Sistema de Inventario')

        self.inventario = pd.DataFrame(columns=['Nombre', 'Código', 'Precio', 'Cantidad', 'Proveedor', 'Foto'])
        self.productos_frames = []

        self.crear_widgets()

    def crear_widgets(self):
        self.boton_agregar_producto = tk.Button(self.master, text="Agregar Producto", command=self.agregar_producto)
        self.boton_agregar_producto.pack()

        self.contenedor_productos = tk.Frame(self.master)
        self.contenedor_productos.pack(fill='both', expand=True)
        # Configurar la grilla del contenedor de productos para que se expanda
        self.contenedor_productos.grid_columnconfigure(0, weight=1)
        self.contenedor_productos.grid_columnconfigure(1, weight=1)
        self.contenedor_productos.grid_columnconfigure(2, weight=1)

        self.boton_informe = tk.Button(self.master, text="Generar Informe", command=self.generar_informe)
        self.boton_informe.pack()

        self.boton_guardar = tk.Button(self.master, text="Guardar Cambios", command=self.guardar_cambios)
        self.boton_guardar.pack()

        self.boton_salir = tk.Button(self.master, text="Salir", command=self.master.quit)
        self.boton_salir.pack()

    def agregar_producto(self):
        detalles_producto = self.solicitar_detalles_producto()
        if detalles_producto:
            detalles_producto_df = pd.DataFrame([detalles_producto])
            self.inventario = pd.concat([self.inventario, detalles_producto_df], ignore_index=True)
            self.mostrar_producto(detalles_producto)

    def solicitar_detalles_producto(self):
        nombre = simpledialog.askstring("Nombre", "Ingrese el nombre del producto:", parent=self.master)
        if not nombre:
            return None
        codigo = simpledialog.askstring("Código", "Ingrese el código del producto:", parent=self.master)
        precio = simpledialog.askfloat("Precio", "Ingrese el precio del producto:", parent=self.master)
        cantidad = simpledialog.askinteger("Cantidad", "Ingrese la cantidad del producto:", parent=self.master)
        proveedor = simpledialog.askstring("Proveedor", "Ingrese el proveedor del producto:", parent=self.master)
        foto_path = filedialog.askopenfilename(title="Seleccione una foto para el producto",
                                               filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        return {'Nombre': nombre, 'Código': codigo, 'Precio': precio, 'Cantidad': cantidad, 'Proveedor': proveedor,
                'Foto': foto_path}

    def mostrar_producto(self, detalles_producto):
        indice_producto = len(self.productos_frames)
        fila = indice_producto // 3
        columna = indice_producto % 3

        marco_producto = tk.LabelFrame(self.contenedor_productos, text=detalles_producto['Nombre'], bd=2, relief='groove')
        marco_producto.grid(row=fila, column=columna, padx=10, pady=10, sticky='nsew')

        self.contenedor_productos.grid_rowconfigure(fila, weight=1)

        try:
            imagen = Image.open(detalles_producto['Foto'])
            imagen = imagen.resize((100, 100), Image.LANCZOS)
            foto = ImageTk.PhotoImage(imagen)

            etiqueta_imagen = tk.Label(marco_producto, image=foto)
            etiqueta_imagen.image = foto
            etiqueta_imagen.grid(row=0, column=0, columnspan=3)

        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            messagebox.showerror('Error', f'Error al cargar la imagen: {e}')

        # Crea el botón quitar con el comando para modificar el stock
        boton_quitar = tk.Button(marco_producto, text="-",
                                 command=lambda: self.modificar_stock(detalles_producto['Código'], -1,
                                                                      etiqueta_cantidad))
        boton_quitar.grid(row=1, column=0)

        # Crea la etiqueta de cantidad
        etiqueta_cantidad = tk.Label(marco_producto, text=f"Stock: {detalles_producto['Cantidad']}")
        etiqueta_cantidad.grid(row=1, column=1)

        # Crea el botón agregar con el comando para modificar el stock
        boton_agregar = tk.Button(marco_producto, text="+",
                                  command=lambda: self.modificar_stock(detalles_producto['Código'], 1,
                                                                       etiqueta_cantidad))
        boton_agregar.grid(row=1, column=2)

        self.productos_frames.append(marco_producto)

    def modificar_stock(self, codigo, cambio, etiqueta_cantidad):
        # Encuentra el índice del producto en el inventario
        indice = self.inventario[self.inventario['Código'] == codigo].index[0]
        # Actualiza la cantidad en el DataFrame
        self.inventario.at[indice, 'Cantidad'] += cambio
        # Actualiza la etiqueta de cantidad en la GUI
        etiqueta_cantidad.config(text=f"Stock: {self.inventario.at[indice, 'Cantidad']}")

    def generar_informe(self):
        archivo = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                               filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if archivo:
            try:
                informe_df = self.inventario.drop(columns=['Foto'])
                informe_df.to_excel(archivo, index=False)
                messagebox.showinfo("Información", "El informe se ha generado con éxito.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el informe: {e}")

    def guardar_cambios(self):
        archivo = filedialog.asksaveasfilename(defaultextension='.csv',
                                               filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if archivo:
            try:
                self.inventario.to_csv(archivo, index=False)
                messagebox.showinfo("Información", "Los cambios se han guardado con éxito.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionInventario(root)
    root.mainloop()

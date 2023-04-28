"""
Descripción
Se presenta un programa para realizar un Informe Diario de
producción de una industria de termotanques eléctricos.
El mismo permite el alta, baja, consulta y modificación de los
registros ingresados.
Muestra un gráfico de producción diaria con los modelos y
cantidades producidas.
"""


######################################## Import ######################################
    
import tkinter as tk
from tkinter import ttk, messagebox
import trabajo_final_niv_inicia_metodos as met


########################################### Vistas  ##################################

# Crear Ventana

ventana = tk.Tk()

ventana.title('Produccion de Termotanques')


# Variables

var_fecha = tk.StringVar()
var_modelo = tk.StringVar()
var_cantidad = tk.IntVar()

# Labels



titulo = ttk.Label(ventana, text='Informe de producción',
                   font=('Roboto', 18, 'bold'),
                   background= '#9AB3FF',
                   foreground ='#323133')
titulo.grid(row=0, column=0, columnspan=6, pady=15, sticky='EWNS')

subtitulo = ttk.Label(ventana, text='Alta de producción',
                      font=('Roboto', 14, 'bold'),
                      background= '#9AB3FF',
                      foreground ='#323133')
subtitulo.grid(row=1, column=0, columnspan=6, pady=20 ,sticky='EW')


fecha_label = ttk.Label(ventana, text='Fecha. dd/mm/aaaa',
                  font=('Roboto', 12),
                  foreground ='#323133')
fecha_label.grid(row=3, column=1, pady=7, padx=10)



modelo_label = ttk.Label(ventana, text='Modelo',
                   font=('Roboto', 12),
                   foreground ='#323133')
modelo_label.grid(row=4, column=1, pady=7, padx=10)

cantidad_label = ttk.Label(ventana, text='Cantidad',
                     font=('Roboto', 12),
                     foreground ='#323133')
cantidad_label.grid(row=5, column=1, pady=7, padx=10)

                    # Input

fecha_input = ttk.Entry(ventana, textvariable=var_fecha,
                        width=35,
                        font=('Roboto', 12))
fecha_input.grid(row=3, column=2, columnspan=4, pady=7)



modelo_input = ttk.Combobox(ventana,state="normal",
                            values=('30Lt','50Lt', '80Lt'),
                         textvariable=var_modelo,
                         width=35,
                         font=('Roboto', 12))
modelo_input.grid(row=4, column=2, columnspan=4, pady=7)

cantidad_input = ttk.Entry(ventana, textvariable=var_cantidad,
                           width=35,
                           font=('Roboto', 12))
cantidad_input.grid(row=5, column=2, columnspan=4, pady=7)




 # Botones

def alta_reg_vista(fecha_v, modelo_v, cantidad_v, tree_v):
    retorno = met.alta_registro(fecha_v, modelo_v, cantidad_v, tree_v)
    messagebox.showinfo(retorno)

boton_alta = tk.Button(ventana,text="Alta Registro" , 
command=lambda:alta_reg_vista(var_fecha, var_modelo, var_cantidad, tree),
bg='#093B92', 
fg='white', 
font=('Roboto', 12))
boton_alta.grid(row=6, column=1, pady=7, padx=7)

def guardar_reg_vista(fecha_v, modelo_v, cantidad_v, tree_v):
    


boton_guardar = tk.Button(ventana,text="Guardar Registro", 
                            command=lambda:guardar_registro(var_fecha.get(),var_modelo.get(),var_cantidad.get(),tree),
                            bg='#5391BD',
                            fg='white',
                            font=('Roboto', 12))


boton_exportar = tk.Button(ventana,text="Exportar Registros", 
                           command=exportar_registros, 
                           bg='#093B92', 
                           fg='white', 
                           font=('Roboto', 12))
boton_exportar.grid(row=6, column=3, pady=7, padx=7)

boton_eliminar = tk.Button(ventana,text="Eliminar Registro", 
                           command=lambda:eliminar_registro(tree),
                           bg='#093B92', 
                           fg='white', 
                           font=('Roboto', 12))
boton_eliminar.grid(row=6, column=4, pady=7, padx=7, sticky="E")

boton_limpiar = tk.Button(ventana,text="Limpiar", 
                           command=limpiar, 
                           bg='#093B92', 
                           fg='white', 
                           font=('Roboto', 12))
boton_limpiar.grid(row=3, column=5)

boton_modificar = tk.Button(ventana,text="Modificar registro", 
                           command=lambda:modificar_registro(tree), 
                           bg='#093B92', 
                           fg='white', 
                           font=('Roboto', 12))
boton_modificar.grid(row=6, column=2, pady=7, padx=7)


                       # Treeview

titulo_tree = ttk.Label(ventana, text='Registro produccion',
                      font=('Roboto', 14, 'bold'), 
                      background= '#9AB3FF',
                      foreground ='#323133')
titulo_tree.grid(row=7, column=0, columnspan=6, pady=20, sticky='EW')

tree = ttk.Treeview(ventana)
tree["columns"]=("col1", "col2", "col3")
tree.column("#0", width=90, minwidth=50, anchor="w")
tree.column("col1", width=200, minwidth=80, anchor= 'center')
tree.column("col2", width=200, minwidth=80, anchor= 'center')
tree.column("col3", width=200, minwidth=80, anchor= 'center')
tree.heading("#0", text="ID")
tree.heading("col1", text="fecha")
tree.heading("col2", text="modelo")
tree.heading("col3", text="cantidad")
tree.grid(row=8, column=1, columnspan=5)

scrollbar = ttk.Scrollbar(ventana, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=8, column=6, sticky='ns')

actualizar_tree(tree)

el_grafico(ventana)



ventana.mainloop()



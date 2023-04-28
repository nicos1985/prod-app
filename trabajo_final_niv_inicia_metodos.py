"""
Descripción
Se presenta un programa para realizar un Informe Diario de
producción de una industria de termotanques eléctricos.
El mismo permite el alta, baja, consulta y modificación de los
registros ingresados.
Muestra un gráfico de producción diaria con los modelos y
cantidades producidas.
"""



import re
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure




# Crear BD
connection = sqlite3.connect('produccion_db.db')

# Crear Tabla
cursor = connection.cursor()

# Chequear si tabla existe: si existe, no crea nuevamente. 


def tabla_existe():
    sql_create_table = "CREATE TABLE IF NOT EXISTS produccion(id integer PRIMARY KEY AUTOINCREMENT, fecha date, modelo text, cantidad integer)"
    cursor.execute(sql_create_table)
    connection.commit()
    

tabla_existe()




# Funciones
def valida_fecha(patron_fecha, fecha):
    """ Valida la fecha en los input, segun regex (dd/mm/aaaa)"""
    valida = re.match(patron_fecha, fecha)
    return valida

def formatea_fecha(fecha):
    """Ordena la fecha para ponerla en formato aaaa/mm/dd en la BD"""

    fecha_formateada = f'{fecha[6:10]}/{fecha[3:5]}/{fecha[0:2]}'
    return fecha_formateada

def fecha_ortodoxa(fecha):
    """Ordena la fecha para ponerla en formato dd/mm/aaaa en el treeview y archivo txt export"""

    fecha_procesada = f'{fecha[8:10]}/{fecha[5:7]}/{fecha[0:4]}'
    return fecha_procesada

def alta_registro(fecha, modelo, cantidad, treeview):
    """Realiza el alta de un registro de produccion en la BD"""

    patron_fecha = r'^\d{2}/\d{2}/\d{4}$'
    

    if not fecha.get() or not modelo.get() or not cantidad.get():
        return ('Información erronea', f'Debe completar todos los campos. \n FECHA: {fecha.get()}\n MODELO: {modelo.get()} \n CANTIDAD: {cantidad.get()}')


    else:
        if valida_fecha(patron_fecha, fecha.get()):
            fecha_formateada = formatea_fecha(fecha.get())
            data = (fecha_formateada, modelo.get(), cantidad.get())
            sql = "INSERT INTO produccion (fecha, modelo, cantidad) VALUES (?,?,?)"

            cursor.execute(sql, data)
            connection.commit()
            global label_aviso
            #label_aviso = ttk.Label(text='Registro Ingresado', background= '#3CA345', foreground= 'white')
            #label_aviso.grid(row = 1, column=0, columnspan=6, sticky='E', pady=20)

            actualizar_tree(treeview)
            #el_grafico(ventana)

            print(f'Alta --> Fecha: {fecha}, Modelo: {modelo}, Cantidad: {cantidad}')
        else:
             return ('Información erronea. Campo Fecha', 'El campo fecha debe ser del modelo dd/mm/aaaa.')

def modificar_registro(mod_tree):
    """Trae la info de seleccion, prepara los input para completar la modificacion."""
    if mod_tree.selection():
        
        
        valor = mod_tree.selection()
        item = mod_tree.item(valor)
        mi_id = item['text']

        data = (mi_id,)
        sql_consulta_id = "SELECT id, fecha, modelo, cantidad FROM produccion WHERE id = ?"
        consulta = cursor.execute(sql_consulta_id, data)
        registro = consulta.fetchone()
        #convierto a lista para poder modificar la fecha a ortodoxa
        registro1 = list(registro)
        #aplico funcion
        registro1[1] = fecha_ortodoxa(registro1[1])
        #vuelvo a pasar a Tupla
        registro = tuple(registro1)
        
        connection.commit()
        
        return registro
    
    else:
        return None

def guardar_registro(fecha, modelo, cantidad, mod_tree):
    """Realiza el guardado de un registro de produccion en la BD (modificacion de existente)"""

    patron_fecha = r'^\d{2}/\d{2}/\d{4}$'

    valor = mod_tree.selection()
    item = mod_tree.item(valor)
    mi_id = item['text']
    
    # valida la fecha segun regex (dd/mm/aaaa). Si hace match, entoces realiza el upadte. Else: envia mensaje warning
    if valida_fecha(patron_fecha, fecha):
        
        data = (formatea_fecha(fecha), modelo, cantidad, mi_id)
        sql = "UPDATE produccion SET fecha=?, modelo=?, cantidad=? WHERE id = ?;"
        cursor.execute(sql, data)
        connection.commit()
        global label_aviso_mod
        #esto lo modifico despues
        #label_aviso_mod = ttk.Label(text='Registro Modificado', background= '#5391BD', foreground= 'white')
        #label_aviso_mod.grid(row = 1, column=0, columnspan=6, sticky='E', pady=20)

        actualizar_tree(mod_tree)
        print(f'Modificacion --> Fecha: {fecha}, Modelo: {modelo}, Cantidad: {cantidad}')
        return 'guardado'
        
    else:
        return False
        
    

def consultar_registros():
    """Realiza la consulta de registros de produccion en la BD"""
    sql_consulta = "SELECT * FROM produccion ORDER BY fecha ASC"
    datos = cursor.execute(sql_consulta)
    data= datos.fetchall()
    connection.commit()
    return data


def exportar_registros():
    """ Realiza la exportacion de un archivo de todos los datos de la base en formato txt."""
    with open('registros.txt', 'w', encoding='utf8') as registros:
        registros.write('ID |    FECHA     | MODELO | CANTIDAD |\n' )
        for registro in consultar_registros():
            registros.write(f'{registro[0]} |  {fecha_ortodoxa(registro[1])}  |  {registro[2]}  |    {registro[3]}    |\n' )

def desea_eliminar(del_tree):
    """Elimina un registro elegido desde el treeview"""

    if del_tree.selection():
        return del_tree
    else:
        return 'No Seleccionado'
        
def eliminar_registro(del_tree):
    
    valor = del_tree.selection()
    item = del_tree.item(valor)
    mi_id = item['text']

    data = (mi_id,)
    sql = "DELETE FROM produccion WHERE id = ?;"
    cursor.execute(sql, data)
    connection.commit()
    del_tree.delete(valor)

        
        #Esto lo veo despues
        #global label_aviso_del
        #label_aviso_del = ttk.Label(text='Registro Eliminado', background= '#FF413E', foreground= 'white')
        #label_aviso_del.grid(row = 1, column=0, columnspan=6, sticky='E', pady=20)
   



def actualizar_tree(mitreeview):
    """Actualiza el treeview con la consulta de la BD"""
    registros = mitreeview.get_children()
    for elemento in registros:
        mitreeview.delete(elemento)

    for fila in consultar_registros():
        mitreeview.insert("", 0, text=fila[0], values=(fecha_ortodoxa(fila[1]), fila[2], fila[3]))


# Gráfico
def el_grafico(ventana):

    con = sqlite3.connect('produccion_db.db')
    cursor = con.cursor()
    cursor.execute('SELECT fecha, modelo, cantidad FROM produccion')
    data = cursor.fetchall()
    con.close()
    fecha = [row[0] for row in data]
    cantidad = [row[2] for row in data]
    print(fecha,cantidad) 

    # gráfico con matplotlib

    fig, ax = plt.subplots()
    ax.bar(fecha,cantidad)
    ax.set_xlabel('Fecha')
    ax.set_ylabel('cantidad')
    ax.set_title('Producción Diaria')

    canvas = FigureCanvasTkAgg(fig, ventana)
    print('canvas')
    canvas.draw()
    print('draw')
    canvas.get_tk_widget().grid(row=3, column=8, columnspan=80, rowspan=15, padx=15, pady=15)
    print('grid')
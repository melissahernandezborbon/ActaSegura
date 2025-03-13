from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar  # Importar el calendario
from database import crear_conexion, crear_tabla, agregar_registro as db_agregar_registro, obtener_registros
from datetime import datetime
import re

# Inicialización de la base de datos
def inicializar_db():
    try:
        # Crear la conexión a la base de datos
        conexion = crear_conexion("registros.db")
        print("Conexión a la base de datos establecida.")

        # Crear la tabla de registros si no existe
        crear_tabla(conexion)
        print("Tabla de registros creada o ya existente.")
        return conexion
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return None

# Crear la conexión e inicializar la base de datos al iniciar la app
conexion = inicializar_db()

if conexion is None:
    print("Error al inicializar la base de datos. Saliendo...")
    exit()

# Crear la interfaz gráfica con Tkinter
def registrar_visita():
    """ Agregar un nuevo registro a la base de datos """
    try:
        # Obtener los datos de los campos de entrada
        fecha = entry_fecha.get()
        hora = entry_hora.get()
        nombre = entry_nombre.get()
        clave = entry_clave.get()
        colonia = entry_colonia.get()
        manzana = entry_manzana.get()
        lote = entry_lote.get()
        telefono = entry_telefono.get()
        asunto = entry_asunto.get()

        # Validar que los campos obligatorios no estén vacíos
        if not fecha.strip() or not hora.strip() or not nombre.strip() or not colonia.strip():
            messagebox.showerror("Error", "Debe completar los campos: Fecha, Hora, Nombre y Colonia.")
            return

         # Formatear la fecha antes de agregar el registro
        fecha_formateada = formatear_fecha(fecha)
        if fecha_formateada is None:
            return

        # Formatear la hora antes de agregar el registro
        hora_formateada = formatear_hora(hora)
        if hora_formateada is None:
            return
        
        # Validar que el número de teléfono tenga 10 dígitos
        if not re.match(r"^\d{10}$", telefono):
            messagebox.showerror("Error", "El número de teléfono debe ser válido (10 dígitos).")
            return


        # Agregar el registro 
        db_agregar_registro(conexion, fecha_formateada, hora_formateada, nombre, clave, colonia, manzana, lote, telefono, asunto)
       
        # Limpiar los campos después de agregar
        entry_nombre.delete(0, END)
        entry_clave.delete(0, END)
        entry_colonia.delete(0, END)
        entry_manzana.delete(0, END)
        entry_lote.delete(0, END)
        entry_telefono.delete(0, END)
        entry_asunto.delete(0, END)

        # Actualizar la fecha y hora a las actuales
        entry_fecha.delete(0, END)
        entry_fecha.insert(0, datetime.today().strftime("%d/%m/%Y"))
        entry_hora.delete(0, END)
        entry_hora.insert(0, datetime.now().strftime("%H:%M"))

        # Actualizar la tabla
        actualizar_tabla()

    except Exception as e:
        print(f"Error al agregar el registro: {e}")

# Función para cargar los registros en la tabla
def actualizar_tabla():
    # Eliminar filas anteriores
    for row in tabla.get_children():
        tabla.delete(row)

    # Obtener registros y agregarlos a la tabla
    registros = obtener_registros(conexion)
    for registro in registros:
        tabla.insert("", END, values=registro)

def actualizar_hora():
    entry_hora.delete(0, END)
    entry_hora.insert(0, datetime.now().strftime("%H:%M"))
    root.after(600000, actualizar_hora)  # 300000 ms = 10 minutos

def formatear_fecha(fecha_str):
    """ Formatear la fecha ingresada a dd/mm/yyyy"""
    # Reemplazar los separadores con '/'
    fecha_str = re.sub(r"[-. ]", "/", fecha_str)

    # Verificar si el formato es correcto (dd/mm/yyyy)
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
        return fecha.strftime("%d/%m/%Y") # Formato correcto
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha incorrecto. Use el formato dd/mm/yyyy.")
        return None

def formatear_hora(hora_str):
    """ Formatear la hora ingresada a hh:mm """
    # Reemplazar cualquier separador distinto de ":" por ":"
    hora_str = re.sub(r"[^0-9:]", ":", hora_str)  # Reemplazar todo lo que no sea número o ":" por ":"

    # Verificar si el formato es correcto (hh:mm)
    try:
        hora = datetime.strptime(hora_str, "%H:%M")  # Intentamos convertirlo a un objeto datetime
        return hora.strftime("%H:%M")  # Devolvemos en el formato correcto
    except ValueError:
        messagebox.showerror("Error", "Formato de hora incorrecto. Use el formato hh:mm.")
        return None

# Función para abrir el calendario en una nueva ventana
def abrir_calendario():
    # Crear una nueva ventana
    ventana_calendario = Toplevel(root)
    ventana_calendario.iconbitmap("assets\logo_indivi.ico")  # Icono de la ventana
    ventana_calendario.title("Calendario")
    ventana_calendario.geometry("300x300+700+100")  # Tamaño y posición de la ventana

    # Crear el calendario dentro de esta ventana
    calendario = Calendar(ventana_calendario, selectmode='day', date_pattern='dd/mm/yyyy')
    calendario.pack(pady=20)

    # Función para seleccionar la fecha del calendario
    def seleccionar_fecha():
        fecha_seleccionada = calendario.get_date()  # Obtener la fecha seleccionada
        entry_fecha.delete(0, END)  # Limpiar el campo de fecha
        entry_fecha.insert(0, fecha_seleccionada)  # Insertar la fecha seleccionada
        ventana_calendario.destroy()  # Cerrar la ventana del calendario

    # Botón para seleccionar la fecha
    boton_seleccionar = Button(ventana_calendario, text="Seleccionar Fecha", command=seleccionar_fecha)
    boton_seleccionar.pack()

def cambiar_foco(event):
    event.widget.tk_focusNext().focus()
    return "break"  # Evita que el Enter inserte un salto de línea en el campo de texto


# Configuración de la ventana principal
root = Tk()
root.title("Registro de Visitas")
root.geometry("1100x700+200+50")  # Ajustar tamaño inicial y centrarlo
root.minsize(700, 500)  # Tamaño mínimo

root.iconbitmap("assets\logo_indivi.ico")  # Icono de la ventana

# Permitir que las columnas y filas de la ventana se expandan
root.columnconfigure(0, weight=1)
root.rowconfigure(3, weight=1)

# Crear un frame para los campos de entrada y centrarlo
frame_formulario = Frame(root)
frame_formulario.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="")

# Crear etiquetas y campos de entrada centrados
Label(frame_formulario, text="Fecha:").grid(row=0, column=0, sticky=E, padx=5, pady=2)
entry_fecha = Entry(frame_formulario, width=30)
entry_fecha.grid(row=0, column=1, padx=5, pady=2)
entry_fecha.insert(0, datetime.today().strftime("%d/%m/%Y"))

# Botón para abrir el calendario
boton_fecha = Button(frame_formulario, text="Buscar Fecha", command=abrir_calendario)
boton_fecha.grid(row=0, column=2, padx=10, pady=5)

# Asignar la tecla Enter para cambiar de campo
entry_fecha.bind("<Return>", cambiar_foco)

# Resto de campos de entrada
Label(frame_formulario, text="Hora:").grid(row=1, column=0, sticky=E, padx=5, pady=2)
entry_hora = Entry(frame_formulario, width=30)
entry_hora.grid(row=1, column=1, padx=5, pady=2)
entry_hora.insert(0, datetime.now().strftime("%H:%M"))
# Asignar la tecla Enter para cambiar de campo
entry_hora.bind("<Return>", cambiar_foco)

Label(frame_formulario, text="Nombre:").grid(row=2, column=0, sticky=E, padx=5, pady=2)
entry_nombre = Entry(frame_formulario, width=30)
entry_nombre.grid(row=2, column=1, padx=5, pady=2)
# Asignar la tecla Enter para cambiar de campo
entry_nombre.bind("<Return>", cambiar_foco)

Label(frame_formulario, text="Clave:").grid(row=3, column=0, sticky=E, padx=5, pady=2)
entry_clave = Entry(frame_formulario, width=30)
entry_clave.grid(row=3, column=1, padx=5, pady=2)
# Asignar la tecla Enter para cambiar de campo
entry_clave.bind("<Return>", cambiar_foco)

Label(frame_formulario, text="Colonia:").grid(row=4, column=0, sticky=E, padx=5, pady=2)
entry_colonia = Entry(frame_formulario, width=30)
entry_colonia.grid(row=4, column=1, padx=5, pady=2)
# Asignar la tecla Enter para cambiar de campo
entry_colonia.bind("<Return>", cambiar_foco)

Label(frame_formulario, text="Manzana:").grid(row=5, column=0, sticky=E, padx=5, pady=2)
entry_manzana = Entry(frame_formulario, width=30)
entry_manzana.grid(row=5, column=1, padx=5, pady=2)
# Asignar la tecla Enter para cambiar de campo
entry_manzana.bind("<Return>", cambiar_foco)

Label(frame_formulario, text="Lote:").grid(row=6, column=0, sticky=E, padx=5, pady=2)
entry_lote = Entry(frame_formulario, width=30)
entry_lote.grid(row=6, column=1, padx=5, pady=2)
# Asignar la tecla Enter para cambiar de campo
entry_lote.bind("<Return>", cambiar_foco)

Label(frame_formulario, text="Teléfono:").grid(row=7, column=0, sticky=E, padx=5, pady=2)
entry_telefono = Entry(frame_formulario, width=30)
entry_telefono.grid(row=7, column=1, padx=5, pady=2)
# Asignar la tecla Enter para cambiar de campo
entry_telefono.bind("<Return>", cambiar_foco)

Label(frame_formulario, text="Asunto:").grid(row=8, column=0, sticky=E, padx=5, pady=2)
entry_asunto = Entry(frame_formulario, width=30)
entry_asunto.grid(row=8, column=1, padx=5, pady=2)
# Asignar la tecla Enter para cambiar de campo
entry_asunto.bind("<Return>", cambiar_foco)

# Botón para agregar registro
boton_agregar = Button(root, text="Agregar registro", command=registrar_visita)
boton_agregar.grid(row=1, column=0, columnspan=2, pady=10)

# Crear tabla para mostrar registros
columnas = ("ID", "Fecha", "Hora", "Nombre", "Clave", "Colonia", "Manzana", "Lote", "Teléfono", "Asunto")
tabla = ttk.Treeview(root, columns=columnas, show="headings", height=15)

# Definir encabezados y ajustar tamaño de columnas
for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=100, anchor="center")

# Agregar scrollbar horizontal y vertical
scroll_y = Scrollbar(root, orient="vertical", command=tabla.yview)
scroll_x = Scrollbar(root, orient="horizontal", command=tabla.xview)
tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

tabla.grid(row=2, column=0, columnspan=2, pady=20, sticky="nsew")
scroll_y.grid(row=2, column=2, sticky="ns")
scroll_x.grid(row=3, column=0, columnspan=2, sticky="ew")

# Inicializar la tabla con los registros
actualizar_tabla()

# Actualizar la hora cada 10 minutos
actualizar_hora()

# Ejecutar la aplicación
root.mainloop()

import sqlite3
from sqlite3 import Error

# Función para crear la conexión a la base de datos
def crear_conexion(db_file):
    """Crear una conexión a la base de datos SQLite"""
    try:
        conexion = sqlite3.connect(db_file)
        print("Conexión exitosa a la base de datos")
        return conexion
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

# Función para crear la tabla de registros
def crear_tabla(conexion):
    """Crear la tabla 'registros' en la base de datos"""
    try:
        sql = '''
        CREATE TABLE IF NOT EXISTS registros (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            hora TEXT,
            nombre TEXT,
            clave TEXT,
            colonia TEXT,
            manzana TEXT,
            lote TEXT,
            telefono TEXT,
            asunto TEXT
        );
        '''
        with conexion:
            conexion.execute(sql)
        print("Tabla creada o ya existe")
    except Error as e:
        print(f"Error al crear la tabla: {e}")

# Función para agregar un nuevo registro
def agregar_registro(conexion, fecha, hora, nombre, clave, colonia, manzana, lote, telefono, asunto):
    try:
        # SQL para insertar el registro sin el campo ID (que es autoincremental)
        query = """INSERT INTO registros (fecha, hora, nombre, clave, colonia, manzana, lote, telefono, asunto)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor = conexion.cursor()
        cursor.execute(query, (fecha, hora, nombre, clave, colonia, manzana, lote, telefono, asunto))
        conexion.commit()
        print("Registro agregado exitosamente.")
        cursor.close()  # Cerrar el cursor después de usarlo
    except Exception as e:
        print(f"Error al agregar el registro: {e}")

# Función para obtener todos los registros
def obtener_registros(conexion):
    """Obtener todos los registros de la tabla 'registros'"""
    try:
        with conexion:
            cursor = conexion.execute('SELECT * FROM registros')
            registros = cursor.fetchall()
        cursor.close()  # Cerrar el cursor después de usarlo
        return registros
    except Error as e:
        print(f"Error al obtener los registros: {e}")
        return []


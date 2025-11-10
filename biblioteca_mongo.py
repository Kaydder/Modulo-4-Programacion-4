from pymongo import MongoClient, errors
from bson.objectid import ObjectId

# ============================================================
# Aplicación de Biblioteca Personal con MongoDB y pymongo
# Autor: [Tu nombre]
# Descripción: Programa de línea de comandos que administra
# libros almacenados como documentos en MongoDB.
# ============================================================

# ------------------------------------------------------------
# Conexión con MongoDB
# ------------------------------------------------------------
def obtener_coleccion():
    """
    Crea la conexión con MongoDB y devuelve la colección 'libros'.
    Maneja errores de conexión.
    """
    try:
        # Ajusta esta URI según tu entorno:
        # - Para local: "mongodb://localhost:27017/"
        # - Para Atlas: "mongodb+srv://usuario:password@cluster-url/"
        uri = "mongodb://localhost:27017/"

        cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # Probar conexión
        cliente.server_info()

        bd = cliente["biblioteca_db"]
        coleccion = bd["libros"]
        return coleccion
    except errors.ServerSelectionTimeoutError:
        print("Error: No se pudo conectar al servidor de MongoDB. Verifica que esté en ejecución o revisa la URI.")
        exit(1)
    except Exception as e:
        print(f"Error inesperado al conectar con MongoDB: {e}")
        exit(1)

# ------------------------------------------------------------
# Funciones de validación
# ------------------------------------------------------------
def validar_estado(estado):
    estado_normalizado = estado.strip().lower()
    if estado_normalizado == "leído" or estado_normalizado == "leido":
        return "Leído"
    elif estado_normalizado == "no leído" or estado_normalizado == "no leido":
        return "No leído"
    else:
        print("Estado inválido. Se debe ingresar 'Leído' o 'No leído'.")
        return None

# ------------------------------------------------------------
# Funciones CRUD
# ------------------------------------------------------------
def agregar_libro(coleccion):
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    genero = input("Género: ").strip()
    estado_input = input("Estado (Leído/No leído): ")

    estado = validar_estado(estado_input)
    if estado is None:
        print("No se agregó el libro debido a un estado inválido.\n")
        return

    documento = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }

    try:
        resultado = coleccion.insert_one(documento)
        print(f"Libro agregado correctamente con ID: {resultado.inserted_id}\n")
    except errors.PyMongoError as e:
        print(f"Error al agregar libro: {e}\n")

def ver_libros(coleccion):
    try:
        libros = list(coleccion.find())
    except errors.PyMongoError as e:
        print(f"Error al consultar libros: {e}\n")
        return

    if libros:
        print("\nLISTADO DE LIBROS:")
        print("-" * 80)
        for libro in libros:
            print(f"ID: {libro.get('_id')} | "
                  f"Título: {libro.get('titulo')} | "
                  f"Autor: {libro.get('autor')} | "
                  f"Género: {libro.get('genero')} | "
                  f"Estado: {libro.get('estado')}")
        print("-" * 80 + "\n")
    else:
        print("\nNo hay libros registrados.\n")

def actualizar_libro(coleccion):
    ver_libros(coleccion)
    id_str = input("Ingrese el ID del libro que desea actualizar: ").strip()

    try:
        _id = ObjectId(id_str)
    except Exception:
        print("ID no válido. Debe ser un ObjectId de MongoDB.\n")
        return

    try:
        libro = coleccion.find_one({"_id": _id})
    except errors.PyMongoError as e:
        print(f"Error al buscar el libro: {e}\n")
        return

    if not libro:
        print("No se encontró un libro con ese ID.\n")
        return

    print("Deje el campo vacío si no desea cambiarlo.")
    nuevo_titulo = input(f"Nuevo título [{libro.get('titulo')}]: ").strip()
    nuevo_autor = input(f"Nuevo autor [{libro.get('autor')}]: ").strip()
    nuevo_genero = input(f"Nuevo género [{libro.get('genero')}]: ").strip()
    nuevo_estado_input = input(f"Nuevo estado (Leído/No leído) [{libro.get('estado')}]: ").strip()

    campos_actualizados = {}

    if nuevo_titulo:
        campos_actualizados["titulo"] = nuevo_titulo
    if nuevo_autor:
        campos_actualizados["autor"] = nuevo_autor
    if nuevo_genero:
        campos_actualizados["genero"] = nuevo_genero
    if nuevo_estado_input:
        estado_validado = validar_estado(nuevo_estado_input)
        if estado_validado is None:
            print("No se actualizó el libro debido a un estado inválido.\n")
            return
        campos_actualizados["estado"] = estado_validado

    if not campos_actualizados:
        print("No se realizaron cambios.\n")
        return

    try:
        resultado = coleccion.update_one({"_id": _id}, {"$set": campos_actualizados})
        if resultado.modified_count > 0:
            print("Libro actualizado exitosamente.\n")
        else:
            print("No se realizaron cambios en el documento.\n")
    except errors.PyMongoError as e:
        print(f"Error al actualizar libro: {e}\n")

def eliminar_libro(coleccion):
    ver_libros(coleccion)
    id_str = input("Ingrese el ID del libro que desea eliminar: ").strip()

    try:
        _id = ObjectId(id_str)
    except Exception:
        print("ID no válido. Debe ser un ObjectId de MongoDB.\n")
        return

    try:
        resultado = coleccion.delete_one({"_id": _id})
        if resultado.deleted_count > 0:
            print("Libro eliminado correctamente.\n")
        else:
            print("No se encontró un libro con ese ID.\n")
    except errors.PyMongoError as e:
        print(f"Error al eliminar libro: {e}\n")

def buscar_libros(coleccion):
    campo = input("Buscar por (titulo/autor/genero): ").strip().lower()
    if campo not in ["titulo", "autor", "genero"]:
        print("Campo no válido. Debe ser: titulo, autor o genero.\n")
        return

    termino = input(f"Ingrese el {campo} que desea buscar: ").strip()

    filtro = {campo: {"$regex": termino, "$options": "i"}}

    try:
        resultados = list(coleccion.find(filtro))
    except errors.PyMongoError as e:
        print(f"Error en la búsqueda: {e}\n")
        return

    if resultados:
        print("\nRESULTADOS DE BÚSQUEDA:")
        print("-" * 80)
        for libro in resultados:
            print(f"ID: {libro.get('_id')} | "
                  f"Título: {libro.get('titulo')} | "
                  f"Autor: {libro.get('autor')} | "
                  f"Género: {libro.get('genero')} | "
                  f"Estado: {libro.get('estado')}")
        print("-" * 80 + "\n")
    else:
        print("No se encontraron libros que coincidan con el criterio de búsqueda.\n")

# ------------------------------------------------------------
# Menú principal
# ------------------------------------------------------------
def menu():
    coleccion = obtener_coleccion()

    while True:
        print("========= MENÚ BIBLIOTECA PERSONAL (MongoDB) =========")
        print("1. Agregar nuevo libro")
        print("2. Actualizar información de un libro")
        print("3. Eliminar libro")
        print("4. Ver listado de libros")
        print("5. Buscar libros")
        print("6. Salir")
        print("======================================================")

        opcion = input("Seleccione una opción (1-6): ").strip()
        print()

        if opcion == "1":
            agregar_libro(coleccion)
        elif opcion == "2":
            actualizar_libro(coleccion)
        elif opcion == "3":
            eliminar_libro(coleccion)
        elif opcion == "4":
            ver_libros(coleccion)
        elif opcion == "5":
            buscar_libros(coleccion)
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente de nuevo.\n")

# ------------------------------------------------------------
# Punto de entrada
# ------------------------------------------------------------
if __name__ == "__main__":
    menu()

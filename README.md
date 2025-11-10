# Biblioteca Personal con MongoDB y pymongo

## Objetivo
Modificar la aplicación de línea de comandos de biblioteca personal para utilizar una base de datos no relacional, almacenando los libros como documentos en MongoDB y utilizando el cliente oficial `pymongo`.

Cada libro se almacena como un documento JSON dentro de una colección.

---

## Funcionalidades

La aplicación ofrece las siguientes operaciones:

- Agregar nuevo libro
- Actualizar información de un libro
- Eliminar libro existente
- Ver listado de libros
- Buscar libros por título, autor o género
- Salir del programa

---

## Requisitos

- Python 3.8 o superior
- MongoDB instalado (local) o cuenta en MongoDB Atlas
- Dependencias listadas en `requirements.txt`

Instalación de dependencias:

```bash
pip install -r requirements.txt

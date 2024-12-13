import redis
import json

# Conectar a la base de datos KeyDB
keydb = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Función para agregar una receta
def agregar_receta():
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ")
    pasos = input("Pasos: ")

    # Crear un diccionario con los datos de la receta
    receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos
    }

    # Guardar la receta en KeyDB (clave: nombre de la receta)
    keydb.set(nombre, json.dumps(receta))
    print("Receta agregada con éxito.")

# Función para actualizar una receta existente
def actualizar_receta():
    ver_recetas()
    nombre = input("Nombre de la receta a actualizar: ")

    # Verificar si la receta existe
    if keydb.exists(nombre):
        receta = json.loads(keydb.get(nombre))
        print(f"Nombre actual: {receta['nombre']}")
        print(f"Ingredientes actuales: {receta['ingredientes']}")
        print(f"Pasos actuales: {receta['pasos']}")

        nuevo_nombre = input("Nuevo nombre de la receta (deja en blanco para no cambiar): ")
        nuevos_ingredientes = input("Nuevos ingredientes (deja en blanco para no cambiar): ")
        nuevos_pasos = input("Nuevos pasos (deja en blanco para no cambiar): ")

        if nuevo_nombre:
            receta["nombre"] = nuevo_nombre
        if nuevos_ingredientes:
            receta["ingredientes"] = nuevos_ingredientes
        if nuevos_pasos:
            receta["pasos"] = nuevos_pasos

        # Actualizar la receta en KeyDB
        keydb.delete(nombre)
        keydb.set(receta["nombre"], json.dumps(receta))
        print("Receta actualizada con éxito.")
    else:
        print("Receta no encontrada.")

# Función para eliminar una receta existente
def eliminar_receta():
    ver_recetas()
    nombre = input("Nombre de la receta a eliminar: ")

    # Eliminar la receta de KeyDB
    if keydb.exists(nombre):
        keydb.delete(nombre)
        print("Receta eliminada con éxito.")
    else:
        print("Receta no encontrada.")

# Función para ver el listado de recetas
def ver_recetas():
    claves = keydb.keys()
    print("\nListado de recetas:")
    for clave in claves:
        receta = json.loads(keydb.get(clave))
        print(f"Nombre: {receta['nombre']}")
    print()

# Función para buscar ingredientes y pasos de una receta
def buscar_receta():
    nombre = input("Nombre de la receta a buscar: ")

    # Buscar la receta por nombre en KeyDB
    if keydb.exists(nombre):
        receta = json.loads(keydb.get(nombre))
        print("\nIngredientes:", receta["ingredientes"])
        print("Pasos:", receta["pasos"])
    else:
        print("Receta no encontrada.")

# Menú principal
def menu():
    while True:
        print("\n--- Libro de Recetas ---")
        print("1. Agregar nueva receta")
        print("2. Actualizar receta existente")
        print("3. Eliminar receta existente")
        print("4. Ver listado de recetas")
        print("5. Buscar ingredientes y pasos de receta")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            agregar_receta()
        elif opcion == '2':
            actualizar_receta()
        elif opcion == '3':
            eliminar_receta()
        elif opcion == '4':
            ver_recetas()
        elif opcion == '5':
            buscar_receta()
        elif opcion == '6':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# Ejecución del programa
if __name__ == "__main__":
    menu()
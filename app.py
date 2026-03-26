from servicios import (
    agregar_producto,
    mostrar_inventario,
    buscar_producto,
    actualizar_producto,
    eliminar_producto,
    mostrar_estadisticas,
)
from archivos import guardar_csv, cargar_csv, fusionar_inventarios

def pedir_float(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("Error: El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("Error: Ingrese un número válido.")

def pedir_int(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("Error: El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("Error: Ingrese un número entero válido.")

def pedir_nombre(mensaje):
    while True:
        nombre = input(mensaje).strip()
        if nombre:
            return nombre
        print("Error: El nombre no puede estar vacío.")

def menu_agregar(inventario):
    print("\n--- AGREGAR PRODUCTO ---")
    nombre = pedir_nombre("Nombre del producto: ")
    precio = pedir_float("Precio unitario: ")
    cantidad = pedir_int("Cantidad en stock: ")
    mensaje = agregar_producto(inventario, nombre, precio, cantidad)
    print(mensaje)

def menu_mostrar(inventario):
    print("\n--- INVENTARIO ACTUAL ---")
    mostrar_inventario(inventario)

def menu_buscar(inventario):
    print("\n--- BUSCAR PRODUCTO ---")
    nombre = pedir_nombre("Nombre a buscar: ")
    resultado = buscar_producto(inventario, nombre)
    if resultado:
        print("\nProducto encontrado:")
        print(f"Nombre: {resultado['nombre']}")
        print(f"Precio: {resultado['precio']:.2f}")
        print(f"Cantidad: {resultado['cantidad']}")
        subtotal = resultado["precio"] * resultado["cantidad"]
        print(f"Subtotal: {subtotal:.2f}\n")
    else:
        print(f"El producto '{nombre}' no existe en el sistema.")

def menu_actualizar(inventario):
    print("\n--- ACTUALIZAR PRODUCTO ---")
    nombre = pedir_nombre("Nombre del producto a actualizar: ")

    if not buscar_producto(inventario, nombre):
        print(f"Error: El producto '{nombre}' no fue encontrado.")
        return

    print("(Deje vacío para mantener el valor actual)")
    nuevo_precio = None
    nueva_cantidad = None

    entrada_precio = input("Nuevo precio: ").strip()
    if entrada_precio:
        try:
            nuevo_precio = float(entrada_precio)
            if nuevo_precio < 0:
                print("Precio negativo ignorado.")
                nuevo_precio = None
        except ValueError:
            print("Precio inválido ignorado.")

    entrada_cantidad = input("Nueva cantidad: ").strip()
    if entrada_cantidad:
        try:
            nueva_cantidad = int(entrada_cantidad)
            if nueva_cantidad < 0:
                print("Cantidad negativa ignorada.")
                nueva_cantidad = None
        except ValueError:
            print("Cantidad inválida ignorada.")

    mensaje = actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)
    print(mensaje)

def menu_eliminar(inventario):
    print("\n--- ELIMINAR PRODUCTO ---")
    nombre = pedir_nombre("Nombre del producto a eliminar: ")

    confirmacion = input(f"¿Confirma que desea eliminar '{nombre}'? (s/n): ").strip().lower()
    if confirmacion == "s":
        mensaje = eliminar_producto(inventario, nombre)
        print(mensaje)
    else:
        print("Operación cancelada.")

def menu_estadisticas(inventario):
    mostrar_estadisticas(inventario)

def menu_guardar_csv(inventario):
    print("\n--- GUARDAR EN ARCHIVO ---")
    ruta = input("Nombre del archivo (ej: inventario.csv): ").strip()
    if not ruta:
        ruta = "inventario.csv"
    if not ruta.endswith(".csv"):
        ruta += ".csv"
    guardar_csv(inventario, ruta)

def menu_cargar_csv(inventario):
    print("\n--- CARGAR DESDE ARCHIVO ---")
    ruta = input("Ruta del archivo CSV: ").strip()
    if not ruta:
        print("Ruta no válida.")
        return

    productos_cargados, errores = cargar_csv(ruta)

    if productos_cargados is None:
        return

    if not productos_cargados and errores == 0:
        print("El archivo está vacío.")
        return

    print(f"\nLectura finalizada: {len(productos_cargados)} válidos, {errores} errores.")
    
    print("\nOpciones de carga:")
    print("1. Reemplazar inventario actual")
    print("2. Fusionar con inventario actual")
    
    decision = input("Seleccione una opción: ").strip()

    if decision == "1":
        inventario.clear()
        inventario.extend(productos_cargados)
        print(f"Inventario reemplazado con {len(productos_cargados)} productos.")
    else:
        agregados, actualizados = fusionar_inventarios(inventario, productos_cargados)
        print(f"Fusión completada: {agregados} agregados, {actualizados} actualizados.")

MENU = """
------------------------------------------
          SISTEMA DE INVENTARIO
------------------------------------------
1. Agregar producto
2. Mostrar inventario
3. Buscar producto
4. Actualizar producto
5. Eliminar producto
6. Estadísticas
7. Guardar CSV
8. Cargar CSV
9. Salir
------------------------------------------
"""

OPCIONES = {
    "1": menu_agregar,
    "2": menu_mostrar,
    "3": menu_buscar,
    "4": menu_actualizar,
    "5": menu_eliminar,
    "6": menu_estadisticas,
    "7": menu_guardar_csv,
    "8": menu_cargar_csv,
}

def main():
    inventario = []
    while True:
        print(MENU)
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "9":
            print("Saliendo del sistema...")
            break
        
        accion = OPCIONES.get(opcion)
        if accion:
            accion(inventario)
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    main()

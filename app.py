

from servicios import (
    agregar_producto,
    mostrar_inventario,
    buscar_producto,
    actualizar_producto,
    eliminar_producto,
    mostrar_estadisticas,
)
from archivos import guardar_csv, cargar_csv, fusionar_inventarios


# ──────────────────────────────────────────────
#  Helpers de entrada con validación
# ──────────────────────────────────────────────

def pedir_float(mensaje):
    """Solicita un número flotante no negativo al usuario."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("  ⚠️  El valor no puede ser negativo. Intenta de nuevo.")
                continue
            return valor
        except ValueError:
            print("  ⚠️  Debes ingresar un número válido. Intenta de nuevo.")


def pedir_int(mensaje):
    """Solicita un número entero no negativo al usuario."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("  ⚠️  El valor no puede ser negativo. Intenta de nuevo.")
                continue
            return valor
        except ValueError:
            print("  ⚠️  Debes ingresar un número entero válido. Intenta de nuevo.")


def pedir_nombre(mensaje):
    """Solicita un nombre no vacío al usuario."""
    while True:
        nombre = input(mensaje).strip()
        if nombre:
            return nombre
        print("  ⚠️  El nombre no puede estar vacío. Intenta de nuevo.")


# ──────────────────────────────────────────────
#  Opciones del menú
# ──────────────────────────────────────────────

def menu_agregar(inventario):
    """Flujo para agregar un producto al inventario."""
    print("\n─── AGREGAR PRODUCTO ───")
    nombre = pedir_nombre("  Nombre del producto : ")
    precio = pedir_float("  Precio unitario     : $")
    cantidad = pedir_int("  Cantidad en stock   : ")
    mensaje = agregar_producto(inventario, nombre, precio, cantidad)
    print(f"  {mensaje}")


def menu_mostrar(inventario):
    """Muestra todos los productos del inventario."""
    print("\n─── INVENTARIO ACTUAL ───")
    mostrar_inventario(inventario)


def menu_buscar(inventario):
    """Busca y muestra un producto por nombre."""
    print("\n─── BUSCAR PRODUCTO ───")
    nombre = pedir_nombre("  Nombre a buscar: ")
    resultado = buscar_producto(inventario, nombre)
    if resultado:
        print(f"\n  ✅ Producto encontrado:")
        print(f"     Nombre   : {resultado['nombre']}")
        print(f"     Precio   : ${resultado['precio']:.2f}")
        print(f"     Cantidad : {resultado['cantidad']}")
        subtotal = resultado["precio"] * resultado["cantidad"]
        print(f"     Subtotal : ${subtotal:.2f}\n")
    else:
        print(f"  ❌ Producto '{nombre}' no encontrado en el inventario.")


def menu_actualizar(inventario):
    """Flujo para actualizar precio y/o cantidad de un producto."""
    print("\n─── ACTUALIZAR PRODUCTO ───")
    nombre = pedir_nombre("  Nombre del producto a actualizar: ")

    # Verificar que el producto existe antes de pedir datos
    if not buscar_producto(inventario, nombre):
        print(f"  ❌ Producto '{nombre}' no encontrado.")
        return

    print("  (Presiona Enter para mantener el valor actual)")
    nuevo_precio = None
    nueva_cantidad = None

    entrada_precio = input("  Nuevo precio   : $").strip()
    if entrada_precio:
        try:
            nuevo_precio = float(entrada_precio)
            if nuevo_precio < 0:
                print("  ⚠️  Precio negativo ignorado.")
                nuevo_precio = None
        except ValueError:
            print("  ⚠️  Precio inválido ignorado.")

    entrada_cantidad = input("  Nueva cantidad : ").strip()
    if entrada_cantidad:
        try:
            nueva_cantidad = int(entrada_cantidad)
            if nueva_cantidad < 0:
                print("  ⚠️  Cantidad negativa ignorada.")
                nueva_cantidad = None
        except ValueError:
            print("  ⚠️  Cantidad inválida ignorada.")

    mensaje = actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)
    print(f"  {mensaje}")


def menu_eliminar(inventario):
    """Flujo para eliminar un producto del inventario."""
    print("\n─── ELIMINAR PRODUCTO ───")
    nombre = pedir_nombre("  Nombre del producto a eliminar: ")

    # Confirmar antes de eliminar
    confirmacion = input(f"  ¿Confirmas eliminar '{nombre}'? (S/N): ").strip().upper()
    if confirmacion == "S":
        mensaje = eliminar_producto(inventario, nombre)
        print(f"  {mensaje}")
    else:
        print("  ↩️  Operación cancelada.")


def menu_estadisticas(inventario):
    """Muestra las estadísticas del inventario."""
    mostrar_estadisticas(inventario)


def menu_guardar_csv(inventario):
    """Flujo para guardar el inventario en un archivo CSV."""
    print("\n─── GUARDAR CSV ───")
    ruta = input("  Ruta del archivo (ej: inventario.csv): ").strip()
    if not ruta:
        ruta = "inventario.csv"
    if not ruta.endswith(".csv"):
        ruta += ".csv"
    guardar_csv(inventario, ruta)


def menu_cargar_csv(inventario):
    """Flujo para cargar un CSV y actualizar el inventario."""
    print("\n─── CARGAR CSV ───")
    ruta = input("  Ruta del archivo CSV a cargar: ").strip()
    if not ruta:
        print("  ⚠️  Ruta vacía. Operación cancelada.")
        return

    # Intentar cargar el archivo
    productos_cargados, errores = cargar_csv(ruta)

    # Si la carga falló completamente
    if productos_cargados is None:
        return

    if not productos_cargados and errores == 0:
        print("  ⚠️  El archivo está vacío. No se realizaron cambios.")
        return

    print(f"\n  📄 Archivo leído: {len(productos_cargados)} producto(s) válidos, {errores} fila(s) inválida(s) omitidas.")

    # Mostrar política de fusión
    print("\n  Política de fusión:")
    print("    • Si el producto ya existe → se suma la cantidad y se actualiza el precio.")
    print("    • Si el producto es nuevo  → se agrega al inventario.")

    # Preguntar sobrescribir o fusionar
    print("\n  ¿Qué deseas hacer con el inventario actual?")
    decision = input("  ¿Sobrescribir inventario actual? (S/N): ").strip().upper()

    if decision == "S":
        # Reemplazar todo el inventario
        inventario.clear()
        inventario.extend(productos_cargados)
        accion = "Reemplazo completo"
        print(f"\n  ✅ Inventario reemplazado con {len(productos_cargados)} producto(s).")
    else:
        # Fusionar con el inventario actual
        agregados, actualizados = fusionar_inventarios(inventario, productos_cargados)
        accion = "Fusión"
        print(f"\n  ✅ Fusión completada: {agregados} nuevo(s) agregado(s), {actualizados} actualizado(s).")

    # Resumen final
    print("\n  ─── Resumen de carga ───")
    print(f"    Archivo       : {ruta}")
    print(f"    Válidos       : {len(productos_cargados)}")
    print(f"    Inválidos     : {errores}")
    print(f"    Acción        : {accion}")
    print(f"    Total actual  : {len(inventario)} producto(s) en inventario")


# ──────────────────────────────────────────────
#  Menú principal
# ──────────────────────────────────────────────

MENU = """
╔══════════════════════════════════════════╗
║       SISTEMA DE INVENTARIO v1.0         ║
╠══════════════════════════════════════════╣
║  1. Agregar producto                     ║
║  2. Mostrar inventario                   ║
║  3. Buscar producto                      ║
║  4. Actualizar producto                  ║
║  5. Eliminar producto                    ║
║  6. Estadísticas                         ║
║  7. Guardar CSV                          ║
║  8. Cargar CSV                           ║
║  9. Salir                                ║
╚══════════════════════════════════════════╝
"""

# Mapeo de opciones a funciones del menú
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
    """Función principal. Ejecuta el bucle del menú hasta que el usuario elija Salir."""
    inventario = []  # Inventario en memoria: lista de diccionarios
    print("\n  Bienvenido al Sistema de Inventario 📦")

    while True:
        print(MENU)
        opcion = input("  Selecciona una opción (1-9): ").strip()

        if opcion == "9":
            print("\n  👋 ¡Hasta luego! Cerrando el sistema...\n")
            break
        elif opcion in OPCIONES:
            try:
                # Llamar a la función correspondiente pasando el inventario
                OPCIONES[opcion](inventario)
            except Exception as e:
                # Captura genérica para que ningún error cierre la aplicación
                print(f"\n  ⚠️  Error inesperado: {e}. Por favor, intenta de nuevo.")
        else:
            print(f"\n  ⚠️  Opción '{opcion}' inválida. Ingresa un número del 1 al 9.")


if __name__ == "__main__":
    main()

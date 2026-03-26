

def agregar_producto(inventario, nombre, precio, cantidad):
    
    nombre = nombre.strip()
    # Verificar si el producto ya existe
    existente = buscar_producto(inventario, nombre)
    if existente:
        # Si ya existe, actualizar precio y sumar cantidad
        existente["precio"] = precio
        existente["cantidad"] += cantidad
        return f"⚠️  Producto '{nombre}' ya existía. Precio actualizado y cantidad sumada."
    
    # Agregar nuevo producto como diccionario
    inventario.append({
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    })
    return f"✅ Producto '{nombre}' agregado correctamente."


def mostrar_inventario(inventario):
    """
    Muestra todos los productos del inventario en formato tabular.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.

    Retorno:
        None. Imprime directamente en consola.
    """
    if not inventario:
        print("\n  📦 El inventario está vacío.\n")
        return

    # Encabezado de la tabla
    print("\n" + "═" * 55)
    print(f"  {'NOMBRE':<20} {'PRECIO':>10} {'CANTIDAD':>10}  {'SUBTOTAL':>10}")
    print("═" * 55)

    # Mostrar cada producto con su subtotal
    subtotal = lambda p: p["precio"] * p["cantidad"]  # Lambda opcional para subtotal
    for producto in inventario:
        print(
            f"  {producto['nombre']:<20} "
            f"${producto['precio']:>9.2f} "
            f"{producto['cantidad']:>10} "
            f"  ${subtotal(producto):>9.2f}"
        )

    print("═" * 55 + "\n")


def buscar_producto(inventario, nombre):
    """
    Busca un producto en el inventario por nombre (sin distinción de mayúsculas).

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        nombre (str): Nombre del producto a buscar.

    Retorno:
        dict | None: El diccionario del producto si se encuentra, None si no existe.
    """
    nombre = nombre.strip().lower()
    for producto in inventario:
        if producto["nombre"].lower() == nombre:
            return producto
    return None


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    """
    Actualiza el precio y/o cantidad de un producto existente.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        nombre (str): Nombre del producto a actualizar.
        nuevo_precio (float | None): Nuevo precio del producto, si se desea cambiar.
        nueva_cantidad (int | None): Nueva cantidad del producto, si se desea cambiar.

    Retorno:
        str: Mensaje indicando si la actualización fue exitosa o el producto no existe.
    """
    producto = buscar_producto(inventario, nombre)
    if not producto:
        return f"❌ Producto '{nombre}' no encontrado en el inventario."

    cambios = []
    if nuevo_precio is not None:
        producto["precio"] = nuevo_precio
        cambios.append(f"precio → ${nuevo_precio:.2f}")
    if nueva_cantidad is not None:
        producto["cantidad"] = nueva_cantidad
        cambios.append(f"cantidad → {nueva_cantidad}")

    if cambios:
        return f"✅ Producto '{producto['nombre']}' actualizado: {', '.join(cambios)}."
    return "⚠️  No se realizó ningún cambio (sin nuevos valores proporcionados)."


def eliminar_producto(inventario, nombre):
    """
    Elimina un producto del inventario por nombre.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        nombre (str): Nombre del producto a eliminar.

    Retorno:
        str: Mensaje indicando si se eliminó correctamente o no fue encontrado.
    """
    producto = buscar_producto(inventario, nombre)
    if not producto:
        return f"❌ Producto '{nombre}' no encontrado en el inventario."
    
    inventario.remove(producto)
    return f"🗑️  Producto '{producto['nombre']}' eliminado correctamente."


def calcular_estadisticas(inventario):
    """
    Calcula métricas estadísticas del inventario actual.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.

    Retorno:
        dict | None: Diccionario con las métricas calculadas, o None si el inventario
                     está vacío. Claves:
                     - unidades_totales (int)
                     - valor_total (float)
                     - producto_mas_caro (dict con 'nombre' y 'precio')
                     - producto_mayor_stock (dict con 'nombre' y 'cantidad')
    """
    if not inventario:
        return None

    # Lambda para calcular subtotal de un producto
    subtotal = lambda p: p["precio"] * p["cantidad"]

    # Calcular métricas con funciones built-in y lambda
    unidades_totales = sum(p["cantidad"] for p in inventario)
    valor_total = sum(subtotal(p) for p in inventario)
    producto_mas_caro = max(inventario, key=lambda p: p["precio"])
    producto_mayor_stock = max(inventario, key=lambda p: p["cantidad"])

    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": {
            "nombre": producto_mas_caro["nombre"],
            "precio": producto_mas_caro["precio"]
        },
        "producto_mayor_stock": {
            "nombre": producto_mayor_stock["nombre"],
            "cantidad": producto_mayor_stock["cantidad"]
        }
    }


def mostrar_estadisticas(inventario):
    """
    Imprime las estadísticas del inventario de forma legible.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.

    Retorno:
        None. Imprime directamente en consola.
    """
    stats = calcular_estadisticas(inventario)
    if not stats:
        print("\n  📊 No hay datos para calcular estadísticas (inventario vacío).\n")
        return

    print("\n" + "═" * 45)
    print("          📊 ESTADÍSTICAS DEL INVENTARIO")
    print("═" * 45)
    print(f"  Unidades totales en stock : {stats['unidades_totales']}")
    print(f"  Valor total del inventario: ${stats['valor_total']:.2f}")
    print(f"  Producto más caro         : {stats['producto_mas_caro']['nombre']}"
          f" (${stats['producto_mas_caro']['precio']:.2f})")
    print(f"  Mayor stock               : {stats['producto_mayor_stock']['nombre']}"
          f" ({stats['producto_mayor_stock']['cantidad']} unidades)")
    print("═" * 45 + "\n")
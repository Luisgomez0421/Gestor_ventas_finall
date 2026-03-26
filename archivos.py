"""
archivos.py - Módulo de persistencia CSV para el inventario.
Gestiona la lectura y escritura del inventario en archivos CSV con validaciones.
"""

import csv
import os


def guardar_csv(inventario, ruta, incluir_header=True):
    """
    Guarda el inventario en un archivo CSV.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        ruta (str): Ruta del archivo CSV de destino.
        incluir_header (bool): Si True, escribe encabezado 'nombre,precio,cantidad'.

    Retorno:
        bool: True si se guardó exitosamente, False si ocurrió un error.
    """
    # Validar que el inventario no esté vacío
    if not inventario:
        print("⚠️  El inventario está vacío. No se puede guardar.")
        return False

    try:
        with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(
                archivo,
                fieldnames=["nombre", "precio", "cantidad"]
            )
            if incluir_header:
                escritor.writeheader()   # Escribir encabezado
            escritor.writerows(inventario)  # Escribir todos los productos

        print(f"💾 Inventario guardado en: {ruta}")
        return True

    except PermissionError:
        print(f"❌ Sin permisos para escribir en '{ruta}'. Verifica los permisos del archivo.")
    except OSError as e:
        print(f"❌ Error al escribir el archivo: {e}")
    except Exception as e:
        print(f"❌ Error inesperado al guardar: {e}")

    return False


def cargar_csv(ruta):
    """
    Carga productos desde un archivo CSV con validaciones fila por fila.

    Parámetros:
        ruta (str): Ruta del archivo CSV a leer.

    Retorno:
        tuple: (lista_productos, errores)
            - lista_productos (list): Productos válidos cargados.
            - errores (int): Número de filas inválidas omitidas.
        Retorna (None, 0) si el archivo no se pudo leer o tiene formato inválido.
    """
    productos = []
    errores = 0

    try:
        with open(ruta, mode="r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            # Validar encabezado
            campos_requeridos = {"nombre", "precio", "cantidad"}
            if not campos_requeridos.issubset(set(lector.fieldnames or [])):
                print(f"❌ El archivo '{ruta}' no tiene el encabezado válido: nombre,precio,cantidad")
                return None, 0

            # Procesar cada fila
            for numero_fila, fila in enumerate(lector, start=2):  # start=2 porque fila 1 es header
                # Validar que tenga exactamente las 3 columnas esperadas
                if len(fila) < 3 or not fila.get("nombre", "").strip():
                    errores += 1
                    continue

                try:
                    nombre = fila["nombre"].strip()
                    precio = float(fila["precio"])
                    cantidad = int(fila["cantidad"])

                    # Validar que precio y cantidad no sean negativos
                    if precio < 0 or cantidad < 0:
                        errores += 1
                        continue

                    productos.append({
                        "nombre": nombre,
                        "precio": precio,
                        "cantidad": cantidad
                    })

                except (ValueError, KeyError):
                    # Fila con datos no convertibles o claves faltantes
                    errores += 1
                    continue

    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: '{ruta}'")
        return None, 0
    except UnicodeDecodeError:
        print(f"❌ Error de codificación al leer '{ruta}'. Verifica que sea UTF-8.")
        return None, 0
    except Exception as e:
        print(f"❌ Error inesperado al cargar: {e}")
        return None, 0

    return productos, errores


def fusionar_inventarios(inventario_actual, productos_nuevos):
    """
    Fusiona productos nuevos al inventario existente.

    Política de fusión:
    - Si el producto ya existe: suma las cantidades y actualiza el precio al nuevo.
    - Si el producto es nuevo: lo agrega directamente.

    Parámetros:
        inventario_actual (list): Inventario en memoria con los productos actuales.
        productos_nuevos (list): Lista de productos a fusionar.

    Retorno:
        tuple: (agregados, actualizados)
            - agregados (int): Productos nuevos añadidos.
            - actualizados (int): Productos existentes actualizados.
    """
    agregados = 0
    actualizados = 0

    for nuevo in productos_nuevos:
        nombre_lower = nuevo["nombre"].lower()
        # Buscar si ya existe en el inventario actual
        existente = next(
            (p for p in inventario_actual if p["nombre"].lower() == nombre_lower),
            None
        )
        if existente:
            # Actualizar: sumar cantidad y tomar el nuevo precio
            existente["cantidad"] += nuevo["cantidad"]
            existente["precio"] = nuevo["precio"]
            actualizados += 1
        else:
            inventario_actual.append(nuevo)
            agregados += 1

    return agregados, actualizados
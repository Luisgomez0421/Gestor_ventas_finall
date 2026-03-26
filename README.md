# 📦 Sistema de Inventario en Python

Un sistema de gestión de inventario desarrollado en **Python** que permite administrar productos de forma sencilla desde la consola.
El programa permite **agregar, buscar, actualizar, eliminar productos, calcular estadísticas y guardar/cargar inventarios en archivos CSV**.

Este proyecto demuestra buenas prácticas de programación como:

* Modularización del código
* Validación de entradas
* Manejo de errores
* Uso de estructuras de datos
* Persistencia de datos con archivos CSV

---

# 🚀 Características

El sistema permite realizar las siguientes operaciones:

### 📦 Gestión de productos

* Agregar nuevos productos al inventario
* Mostrar todos los productos en formato tabular
* Buscar productos por nombre
* Actualizar precio o cantidad de un producto
* Eliminar productos del inventario

### 📊 Estadísticas del inventario

El sistema puede calcular automáticamente:

* Unidades totales en stock
* Valor total del inventario
* Producto más caro
* Producto con mayor cantidad en stock

### 💾 Persistencia de datos

El sistema permite trabajar con archivos **CSV**:

* Guardar el inventario actual en un archivo `.csv`
* Cargar productos desde un archivo `.csv`
* Fusionar inventarios automáticamente

Política de fusión:

* Si el producto **ya existe**, se **suma la cantidad** y se **actualiza el precio**.
* Si el producto **no existe**, se **agrega al inventario**.

---

# 🗂️ Estructura del Proyecto

```
inventario/
│
├── main.py
├── servicios.py
├── archivos.py
└── inventario.csv (opcional)
```

### 📄 main.py

Contiene la lógica principal del programa:

* Menú interactivo
* Validaciones de entrada
* Conexión entre los módulos
* Flujo del sistema

### 📄 servicios.py

Contiene las funciones que manejan la lógica del inventario:

* agregar_producto()
* mostrar_inventario()
* buscar_producto()
* actualizar_producto()
* eliminar_producto()
* calcular_estadisticas()
* mostrar_estadisticas()

### 📄 archivos.py

Maneja la **persistencia del inventario** en archivos CSV:

* guardar_csv()
* cargar_csv()
* fusionar_inventarios()

---

# 🧠 Estructura de los Datos

El inventario se almacena como una **lista de diccionarios**:

```python
inventario = [
    {
        "nombre": "Laptop",
        "precio": 3500.00,
        "cantidad": 5
    },
    {
        "nombre": "Mouse",
        "precio": 25.50,
        "cantidad": 20
    }
]
```

Cada producto contiene:

| Campo    | Tipo   | Descripción         |
| -------- | ------ | ------------------- |
| nombre   | string | Nombre del producto |
| precio   | float  | Precio unitario     |
| cantidad | int    | Cantidad disponible |

---

# 📄 Formato del Archivo CSV

El archivo CSV debe tener el siguiente formato:

```
nombre,precio,cantidad
Laptop,3500,5
Mouse,25.5,20
Teclado,120,10
```

El sistema valida automáticamente:

* Encabezados correctos
* Valores numéricos válidos
* Precios y cantidades no negativas
* Filas con datos incompletos

Las filas inválidas se **ignoran automáticamente**.

---

# ▶️ Cómo ejecutar el programa

1. Clonar o descargar el proyecto.

2. Ejecutar el archivo principal:

```bash
python main.py
```

3. Aparecerá el menú del sistema:

```
1. Agregar producto
2. Mostrar inventario
3. Buscar producto
4. Actualizar producto
5. Eliminar producto
6. Estadísticas
7. Guardar CSV
8. Cargar CSV
9. Salir
```

4. Selecciona la opción deseada.

---

# 🛡️ Validaciones implementadas

El sistema incluye múltiples validaciones para evitar errores:

* Nombres de productos vacíos
* Precios negativos
* Cantidades negativas
* Entradas no numéricas
* Archivos CSV inválidos
* Manejo de excepciones

Además, el programa incluye **manejo global de errores** para evitar que el sistema se cierre inesperadamente.

---

# 🧩 Tecnologías utilizadas

* **Python 3**
* Módulo estándar `csv`
* Programación modular
* Manejo de excepciones
* Estructuras de datos (listas y diccionarios)

---

# 📈 Posibles mejoras futuras

Algunas mejoras que podrían agregarse al proyecto:

* Interfaz gráfica (Tkinter o PyQt)
* Base de datos (SQLite o PostgreSQL)
* Sistema de usuarios
* Control de ventas
* Reportes automáticos
* API REST para inventario

---

# 👨‍💻 Autor

**Luis David Gómez Díaz**

Proyecto académico desarrollado como práctica de **programación en Python y manejo de estructuras de datos**.

---

# 📜 Licencia

Este proyecto es de uso **educativo y académico**.

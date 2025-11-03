# QuadTree - Sistema de Búsqueda Espacial

## 📋 Descripción del Proyecto

Este proyecto implementa un **QuadTree** (árbol cuaternario) para búsqueda espacial eficiente en espacios bidimensionales. El QuadTree es una estructura de datos que particiona recursivamente el espacio en cuatro cuadrantes, permitiendo realizar consultas espaciales de manera óptima.

### Funcionalidades Principales

✅ **Inserción de puntos** con atributos personalizados  
✅ **Consultas de rango rectangular** - Encuentra todos los puntos dentro de un área  
✅ **Búsqueda del vecino más cercano** - Algoritmo optimizado con poda  
✅ **Filtrado por atributos** - Busca puntos con características específicas  
✅ **Conteo por atributos** - Estadísticas sobre categorías de puntos  
✅ **Interfaz gráfica interactiva** - Visualización en tiempo real con pygame  
✅ **Suite completa de pruebas** - Tests unitarios exhaustivos  

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar o descargar el proyecto

```bash
cd "Búsqueda espacial con QuadTree"
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

**Dependencias:**
- `pygame==2.5.2` - Para la interfaz gráfica
- `numpy==1.24.3` - Operaciones numéricas
- `matplotlib==3.7.1` - Visualizaciones adicionales (opcional)

---

## 📖 Uso del Sistema

### 1. Interfaz Gráfica Interactiva (Recomendado)

La forma más visual e intuitiva de usar el QuadTree:

```bash
python visualization.py
```

O usando el script principal:

```bash
python main.py --gui
```

#### Controles de la Interfaz:

| Tecla | Función |
|-------|---------|
| **1** | Modo Inserción - Click para agregar puntos |
| **2** | Modo Consulta de Rango - Arrastra para seleccionar área |
| **3** | Modo Vecino Más Cercano - Click para buscar vecino |
| **4** | Modo Filtro por Categoría - Click en categoría para filtrar |
| **C** | Limpiar todos los puntos |
| **R** | Generar puntos aleatorios |
| **ESC** | Salir |

#### Características de la Interfaz:

- **Visualización en tiempo real** del árbol con subdivisiones
- **Colores por categoría**: Restaurant (rojo), Hospital (azul), School (verde), etc.
- **Estadísticas dinámicas**: Conteo de puntos, resultados de consultas
- **Retroalimentación visual**: Resaltado de resultados de búsqueda

---

### 2. Trabajar con Datos de Entrada/Salida

Procesa datos desde `input_data/` y guarda resultados en `output_data/`:

```bash
python trabajar_con_datos.py
```

**Este script:**
- ✅ Carga datos desde `input_data/city_locations.json`
- ✅ Realiza múltiples consultas (rango, vecino más cercano, filtrado)
- ✅ Genera estadísticas
- ✅ Guarda todos los resultados en `output_data/`

**Archivos generados:**
- `puntos_centro.json` - Puntos en el centro de la ciudad
- `vecino_mas_cercano.json` - Resultado de búsqueda del vecino más cercano
- `restaurantes.json` - Todos los restaurantes encontrados
- `hospitales.json` - Todos los hospitales encontrados
- `estadisticas_generales.json` - Resumen completo

### 3. Demostración Básica

Ver una demostración de todas las operaciones:

```bash
python main.py --demo
```

**Salida esperada:**
```
==============================================================
DEMOSTRACIÓN: Operaciones Básicas del QuadTree
==============================================================

1. Insertando puntos...
   ✓ Insertado: Restaurant A en (100, 100)
   ✓ Insertado: Hospital B en (200, 200)
   ...

2. Consulta de Rango Rectangular...
   Puntos encontrados: 3
   ...

3. Búsqueda de Vecino Más Cercano...
   ✓ Vecino más cercano: Hospital B
   ...

4. Filtrado por Atributo...
   Restaurantes encontrados: 2
   ...
```

---

### 4. Uso con Archivos de Datos

#### Cargar y procesar datos:

```bash
python main.py --file input_data/city_locations.json
```

**Salida:**
```
==============================================================
DEMOSTRACIÓN: Cargando datos desde input_data/city_locations.json
==============================================================

Insertando 120 puntos...
✓ 120 puntos insertados exitosamente

Estadísticas por categoría:
   Bank: 10
   Gas Station: 8
   Hospital: 8
   ...
```

---

### 5. Modo Interactivo (Consola)

Para uso programático desde la consola:

```bash
python main.py --interactive
```

**Comandos disponibles:**

```bash
quadtree> insert 100 150 Restaurant Central
✓ Punto insertado en (100.0, 150.0)

quadtree> insert 200 250 Hospital Norte
✓ Punto insertado en (200.0, 250.0)

quadtree> count
Total de puntos: 2

quadtree> range 150 200 100 100
Encontrados: 2 puntos
  (100.00, 150.00)
  (200.00, 250.00)

quadtree> nearest 180 200
Vecino más cercano: (200.00, 250.00)
Distancia: 54.08

quadtree> exit
```

---

## 💾 Trabajar con Archivos de Entrada y Salida

### Estructura de Carpetas

```
input_data/              # Datos de entrada
  ├── city_locations.json      # 30 lugares urbanos
  └── example_queries.json     # Consultas de ejemplo

output_data/             # Resultados generados
  ├── puntos_centro.json
  ├── vecino_mas_cercano.json
  ├── restaurantes.json
  ├── hospitales.json
  └── estadisticas_generales.json
```

### Ejemplo: Cargar Datos Personalizados

**Crea tu propio archivo en `input_data/mis_datos.json`:**

```json
[
  {
    "id": 1,
    "x": 300.5,
    "y": 450.2,
    "category": "Restaurant",
    "name": "Mi Restaurant",
    "rating": 4.5
  },
  {
    "id": 2,
    "x": 600.0,
    "y": 700.0,
    "category": "Hospital",
    "name": "Hospital Central",
    "rating": 4.8
  }
]
```

**Cargar y usar:**

```bash
python main.py --file input_data/mis_datos.json
```

### Código para Guardar Resultados

```python
import json

# Realizar consulta
results = qt.query_range(Rectangle(500, 500, 200, 200))

# Guardar en output_data/
output = {
    'total': len(results),
    'puntos': [{'x': p.x, 'y': p.y, **p.attributes} for p in results]
}

with open('output_data/mi_consulta.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
```

---

## 📁 Estructura del Proyecto

```
Búsqueda espacial con QuadTree/
│
├── quadtree.py              # Implementación del QuadTree
├── visualization.py          # Interfaz gráfica con pygame
├── main.py                   # Script principal con múltiples modos
├── trabajar_con_datos.py    # Script para trabajar con entrada/salida
│
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Este archivo
├── INFORME.md               # Informe técnico del proyecto
│
├── input_data/              # Datos de entrada
│   ├── city_locations.json
│   └── example_queries.json
│
└── output_data/             # Resultados y salidas
    └── expected_outputs.json
```

---

## 🎯 Casos de Uso Prácticos

### 1. **Sistema de Geolocalización**
Encuentra restaurantes, hospitales o servicios cercanos a tu ubicación.

```python
from quadtree import QuadTree, Point, Rectangle

# Crear mapa de la ciudad
boundary = Rectangle(500, 500, 1000, 1000)
city_map = QuadTree(boundary)

# Agregar lugares
city_map.insert(Point(300, 400, {'type': 'restaurant', 'name': 'Pizza Palace'}))
city_map.insert(Point(320, 410, {'type': 'hospital', 'name': 'City Hospital'}))

# Buscar lugares cercanos a mi ubicación
my_location = Point(310, 405)
nearest = city_map.nearest_neighbor(my_location)
print(f"Lugar más cercano: {nearest.attributes['name']}")
```

### 2. **Detección de Colisiones en Juegos**
Busca objetos en un área específica para detectar colisiones.

```python
# Buscar todos los enemigos en el rango de visión del jugador
player_vision = Rectangle(player_x, player_y, 200, 200)
visible_enemies = game_quadtree.query_range(player_vision)
```

### 3. **Análisis de Datos Espaciales**
Estadísticas sobre distribución de puntos de interés.

```python
# Contar tipos de establecimientos
restaurants = city_map.count_by_attribute('type', 'restaurant')
hospitals = city_map.count_by_attribute('type', 'hospital')
print(f"Restaurantes: {restaurants}, Hospitales: {hospitals}")
```

---

## 📊 Complejidad Temporal

| Operación | Caso Promedio | Caso Peor |
|-----------|---------------|-----------|
| **Inserción** | O(log n) | O(n) |
| **Consulta de Rango** | O(log n + k) | O(n) |
| **Vecino Más Cercano** | O(log n) | O(n) |
| **Filtrado** | O(n) | O(n) |

*Donde n es el número de puntos y k es el número de puntos en el rango*

---

## 🔧 Configuración Avanzada

### Ajustar capacidad del nodo:

```python
# Mayor capacidad = menos subdivisiones, más puntos por nodo
qt = QuadTree(boundary, capacity=8)  # Default es 4
```

### Boundary personalizado:

```python
# Para mapas de diferentes tamaños
boundary = Rectangle(
    center_x=1000,
    center_y=1000,
    width=2000,    # Mapa de 2000x2000
    height=2000
)
```

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'pygame'"

**Solución:**
```bash
pip install pygame
```

### Error: "Point outside boundary"

**Causa:** Intentando insertar un punto fuera del área del QuadTree.

**Solución:** Verificar que las coordenadas estén dentro del boundary definido.

```python
# Verificar antes de insertar
if boundary.contains(point):
    quadtree.insert(point)
```

### La interfaz gráfica no se muestra

**Posibles causas:**
- pygame no instalado correctamente
- Problema con drivers gráficos

**Solución:**
```bash
pip uninstall pygame
pip install pygame --upgrade
```

---

## 📝 Ejemplos de Código

### Ejemplo Completo:

```python
from quadtree import QuadTree, Point, Rectangle

# 1. Crear QuadTree
boundary = Rectangle(500, 500, 1000, 1000)
qt = QuadTree(boundary, capacity=4)

# 2. Insertar puntos
points = [
    Point(100, 100, {'name': 'A', 'type': 'restaurant'}),
    Point(200, 150, {'name': 'B', 'type': 'hospital'}),
    Point(300, 200, {'name': 'C', 'type': 'school'}),
    Point(150, 120, {'name': 'D', 'type': 'restaurant'}),
]

for point in points:
    qt.insert(point)

# 3. Consulta de rango
search_area = Rectangle(150, 125, 100, 100)
results = qt.query_range(search_area)
print(f"Puntos en área: {len(results)}")

# 4. Vecino más cercano
query = Point(180, 140)
nearest = qt.nearest_neighbor(query)
print(f"Más cercano: {nearest.attributes['name']}")

# 5. Filtrar por atributo
restaurants = qt.filter_by_attribute('type', 'restaurant')
print(f"Restaurantes: {len(restaurants)}")
```

---

## 👥 Autor

**Práctica Calificada N° 01**  
Estructura de Datos - QuadTree para Búsqueda Espacial

---

## 📄 Licencia

Este proyecto es de uso académico para la práctica calificada.

---

## 📚 Referencias

- [Quadtree - Wikipedia](https://en.wikipedia.org/wiki/Quadtree)
- [Spatial Indexing with Quadtrees](https://www.youtube.com/watch?v=OJxEcs0w_kE)
- [Pygame Documentation](https://www.pygame.org/docs/)

---

## ✅ Checklist de Entregables

- [x] Código fuente completo y documentado
- [x] README con instrucciones detalladas
- [x] Casos de prueba y validación
- [x] Archivos de entrada/salida de ejemplo
- [x] Interfaz gráfica para demostración
- [x] Informe técnico (INFORME.md)
- [ ] Demo en vivo (presentación)

---

**¿Preguntas o problemas?** Revisa la sección de solución de problemas o consulta el código fuente con comentarios detallados.

**¡Disfruta explorando el QuadTree! 🌳**


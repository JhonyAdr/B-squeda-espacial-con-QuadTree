CARPETA INPUT_DATA - Datos de Entrada para QuadTree
=====================================================

Esta carpeta contiene archivos de datos que puedes cargar en el QuadTree.

ARCHIVOS INCLUIDOS:
-------------------

1. city_locations.json
   - 30 puntos simulando lugares en una ciudad
   - Incluye: Restaurantes, Hospitales, Escuelas, Parques, Tiendas, Bancos, Farmacias
   - Cada punto tiene: id, x, y, category, name, rating

2. example_queries.json
   - Ejemplos de consultas predefinidas
   - Incluye: consultas de rango, vecino más cercano, filtrado

FORMATO DE DATOS:
-----------------

Los archivos JSON deben tener este formato:

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

CAMPOS REQUERIDOS:
- x: coordenada X (0-1000)
- y: coordenada Y (0-1000)

CAMPOS OPCIONALES:
- Puedes agregar cualquier atributo adicional (category, name, rating, etc.)

CÓMO USAR:
----------

1. Para cargar datos:
   python main.py --file input_data/city_locations.json

2. Para procesar y guardar resultados:
   python trabajar_con_datos.py

3. Para crear tus propios datos:
   - Crea un archivo JSON con el formato indicado
   - Guárdalo en esta carpeta
   - Carga con: python main.py --file input_data/TU_ARCHIVO.json

EJEMPLO DE CREACIÓN DE DATOS PERSONALIZADOS:
---------------------------------------------

Crea un archivo "mis_lugares.json" en esta carpeta:

[
  {
    "id": 1,
    "x": 100,
    "y": 100,
    "tipo": "Casa",
    "nombre": "Mi Casa"
  },
  {
    "id": 2,
    "x": 500,
    "y": 500,
    "tipo": "Trabajo",
    "nombre": "Mi Oficina"
  }
]

Luego carga con:
python main.py --file input_data/mis_lugares.json


CARPETA OUTPUT_DATA - Resultados del QuadTree
===============================================

Esta carpeta almacena los resultados de las consultas realizadas sobre el QuadTree.

ARCHIVOS QUE SE GENERAN:
------------------------

Cuando ejecutas: python trabajar_con_datos.py

Se generan automáticamente estos archivos:

1. puntos_centro.json
   - Puntos encontrados en el centro de la ciudad
   - Resultado de consulta de rango rectangular

2. vecino_mas_cercano.json
   - Resultado de búsqueda del vecino más cercano
   - Incluye distancia calculada

3. restaurantes.json
   - Todos los restaurantes encontrados
   - Resultado de filtrado por categoría

4. hospitales.json
   - Todos los hospitales encontrados
   - Resultado de filtrado por categoría

5. estadisticas_generales.json
   - Resumen completo de todas las consultas
   - Estadísticas del QuadTree

FORMATO DE SALIDA:
------------------

Los archivos JSON de salida tienen este formato:

{
  "fecha": "2025-11-03 20:30:00",
  "consulta": "Nombre de la consulta",
  "total_encontrados": 5,
  "puntos": [
    {
      "x": 300.5,
      "y": 450.2,
      "category": "Restaurant",
      "name": "Mi Restaurant"
    },
    ...
  ]
}

CÓMO LEER LOS RESULTADOS:
--------------------------

1. Abre los archivos JSON con cualquier editor de texto
2. O usa Python:

   import json
   
   with open('output_data/puntos_centro.json', 'r') as f:
       data = json.load(f)
       print(f"Total encontrados: {data['total_encontrados']}")

3. O visualiza en línea:
   - jsonviewer.stack.hu
   - jsonformatter.org

EJEMPLO DE USO:
---------------

# 1. Ejecutar consultas
python trabajar_con_datos.py

# 2. Los resultados se guardan automáticamente aquí

# 3. Revisar resultados
python -c "import json; print(json.load(open('output_data/estadisticas_generales.json')))"

PERSONALIZAR SALIDAS:
---------------------

Para crear tus propios archivos de salida, usa este código:

import json

# Tu consulta
results = qt.query_range(Rectangle(500, 500, 200, 200))

# Guardar resultado
output = {
    'fecha': '2025-11-03',
    'mi_consulta': 'descripción',
    'resultados': [{'x': p.x, 'y': p.y, **p.attributes} for p in results]
}

with open('output_data/mi_resultado.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)


"""
Script para trabajar con datos de entrada y salida del QuadTree
Carga datos desde input_data/, realiza consultas, y guarda resultados en output_data/
"""
from quadtree import QuadTree, Point, Rectangle
import json
import os
from datetime import datetime


def cargar_datos_desde_archivo(filename):
    """Carga datos desde un archivo JSON en input_data/"""
    filepath = os.path.join('input_data', filename)
    
    print(f"📥 Cargando datos desde {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ {len(data)} registros cargados exitosamente\n")
        return data
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {filepath}")
        return []
    except json.JSONDecodeError:
        print(f"❌ Error: El archivo {filepath} no es un JSON válido")
        return []


def crear_quadtree_con_datos(data):
    """Crea un QuadTree e inserta los datos"""
    print("🌳 Creando QuadTree e insertando puntos...")
    
    # Crear QuadTree con boundary de 1000x1000
    boundary = Rectangle(500, 500, 1000, 1000)
    qt = QuadTree(boundary, capacity=4)
    
    # Insertar cada punto
    insertados = 0
    for item in data:
        if 'x' in item and 'y' in item:
            # Crear punto con todos los atributos del registro
            attributes = {k: v for k, v in item.items() if k not in ['x', 'y']}
            point = Point(item['x'], item['y'], attributes)
            
            if qt.insert(point):
                insertados += 1
        else:
            print(f"⚠️  Advertencia: Registro sin coordenadas x,y: {item}")
    
    print(f"✅ {insertados} puntos insertados en el QuadTree")
    print(f"🌳 Árbol subdividido: {'Sí' if qt.root.divided else 'No'}\n")
    
    return qt


def realizar_consulta_rango(qt, center_x, center_y, width, height, descripcion=""):
    """Realiza una consulta de rango rectangular"""
    print(f"📦 Consulta de Rango: {descripcion}")
    print(f"   Centro: ({center_x}, {center_y}), Tamaño: {width}x{height}")
    
    rect = Rectangle(center_x, center_y, width, height)
    results = qt.query_range(rect)
    
    print(f"   ✅ Encontrados: {len(results)} puntos\n")
    
    return results


def realizar_vecino_mas_cercano(qt, query_x, query_y, descripcion=""):
    """Busca el vecino más cercano a un punto"""
    print(f"🎯 Vecino Más Cercano: {descripcion}")
    print(f"   Desde punto: ({query_x}, {query_y})")
    
    query_point = Point(query_x, query_y)
    nearest = qt.nearest_neighbor(query_point)
    
    if nearest:
        distance = query_point.distance_to(nearest)
        print(f"   ✅ Encontrado: {nearest.attributes.get('name', 'Sin nombre')}")
        print(f"   📍 Ubicación: ({nearest.x:.2f}, {nearest.y:.2f})")
        print(f"   📏 Distancia: {distance:.2f} unidades\n")
        return nearest, distance
    else:
        print(f"   ❌ No se encontró ningún punto\n")
        return None, None


def filtrar_por_categoria(qt, categoria):
    """Filtra puntos por categoría"""
    print(f"🔍 Filtrando por categoría: {categoria}")
    
    results = qt.filter_by_attribute('category', categoria)
    
    print(f"   ✅ Encontrados: {len(results)} puntos\n")
    
    return results


def generar_estadisticas(qt):
    """Genera estadísticas del QuadTree"""
    print("📊 Generando estadísticas...")
    
    all_points = qt.get_all_points()
    
    # Contar por categoría
    categorias = {}
    for point in all_points:
        cat = point.attributes.get('category', 'Sin categoría')
        categorias[cat] = categorias.get(cat, 0) + 1
    
    # Calcular ratings promedio si existen
    ratings = [p.attributes.get('rating', 0) for p in all_points if 'rating' in p.attributes]
    rating_promedio = sum(ratings) / len(ratings) if ratings else 0
    
    estadisticas = {
        'total_puntos': len(all_points),
        'por_categoria': categorias,
        'rating_promedio': round(rating_promedio, 2),
        'arbol_subdividido': qt.root.divided
    }
    
    print(f"   Total de puntos: {estadisticas['total_puntos']}")
    print(f"   Categorías encontradas: {len(categorias)}")
    print(f"   Rating promedio: {estadisticas['rating_promedio']}\n")
    
    return estadisticas


def guardar_resultados(data, filename):
    """Guarda resultados en un archivo JSON en output_data/"""
    # Asegurar que existe el directorio
    os.makedirs('output_data', exist_ok=True)
    
    filepath = os.path.join('output_data', filename)
    
    print(f"💾 Guardando resultados en {filepath}...")
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Resultados guardados exitosamente\n")
        return True
    except Exception as e:
        print(f"❌ Error al guardar: {e}\n")
        return False


def puntos_a_dict(points):
    """Convierte una lista de Points a diccionarios para JSON"""
    return [
        {
            'x': p.x,
            'y': p.y,
            **p.attributes
        }
        for p in points
    ]


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("  🌳 TRABAJAR CON DATOS DE ENTRADA Y SALIDA - QuadTree")
    print("="*70 + "\n")
    
    # ========== 1. CARGAR DATOS DE ENTRADA ==========
    data = cargar_datos_desde_archivo('city_locations.json')
    
    if not data:
        print("❌ No se pudieron cargar datos. Saliendo...")
        return
    
    # ========== 2. CREAR QUADTREE ==========
    qt = crear_quadtree_con_datos(data)
    
    # ========== 3. REALIZAR CONSULTAS ==========
    print("-"*70)
    print("  REALIZANDO CONSULTAS")
    print("-"*70 + "\n")
    
    # Consulta 1: Rango en el centro
    puntos_centro = realizar_consulta_rango(
        qt, 500, 500, 300, 300, 
        "Centro de la ciudad"
    )
    
    # Consulta 2: Vecino más cercano
    nearest, distance = realizar_vecino_mas_cercano(
        qt, 400, 400,
        "Desde coordenada (400, 400)"
    )
    
    # Consulta 3: Filtrar restaurantes
    restaurantes = filtrar_por_categoria(qt, 'Restaurant')
    
    # Consulta 4: Filtrar hospitales
    hospitales = filtrar_por_categoria(qt, 'Hospital')
    
    # ========== 4. GENERAR ESTADÍSTICAS ==========
    print("-"*70)
    print("  ESTADÍSTICAS")
    print("-"*70 + "\n")
    
    estadisticas = generar_estadisticas(qt)
    
    # ========== 5. GUARDAR RESULTADOS ==========
    print("-"*70)
    print("  GUARDANDO RESULTADOS")
    print("-"*70 + "\n")
    
    # Resultado 1: Puntos en el centro
    resultado_centro = {
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'consulta': 'Rango rectangular en centro',
        'parametros': {
            'center_x': 500,
            'center_y': 500,
            'width': 300,
            'height': 300
        },
        'total_encontrados': len(puntos_centro),
        'puntos': puntos_a_dict(puntos_centro)
    }
    guardar_resultados(resultado_centro, 'puntos_centro.json')
    
    # Resultado 2: Vecino más cercano
    if nearest:
        resultado_vecino = {
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'consulta': 'Vecino más cercano',
            'punto_consulta': {'x': 400, 'y': 400},
            'vecino_encontrado': {
                'x': nearest.x,
                'y': nearest.y,
                'distancia': round(distance, 2),
                **nearest.attributes
            }
        }
        guardar_resultados(resultado_vecino, 'vecino_mas_cercano.json')
    
    # Resultado 3: Restaurantes
    resultado_restaurantes = {
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'consulta': 'Filtrado por categoría',
        'categoria': 'Restaurant',
        'total_encontrados': len(restaurantes),
        'puntos': puntos_a_dict(restaurantes)
    }
    guardar_resultados(resultado_restaurantes, 'restaurantes.json')
    
    # Resultado 4: Hospitales
    resultado_hospitales = {
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'consulta': 'Filtrado por categoría',
        'categoria': 'Hospital',
        'total_encontrados': len(hospitales),
        'puntos': puntos_a_dict(hospitales)
    }
    guardar_resultados(resultado_hospitales, 'hospitales.json')
    
    # Resultado 5: Estadísticas generales
    resultado_estadisticas = {
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'estadisticas': estadisticas,
        'resumen_consultas': {
            'puntos_en_centro': len(puntos_centro),
            'total_restaurantes': len(restaurantes),
            'total_hospitales': len(hospitales),
            'vecino_mas_cercano_distancia': round(distance, 2) if distance else None
        }
    }
    guardar_resultados(resultado_estadisticas, 'estadisticas_generales.json')
    
    # ========== 6. RESUMEN FINAL ==========
    print("="*70)
    print("  ✅ PROCESO COMPLETADO")
    print("="*70 + "\n")
    
    print("📂 Archivos generados en output_data/:")
    print("   • puntos_centro.json")
    print("   • vecino_mas_cercano.json")
    print("   • restaurantes.json")
    print("   • hospitales.json")
    print("   • estadisticas_generales.json")
    print("\n")


if __name__ == '__main__':
    main()


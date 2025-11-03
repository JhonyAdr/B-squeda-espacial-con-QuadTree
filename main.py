"""
Script principal para ejecutar diferentes modos del QuadTree
"""
import argparse
import json
from quadtree import QuadTree, Point, Rectangle


def load_data_from_json(filename):
    """Carga datos desde un archivo JSON"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def demo_basic_operations():
    """Demostración de operaciones básicas"""
    print("=" * 60)
    print("DEMOSTRACIÓN: Operaciones Básicas del QuadTree")
    print("=" * 60)
    
    # Crear QuadTree
    boundary = Rectangle(500, 500, 1000, 1000)
    qt = QuadTree(boundary, capacity=4)
    
    # Insertar puntos
    print("\n1. Insertando puntos...")
    points = [
        Point(100, 100, {'name': 'Restaurant A', 'category': 'Restaurant'}),
        Point(200, 200, {'name': 'Hospital B', 'category': 'Hospital'}),
        Point(300, 300, {'name': 'School C', 'category': 'School'}),
        Point(150, 150, {'name': 'Restaurant D', 'category': 'Restaurant'}),
        Point(400, 400, {'name': 'Park E', 'category': 'Park'}),
    ]
    
    for point in points:
        qt.insert(point)
        print(f"   ✓ Insertado: {point.attributes['name']} en ({point.x}, {point.y})")
    
    print(f"\n   Total de puntos insertados: {qt.count_points()}")
    
    # Consulta de rango
    print("\n2. Consulta de Rango Rectangular...")
    query_rect = Rectangle(200, 200, 200, 200)
    print(f"   Buscando en rectángulo: centro=({query_rect.x}, {query_rect.y}), "
          f"tamaño=({query_rect.width}, {query_rect.height})")
    
    results = qt.query_range(query_rect)
    print(f"   Puntos encontrados: {len(results)}")
    for p in results:
        print(f"   - {p.attributes['name']} en ({p.x}, {p.y})")
    
    # Vecino más cercano
    print("\n3. Búsqueda de Vecino Más Cercano...")
    query_point = Point(180, 180)
    print(f"   Buscando vecino más cercano a ({query_point.x}, {query_point.y})")
    
    nearest = qt.nearest_neighbor(query_point)
    if nearest:
        distance = query_point.distance_to(nearest)
        print(f"   ✓ Vecino más cercano: {nearest.attributes['name']}")
        print(f"     Posición: ({nearest.x}, {nearest.y})")
        print(f"     Distancia: {distance:.2f} unidades")
    
    # Filtrado por atributo
    print("\n4. Filtrado por Atributo...")
    restaurants = qt.filter_by_attribute('category', 'Restaurant')
    print(f"   Restaurantes encontrados: {len(restaurants)}")
    for r in restaurants:
        print(f"   - {r.attributes['name']} en ({r.x}, {r.y})")
    
    print("\n" + "=" * 60)


def demo_with_file(filename):
    """Demostración usando datos de un archivo"""
    print("=" * 60)
    print(f"DEMOSTRACIÓN: Cargando datos desde {filename}")
    print("=" * 60)
    
    # Cargar datos
    data = load_data_from_json(filename)
    
    # Crear QuadTree
    boundary = Rectangle(500, 500, 1000, 1000)
    qt = QuadTree(boundary, capacity=4)
    
    # Insertar puntos
    print(f"\nInsertando {len(data)} puntos...")
    for item in data:
        point = Point(
            item['x'],
            item['y'],
            {k: v for k, v in item.items() if k not in ['x', 'y']}
        )
        qt.insert(point)
    
    print(f"✓ {qt.count_points()} puntos insertados exitosamente")
    
    # Estadísticas por categoría
    if 'category' in data[0]:
        print("\nEstadísticas por categoría:")
        categories = set(item['category'] for item in data)
        for category in sorted(categories):
            count = qt.count_by_attribute('category', category)
            print(f"   {category}: {count}")
    
    # Ejemplo de consulta de rango
    print("\nEjemplo de consulta de rango (centro de la ciudad):")
    query_rect = Rectangle(500, 500, 300, 300)
    results = qt.query_range(query_rect)
    print(f"   Puntos encontrados en el centro: {len(results)}")
    
    # Mostrar algunos resultados
    if results:
        print("   Primeros 5 resultados:")
        for p in results[:5]:
            attrs_str = ', '.join(f"{k}={v}" for k, v in list(p.attributes.items())[:2])
            print(f"   - ({p.x:.2f}, {p.y:.2f}) - {attrs_str}")
    
    print("\n" + "=" * 60)


def interactive_mode():
    """Modo interactivo de consola"""
    print("=" * 60)
    print("MODO INTERACTIVO - QuadTree")
    print("=" * 60)
    
    boundary = Rectangle(500, 500, 1000, 1000)
    qt = QuadTree(boundary, capacity=4)
    
    print("\nComandos disponibles:")
    print("  insert <x> <y> [atributos] - Insertar punto")
    print("  range <cx> <cy> <w> <h>     - Consulta de rango")
    print("  nearest <x> <y>             - Vecino más cercano")
    print("  count                        - Contar puntos")
    print("  filter <attr> <valor>       - Filtrar por atributo")
    print("  exit                         - Salir")
    print()
    
    while True:
        try:
            cmd = input("quadtree> ").strip().split()
            
            if not cmd:
                continue
            
            if cmd[0] == 'exit':
                break
            
            elif cmd[0] == 'insert' and len(cmd) >= 3:
                x, y = float(cmd[1]), float(cmd[2])
                attrs = {}
                if len(cmd) > 3:
                    attrs['name'] = ' '.join(cmd[3:])
                point = Point(x, y, attrs)
                if qt.insert(point):
                    print(f"✓ Punto insertado en ({x}, {y})")
                else:
                    print("✗ Error: Punto fuera del boundary")
            
            elif cmd[0] == 'range' and len(cmd) >= 5:
                cx, cy = float(cmd[1]), float(cmd[2])
                w, h = float(cmd[3]), float(cmd[4])
                rect = Rectangle(cx, cy, w, h)
                results = qt.query_range(rect)
                print(f"Encontrados: {len(results)} puntos")
                for p in results[:10]:  # Mostrar máximo 10
                    print(f"  ({p.x:.2f}, {p.y:.2f})")
            
            elif cmd[0] == 'nearest' and len(cmd) >= 3:
                x, y = float(cmd[1]), float(cmd[2])
                query = Point(x, y)
                nearest = qt.nearest_neighbor(query)
                if nearest:
                    dist = query.distance_to(nearest)
                    print(f"Vecino más cercano: ({nearest.x:.2f}, {nearest.y:.2f})")
                    print(f"Distancia: {dist:.2f}")
                else:
                    print("No hay puntos en el árbol")
            
            elif cmd[0] == 'count':
                print(f"Total de puntos: {qt.count_points()}")
            
            elif cmd[0] == 'filter' and len(cmd) >= 3:
                attr = cmd[1]
                value = cmd[2]
                results = qt.filter_by_attribute(attr, value)
                print(f"Encontrados: {len(results)} puntos con {attr}={value}")
            
            else:
                print("Comando no reconocido o argumentos incorrectos")
        
        except ValueError:
            print("Error: Coordenadas deben ser números")
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='QuadTree - Sistema de Búsqueda Espacial',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py --demo              # Demostración básica
  python main.py --file input_data/city_locations.json
  python main.py --interactive       # Modo interactivo
  python main.py --gui              # Interfaz gráfica (ejecuta visualization.py)
        """
    )
    
    parser.add_argument('--demo', action='store_true',
                       help='Ejecutar demostración básica')
    parser.add_argument('--file', type=str,
                       help='Cargar datos desde archivo JSON')
    parser.add_argument('--interactive', action='store_true',
                       help='Modo interactivo de consola')
    parser.add_argument('--gui', action='store_true',
                       help='Iniciar interfaz gráfica')
    
    args = parser.parse_args()
    
    if args.gui:
        print("Iniciando interfaz gráfica...")
        from visualization import QuadTreeVisualizer
        visualizer = QuadTreeVisualizer()
        visualizer.run()
    elif args.demo:
        demo_basic_operations()
    elif args.file:
        demo_with_file(args.file)
    elif args.interactive:
        interactive_mode()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()


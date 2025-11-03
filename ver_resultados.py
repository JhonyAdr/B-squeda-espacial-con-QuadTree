"""
Script simple para ver los resultados generados en output_data/
"""
import json
import os


def ver_archivo(filename):
    """Lee y muestra un archivo JSON de resultados"""
    filepath = os.path.join('output_data', filename)
    
    if not os.path.exists(filepath):
        print(f"El archivo {filename} no existe aún.")
        print(f"   Ejecuta primero: python trabajar_con_datos.py\n")
        return
    
    print(f"\n{'='*70}")
    print(f"  {filename}")
    print('='*70)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Mostrar información según el tipo de archivo
    if 'estadisticas' in data:
        # Es el archivo de estadísticas generales
        print(f"\nEstadísticas Generales:")
        print(f"   Fecha: {data.get('fecha', 'N/A')}")
        print(f"   Total de puntos: {data['estadisticas']['total_puntos']}")
        print(f"\n   Por categoría:")
        for cat, count in data['estadisticas']['por_categoria'].items():
            print(f"      • {cat}: {count}")
        print(f"\n   Rating promedio: {data['estadisticas']['rating_promedio']}")
        
        if 'resumen_consultas' in data:
            print(f"\nResumen de Consultas:")
            for key, value in data['resumen_consultas'].items():
                print(f"      • {key.replace('_', ' ').title()}: {value}")
    
    elif 'vecino_encontrado' in data:
        # Es el archivo de vecino más cercano
        print(f"\nVecino Más Cercano:")
        print(f"   Fecha: {data.get('fecha', 'N/A')}")
        print(f"   Punto de consulta: ({data['punto_consulta']['x']}, {data['punto_consulta']['y']})")
        vecino = data['vecino_encontrado']
        print(f"\n   Vecino encontrado:")
        print(f"      • Nombre: {vecino.get('name', 'N/A')}")
        print(f"      • Ubicación: ({vecino['x']:.2f}, {vecino['y']:.2f})")
        print(f"      • Distancia: {vecino['distancia']:.2f} unidades")
        print(f"      • Categoría: {vecino.get('category', 'N/A')}")
    
    elif 'puntos' in data and 'total_encontrados' in data:
        # Es un archivo de consulta (rango o filtrado)
        print(f"\nConsulta: {data.get('consulta', 'N/A')}")
        print(f"   Fecha: {data.get('fecha', 'N/A')}")
        
        if 'parametros' in data:
            print(f"   Parámetros:")
            for key, value in data['parametros'].items():
                print(f"      • {key}: {value}")
        
        if 'categoria' in data:
            print(f"   Categoría filtrada: {data['categoria']}")
        
        print(f"\n   Total encontrados: {data['total_encontrados']}")
        
        if data['puntos']:
            print(f"\n   Puntos encontrados:")
            for i, punto in enumerate(data['puntos'][:10], 1):  # Mostrar máximo 10
                nombre = punto.get('name', 'Sin nombre')
                cat = punto.get('category', 'N/A')
                print(f"      {i}. {nombre} - {cat} - ({punto['x']:.2f}, {punto['y']:.2f})")
            
            if len(data['puntos']) > 10:
                print(f"      ... y {len(data['puntos']) - 10} más")
    
    print()


def main():
    """Muestra todos los resultados disponibles"""
    print("\n" + "="*70)
    print("  VISUALIZADOR DE RESULTADOS - QuadTree")
    print("="*70)
    
    # Lista de archivos a buscar
    archivos = [
        'estadisticas_generales.json',
        'puntos_centro.json',
        'vecino_mas_cercano.json',
        'restaurantes.json',
        'hospitales.json'
    ]
    
    archivos_encontrados = []
    
    # Verificar qué archivos existen
    for archivo in archivos:
        if os.path.exists(os.path.join('output_data', archivo)):
            archivos_encontrados.append(archivo)
    
    if not archivos_encontrados:
        print("\nNo se encontraron archivos de resultados.")
        print("\nPara generar resultados, ejecuta:")
        print("   python trabajar_con_datos.py")
        print()
        return
    
    print(f"\nSe encontraron {len(archivos_encontrados)} archivos de resultados\n")
    
    # Mostrar cada archivo
    for archivo in archivos_encontrados:
        ver_archivo(archivo)
    
    print("="*70)
    print("  Fin de los resultados")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()


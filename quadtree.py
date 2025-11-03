"""
Implementación de QuadTree para búsqueda espacial
Soporta: inserción, consultas de rango, vecino más cercano, filtrado por atributos
"""
import math
from typing import List, Tuple, Optional, Dict, Any


class Point:
    """Representa un punto en el espacio 2D con atributos adicionales"""
    
    def __init__(self, x: float, y: float, attributes: Dict[str, Any] = None):
        self.x = x
        self.y = y
        self.attributes = attributes if attributes is not None else {}
    
    def distance_to(self, other: 'Point') -> float:
        """Calcula la distancia euclidiana a otro punto"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.attributes})"


class Rectangle:
    """Representa un rectángulo (bounding box)"""
    
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x  # Centro x
        self.y = y  # Centro y
        self.width = width
        self.height = height
        self.half_width = width / 2
        self.half_height = height / 2
    
    def contains(self, point: Point) -> bool:
        """Verifica si un punto está dentro del rectángulo"""
        return (self.x - self.half_width <= point.x <= self.x + self.half_width and
                self.y - self.half_height <= point.y <= self.y + self.half_height)
    
    def intersects(self, other: 'Rectangle') -> bool:
        """Verifica si este rectángulo intersecta con otro"""
        return not (other.x - other.half_width > self.x + self.half_width or
                   other.x + other.half_width < self.x - self.half_width or
                   other.y - other.half_height > self.y + self.half_height or
                   other.y + other.half_height < self.y - self.half_height)
    
    def distance_to_point(self, point: Point) -> float:
        """Calcula la distancia mínima desde el punto al rectángulo"""
        dx = max(self.x - self.half_width - point.x, 0, point.x - (self.x + self.half_width))
        dy = max(self.y - self.half_height - point.y, 0, point.y - (self.y + self.half_height))
        return math.sqrt(dx * dx + dy * dy)


class QuadTreeNode:
    """Nodo del QuadTree"""
    
    def __init__(self, boundary: Rectangle, capacity: int = 4):
        self.boundary = boundary
        self.capacity = capacity
        self.points: List[Point] = []
        self.divided = False
        
        # Subdivisiones
        self.northwest: Optional['QuadTreeNode'] = None
        self.northeast: Optional['QuadTreeNode'] = None
        self.southwest: Optional['QuadTreeNode'] = None
        self.southeast: Optional['QuadTreeNode'] = None
    
    def subdivide(self):
        """Divide el nodo en 4 cuadrantes"""
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.half_width
        h = self.boundary.half_height
        
        nw = Rectangle(x - w/2, y - h/2, w, h)
        ne = Rectangle(x + w/2, y - h/2, w, h)
        sw = Rectangle(x - w/2, y + h/2, w, h)
        se = Rectangle(x + w/2, y + h/2, w, h)
        
        self.northwest = QuadTreeNode(nw, self.capacity)
        self.northeast = QuadTreeNode(ne, self.capacity)
        self.southwest = QuadTreeNode(sw, self.capacity)
        self.southeast = QuadTreeNode(se, self.capacity)
        
        self.divided = True
    
    def insert(self, point: Point) -> bool:
        """Inserta un punto en el QuadTree"""
        # Si el punto no está en el boundary, rechazar
        if not self.boundary.contains(point):
            return False
        
        # Si hay capacidad y no está dividido, agregar aquí
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            return True
        
        # Si no está dividido, subdividir
        if not self.divided:
            self.subdivide()
            # Redistribuir puntos existentes
            for p in self.points:
                self._insert_to_children(p)
            self.points.clear()
        
        # Insertar en hijo apropiado
        return self._insert_to_children(point)
    
    def _insert_to_children(self, point: Point) -> bool:
        """Inserta el punto en el hijo apropiado"""
        if self.northwest.insert(point):
            return True
        if self.northeast.insert(point):
            return True
        if self.southwest.insert(point):
            return True
        if self.southeast.insert(point):
            return True
        return False
    
    def query_range(self, range_rect: Rectangle, found: List[Point] = None) -> List[Point]:
        """Consulta todos los puntos dentro de un rango rectangular"""
        if found is None:
            found = []
        
        # Si no hay intersección, retornar
        if not self.boundary.intersects(range_rect):
            return found
        
        # Verificar puntos en este nodo
        for point in self.points:
            if range_rect.contains(point):
                found.append(point)
        
        # Si está dividido, consultar hijos
        if self.divided:
            self.northwest.query_range(range_rect, found)
            self.northeast.query_range(range_rect, found)
            self.southwest.query_range(range_rect, found)
            self.southeast.query_range(range_rect, found)
        
        return found
    
    def nearest_neighbor(self, query_point: Point, best: Optional[Tuple[Point, float]] = None) -> Optional[Tuple[Point, float]]:
        """Encuentra el vecino más cercano al punto de consulta"""
        # Si el boundary está más lejos que el mejor candidato actual, podar
        if best is not None:
            if self.boundary.distance_to_point(query_point) > best[1]:
                return best
        
        # Verificar puntos en este nodo
        for point in self.points:
            if point is query_point:  # No comparar consigo mismo
                continue
            dist = query_point.distance_to(point)
            if best is None or dist < best[1]:
                best = (point, dist)
        
        # Si está dividido, consultar hijos
        if self.divided:
            # Ordenar hijos por distancia para optimizar búsqueda
            children = [
                (self.northwest, self.northwest.boundary.distance_to_point(query_point)),
                (self.northeast, self.northeast.boundary.distance_to_point(query_point)),
                (self.southwest, self.southwest.boundary.distance_to_point(query_point)),
                (self.southeast, self.southeast.boundary.distance_to_point(query_point))
            ]
            children.sort(key=lambda x: x[1])
            
            for child, _ in children:
                best = child.nearest_neighbor(query_point, best)
        
        return best
    
    def count_points(self) -> int:
        """Cuenta el número total de puntos en el árbol"""
        count = len(self.points)
        if self.divided:
            count += self.northwest.count_points()
            count += self.northeast.count_points()
            count += self.southwest.count_points()
            count += self.southeast.count_points()
        return count
    
    def get_all_points(self, points: List[Point] = None) -> List[Point]:
        """Obtiene todos los puntos del árbol"""
        if points is None:
            points = []
        
        points.extend(self.points)
        
        if self.divided:
            self.northwest.get_all_points(points)
            self.northeast.get_all_points(points)
            self.southwest.get_all_points(points)
            self.southeast.get_all_points(points)
        
        return points


class QuadTree:
    """Estructura QuadTree para búsqueda espacial eficiente"""
    
    def __init__(self, boundary: Rectangle, capacity: int = 4):
        self.root = QuadTreeNode(boundary, capacity)
        self.boundary = boundary
    
    def insert(self, point: Point) -> bool:
        """Inserta un punto en el QuadTree"""
        return self.root.insert(point)
    
    def query_range(self, range_rect: Rectangle) -> List[Point]:
        """Consulta de rango rectangular"""
        return self.root.query_range(range_rect)
    
    def nearest_neighbor(self, query_point: Point) -> Optional[Point]:
        """Encuentra el vecino más cercano"""
        result = self.root.nearest_neighbor(query_point)
        return result[0] if result else None
    
    def filter_by_attribute(self, attribute_name: str, attribute_value: Any) -> List[Point]:
        """Filtra puntos por un atributo específico"""
        all_points = self.root.get_all_points()
        return [p for p in all_points 
                if attribute_name in p.attributes 
                and p.attributes[attribute_name] == attribute_value]
    
    def count_by_attribute(self, attribute_name: str, attribute_value: Any) -> int:
        """Cuenta puntos con un atributo específico"""
        return len(self.filter_by_attribute(attribute_name, attribute_value))
    
    def count_points(self) -> int:
        """Cuenta el total de puntos en el árbol"""
        return self.root.count_points()
    
    def get_all_points(self) -> List[Point]:
        """Obtiene todos los puntos del árbol"""
        return self.root.get_all_points()


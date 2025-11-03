"""
Interfaz gráfica con pygame para visualizar y demostrar el QuadTree
"""
import pygame
import random
from quadtree import QuadTree, Point, Rectangle, QuadTreeNode

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 150, 0)
ORANGE = (255, 165, 0)

# Categorías de puntos
CATEGORIES = ['Restaurant', 'Hospital', 'School', 'Park', 'Store']
CATEGORY_COLORS = {
    'Restaurant': RED,
    'Hospital': BLUE,
    'School': GREEN,
    'Park': DARK_GREEN,
    'Store': ORANGE
}


class QuadTreeVisualizer:
    """Visualizador interactivo del QuadTree"""
    
    def __init__(self, width=1000, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("QuadTree - Búsqueda Espacial")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Área de visualización
        self.vis_width = 700
        self.vis_height = 700
        self.offset_x = 50
        self.offset_y = 50
        
        # QuadTree
        boundary = Rectangle(self.vis_width/2, self.vis_height/2, 
                           self.vis_width, self.vis_height)
        self.quadtree = QuadTree(boundary, capacity=4)
        
        # Estado de la aplicación
        self.mode = "insert"  # insert, range_query, nearest_neighbor, filter
        self.range_start = None
        self.range_rect = None
        self.query_point = None
        self.nearest_point = None
        self.filtered_points = []
        self.selected_category = None
        
        # Generar puntos de ejemplo
        self.generate_random_points(30)
    
    def generate_random_points(self, count):
        """Genera puntos aleatorios con categorías"""
        for _ in range(count):
            x = random.uniform(10, self.vis_width - 10)
            y = random.uniform(10, self.vis_height - 10)
            category = random.choice(CATEGORIES)
            point = Point(x, y, {'category': category, 'id': random.randint(1000, 9999)})
            self.quadtree.insert(point)
    
    def world_to_screen(self, x, y):
        """Convierte coordenadas del mundo a coordenadas de pantalla"""
        return (int(x + self.offset_x), int(y + self.offset_y))
    
    def screen_to_world(self, screen_x, screen_y):
        """Convierte coordenadas de pantalla a coordenadas del mundo"""
        return (screen_x - self.offset_x, screen_y - self.offset_y)
    
    def draw_rectangle(self, rect: Rectangle, color, width=1):
        """Dibuja un rectángulo en la pantalla"""
        x, y = self.world_to_screen(rect.x - rect.half_width, rect.y - rect.half_height)
        pygame.draw.rect(self.screen, color, 
                        (x, y, rect.width, rect.height), width)
    
    def draw_quadtree_node(self, node: QuadTreeNode):
        """Dibuja recursivamente el QuadTree"""
        # Dibujar boundary del nodo
        self.draw_rectangle(node.boundary, GRAY, 1)
        
        # Si está dividido, dibujar hijos
        if node.divided:
            self.draw_quadtree_node(node.northwest)
            self.draw_quadtree_node(node.northeast)
            self.draw_quadtree_node(node.southwest)
            self.draw_quadtree_node(node.southeast)
    
    def draw_point(self, point: Point, color=None, size=5):
        """Dibuja un punto"""
        if color is None:
            category = point.attributes.get('category', 'Store')
            color = CATEGORY_COLORS.get(category, BLACK)
        
        screen_pos = self.world_to_screen(point.x, point.y)
        pygame.draw.circle(self.screen, color, screen_pos, size)
        pygame.draw.circle(self.screen, BLACK, screen_pos, size, 1)
    
    def draw_ui(self):
        """Dibuja la interfaz de usuario"""
        # Panel derecho
        panel_x = self.vis_width + self.offset_x + 20
        y = 50
        
        # Título
        title = self.font.render("QuadTree Visualizer", True, BLACK)
        self.screen.blit(title, (panel_x, y))
        y += 40
        
        # Modos
        modes_text = [
            "Modos de Operación:",
            "1: Insertar Puntos",
            "2: Consulta de Rango",
            "3: Vecino Más Cercano",
            "4: Filtrar por Categoría",
            "C: Limpiar",
            "R: Generar Aleatorios",
            "ESC: Salir"
        ]
        
        for text in modes_text:
            if text == "Modos de Operación:":
                surface = self.font.render(text, True, BLACK)
            else:
                surface = self.small_font.render(text, True, BLACK)
            self.screen.blit(surface, (panel_x, y))
            y += 25
        
        y += 20
        
        # Modo actual
        mode_text = f"Modo Actual: {self.mode.upper()}"
        mode_surface = self.font.render(mode_text, True, BLUE)
        self.screen.blit(mode_surface, (panel_x, y))
        y += 35
        
        # Estadísticas
        stats_text = [
            f"Total Puntos: {self.quadtree.count_points()}",
        ]
        
        if self.mode == "range_query" and self.range_rect:
            points_in_range = len(self.quadtree.query_range(self.range_rect))
            stats_text.append(f"En Rango: {points_in_range}")
        
        if self.mode == "filter" and self.selected_category:
            count = self.quadtree.count_by_attribute('category', self.selected_category)
            stats_text.append(f"Filtrados: {count}")
        
        for text in stats_text:
            surface = self.small_font.render(text, True, BLACK)
            self.screen.blit(surface, (panel_x, y))
            y += 25
        
        y += 20
        
        # Leyenda de categorías
        legend_title = self.font.render("Categorías:", True, BLACK)
        self.screen.blit(legend_title, (panel_x, y))
        y += 30
        
        for category, color in CATEGORY_COLORS.items():
            pygame.draw.circle(self.screen, color, (panel_x + 10, y + 8), 6)
            pygame.draw.circle(self.screen, BLACK, (panel_x + 10, y + 8), 6, 1)
            text = self.small_font.render(category, True, BLACK)
            self.screen.blit(text, (panel_x + 25, y))
            y += 25
        
        # Si estamos en modo filtro, mostrar controles
        if self.mode == "filter":
            y += 20
            filter_text = "Click categoría para filtrar:"
            surface = self.small_font.render(filter_text, True, RED)
            self.screen.blit(surface, (panel_x, y))
    
    def handle_insert(self, world_x, world_y):
        """Maneja la inserción de un punto"""
        if 0 <= world_x <= self.vis_width and 0 <= world_y <= self.vis_height:
            category = random.choice(CATEGORIES)
            point = Point(world_x, world_y, 
                         {'category': category, 'id': random.randint(1000, 9999)})
            self.quadtree.insert(point)
    
    def handle_range_query_start(self, world_x, world_y):
        """Inicia la selección de rango"""
        if 0 <= world_x <= self.vis_width and 0 <= world_y <= self.vis_height:
            self.range_start = (world_x, world_y)
    
    def handle_range_query_drag(self, world_x, world_y):
        """Actualiza el rectángulo de rango mientras se arrastra"""
        if self.range_start:
            x1, y1 = self.range_start
            width = abs(world_x - x1)
            height = abs(world_y - y1)
            center_x = (x1 + world_x) / 2
            center_y = (y1 + world_y) / 2
            self.range_rect = Rectangle(center_x, center_y, width, height)
    
    def handle_nearest_neighbor(self, world_x, world_y):
        """Busca el vecino más cercano"""
        if 0 <= world_x <= self.vis_width and 0 <= world_y <= self.vis_height:
            self.query_point = Point(world_x, world_y)
            self.nearest_point = self.quadtree.nearest_neighbor(self.query_point)
    
    def handle_filter_click(self, screen_x, screen_y):
        """Maneja el click para filtrar por categoría"""
        panel_x = self.vis_width + self.offset_x + 20
        y = 330  # Posición aproximada donde empieza la leyenda
        
        for i, category in enumerate(CATEGORY_COLORS.keys()):
            circle_y = y + 30 + (i * 25) + 8
            if (panel_x + 10 - 10 <= screen_x <= panel_x + 10 + 10 and
                circle_y - 10 <= screen_y <= circle_y + 10):
                self.selected_category = category
                self.filtered_points = self.quadtree.filter_by_attribute('category', category)
                return
    
    def run(self):
        """Loop principal de la aplicación"""
        running = True
        mouse_pressed = False
        
        while running:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_1:
                        self.mode = "insert"
                        self.reset_selections()
                    elif event.key == pygame.K_2:
                        self.mode = "range_query"
                        self.reset_selections()
                    elif event.key == pygame.K_3:
                        self.mode = "nearest_neighbor"
                        self.reset_selections()
                    elif event.key == pygame.K_4:
                        self.mode = "filter"
                        self.reset_selections()
                    elif event.key == pygame.K_c:
                        self.clear_tree()
                    elif event.key == pygame.K_r:
                        self.clear_tree()
                        self.generate_random_points(30)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pressed = True
                    x, y = pygame.mouse.get_pos()
                    world_x, world_y = self.screen_to_world(x, y)
                    
                    if self.mode == "insert":
                        self.handle_insert(world_x, world_y)
                    elif self.mode == "range_query":
                        self.handle_range_query_start(world_x, world_y)
                    elif self.mode == "nearest_neighbor":
                        self.handle_nearest_neighbor(world_x, world_y)
                    elif self.mode == "filter":
                        self.handle_filter_click(x, y)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pressed = False
                    if self.mode == "range_query":
                        self.range_start = None
                
                elif event.type == pygame.MOUSEMOTION:
                    if mouse_pressed and self.mode == "range_query" and self.range_start:
                        x, y = pygame.mouse.get_pos()
                        world_x, world_y = self.screen_to_world(x, y)
                        self.handle_range_query_drag(world_x, world_y)
            
            # Dibujar
            self.screen.fill(WHITE)
            
            # Dibujar QuadTree
            self.draw_quadtree_node(self.quadtree.root)
            
            # Dibujar puntos
            all_points = self.quadtree.get_all_points()
            for point in all_points:
                self.draw_point(point)
            
            # Dibujar elementos específicos del modo
            if self.mode == "range_query" and self.range_rect:
                self.draw_rectangle(self.range_rect, BLUE, 2)
                points_in_range = self.quadtree.query_range(self.range_rect)
                for point in points_in_range:
                    self.draw_point(point, YELLOW, 7)
            
            if self.mode == "nearest_neighbor" and self.query_point:
                self.draw_point(self.query_point, RED, 8)
                if self.nearest_point:
                    self.draw_point(self.nearest_point, GREEN, 8)
                    # Dibujar línea entre query y nearest
                    start_pos = self.world_to_screen(self.query_point.x, self.query_point.y)
                    end_pos = self.world_to_screen(self.nearest_point.x, self.nearest_point.y)
                    pygame.draw.line(self.screen, GREEN, start_pos, end_pos, 2)
            
            if self.mode == "filter" and self.filtered_points:
                for point in self.filtered_points:
                    self.draw_point(point, CYAN, 7)
            
            # Dibujar UI
            self.draw_ui()
            
            pygame.display.flip()
        
        pygame.quit()
    
    def reset_selections(self):
        """Resetea las selecciones del modo anterior"""
        self.range_start = None
        self.range_rect = None
        self.query_point = None
        self.nearest_point = None
        self.filtered_points = []
        self.selected_category = None
    
    def clear_tree(self):
        """Limpia el QuadTree"""
        boundary = Rectangle(self.vis_width/2, self.vis_height/2, 
                           self.vis_width, self.vis_height)
        self.quadtree = QuadTree(boundary, capacity=4)
        self.reset_selections()


if __name__ == "__main__":
    visualizer = QuadTreeVisualizer()
    visualizer.run()


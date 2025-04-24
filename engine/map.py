"""
Map class for DOOM recreation
"""
import os
import math
import numpy as np

class Map:
    """Map class that handles level data and collision detection"""
    
    def __init__(self, level_num):
        """Initialize the map with a specific level"""
        self.level_num = level_num
        
        # Load the map data
        self.load_map()
        
        # Map properties
        self.wall_height = 1.0
        
        # Textures and colors for different wall types
        self.wall_textures = {
            1: "wall1",  # Regular wall
            2: "wall2",  # Different wall type
            3: "door",   # Door
            # More wall types will be added
        }
    
    def load_map(self):
        """Load map data from file"""
        map_file = f"assets/maps/e1m{self.level_num}.txt"
        
        try:
            with open(map_file, 'r') as f:
                lines = f.readlines()
            
            # Parse map data
            map_data = []
            enemy_spawns = []
            item_spawns = []
            
            # Parse the file
            section = None
            for line in lines:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Check for section markers
                if line == "MAP":
                    section = "map"
                    continue
                elif line == "END_MAP":
                    section = None
                    continue
                elif line == "ENEMIES":
                    section = "enemies"
                    continue
                elif line == "END_ENEMIES":
                    section = None
                    continue
                elif line == "ITEMS":
                    section = "items"
                    continue
                elif line == "END_ITEMS":
                    section = None
                    continue
                
                # Parse data based on current section
                if section == "map":
                    # Convert characters to integers
                    row = []
                    for char in line:
                        if char == '1':
                            row.append(1)  # Wall
                        elif char == '2':
                            row.append(2)  # Different wall type
                        elif char == '3':
                            row.append(3)  # Door
                        elif char == '0':
                            row.append(0)  # Empty space
                        elif char == 'P':
                            row.append(0)  # Player start (empty space)
                            self.player_start = (len(map_data), len(row) - 1)
                        elif char in ['E', 'I']:
                            row.append(0)  # Enemy or item (empty space)
                    
                    if row:
                        map_data.append(row)
                
                elif section == "enemies":
                    # Parse enemy spawn data
                    parts = line.split(',')
                    if len(parts) == 3:
                        enemy_type = parts[0].strip()
                        x = int(parts[1].strip())
                        y = int(parts[2].strip())
                        enemy_spawns.append({"type": enemy_type, "x": x, "y": y})
                
                elif section == "items":
                    # Parse item spawn data
                    parts = line.split(',')
                    if len(parts) == 3:
                        item_type = parts[0].strip()
                        x = int(parts[1].strip())
                        y = int(parts[2].strip())
                        item_spawns.append({"type": item_type, "x": x, "y": y})
            
            # Convert map data to numpy array
            self.data = np.array(map_data)
            
            # Map dimensions
            self.width = self.data.shape[1]
            self.height = self.data.shape[0]
            
            # Store enemy and item spawns
            self.enemy_spawns = enemy_spawns
            self.item_spawns = item_spawns
            
            # Initialize enemy manager
            from engine.enemy import EnemyManager
            self.enemy_manager = EnemyManager(self)
            
            print(f"Map loaded: {map_file}")
            print(f"Map dimensions: {self.width}x{self.height}")
            print(f"Enemy spawns: {len(self.enemy_spawns)}")
            print(f"Item spawns: {len(self.item_spawns)}")
        
        except Exception as e:
            print(f"Error loading map: {e}")
            # Fallback to a simple test map
            self.data = np.array([
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 1, 0, 1, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ])
            
            # Map dimensions
            self.width = self.data.shape[1]
            self.height = self.data.shape[0]
            
            # Default spawns
            self.enemy_spawns = [
                {"type": "imp", "x": 5, "y": 5},
                {"type": "demon", "x": 7, "y": 3}
            ]
            
            self.item_spawns = [
                {"type": "health", "x": 2, "y": 2},
                {"type": "ammo", "x": 8, "y": 8}
            ]
            
            # Initialize enemy manager
            from engine.enemy import EnemyManager
            self.enemy_manager = EnemyManager(self)
    
    def is_wall(self, x, y):
        """Check if the given coordinates contain a wall"""
        # Make sure coordinates are within map bounds
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True  # Treat out-of-bounds as walls
        
        # Check if the cell contains a wall
        return self.data[int(y)][int(x)] != 0
    
    def get_wall_type(self, x, y):
        """Get the type of wall at the given coordinates"""
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return 1  # Default wall type for out-of-bounds
        
        return self.data[int(y)][int(x)]
    
    def get_spawn_points(self, spawn_type):
        """Get spawn points for enemies or items"""
        if spawn_type == "enemy":
            return self.enemy_spawns
        elif spawn_type == "item":
            return self.item_spawns
        return []
    
    def save_map(self):
        """Save the current map to a file (for editor functionality)"""
        # This will be implemented later if we add a map editor
        pass
    
    def cast_ray_entities(self, x, y, angle, max_distance, player):
        """Cast a ray and check for entity hits (for weapon hit detection)"""
        # Direction vector
        dx = math.cos(angle)
        dy = math.sin(angle)
        
        # Step along the ray
        step_size = 0.1
        distance = 0
        
        # Keep track of what we hit
        hit = False
        hit_entity = None
        
        while not hit and distance < max_distance:
            # Calculate current position
            current_x = x + dx * distance
            current_y = y + dy * distance
            
            # Check for wall hit
            if self.is_wall(int(current_x), int(current_y)):
                hit = True
                break
            
            # Check for entity hits
            if hasattr(self, 'enemy_manager'):
                for enemy in self.enemy_manager.enemies:
                    # Skip dead enemies
                    if enemy.state == "death":
                        continue
                    
                    # Calculate distance to enemy
                    enemy_dx = enemy.x - current_x
                    enemy_dy = enemy.y - current_y
                    enemy_dist = math.sqrt(enemy_dx*enemy_dx + enemy_dy*enemy_dy)
                    
                    # Check if we hit the enemy (using a simple radius check)
                    if enemy_dist < 0.5:  # Enemy collision radius
                        hit = True
                        hit_entity = enemy
                        break
            
            # Increment distance
            distance += step_size
            
            # If we hit an entity, break out of the loop
            if hit_entity:
                break
        
        return hit, distance, hit_entity

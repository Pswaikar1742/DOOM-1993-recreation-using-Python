"""
Raycasting engine for DOOM recreation
"""
import math
import pygame
import numpy as np

class Raycaster:
    """Raycaster class that handles 3D rendering using raycasting technique"""
    
    def __init__(self, map_obj):
        """Initialize the raycaster"""
        self.map = map_obj
        
        # Raycasting parameters
        self.fov = math.pi / 3  # 60 degrees field of view
        self.half_fov = self.fov / 2
        self.num_rays = 320  # Number of rays to cast
        self.max_depth = 20  # Maximum ray distance
        
        # Precalculated values for optimization
        self.wall_strip_width = 0  # Will be calculated in render
        
        # Colors
        self.colors = {
            1: (200, 0, 0),    # Red walls
            2: (0, 200, 0),    # Green walls
            3: (0, 0, 200),    # Blue walls
            4: (200, 200, 0),  # Yellow walls
        }
        
        # Textures
        self.textures = {}
        
        # Sprite rendering
        self.sprites = []
    
    def load_textures(self, texture_dict):
        """Load wall textures"""
        self.textures = texture_dict
    
    def cast_ray(self, angle, player_x, player_y):
        """Cast a single ray and return distance to wall and wall type"""
        # Normalize angle
        angle = angle % (2 * math.pi)
        
        # Ray direction
        ray_dir_x = math.cos(angle)
        ray_dir_y = math.sin(angle)
        
        # Current map cell
        map_x = int(player_x)
        map_y = int(player_y)
        
        # Length of ray from current position to next x or y-side
        # Prevent division by zero
        if abs(ray_dir_x) < 0.0001:
            delta_dist_x = float('inf')
        else:
            delta_dist_x = abs(1 / ray_dir_x)
            
        if abs(ray_dir_y) < 0.0001:
            delta_dist_y = float('inf')
        else:
            delta_dist_y = abs(1 / ray_dir_y)
        
        # Direction to step in x or y direction (either +1 or -1)
        step_x = 1 if ray_dir_x >= 0 else -1
        step_y = 1 if ray_dir_y >= 0 else -1
        
        # Length of ray from one side to next in map
        if ray_dir_x < 0:
            side_dist_x = (player_x - map_x) * delta_dist_x
        else:
            side_dist_x = (map_x + 1.0 - player_x) * delta_dist_x
        
        if ray_dir_y < 0:
            side_dist_y = (player_y - map_y) * delta_dist_y
        else:
            side_dist_y = (map_y + 1.0 - player_y) * delta_dist_y
        
        # Perform DDA (Digital Differential Analysis)
        hit = False
        side = 0  # 0 for x-side, 1 for y-side
        wall_type = 0
        
        while not hit and (abs(map_x - player_x) < self.max_depth or abs(map_y - player_y) < self.max_depth):
            # Jump to next map square
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1
            
            # Check if ray has hit a wall
            if self.map.is_wall(map_x, map_y):
                hit = True
                wall_type = self.map.get_wall_type(map_x, map_y)
        
        # Calculate distance projected on camera direction
        # Prevent division by zero
        if side == 0:
            if abs(ray_dir_x) < 0.0001:
                perp_wall_dist = self.max_depth  # Fallback to max depth
            else:
                perp_wall_dist = (map_x - player_x + (1 - step_x) / 2) / ray_dir_x
        else:
            if abs(ray_dir_y) < 0.0001:
                perp_wall_dist = self.max_depth  # Fallback to max depth
            else:
                perp_wall_dist = (map_y - player_y + (1 - step_y) / 2) / ray_dir_y
        
        # Return the distance and wall type
        return perp_wall_dist, wall_type, side
    
    def render(self, screen, player):
        """Render the 3D view using raycasting"""
        # Screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculate wall strip width
        self.wall_strip_width = screen_width / self.num_rays
        
        # Clear the screen with a ceiling and floor
        # Sky/ceiling color
        pygame.draw.rect(screen, (0, 0, 100), 
                         (0, 0, screen_width, screen_height // 2))
        # Floor color
        pygame.draw.rect(screen, (50, 50, 50), 
                         (0, screen_height // 2, screen_width, screen_height // 2))
        
        # Cast rays
        for i in range(self.num_rays):
            # Calculate ray angle
            ray_angle = player.angle - self.half_fov + (i / self.num_rays) * self.fov
            
            # Cast the ray
            distance, wall_type, side = self.cast_ray(ray_angle, player.x, player.y)
            
            # Correct for fisheye effect
            distance = distance * math.cos(player.angle - ray_angle)
            
            # Prevent division by zero
            if distance < 0.0001:
                distance = 0.0001
            
            # Calculate wall height
            wall_height = min(int(screen_height / distance), screen_height)
            
            # Calculate wall top and bottom
            wall_top = (screen_height - wall_height) // 2
            wall_bottom = wall_top + wall_height
            
            # Get wall texture based on type
            texture_name = self.map.wall_textures.get(wall_type, "wall1")
            texture = self.textures.get(texture_name)
            
            if texture:
                # Calculate texture x coordinate
                # Determine where exactly the wall was hit
                if side == 0:
                    wall_x = player.y + distance * math.sin(ray_angle)
                else:
                    wall_x = player.x + distance * math.cos(ray_angle)
                wall_x -= math.floor(wall_x)
                
                # Calculate texture x coordinate
                tex_x = int(wall_x * texture.get_width())
                if (side == 0 and math.cos(ray_angle) > 0) or (side == 1 and math.sin(ray_angle) < 0):
                    tex_x = texture.get_width() - tex_x - 1
                
                # Draw textured wall strip
                if wall_height < screen_height:
                    # Normal case - wall doesn't fill the screen height
                    wall_slice = pygame.Surface((1, wall_height))
                    for y in range(wall_height):
                        # Calculate texture y coordinate
                        tex_y = int(y * texture.get_height() / wall_height)
                        # Get pixel color from texture
                        color = texture.get_at((tex_x, tex_y))
                        # Darken for y-side walls
                        if side == 1:
                            color = (color[0] // 2, color[1] // 2, color[2] // 2)
                        # Draw pixel
                        wall_slice.set_at((0, y), color)
                    
                    # Scale and blit the wall slice
                    scaled_slice = pygame.transform.scale(wall_slice, (int(self.wall_strip_width) + 1, wall_height))
                    screen.blit(scaled_slice, (i * self.wall_strip_width, wall_top))
                else:
                    # Wall fills more than screen height - need to clip
                    visible_height = screen_height
                    tex_start = (wall_height - visible_height) / 2 / wall_height * texture.get_height()
                    tex_end = (wall_height + visible_height) / 2 / wall_height * texture.get_height()
                    
                    wall_slice = pygame.Surface((1, visible_height))
                    for y in range(visible_height):
                        # Calculate texture y coordinate
                        tex_y = int(tex_start + (tex_end - tex_start) * y / visible_height)
                        if tex_y >= texture.get_height():
                            tex_y = texture.get_height() - 1
                        # Get pixel color from texture
                        color = texture.get_at((tex_x, tex_y))
                        # Darken for y-side walls
                        if side == 1:
                            color = (color[0] // 2, color[1] // 2, color[2] // 2)
                        # Draw pixel
                        wall_slice.set_at((0, y), color)
                    
                    # Scale and blit the wall slice
                    scaled_slice = pygame.transform.scale(wall_slice, (int(self.wall_strip_width) + 1, visible_height))
                    screen.blit(scaled_slice, (i * self.wall_strip_width, 0))
            else:
                # Fallback to colored walls if texture not found
                # Get wall color based on type and side
                color = self.colors.get(wall_type, (150, 150, 150))
                
                # Darken the color for y-side walls to create a shadow effect
                if side == 1:
                    color = (color[0] // 2, color[1] // 2, color[2] // 2)
                
                # Draw the wall strip
                pygame.draw.line(screen, color, 
                                (i * self.wall_strip_width, wall_top), 
                                (i * self.wall_strip_width, wall_bottom), 
                                int(self.wall_strip_width) + 1)
        
        # Render sprites (enemies, items, etc.)
        self.render_sprites(screen, player)
    
    def render_sprites(self, screen, player):
        """Render sprites (enemies, items, etc.)"""
        # Get screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Get all sprites to render (enemies, items, etc.)
        sprites = []
        
        # Add enemies
        if hasattr(self.map, 'enemy_manager') and self.map.enemy_manager:
            for enemy in self.map.enemy_manager.enemies:
                # Skip dead enemies that have finished their death animation
                if enemy.state == "death" and enemy.sprite_index >= len(enemy.sprites.get("death", [])) - 1:
                    continue
                
                # Calculate sprite distance from player
                dx = enemy.x - player.x
                dy = enemy.y - player.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Skip sprites that are too far away
                if distance > self.max_depth:
                    continue
                
                # Calculate sprite angle relative to player's view direction
                sprite_angle = math.atan2(dy, dx) - player.angle
                
                # Normalize angle to be between -π and π
                while sprite_angle < -math.pi:
                    sprite_angle += 2 * math.pi
                while sprite_angle > math.pi:
                    sprite_angle += -2 * math.pi
                
                # Skip sprites outside the field of view
                if abs(sprite_angle) > self.half_fov + 0.2:  # Add a small margin
                    continue
                
                # Add sprite to the list
                sprites.append({
                    'x': enemy.x,
                    'y': enemy.y,
                    'distance': distance,
                    'angle': sprite_angle,
                    'type': 'enemy',
                    'entity': enemy
                })
        
        # Add items to render
        if hasattr(self.map, 'item_spawns'):
            for item in self.map.item_spawns:
                # Calculate item distance from player
                dx = item["x"] - player.x
                dy = item["y"] - player.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Skip items that are too far away
                if distance > self.max_depth:
                    continue
                
                # Calculate item angle relative to player's view direction
                item_angle = math.atan2(dy, dx) - player.angle
                
                # Normalize angle to be between -π and π
                while item_angle < -math.pi:
                    item_angle += 2 * math.pi
                while item_angle > math.pi:
                    item_angle += -2 * math.pi
                
                # Skip items outside the field of view
                if abs(item_angle) > self.half_fov + 0.2:  # Add a small margin
                    continue
                
                # Add item to the list
                sprites.append({
                    'x': item["x"],
                    'y': item["y"],
                    'distance': distance,
                    'angle': item_angle,
                    'type': 'item',
                    'item_type': item["type"]
                })
        
        # Sort sprites by distance (furthest first for correct rendering)
        sprites.sort(key=lambda s: s['distance'], reverse=True)
        
        # Render sprites
        for sprite in sprites:
            # Calculate sprite screen position
            sprite_x = (sprite['angle'] / self.fov + 0.5) * screen_width
            
            # Prevent division by zero
            if sprite['distance'] < 0.0001:
                sprite['distance'] = 0.0001
                
            # Calculate sprite height based on distance
            sprite_height = min(int(screen_height / sprite['distance']), screen_height)
            sprite_width = sprite_height  # Assuming square sprites for now
            
            # Calculate sprite top and bottom
            sprite_top = (screen_height - sprite_height) // 2
            
            if sprite['type'] == 'enemy':
                enemy = sprite['entity']
                
                # Get the appropriate sprite texture based on enemy state and type
                sprite_name = enemy.get_sprite()
                sprite_texture = None
                
                if sprite_name and sprite_name in self.textures:
                    sprite_texture = self.textures[sprite_name]
                
                if sprite_texture:
                    # Scale the sprite texture to the appropriate size
                    scaled_sprite = pygame.transform.scale(sprite_texture, (sprite_width, sprite_height))
                    
                    # Apply distance-based darkening
                    if sprite['distance'] > 5:
                        darkness = min(100, int(sprite['distance'] * 10))
                        dark_overlay = pygame.Surface((sprite_width, sprite_height))
                        dark_overlay.fill((0, 0, 0))
                        dark_overlay.set_alpha(darkness)
                        scaled_sprite.blit(dark_overlay, (0, 0))
                    
                    # Draw the sprite
                    screen.blit(scaled_sprite, (sprite_x - sprite_width // 2, sprite_top))
                else:
                    # Fallback to colored rectangle if texture not found
                    sprite_color = (255, 0, 0)  # Red for enemies
                    
                    # Different colors based on enemy type
                    if enemy.type == "imp":
                        sprite_color = (255, 100, 0)  # Orange
                    elif enemy.type == "demon":
                        sprite_color = (255, 0, 0)  # Red
                    elif enemy.type == "cacodemon":
                        sprite_color = (255, 0, 255)  # Purple
                    
                    # Draw the sprite
                    pygame.draw.rect(screen, sprite_color, 
                                    (sprite_x - sprite_width // 2, sprite_top, 
                                     sprite_width, sprite_height))
                    
                    # Draw a border
                    pygame.draw.rect(screen, (0, 0, 0), 
                                    (sprite_x - sprite_width // 2, sprite_top, 
                                     sprite_width, sprite_height), 2)
            
            elif sprite['type'] == 'item':
                # Get the appropriate item texture
                item_type = sprite['item_type']
                item_texture = None
                
                if item_type in self.textures:
                    item_texture = self.textures[item_type]
                
                if item_texture:
                    # Scale the item texture to the appropriate size
                    scaled_item = pygame.transform.scale(item_texture, (sprite_width, sprite_height))
                    
                    # Apply distance-based darkening
                    if sprite['distance'] > 5:
                        darkness = min(100, int(sprite['distance'] * 10))
                        dark_overlay = pygame.Surface((sprite_width, sprite_height))
                        dark_overlay.fill((0, 0, 0))
                        dark_overlay.set_alpha(darkness)
                        scaled_item.blit(dark_overlay, (0, 0))
                    
                    # Draw the item with a bobbing effect
                    bob_offset = int(math.sin(pygame.time.get_ticks() * 0.005) * 5)
                    screen.blit(scaled_item, (sprite_x - sprite_width // 2, sprite_top + bob_offset))
                else:
                    # Fallback to colored rectangle if texture not found
                    item_color = (0, 255, 0)  # Green for items
                    
                    # Different colors based on item type
                    if item_type == "health":
                        item_color = (0, 255, 0)  # Green
                    elif item_type == "armor":
                        item_color = (0, 0, 255)  # Blue
                    elif item_type == "ammo":
                        item_color = (255, 255, 0)  # Yellow
                    
                    # Draw the item with a bobbing effect
                    bob_offset = int(math.sin(pygame.time.get_ticks() * 0.005) * 5)
                    pygame.draw.rect(screen, item_color, 
                                    (sprite_x - sprite_width // 2, sprite_top + bob_offset, 
                                     sprite_width, sprite_height))

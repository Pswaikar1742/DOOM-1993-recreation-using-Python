# Raycasting Algorithm Explained

This document provides a detailed explanation of the raycasting algorithm used in the DOOM Python Recreation project. Raycasting is the core rendering technique that creates the pseudo-3D effect in the game.

## Table of Contents

1. [Introduction to Raycasting](#introduction-to-raycasting)
2. [Basic Principles](#basic-principles)
3. [The Algorithm Step by Step](#the-algorithm-step-by-step)
4. [Digital Differential Analysis (DDA)](#digital-differential-analysis-dda)
5. [Wall Rendering](#wall-rendering)
6. [Texture Mapping](#texture-mapping)
7. [Sprite Rendering](#sprite-rendering)
8. [Optimizations](#optimizations)
9. [Limitations and Solutions](#limitations-and-solutions)
10. [Code Implementation](#code-implementation)

## Introduction to Raycasting

Raycasting is a rendering technique that creates a 3D perspective from a 2D map. Unlike full 3D rendering, raycasting is computationally efficient while still providing an immersive 3D-like experience. This technique was popularized by games like Wolfenstein 3D and DOOM in the early 1990s.

The basic idea is to cast rays from the player's viewpoint and calculate where they intersect with walls. The distance to these intersections determines how tall walls appear on screen, creating the illusion of depth.

## Basic Principles

Raycasting relies on several key principles:

1. **Player's View**: The player has a position (x, y) and a viewing direction (angle).
2. **Field of View (FOV)**: The player can see a certain angle to the left and right of their viewing direction.
3. **Ray Casting**: For each vertical strip of the screen, a ray is cast from the player's position in the appropriate direction.
4. **Wall Detection**: The algorithm determines where each ray intersects with a wall.
5. **Distance Calculation**: The perpendicular distance to the wall is calculated to avoid the "fisheye" effect.
6. **Wall Height**: The height of the wall on screen is inversely proportional to the distance (farther walls appear shorter).

## The Algorithm Step by Step

Here's how the raycasting algorithm works in our implementation:

1. **For each vertical strip of the screen**:
   - Calculate the ray angle based on the player's viewing direction and the current strip's position relative to the center of the screen.
   - Cast a ray from the player's position in that direction.
   - Find where the ray intersects with a wall using the DDA algorithm.
   - Calculate the perpendicular distance to the wall to avoid the fisheye effect.
   - Determine the height of the wall strip based on this distance.
   - Apply texture mapping to the wall strip.
   - Render the wall strip on screen.

2. **After rendering all wall strips**:
   - Sort sprites (enemies, items) by distance from the player.
   - Render sprites from farthest to nearest to handle occlusion correctly.

## Digital Differential Analysis (DDA)

The DDA algorithm is an efficient way to find where a ray intersects with a wall in a grid-based map. Here's how it works:

1. Calculate the ray direction vector based on the ray angle.
2. Determine which map square the player is in.
3. Calculate the distance the ray has to travel to cross a vertical or horizontal grid line.
4. Step through the grid by moving to the next x or y grid line, whichever is closer.
5. Check if the new grid cell contains a wall.
6. If a wall is found, calculate the exact intersection point and distance.

```python
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
    
    # Calculate initial side_dist
    if ray_dir_x < 0:
        side_dist_x = (player_x - map_x) * delta_dist_x
    else:
        side_dist_x = (map_x + 1.0 - player_x) * delta_dist_x
    
    if ray_dir_y < 0:
        side_dist_y = (player_y - map_y) * delta_dist_y
    else:
        side_dist_y = (map_y + 1.0 - player_y) * delta_dist_y
    
    # Perform DDA
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
    if side == 0:
        perp_wall_dist = (map_x - player_x + (1 - step_x) / 2) / ray_dir_x
    else:
        perp_wall_dist = (map_y - player_y + (1 - step_y) / 2) / ray_dir_y
    
    # Return the distance and wall type
    return perp_wall_dist, wall_type, side
```

## Wall Rendering

Once we know the distance to a wall, we can calculate how tall it should appear on screen:

1. The wall height is inversely proportional to the distance: `wall_height = screen_height / distance`
2. The wall is centered vertically on the screen: `wall_top = (screen_height - wall_height) / 2`
3. The wall strip is drawn from `wall_top` to `wall_top + wall_height`

```python
# Calculate wall height
wall_height = min(int(screen_height / distance), screen_height)

# Calculate wall top and bottom
wall_top = (screen_height - wall_height) // 2
wall_bottom = wall_top + wall_height
```

## Texture Mapping

To make walls look more realistic, we apply textures to them:

1. Determine which texture to use based on the wall type.
2. Calculate the exact position where the ray hit the wall.
3. Use this position to determine which column of the texture to sample.
4. Scale the texture column to the height of the wall strip.
5. Apply shading based on distance and whether the wall is horizontal or vertical.

```python
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
```

## Sprite Rendering

After rendering the walls, we render sprites (enemies, items) using a similar technique:

1. Calculate the sprite's position relative to the player.
2. Determine if the sprite is within the player's field of view.
3. Calculate the sprite's distance from the player.
4. Calculate the sprite's size on screen based on distance.
5. Render the sprite at the appropriate position and size.

```python
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
    # ...
    
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
        
        # Render the appropriate sprite based on type
        # ...
```

## Optimizations

Several optimizations are implemented to improve performance:

1. **Distance Culling**: Objects beyond a certain distance are not rendered.
2. **Sprite Sorting**: Sprites are sorted by distance to ensure correct rendering order.
3. **Texture Caching**: Textures are loaded once and reused.
4. **Clipping**: Wall strips that would be off-screen are not rendered.
5. **Precalculated Values**: Some values are precalculated to avoid redundant calculations.

## Limitations and Solutions

Raycasting has some inherent limitations:

1. **No Vertical Looking**: Traditional raycasting doesn't support looking up or down.
   - Solution: We could implement vertical offset for the horizon line to simulate looking up/down.

2. **Limited Geometry**: Only vertical walls are supported.
   - Solution: For more complex geometry, we would need to implement a more sophisticated rendering technique.

3. **No Ceiling/Floor Textures**: Traditional raycasting only textures walls.
   - Solution: We could implement floor/ceiling casting for more realistic environments.

4. **Z-Fighting**: When sprites are at the same distance, they can flicker.
   - Solution: We add a small bias to sprite distances based on their type.

## Code Implementation

The raycasting implementation is contained in the `engine/raycasting.py` file. The main components are:

1. **Raycaster Class**: Manages the raycasting process and rendering.
2. **cast_ray Method**: Implements the DDA algorithm to find wall intersections.
3. **render Method**: Renders the 3D view by casting rays for each screen column.
4. **render_sprites Method**: Renders sprites in the 3D view.

The implementation balances performance and visual quality, making it suitable for real-time rendering on modern hardware while maintaining the classic DOOM aesthetic.

## Conclusion

Raycasting is a powerful technique that allows us to create a convincing 3D environment from a 2D map. While it has limitations compared to modern 3D rendering techniques, it provides an efficient way to recreate the classic DOOM experience while maintaining good performance.

The implementation in this project demonstrates how raycasting can be used to create an immersive game environment with textured walls, sprites, and lighting effects, all while maintaining the nostalgic feel of the original DOOM game.

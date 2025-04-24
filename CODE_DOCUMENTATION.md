# DOOM Python Recreation - Code Documentation

This document provides a detailed explanation of the codebase for the DOOM Python Recreation project. It covers the architecture, key components, and how they work together to recreate the classic DOOM gameplay experience using Python and Pygame.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Engine Components](#engine-components)
   - [Game Loop](#game-loop)
   - [Raycasting Engine](#raycasting-engine)
   - [Player System](#player-system)
   - [Enemy System](#enemy-system)
   - [Weapon System](#weapon-system)
   - [Map System](#map-system)
   - [Controller Support](#controller-support)
4. [UI Components](#ui-components)
   - [HUD (Heads-Up Display)](#hud-heads-up-display)
   - [Menu System](#menu-system)
5. [Asset Management](#asset-management)
6. [Map Format](#map-format)
7. [Implementation Details](#implementation-details)
8. [Performance Considerations](#performance-considerations)

## Project Overview

This project is a recreation of the classic DOOM (1993) game using Python and modern libraries. It implements core features of the original game including:

- Raycasting engine for pseudo-3D rendering
- Player movement and combat
- Enemy AI with different enemy types
- Weapon system with multiple weapons
- Level loading from map files
- HUD and menu systems
- Xbox controller support

The project uses Pygame for rendering and input handling, NumPy for efficient numerical operations, and the Inputs library for controller support.

## Architecture

The project follows a modular architecture with clear separation of concerns:

```
doom/
├── main.py                # Entry point
├── run.py                 # Setup and launcher
├── requirements.txt       # Dependencies
├── assets/                # Game assets
│   ├── images/            # Textures and sprites
│   ├── sounds/            # Sound effects
│   └── maps/              # Level definitions
├── engine/                # Game engine components
│   ├── __init__.py
│   ├── game.py            # Main game class
│   ├── player.py          # Player logic
│   ├── enemy.py           # Enemy AI
│   ├── entity.py          # Base entity class
│   ├── map.py             # Map loading and collision
│   ├── raycasting.py      # 3D rendering
│   ├── weapon.py          # Weapon mechanics
│   └── controller.py      # Controller support
└── ui/                    # User interface
    ├── __init__.py
    ├── hud.py             # Heads-up display
    └── menu.py            # Game menus
```

The architecture follows these key principles:

1. **Component-based design**: Each major system is encapsulated in its own module
2. **Separation of rendering and logic**: Game state is updated separately from rendering
3. **Entity-based architecture**: Game objects inherit from a common Entity base class
4. **Event-driven input handling**: Input is processed through events

## Engine Components

### Game Loop

The main game loop is implemented in `engine/game.py` and follows the standard pattern:

1. Process input events
2. Update game state
3. Render the frame
4. Maintain frame rate

```python
def run(self):
    """Main game loop"""
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    
    last_time = time.time()
    
    while self.running:
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
        self.handle_events()
        self.update(dt)
        self.render()
        self.clock.tick(self.fps)
```

The game uses delta time (`dt`) to ensure consistent gameplay speed regardless of frame rate.

### Raycasting Engine

The raycasting engine in `engine/raycasting.py` is the core of the 3D rendering system. It uses the Digital Differential Analysis (DDA) algorithm to efficiently cast rays and determine wall distances.

Key features of the raycasting engine:

- Field of view (FOV) control
- Texture mapping for walls
- Fisheye correction
- Distance-based shading
- Sprite rendering for enemies and items

The raycasting process:

1. For each vertical strip of the screen, cast a ray from the player's position
2. Use DDA to find the distance to the nearest wall
3. Calculate the height of the wall based on the distance
4. Apply textures to the wall slice
5. Render sprites (enemies, items) based on distance from the player

```python
def cast_ray(self, angle, player_x, player_y):
    """Cast a single ray and return distance to wall and wall type"""
    # Normalize angle
    angle = angle % (2 * math.pi)
    
    # Ray direction
    ray_dir_x = math.cos(angle)
    ray_dir_y = math.sin(angle)
    
    # DDA algorithm implementation...
    
    # Return the distance and wall type
    return perp_wall_dist, wall_type, side
```

### Player System

The player system in `engine/player.py` handles:

- Movement and collision detection
- Health and armor management
- Weapon inventory and selection
- Input processing (keyboard, mouse, controller)

The player's position is represented by (x, y) coordinates and an angle for the viewing direction. Movement is handled by calculating new positions based on input and checking for collisions with the map.

```python
def _try_move(self, new_x, new_y):
    """Try to move to a new position, checking for collisions"""
    # Simple collision detection with map walls
    if not self.map.is_wall(int(new_x), int(self.y)):
        self.x = new_x
    
    if not self.map.is_wall(int(self.x), int(new_y)):
        self.y = new_y
```

### Enemy System

The enemy system in `engine/enemy.py` implements:

- Different enemy types with unique properties
- State machine for AI behavior (idle, chase, attack, pain, dead)
- Pathfinding toward the player
- Combat mechanics

Enemies are managed by the `EnemyManager` class, which handles spawning, updating, and removing enemies. Each enemy has its own state machine that determines its behavior:

```python
def update(self, dt, player):
    """Update enemy state and position"""
    self.target = player
    
    # Update timers
    if self.attack_cooldown > 0:
        self.attack_cooldown -= dt
    
    self.state_timer += dt
    
    # State machine
    if self.state == "idle":
        self._update_idle(dt, player)
    elif self.state == "chase":
        self._update_chase(dt, player)
    elif self.state == "attack":
        self._update_attack(dt, player)
    elif self.state == "pain":
        self._update_pain(dt, player)
    elif self.state == "dead":
        self._update_dead(dt)
```

### Weapon System

The weapon system in `engine/weapon.py` handles:

- Different weapon types with unique properties
- Firing mechanics and cooldowns
- Ammunition management
- Weapon switching
- Animation states (idle, firing, reloading)

Weapons are managed by the `WeaponManager` class, which handles weapon creation, selection, and updating. Each weapon has its own properties and behavior:

```python
def _fire(self, player):
    """Fire the weapon"""
    # Check if player has enough ammo
    if self.ammo_type and player.ammo.get(self.ammo_type, 0) < self.ammo_per_shot:
        # Play empty click sound
        # ...
        return False
    
    # Consume ammo
    if self.ammo_type:
        player.ammo[self.ammo_type] -= self.ammo_per_shot
    
    # Start firing animation
    self.is_firing = True
    self.sprite_index = 0
    self.animation_timer = 0
    
    # Set cooldown
    self.fire_timer = 1.0 / self.fire_rate
    
    # Play weapon sound
    # ...
    
    # Calculate damage and hit detection
    hit, distance, entity = self._calculate_hit(player)
    
    # Visual effects for hit
    if hit and entity:
        # Create hit effect
        pass
    
    return True
```

### Map System

The map system in `engine/map.py` handles:

- Loading map data from files
- Collision detection
- Spawning enemies and items
- Raycasting for walls

Maps are defined in text files with a simple format that specifies wall types, enemy spawns, and item spawns. The `Map` class loads and parses these files:

```python
def load_map(self):
    """Load map data from file"""
    map_file = f"assets/maps/e1m{self.level_num}.txt"
    
    try:
        with open(map_file, 'r') as f:
            lines = f.readlines()
        
        # Parse map data
        # ...
        
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
        # ...
```

### Controller Support

The controller support in `engine/controller.py` provides:

- Xbox controller input handling
- Mapping of controller inputs to game actions
- Support for multiple controller types
- Vibration feedback

The controller input is handled in a separate thread to ensure responsive controls:

```python
def _controller_input_loop(self):
    """Background thread to continuously read controller input"""
    while self.running:
        try:
            # Get events from the gamepad
            events = get_gamepad()
            
            for event in events:
                self._process_controller_event(event)
        
        except Exception as e:
            print(f"Controller input error: {e}")
            time.sleep(0.1)  # Avoid busy-waiting if there's an error
```

## UI Components

### HUD (Heads-Up Display)

The HUD in `ui/hud.py` displays:

- Health and armor bars
- Ammo counter
- Current weapon
- Face status icon (changes based on health)
- Kill feed
- Status messages

The HUD is rendered at the bottom of the screen and provides important information to the player:

```python
def render(self):
    """Render the HUD elements"""
    # Render kill feed first (so it's behind other HUD elements)
    self._render_kill_feed()
    
    # Create a DOOM-style HUD background
    hud_bg = pygame.Surface((self.width, 120))
    hud_bg.fill((40, 40, 40))
    
    # Add a top border line
    pygame.draw.line(hud_bg, (100, 100, 100), (0, 0), (self.width, 0), 2)
    
    # Add some texture to the HUD background
    # ...
    
    # Make it semi-transparent
    hud_bg.set_alpha(220)
    self.screen.blit(hud_bg, (0, self.height - 120))
    
    # Render weapon first (at the bottom)
    self._render_weapon()
    
    # Render health
    self._render_health()
    
    # Render armor
    self._render_armor()
    
    # Render ammo
    self._render_ammo()
    
    # Render face
    self._render_face()
    
    # Render keys
    self._render_keys()
    
    # Render a crosshair in the center of the screen
    # ...
    
    # Render message if active
    if self.message and self.message_timer > 0:
        self._render_message()
```

### Menu System

The menu system in `ui/menu.py` provides:

- Main menu
- Pause menu
- Options menus (graphics, sound, gameplay, controls)
- Input handling for keyboard and controller

The menu system uses a state machine to track the current menu and selected item:

```python
def handle_input(self, event, controller_input=None):
    """Handle menu input"""
    if event.type == pygame.KEYDOWN:
        # Navigate menu
        if event.key == pygame.K_UP:
            self.selected_item = (self.selected_item - 1) % len(self.menu_items[self.current_menu])
            self._play_menu_sound('menu_move')
        
        elif event.key == pygame.K_DOWN:
            self.selected_item = (self.selected_item + 1) % len(self.menu_items[self.current_menu])
            self._play_menu_sound('menu_move')

        # Select menu item
        elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
            self._play_menu_sound('menu_select')
            return self._select_menu_item()

        # Back/cancel
        elif event.key == pygame.K_ESCAPE:
            if self.current_menu == "main":
                return "quit"
            else:
                return "back"
    
    # Handle controller input
    # ...
    
    return None
```

## Asset Management

Assets are organized in the `assets` directory:

- `images/`: Textures for walls, sprites for enemies and weapons
- `sounds/`: Sound effects for weapons, enemies, and UI
- `maps/`: Level definitions in text format

The game loads assets dynamically as needed:

```python
def load_assets(self):
    """Load game assets like textures, sounds, etc."""
    self.textures = {}
    # Ensure HUD is passed to enemy manager
    if hasattr(self.map, 'enemy_manager'):
        self.map.enemy_manager.hud = self.hud

    self.sounds = {}
    
    # Load textures
    texture_dir = os.path.join("assets", "images")
    try:
        # Load wall textures
        for i in range(1, 4):
            texture_path = os.path.join(texture_dir, f"wall{i}.png")
            if os.path.exists(texture_path):
                self.textures[f"wall{i}"] = pygame.image.load(texture_path).convert()
        
        # Load door texture
        # ...
        
        # Load weapon textures
        # ...
        
        # Load enemy textures
        # ...
        
        # Load item textures
        # ...
        
        # Load HUD textures
        # ...
        
        # Pass textures to raycaster
        self.raycaster.load_textures(self.textures)
        
        print(f"Loaded {len(self.textures)} textures")
    except Exception as e:
        print(f"Error loading textures: {e}")
    
    # Load sounds
    # ...
```

## Map Format

Maps are defined in text files with a simple format:

```
# Map section
MAP
222222222222222222222222222222
211111111111111111111111111112
210000000000000000000000000012
# ... more map rows ...
END_MAP

# Enemy spawns
ENEMIES
imp,5,10
demon,15,10
# ... more enemy spawns ...
END_ENEMIES

# Item spawns
ITEMS
health,3,3
ammo,17,3
# ... more item spawns ...
END_ITEMS
```

The map format uses:
- Numbers for wall types (1, 2, 3) and empty space (0)
- 'P' for player start position
- Enemy and item spawns are defined separately with type and coordinates

## Implementation Details

### Entity System

All game objects inherit from the `Entity` base class in `engine/entity.py`:

```python
class Entity:
    """Base class for all game entities"""
    
    def __init__(self, x, y):
        """Initialize entity with position"""
        self.x = x
        self.y = y
        self.size = 0.5  # Default hitbox size
        self.health = 100  # Default health
        self.alive = True
        self.map = None  # Will be set by game when added to map
        
    def update(self, dt):
        """Update entity state"""
        pass  # To be overridden by subclasses
        
    def take_damage(self, amount):
        """Handle taking damage"""
        self.health -= amount
        if self.health <= 0:
            self.alive = False
            
    def collides_with(self, other):
        """Check collision with another entity"""
        if not self.alive or not other.alive:
            return False
            
        dx = self.x - other.x
        dy = self.y - other.y
        distance = (dx*dx + dy*dy) ** 0.5
        return distance < (self.size + other.size)
```

### Collision Detection

Collision detection is handled at multiple levels:

1. **Wall collisions**: Simple grid-based collision checking
2. **Entity collisions**: Distance-based collision detection between entities
3. **Weapon hit detection**: Raycasting from the player to detect hits

### Game State Management

The game uses a simple state machine to manage different states:

- Running (normal gameplay)
- Paused (menu overlay)
- Victory/defeat conditions

## Performance Considerations

The game implements several optimizations:

1. **Raycasting optimization**: Using DDA algorithm for efficient ray casting
2. **Texture caching**: Textures are loaded once and reused
3. **Distance culling**: Objects beyond a certain distance are not rendered
4. **Sprite sorting**: Sprites are sorted by distance for correct rendering order
5. **Delta time**: Game logic uses delta time for consistent speed across different frame rates

## Conclusion

This DOOM Python Recreation demonstrates how to implement a classic 3D game using modern Python libraries. The modular architecture makes it easy to understand and extend the codebase with new features.

The raycasting technique, while simple compared to modern 3D engines, provides an efficient way to create a pseudo-3D environment that captures the essence of the original DOOM game.

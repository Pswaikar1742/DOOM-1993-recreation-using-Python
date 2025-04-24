# Enemy AI System Explained

This document provides a detailed explanation of the enemy AI system used in the DOOM Python Recreation project. Understanding how the enemy AI works is essential for both playing the game effectively and extending it with new enemy types or behaviors.

## Table of Contents

1. [Introduction](#introduction)
2. [AI Architecture](#ai-architecture)
3. [State Machine](#state-machine)
4. [Enemy Types](#enemy-types)
5. [Pathfinding](#pathfinding)
6. [Combat Mechanics](#combat-mechanics)
7. [Enemy Spawning](#enemy-spawning)
8. [Performance Considerations](#performance-considerations)
9. [Extending the AI](#extending-the-ai)
10. [Code Implementation](#code-implementation)

## Introduction

The enemy AI in the DOOM Python Recreation is designed to recreate the behavior of enemies from the original DOOM game. The AI is based on a state machine architecture, where each enemy can be in one of several states (idle, chase, attack, pain, dead) and transitions between these states based on game events and player actions.

The AI system is implemented in the `engine/enemy.py` file, which contains the `Enemy` class and the `EnemyManager` class. The `Enemy` class handles individual enemy behavior, while the `EnemyManager` class manages all enemies in the game.

## AI Architecture

The enemy AI architecture consists of several key components:

1. **EnemyManager**: Manages all enemies in the game, handling spawning, updating, and removing enemies.
2. **Enemy Class**: Represents an individual enemy with properties like health, speed, and damage.
3. **State Machine**: Controls enemy behavior based on current state and transitions.
4. **Update Methods**: Specific methods for updating enemy behavior in each state.
5. **Collision Detection**: Ensures enemies don't walk through walls or each other.

```python
class EnemyManager:
    """Manages all enemies in the game"""
    
    def __init__(self, map):
        """Initialize with reference to map"""
        self.map = map
        self.enemies = []
        self.hud = None  # Will be set by game
        
        # Spawn initial enemies
        for spawn in map.get_spawn_points("enemy"):
            self.spawn_enemy(spawn["type"], spawn["x"], spawn["y"])
    
    def spawn_enemy(self, enemy_type, x, y):
        """Create and add a new enemy"""
        enemy = Enemy(x, y, enemy_type)
        enemy.map = self.map
        if self.hud:
            enemy.hud = self.hud
        self.enemies.append(enemy)
    
    def update(self, dt, player):
        """Update all enemies"""
        for enemy in self.enemies[:]:  # Iterate over copy for safe removal
            enemy.update(dt, player)
            
            # Remove dead enemies that finished death animation
            if enemy.state == "dead":
                self.enemies.remove(enemy)
```

## State Machine

The core of the enemy AI is a state machine that controls behavior. Each enemy can be in one of the following states:

1. **Idle**: The enemy is inactive, waiting to detect the player.
2. **Chase**: The enemy has detected the player and is moving toward them.
3. **Attack**: The enemy is in range and attacking the player.
4. **Pain**: The enemy has been hit and is briefly stunned.
5. **Dead**: The enemy has been killed and will be removed after the death animation.

The state machine is implemented in the `update` method of the `Enemy` class:

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

Each state has its own update method that handles the specific behavior for that state:

### Idle State

In the idle state, the enemy is stationary and periodically checks if the player is within detection range:

```python
def _update_idle(self, dt, player):
    """Idle state behavior"""
    # Check if player is within detection range
    dx = player.x - self.x
    dy = player.y - self.y
    distance = math.sqrt(dx*dx + dy*dy)
    
    if distance < self.detection_range:
        self.state = "chase"
        self.state_timer = 0
```

### Chase State

In the chase state, the enemy moves toward the player, avoiding obstacles:

```python
def _update_chase(self, dt, player):
    """Chase state behavior"""
    # Calculate direction to player
    dx = player.x - self.x
    dy = player.y - self.y
    distance = math.sqrt(dx*dx + dy*dy)
    self.direction = math.atan2(dy, dx)
    
    # Move toward player
    if distance > self.attack_range:
        new_x = self.x + math.cos(self.direction) * self.speed * dt
        new_y = self.y + math.sin(self.direction) * self.speed * dt
        
        # Simple collision detection
        if not self._check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y
    
    # Transition to attack state if in range
    elif distance <= self.attack_range and self.attack_cooldown <= 0:
        self.state = "attack"
        self.state_timer = 0
```

### Attack State

In the attack state, the enemy attacks the player:

```python
def _update_attack(self, dt, player):
    """Attack state behavior"""
    # Attack the player
    if self.state_timer >= 1.0 / self.attack_rate:
        player.take_damage(self.damage)
        self.attack_cooldown = 1.0 / self.attack_rate
        self.state = "chase"
        self.state_timer = 0
```

### Pain State

In the pain state, the enemy is briefly stunned after being hit:

```python
def _update_pain(self, dt, player):
    """Pain state behavior (when hit by player)"""
    if self.state_timer >= 0.5:  # Pain animation duration
        self.state = "chase"
        self.state_timer = 0
```

### Dead State

In the dead state, the enemy plays a death animation and is then removed:

```python
def _update_dead(self, dt):
    """Dead state behavior"""
    pass  # Could add corpse physics or removal timer
```

## Enemy Types

The game includes different enemy types, each with unique properties:

### Imp

Imps are fast but relatively weak enemies:

```python
if self.type == "imp":
    self.health = 60
    self.speed = 1.2
    self.damage = 15
    self.attack_range = 1.2
    self.attack_rate = 1.5
    self.size = 0.4
```

### Demon

Demons are slower but stronger enemies:

```python
elif self.type == "demon":
    self.health = 150
    self.speed = 0.8
    self.damage = 25
    self.attack_range = 2.0
    self.attack_rate = 0.8
    self.size = 0.6
```

Each enemy type has its own sprites for different states, which are rendered by the raycasting engine.

## Pathfinding

The current implementation uses a simple direct pathfinding approach, where enemies move directly toward the player and avoid obstacles through collision detection. This approach works well for the original DOOM-style gameplay but could be extended with more sophisticated pathfinding algorithms.

The collision detection is handled by the `_check_collision` method:

```python
def _check_collision(self, new_x, new_y):
    """Check for collisions with walls"""
    # Simple wall collision
    if self.map.is_wall(int(new_x), int(new_y)):
        return True
    
    # More advanced collision checking could go here
    return False
```

## Combat Mechanics

Enemy combat is handled through the attack state and the `take_damage` method:

```python
def take_damage(self, amount):
    """Handle enemy taking damage"""
    if self.state == "dead":
        return
    
    self.health -= amount
    
    if self.health <= 0:
        self.state = "dead"
        if hasattr(self, 'hud'):
            self.hud.show_message(f"{self.type.upper()} KILLED!", 2.0)
    else:
        self.state = "pain"
        self.state_timer = 0
```

When an enemy is hit, it transitions to the pain state briefly before resuming the chase. If its health drops to zero, it transitions to the dead state.

## Enemy Spawning

Enemies are spawned by the `EnemyManager` based on spawn points defined in the map file:

```python
# Enemy spawns
ENEMIES
imp,5,10
demon,15,10
imp,10,15
END_ENEMIES
```

The `EnemyManager` creates enemies at these spawn points when the map is loaded:

```python
# Spawn initial enemies
for spawn in map.get_spawn_points("enemy"):
    self.spawn_enemy(spawn["type"], spawn["x"], spawn["y"])
```

## Performance Considerations

The enemy AI system is designed to be efficient, with several optimizations:

1. **Limited State Updates**: Only the current state's update method is called.
2. **Distance Checks**: Enemies beyond a certain distance may have simplified behavior.
3. **Removal of Dead Enemies**: Dead enemies are removed from the game after their death animation.
4. **Simple Collision Detection**: Collision detection is kept simple for performance.

## Extending the AI

The enemy AI system can be extended in several ways:

### Adding New Enemy Types

To add a new enemy type, update the `_set_properties` method in the `Enemy` class:

```python
def _set_properties(self):
    """Set enemy properties based on type"""
    if self.type == "imp":
        # Existing imp properties...
    elif self.type == "demon":
        # Existing demon properties...
    elif self.type == "cacodemon":  # New enemy type
        self.health = 200
        self.speed = 0.7
        self.damage = 30
        self.attack_range = 2.5
        self.attack_rate = 0.6
        self.size = 0.7
```

### Adding New States

To add a new state, add a new update method and modify the state machine:

```python
def update(self, dt, player):
    # Existing code...
    
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
    elif self.state == "ranged_attack":  # New state
        self._update_ranged_attack(dt, player)

def _update_ranged_attack(self, dt, player):
    """Ranged attack state behavior"""
    # Implementation for ranged attack
    pass
```

### Improving Pathfinding

To improve pathfinding, you could implement a more sophisticated algorithm like A* or navigation meshes:

```python
def _update_chase(self, dt, player):
    """Chase state behavior with improved pathfinding"""
    # Calculate path to player using A* algorithm
    path = self._calculate_path_to_player(player)
    
    if path:
        # Move along the path
        next_point = path[0]
        direction = math.atan2(next_point[1] - self.y, next_point[0] - self.x)
        
        new_x = self.x + math.cos(direction) * self.speed * dt
        new_y = self.y + math.sin(direction) * self.speed * dt
        
        if not self._check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y
```

## Code Implementation

The enemy AI system is implemented in the `engine/enemy.py` file, which contains:

1. **EnemyManager Class**: Manages all enemies in the game.
2. **Enemy Class**: Represents an individual enemy with AI behavior.

The `Enemy` class inherits from the `Entity` base class, which provides common functionality for all game entities:

```python
class Enemy(Entity):
    """Base enemy class that handles AI, movement, and combat"""
    
    def __init__(self, x, y, enemy_type):
        """Initialize the enemy"""
        super().__init__(x, y)
        self.type = enemy_type
        self.size = 0.5  # Hitbox size (radius)
        self.health = 100
        self.speed = 1.0
        self.damage = 10
        self.attack_range = 1.5
        self.attack_cooldown = 0
        self.attack_rate = 1.0  # Attacks per second
        self.detection_range = 10.0
        self.state = "idle"  # idle, chase, attack, pain, dead
        self.state_timer = 0
        self.direction = 0  # Facing direction in radians
        self.target = None
        
        # Set type-specific properties
        self._set_properties()
```

The enemy AI system is a key component of the game, providing challenging opponents for the player to face. By understanding how it works, you can both play the game more effectively and extend it with new enemy types and behaviors.

## Conclusion

The enemy AI system in the DOOM Python Recreation uses a state machine architecture to create enemies that behave similarly to those in the original DOOM game. The system is designed to be efficient and extensible, allowing for the addition of new enemy types and behaviors.

By understanding the AI system, you can better appreciate how the game works and how to extend it with new features. Whether you're a player looking to understand enemy behavior or a developer looking to add new enemies, this document provides the information you need.

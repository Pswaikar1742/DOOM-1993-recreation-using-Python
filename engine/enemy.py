"""
Enemy classes for DOOM recreation
"""
import math
import random
import pygame
from engine.entity import Entity

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
    
    def _set_properties(self):
        """Set enemy properties based on type"""
        if self.type == "imp":
            self.health = 60
            self.speed = 1.2
            self.damage = 15
            self.attack_range = 1.2
            self.attack_rate = 1.5
            self.size = 0.4
        
        elif self.type == "demon":
            self.health = 150
            self.speed = 0.8
            self.damage = 25
            self.attack_range = 2.0
            self.attack_rate = 0.8
            self.size = 0.6
    
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
    
    def _update_idle(self, dt, player):
        """Idle state behavior"""
        # Check if player is within detection range
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < self.detection_range:
            self.state = "chase"
            self.state_timer = 0
    
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
    
    def _update_attack(self, dt, player):
        """Attack state behavior"""
        # Attack the player
        if self.state_timer >= 1.0 / self.attack_rate:
            player.take_damage(self.damage)
            self.attack_cooldown = 1.0 / self.attack_rate
            self.state = "chase"
            self.state_timer = 0
    
    def _update_pain(self, dt, player):
        """Pain state behavior (when hit by player)"""
        if self.state_timer >= 0.5:  # Pain animation duration
            self.state = "chase"
            self.state_timer = 0
    
    def _update_dead(self, dt):
        """Dead state behavior"""
        pass  # Could add corpse physics or removal timer
    
    def _check_collision(self, new_x, new_y):
        """Check for collisions with walls"""
        # Simple wall collision
        if self.map.is_wall(int(new_x), int(new_y)):
            return True
        
        # More advanced collision checking could go here
        return False
    
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
    
    def get_sprite(self):
        """Get the appropriate sprite name based on enemy state and type"""
        # Basic sprite naming convention: "{type}_{state}{frame}"
        # For now we'll just use the first frame of each animation
        if self.state == "dead":
            return f"{self.type}_death1"
        elif self.state == "pain":
            return f"{self.type}_pain1"
        elif self.state == "attack":
            return f"{self.type}_attack1"
        elif self.state == "chase":
            return f"{self.type}_walk1"
        else:  # idle
            return f"{self.type}_idle1"

    def render(self, screen, player):

        """Render the enemy"""
        # This would normally be handled by the raycaster
        # For hitbox visualization, the game.py render method handles it
        
        # Calculate screen position based on player's view

        dx = self.x - player.x
        dy = self.y - player.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Only render if in front of player
        angle_to_player = math.atan2(dy, dx)
        relative_angle = (angle_to_player - player.angle + math.pi) % (2 * math.pi) - math.pi
        
        if abs(relative_angle) < math.pi/2 and distance < 20:
            # This would be replaced with proper 3D rendering
            screen_x = int((dx * math.cos(player.angle) + dy * math.sin(player.angle)) * 32 + screen.get_width() // 2)
            screen_y = int(screen.get_height() // 2 - distance * 32)
            
            # Draw enemy (placeholder)
            color = (255, 0, 0) if self.type == "demon" else (200, 100, 0)
            pygame.draw.circle(screen, color, (screen_x, screen_y), int(20 / (distance + 1)))

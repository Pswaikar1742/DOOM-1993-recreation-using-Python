"""
Weapon class for DOOM recreation
"""
import math
import pygame
import numpy as np

class Weapon:
    """Base weapon class that handles firing, animations, and damage"""
    
    def __init__(self, weapon_type):
        """Initialize the weapon"""
        self.type = weapon_type
        
        # Set weapon properties based on type
        self._set_properties()
        
        # State
        self.is_firing = False
        self.is_reloading = False
        
        # Animation
        self.sprite_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # seconds per frame
        
        # Cooldown
        self.fire_timer = 0
    
    def _set_properties(self):
        """Set weapon properties based on type"""
        # Default properties
        self.damage = 10
        self.fire_rate = 1.0  # shots per second
        self.reload_time = 1.0  # seconds
        self.ammo_type = "bullets"
        self.ammo_per_shot = 1
        self.range = 20.0
        self.spread = 0.1  # accuracy (lower is more accurate)
        self.sprites = {}
        
        # Type-specific properties
        if self.type == "fist":
            self.damage = 10
            self.fire_rate = 1.5
            self.ammo_type = None  # No ammo needed
            self.range = 1.5
            self.sprites = {
                "idle": ["fist_idle"],
                "fire": ["fist_fire1", "fist_fire2", "fist_fire3"]
            }
        
        elif self.type == "pistol":
            self.damage = 15
            self.fire_rate = 2.0
            self.ammo_type = "bullets"
            self.sprites = {
                "idle": ["pistol_idle"],
                "fire": ["pistol_fire1", "pistol_fire2", "pistol_fire3"]
            }
    
    def update(self, dt, player_input):
        """Update weapon state and animations"""
        # Update timers
        if self.fire_timer > 0:
            self.fire_timer -= dt
        
        self.animation_timer += dt
        
        # Handle firing
        if self.is_firing:
            # Update animation
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.sprite_index += 1
                
                # Check if animation is complete
                if self.sprite_index >= len(self.sprites.get("fire", [])):
                    self.sprite_index = 0
                    self.is_firing = False
        
        # Handle reloading
        elif self.is_reloading:
            # Update animation
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.sprite_index += 1
                
                # Check if animation is complete
                if self.sprite_index >= len(self.sprites.get("reload", [])):
                    self.sprite_index = 0
                    self.is_reloading = False
        
        # Handle idle
        else:
            self.sprite_index = 0
            
            # Check for fire input
            if player_input.get("fire", False) and self.fire_timer <= 0:
                self._fire(player_input.get("player"))
    
    def _fire(self, player):
        """Fire the weapon"""
        # Check if player has enough ammo
        if self.ammo_type and player.ammo.get(self.ammo_type, 0) < self.ammo_per_shot:
            # Play empty click sound
            try:
                # Get game instance to play sound
                from engine.game import Game
                import gc
                game_instances = [obj for obj in gc.get_objects() if isinstance(obj, Game)]
                if game_instances:
                    game = game_instances[0]
                    if "no_ammo" in game.sounds:
                        game.sounds["no_ammo"].play()
            except:
                pass
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
        try:
            # Get game instance to play sound
            from engine.game import Game
            import gc
            game_instances = [obj for obj in gc.get_objects() if isinstance(obj, Game)]
            if game_instances:
                game = game_instances[0]
                sound_name = f"{self.type}_fire"
                if sound_name in game.sounds:
                    game.sounds[sound_name].play()
        except:
            pass
        
        # Calculate damage and hit detection
        hit, distance, entity = self._calculate_hit(player)
        
        # Visual effects for hit
        if hit and entity:
            # Create hit effect (will be implemented in raycaster)
            pass
        
        return True
    
    def _calculate_hit(self, player):
        """Calculate hit detection and damage"""
        # Get player's view direction
        angle = player.angle
        
        # Add some spread/inaccuracy
        if self.spread > 0:
            angle += (np.random.random() - 0.5) * self.spread
        
        # Cast a ray to find what we hit
        hit, distance, entity = player.map.cast_ray_entities(
            player.x, player.y, angle, self.range, player
        )
        
        if hit and entity:
            # Deal damage to the entity
            if hasattr(entity, "take_damage"):
                entity.take_damage(self.damage)
        
        # Return the hit information
        return hit, distance, entity
    
    def get_sprite(self):
        """Get the current sprite for rendering"""
        if self.is_firing:
            sprites = self.sprites.get("fire", [])
        elif self.is_reloading:
            sprites = self.sprites.get("reload", [])
        else:
            sprites = self.sprites.get("idle", [])
        
        if not sprites:
            return None
        
        index = min(self.sprite_index, len(sprites) - 1)
        return sprites[index]


class WeaponManager:
    """Manager class for all weapons in the game"""
    
    def __init__(self, player):
        """Initialize the weapon manager"""
        self.player = player
        self.weapons = {}
        self.current_weapon = None
        
        # Create weapons
        self._create_weapons()
        
        # Set initial weapon
        self.switch_weapon("pistol")
    
    def _create_weapons(self):
        """Create all weapons"""
        weapon_types = ["fist", "pistol"]
        
        for weapon_type in weapon_types:
            self.weapons[weapon_type] = Weapon(weapon_type)
    
    def update(self, dt, player_input):
        """Update the current weapon"""
        if self.current_weapon:
            # Add player reference to input for hit detection
            player_input["player"] = self.player
            
            # Update weapon
            self.current_weapon.update(dt, player_input)
    
    def switch_weapon(self, weapon_type):
        """Switch to a different weapon"""
        if weapon_type in self.weapons and (weapon_type in self.player.weapons or weapon_type == "fist"):
            self.current_weapon = self.weapons[weapon_type]
            return True
        return False
    
    def next_weapon(self):
        """Switch to the next available weapon"""
        if not self.player.weapons:
            return False
        
        # Get current weapon index
        current_type = self.current_weapon.type if self.current_weapon else None
        available_weapons = ["fist"] + [w for w in self.player.weapons if w != "fist"]
        
        if current_type in available_weapons:
            current_index = available_weapons.index(current_type)
            next_index = (current_index + 1) % len(available_weapons)
        else:
            next_index = 0
        
        # Switch to next weapon
        return self.switch_weapon(available_weapons[next_index])
    
    def prev_weapon(self):
        """Switch to the previous available weapon"""
        if not self.player.weapons:
            return False
        
        # Get current weapon index
        current_type = self.current_weapon.type if self.current_weapon else None
        available_weapons = ["fist"] + [w for w in self.player.weapons if w != "fist"]
        
        if current_type in available_weapons:
            current_index = available_weapons.index(current_type)
            prev_index = (current_index - 1) % len(available_weapons)
        else:
            prev_index = 0
        
        # Switch to previous weapon
        return self.switch_weapon(available_weapons[prev_index])
    
    def get_current_sprite(self):
        """Get the current weapon sprite for rendering"""
        if self.current_weapon:
            return self.current_weapon.get_sprite()
        return None

"""
Player class for DOOM recreation
"""
import math
import pygame
import numpy as np

class Player:
    """Player class that handles movement, combat, and player state"""
    
    def __init__(self, map_obj):
        """Initialize the player"""
        self.map = map_obj
        
        # Position and orientation
        self.x = 2.0  # Starting X position
        self.y = 2.0  # Starting Y position
        self.angle = 0.0  # Starting angle (in radians)
        self.height = 0.5  # Player height (for future use with stairs/elevation)
        
        # Movement parameters
        self.move_speed = 3.0  # Units per second
        self.run_speed = 5.0   # Units per second when running
        self.rot_speed = 2.0   # Radians per second
        self.strafe_speed = 2.5  # Units per second when strafing
        
        # Player state
        self.health = 100
        self.armor = 0
        self.max_health = 100
        self.max_armor = 100
        
        # Weapons and ammo
        self.weapons = ["pistol"]
        self.current_weapon = "pistol"
        self.ammo = {
            "bullets": 50
        }
        self.max_ammo = {
            "bullets": 200
        }
        
        # Controller sensitivity settings
        self.mouse_sensitivity = 0.002
        self.controller_sensitivity = 2.0
        
        # Initialize weapon manager
        from engine.weapon import WeaponManager
        self.weapon_manager = WeaponManager(self)
    
    def update(self, keys, mouse_dx, controller_input, dt):
        """Update player position and state based on input"""
        # Handle keyboard movement
        self._handle_keyboard_movement(keys, dt)
        
        # Handle mouse rotation
        self.angle += mouse_dx * self.mouse_sensitivity
        
        # Handle controller input if available
        if controller_input:
            self._handle_controller_input(controller_input, dt)
    
    def _handle_keyboard_movement(self, keys, dt):
        """Handle keyboard movement input"""
        # Determine if running (shift key)
        speed = self.run_speed if keys[pygame.K_LSHIFT] else self.move_speed
        
        # Forward/backward movement
        if keys[pygame.K_w]:
            new_x = self.x + math.cos(self.angle) * speed * dt
            new_y = self.y + math.sin(self.angle) * speed * dt
            self._try_move(new_x, new_y)
        
        if keys[pygame.K_s]:
            new_x = self.x - math.cos(self.angle) * speed * dt
            new_y = self.y - math.sin(self.angle) * speed * dt
            self._try_move(new_x, new_y)
        
        # Strafing left/right
        if keys[pygame.K_a]:
            new_x = self.x + math.cos(self.angle - math.pi/2) * self.strafe_speed * dt
            new_y = self.y + math.sin(self.angle - math.pi/2) * self.strafe_speed * dt
            self._try_move(new_x, new_y)
        
        if keys[pygame.K_d]:
            new_x = self.x + math.cos(self.angle + math.pi/2) * self.strafe_speed * dt
            new_y = self.y + math.sin(self.angle + math.pi/2) * self.strafe_speed * dt
            self._try_move(new_x, new_y)
        
        # Rotation with arrow keys
        if keys[pygame.K_LEFT]:
            self.angle -= self.rot_speed * dt
        
        if keys[pygame.K_RIGHT]:
            self.angle += self.rot_speed * dt
        
        # Weapon switching with number keys
        if keys[pygame.K_1] and "fist" in self.weapons:
            self.current_weapon = "fist"
            self.weapon_manager.switch_weapon("fist")
        elif keys[pygame.K_2] and "pistol" in self.weapons:
            self.current_weapon = "pistol"
            self.weapon_manager.switch_weapon("pistol")
        
        # Weapon firing
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            weapon_input = {'fire': True}
            self.weapon_manager.update(dt, weapon_input)
    
    def _handle_controller_input(self, controller_input, dt):
        """Handle Xbox controller input"""
        # Left stick for movement
        left_x = controller_input.get('left_stick_x', 0)
        left_y = controller_input.get('left_stick_y', 0)
        
        # Only process if stick is moved beyond deadzone
        if abs(left_x) > 0.1 or abs(left_y) > 0.1:
            # Forward/backward movement (with running if left stick is pushed far)
            speed = self.run_speed if abs(left_y) > 0.8 else self.move_speed
            new_x = self.x + math.cos(self.angle) * -left_y * speed * dt
            new_y = self.y + math.sin(self.angle) * -left_y * speed * dt
            self._try_move(new_x, new_y)
            
            # Strafing
            new_x = self.x + math.cos(self.angle + math.pi/2) * left_x * self.strafe_speed * dt
            new_y = self.y + math.sin(self.angle + math.pi/2) * left_x * self.strafe_speed * dt
            self._try_move(new_x, new_y)
        
        # Right stick for looking around
        right_x = controller_input.get('right_stick_x', 0)
        
        # Only process if stick is moved beyond deadzone
        if abs(right_x) > 0.1:
            self.angle += right_x * self.controller_sensitivity * dt
        
        # Handle weapon switching with bumpers or d-pad
        if controller_input.get('next_weapon', False):
            self.weapon_manager.next_weapon()
        
        if controller_input.get('prev_weapon', False):
            self.weapon_manager.prev_weapon()
        
        # Handle firing with right trigger
        if controller_input.get('fire', False):
            weapon_input = {'fire': True}
            self.weapon_manager.update(dt, weapon_input)
    
    def _try_move(self, new_x, new_y):
        """Try to move to a new position, checking for collisions"""
        # Simple collision detection with map walls
        # We'll improve this later with proper collision detection
        if not self.map.is_wall(int(new_x), int(self.y)):
            self.x = new_x
        
        if not self.map.is_wall(int(self.x), int(new_y)):
            self.y = new_y
    
    def take_damage(self, amount):
        """Handle player taking damage"""
        # First apply damage to armor if available
        if self.armor > 0:
            # Armor absorbs 2/3 of damage in original DOOM
            armor_absorption = min(self.armor, amount * 2/3)
            self.armor -= armor_absorption
            amount -= armor_absorption
        
        # Apply remaining damage to health
        self.health = max(0, self.health - amount)
        
        # Check if player is dead
        if self.health <= 0 and hasattr(self, 'hud'):
            self.hud.show_message("YOU DIED!", 5.0)
        
        return self.health <= 0
    
    def add_health(self, amount):
        """Add health to the player"""
        self.health = min(self.max_health, self.health + amount)
    
    def add_armor(self, amount):
        """Add armor to the player"""
        self.armor = min(self.max_armor, self.armor + amount)
    
    def add_ammo(self, ammo_type, amount):
        """Add ammo to the player"""
        if ammo_type in self.ammo:
            self.ammo[ammo_type] = min(self.max_ammo[ammo_type], 
                                     self.ammo[ammo_type] + amount)
    
    def add_weapon(self, weapon):
        """Add a weapon to the player's inventory"""
        if weapon not in self.weapons:
            self.weapons.append(weapon)
            self.current_weapon = weapon
    
    def pickup_item(self, item_type):
        """Handle item pickups from the map"""
        if item_type == "health":
            self.add_health(25)
        elif item_type == "armor":
            self.add_armor(50)
        elif item_type == "ammo":
            self.add_ammo("bullets", 20)

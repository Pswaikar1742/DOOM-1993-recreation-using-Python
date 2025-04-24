"""
Game class for DOOM recreation
"""
import os
import time
import math
import pygame
import numpy as np
from engine.player import Player
from engine.map import Map
from engine.raycasting import Raycaster
from engine.controller import Controller
from ui.hud import HUD
from ui.menu import Menu

class Game:
    """Main game class that manages the game loop and components"""
    
    def __init__(self):
        """Initialize the game"""
        # Set up display
        self.width, self.height = 1024, 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("DOOM Python Recreation")
        
        # Set up clock
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Game state
        self.running = True
        self.paused = False
        self.current_level = 1
        self.show_hitboxes = False  # Toggle for enemy hitboxes
        
        # Initialize components
        self.map = Map(self.current_level)
        self.player = Player(self.map)
        self.raycaster = Raycaster(self.map)
        self.controller = Controller()
        self.hud = HUD(self.screen, self.player)
        self.menu = Menu(self.screen, self)  # Pass game reference to menu

        # Pass HUD reference to map for enemy manager
        self.map.hud = self.hud

        # Load assets
        self.load_assets()
    
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
            door_path = os.path.join(texture_dir, "door.png")
            if os.path.exists(door_path):
                self.textures["door"] = pygame.image.load(door_path).convert()
            
            # Load weapon textures
            for weapon in ["pistol"]:
                for state in ["idle", "fire1", "fire2"]:
                    texture_path = os.path.join(texture_dir, f"{weapon}_{state}.png")
                    if os.path.exists(texture_path):
                        self.textures[f"{weapon}_{state}"] = pygame.image.load(texture_path).convert_alpha()

            
            # Load enemy textures
            for enemy in ["imp", "demon"]:
                for state in ["idle1", "walk1", "attack1"]:
                    texture_path = os.path.join(texture_dir, f"{enemy}_{state}.png")
                    if os.path.exists(texture_path):
                        self.textures[f"{enemy}_{state}"] = pygame.image.load(texture_path).convert_alpha()
            
            # Load item textures
            for item in ["health", "armor", "ammo", "key_blue", "key_red", "key_yellow"]:

                texture_path = os.path.join(texture_dir, f"{item}.png")
                if os.path.exists(texture_path):
                    self.textures[item] = pygame.image.load(texture_path).convert_alpha()
            
            # Load HUD textures
            for hud_element in ["face_normal", "face_hurt"]:
                texture_path = os.path.join(texture_dir, f"{hud_element}.png")
                if os.path.exists(texture_path):
                    self.textures[hud_element] = pygame.image.load(texture_path).convert_alpha()
            
            # Pass textures to raycaster
            self.raycaster.load_textures(self.textures)
            
            print(f"Loaded {len(self.textures)} textures")
        except Exception as e:
            print(f"Error loading textures: {e}")
        
        # Load sounds
        sound_dir = os.path.join("assets", "sounds")
        try:
            # Initialize pygame mixer if not already initialized
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            # Load weapon sounds
            for sound in ["pistol_fire", "no_ammo"]:

                sound_path = os.path.join(sound_dir, f"{sound}.wav")
                if os.path.exists(sound_path):
                    self.sounds[sound] = pygame.mixer.Sound(sound_path)
            
            # Load enemy sounds
            for enemy in ["imp", "demon"]:
                for state in ["sight", "attack", "pain", "death"]:
                    sound_path = os.path.join(sound_dir, f"{enemy}_{state}.wav")
                    if os.path.exists(sound_path):
                        self.sounds[f"{enemy}_{state}"] = pygame.mixer.Sound(sound_path)
            
            # Load player sounds
            for sound in ["player_pain", "player_death", "player_pickup"]:
                sound_path = os.path.join(sound_dir, f"{sound}.wav")
                if os.path.exists(sound_path):
                    self.sounds[sound] = pygame.mixer.Sound(sound_path)
            
            # Load menu sounds
            for sound in ["menu_move", "menu_select"]:
                sound_path = os.path.join(sound_dir, f"{sound}.wav")
                if os.path.exists(sound_path):
                    self.sounds[sound] = pygame.mixer.Sound(sound_path)
            
            # Load ambient sounds
            for sound in ["door_open", "door_close", "switch"]:
                sound_path = os.path.join(sound_dir, f"{sound}.wav")
                if os.path.exists(sound_path):
                    self.sounds[sound] = pygame.mixer.Sound(sound_path)
            
            print(f"Loaded {len(self.sounds)} sounds")
        except Exception as e:
            print(f"Error loading sounds: {e}")
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_SPACE:
                    # Fire weapon when SPACE is pressed
                    weapon_input = {'fire': True}
                    if hasattr(self.player, 'weapon_manager'):
                        self.player.weapon_manager.update(0.016, weapon_input)
                elif event.key == pygame.K_h:  # Toggle hitboxes with H key
                    self.show_hitboxes = not self.show_hitboxes
            
            # Pass events to controller for handling
            self.controller.handle_event(event)
            
            # Handle menu input if paused
            if self.paused:
                # Get controller input
                controller_input = self.controller.get_input()
                
                # Pass event and controller input to menu
                action = self.menu.handle_input(event, controller_input)
                
                # Process menu action
                if action:
                    self._handle_menu_action(action)
    
    def update(self, dt):
        """Update game state"""
        if self.paused:
            # Check for controller start button to toggle pause
            controller_input = self.controller.get_input()
            if controller_input and controller_input.get('start', False):
                self.paused = False
                pygame.time.delay(200)
            return
        
        # Get input from keyboard/mouse and controller
        keys = pygame.key.get_pressed()
        mouse_dx, _ = pygame.mouse.get_rel()
        controller_input = self.controller.get_input()
        
        # Check for controller start button to toggle pause
        if controller_input and controller_input.get('start', False):
            self.paused = True
            self.menu.set_menu("pause")
            pygame.time.delay(200)
            return
        
        # Update player based on input
        self.player.update(keys, mouse_dx, controller_input, dt)
        
        # Handle weapon firing with controller
        if controller_input and controller_input.get('rb', False):
            weapon_input = {'fire': True}
            if hasattr(self.player, 'weapon_manager'):
                self.player.weapon_manager.update(dt, weapon_input)
        
        # Update enemies and check win condition
        if hasattr(self.map, 'enemy_manager'):
            self.map.enemy_manager.update(dt, self.player)
            if len(self.map.enemy_manager.enemies) == 0 and not hasattr(self, 'victory_shown'):
                self.hud.show_message("YOU WON!", 5.0)
                self.victory_shown = True
            
        # Check for item pickups
        self._check_item_pickups()
        
        # Update HUD
        self.hud.update(dt)
    
    def render(self):
        """Render the game"""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        if self.paused:
            # First render the 3D view as background
            self.raycaster.render(self.screen, self.player)
            
            # Then show pause menu overlay
            self.menu.render_pause()
        else:
            # Render 3D view
            self.raycaster.render(self.screen, self.player)
            
            # Render enemy hitboxes if enabled
            if self.show_hitboxes and hasattr(self.map, 'enemy_manager'):
                for enemy in self.map.enemy_manager.enemies:
                    # Convert enemy position to screen coordinates
                    screen_x = int((enemy.x - self.player.x) * 32 + self.width // 2)
                    screen_y = int((enemy.y - self.player.y) * 32 + self.height // 2)
                    
                    # Draw hitbox rectangle
                    hitbox_size = int(enemy.size * 32)
                    pygame.draw.rect(self.screen, (255, 0, 0), 
                                   (screen_x - hitbox_size//2, screen_y - hitbox_size//2, 
                                    hitbox_size, hitbox_size), 1)
            
            # Render HUD
            self.hud.render()
        
        # Update display
        pygame.display.flip()
    
    def _handle_menu_action(self, action):
        """Handle menu actions"""
        if action == "resume":
            self.paused = False
        
        elif action == "new_game":
            # Reset game state for a new game
            self.current_level = 1
            self.map = Map(self.current_level)
            self.player = Player(self.map)
            self.raycaster = Raycaster(self.map)
            self.paused = False
            if hasattr(self, 'victory_shown'):
                delattr(self, 'victory_shown')
        
        elif action == "options_menu":
            self.menu.set_menu("options")
        
        elif action == "graphics_menu":
            self.menu.set_menu("graphics")
        
        elif action == "sound_menu":
            self.menu.set_menu("sound")
        
        elif action == "gameplay_menu":
            self.menu.set_menu("gameplay")
        
        elif action == "controls_menu":
            self.menu.set_menu("controls")
        
        elif action == "main_menu":
            self.menu.set_menu("main")
        
        elif action == "back":
            if self.menu.current_menu in ["graphics", "sound", "gameplay"]:
                self.menu.set_menu("options")
            elif self.menu.current_menu in ["options", "controls"]:
                if self.paused:
                    self.menu.set_menu("pause")
                else:
                    self.menu.set_menu("main")
        
        elif action == "quit":
            self.running = False
    
    def _check_item_pickups(self):
        """Check for item pickups and apply their effects"""
        if not hasattr(self.map, 'item_spawns'):
            return
        
        for item in self.map.item_spawns[:]:
            dx = item["x"] - self.player.x
            dy = item["y"] - self.player.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < 0.5:
                self._pickup_item(item)
                self.map.item_spawns.remove(item)
    
    def _pickup_item(self, item):
        """Apply the effect of picking up an item"""
        item_type = item["type"]
        
        if "player_pickup" in self.sounds:
            self.sounds["player_pickup"].play()
        
        if item_type == "health":
            old_health = self.player.health
            self.player.add_health(25)
            if old_health < 100 and self.player.health >= 100:
                self.hud.show_message("MAXIMUM HEALTH REACHED!", 3.0)
        
        elif item_type == "armor":
            old_armor = self.player.armor
            self.player.add_armor(25)
            if old_armor < 100 and self.player.armor >= 100:
                self.hud.show_message("MAXIMUM ARMOR REACHED!", 3.0)
        
        elif item_type == "ammo":
            self.player.add_ammo("bullets", 20)
        

        
        elif item_type.startswith("key_"):
            key_color = item_type.split("_")[1]
            if not hasattr(self.player, 'keys'):
                self.player.keys = []
            
            if key_color not in self.player.keys:
                self.player.keys.append(key_color)
                self.hud.show_message(f"PICKED UP {key_color.upper()} KEY!", 3.0)
        

    
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

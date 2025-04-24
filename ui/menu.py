"""
Menu class for DOOM recreation
"""
import pygame
import random
import math

class Menu:
    """Menu class that handles game menus"""
    
    def __init__(self, screen, game=None):
        """Initialize the menu"""
        self.screen = screen
        self.game = game  # Reference to game for sound access
        self.last_sound_time = 0  # For sound cooldown
        
        # Screen dimensions
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Menu state
        self.current_menu = "main"  # main, pause, options, etc.
        self.selected_item = 0
        
        # Load fonts
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 32)
        self.small_font = pygame.font.SysFont("Arial", 24)
        
        # Define menu items
        self.menu_items = {
            "main": [
                {"text": "New Game", "action": "new_game"},
                {"text": "Options", "action": "options_menu"},
                {"text": "Controls", "action": "controls_menu"},
                {"text": "Quit", "action": "quit"}
            ],
            "pause": [
                {"text": "Resume", "action": "resume"},
                {"text": "Options", "action": "options_menu"},
                {"text": "Controls", "action": "controls_menu"},
                {"text": "Main Menu", "action": "main_menu"},
                {"text": "Quit", "action": "quit"}
            ],
            "options": [
                {"text": "Graphics", "action": "graphics_menu"},
                {"text": "Sound", "action": "sound_menu"},
                {"text": "Gameplay", "action": "gameplay_menu"},
                {"text": "Back", "action": "back"}
            ],
            "graphics": [
                {"text": "Resolution", "action": "resolution_setting"},
                {"text": "Fullscreen", "action": "fullscreen_setting"},
                {"text": "Texture Quality", "action": "texture_setting"},
                {"text": "Back", "action": "back"}
            ],
            "sound": [
                {"text": "Master Volume", "action": "master_volume"},
                {"text": "Music Volume", "action": "music_volume"},
                {"text": "SFX Volume", "action": "sfx_volume"},
                {"text": "Back", "action": "back"}
            ],
            "gameplay": [
                {"text": "Difficulty", "action": "difficulty_setting"},
                {"text": "Mouse Sensitivity", "action": "mouse_sensitivity"},
                {"text": "Controller Sensitivity", "action": "controller_sensitivity"},
                {"text": "Back", "action": "back"}
            ],
            "controls": [
                {"text": "Keyboard", "action": "keyboard_controls"},
                {"text": "Controller", "action": "controller_controls"},
                {"text": "Back", "action": "back"}
            ]
        }
        
        # Load menu assets
        self.menu_assets = {}
        self._load_menu_assets()
    
    def _load_menu_assets(self):
        """Load menu assets like background, logo, etc."""
        # Create logo placeholder
        logo = pygame.Surface((400, 150))
        logo.fill((150, 0, 0))  # Dark red background
        pygame.draw.rect(logo, (200, 0, 0), (10, 10, 380, 130))  # Red border
        self.menu_assets["logo"] = logo
    
    def _play_menu_sound(self, sound_name):
        """Play a menu sound with cooldown"""
        current_time = pygame.time.get_ticks()
        if (hasattr(self.game, 'sounds') and 
            sound_name in self.game.sounds and 
            current_time - self.last_sound_time > 100):  # 100ms cooldown
            self.game.sounds[sound_name].play()
            self.last_sound_time = current_time
    
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
        
        # Handle controller input from pygame joystick events
        elif event.type == pygame.JOYBUTTONDOWN:
            # A button to select
            if event.button == 0:
                self._play_menu_sound('menu_select')
                return self._select_menu_item()

            # B button to go back
            elif event.button == 1:
                if self.current_menu == "main":
                    return "quit"
                else:
                    return "back"
        
        # Handle controller input from inputs library
        if controller_input:
            # D-pad navigation
            if controller_input.get('dpad_up', False):
                self.selected_item = (self.selected_item - 1) % len(self.menu_items[self.current_menu])
                self._play_menu_sound('menu_move')
                pygame.time.delay(200)
            
            elif controller_input.get('dpad_down', False):
                self.selected_item = (self.selected_item + 1) % len(self.menu_items[self.current_menu])
                self._play_menu_sound('menu_move')
                pygame.time.delay(200)
            
            # A button to select
            if controller_input.get('a', False):
                self._play_menu_sound('menu_select')
                return self._select_menu_item()

            # B button to go back
            elif controller_input.get('b', False):
                if self.current_menu == "main":
                    return "quit"
                else:
                    return "back"
            
            # Start button to toggle pause
            elif controller_input.get('start', False):
                if self.current_menu == "pause":
                    return "resume"
                elif self.current_menu != "main":
                    return "back"
        
        return None
    
    def _select_menu_item(self):
        """Select the current menu item and return its action"""
        if self.selected_item < len(self.menu_items[self.current_menu]):
            return self.menu_items[self.current_menu][self.selected_item]["action"]
        return None
    
    # [Rest of the file remains unchanged...]
    # Including all the render methods exactly as they were
    def render_main_menu(self):
        """Render the main menu"""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Draw background (will be a proper image later)
        pygame.draw.rect(self.screen, (50, 0, 0), (0, 0, self.width, self.height))
        
        # Draw logo
        logo = self.menu_assets["logo"]
        self.screen.blit(logo, (self.width // 2 - 200, 50))
        
        # Draw title
        title_text = self.title_font.render("DOOM PYTHON", True, (255, 0, 0))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 220))
        
        # Draw menu items
        self._render_menu_items("main")
        
        # Draw version info
        version_text = self.small_font.render("v0.1 - Python Recreation", True, (150, 150, 150))
        self.screen.blit(version_text, (self.width - version_text.get_width() - 20, self.height - 30))
    
    def render_pause(self):
        """Render the pause menu"""
        # Create a semi-transparent overlay with subtle noise effect
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0, 0, 0))
        
        # Add noise effect
        for i in range(0, self.width, 2):
            for j in range(0, self.height, 2):
                val = random.randint(0, 30)
                overlay.set_at((i, j), (val, val, val))
        
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        
        # Draw title with drop shadow
        title_text = self.title_font.render("PAUSED", True, (255, 0, 0))
        shadow_text = self.title_font.render("PAUSED", True, (50, 0, 0))
        self.screen.blit(shadow_text, (self.width // 2 - title_text.get_width() // 2 + 3, 103))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 100))
        
        # Draw menu items with animated selection
        self._render_menu_items("pause")
        
        # Draw subtle border effect
        border_color = (100, 0, 0)
        border_size = 5
        pygame.draw.rect(self.screen, border_color, (50, 50, self.width-100, self.height-100), border_size)

    def render_options(self):
        """Render the options menu"""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Draw background
        pygame.draw.rect(self.screen, (0, 0, 50), (0, 0, self.width, self.height))
        
        # Draw title
        title_text = self.title_font.render("OPTIONS", True, (0, 100, 255))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 100))
        
        # Draw menu items
        self._render_menu_items("options")
    
    def render_controls(self):
        """Render the controls menu"""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Draw background
        pygame.draw.rect(self.screen, (0, 50, 0), (0, 0, self.width, self.height))
        
        # Draw title
        title_text = self.title_font.render("CONTROLS", True, (0, 255, 0))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 100))
        
        # Draw menu items
        self._render_menu_items("controls")
    
    def _render_menu_items(self, menu_type):
        """Render menu items for the specified menu type"""
        items = self.menu_items.get(menu_type, [])
        
        for i, item in enumerate(items):
            # Determine text properties
            if i == self.selected_item:
                color = (255, 255, 0)  # Yellow for selected item
                # Add pulsing effect to selected item
                pulse = int(10 * math.sin(pygame.time.get_ticks() * 0.005))
                size = 32 + pulse
                font = pygame.font.SysFont("Arial", size, bold=True)
                
                # Draw selection indicator
                indicator_x = self.width // 2 - 150
                indicator_y = 300 + i * 50 + size//2 - 5
                pygame.draw.polygon(self.screen, color, [
                    (indicator_x, indicator_y),
                    (indicator_x + 20, indicator_y + 10),
                    (indicator_x, indicator_y + 20)
                ])
            else:
                color = (180, 180, 180)  # Light gray for unselected items
                font = self.menu_font
            
            # Render menu item text
            item_text = font.render(item["text"], True, color)
            
            # Position text in the center of the screen
            x = self.width // 2 - item_text.get_width() // 2
            y = 300 + i * 50
            
            # Draw text with drop shadow
            shadow_text = font.render(item["text"], True, (50, 50, 50))
            self.screen.blit(shadow_text, (x + 2, y + 2))
            self.screen.blit(item_text, (x, y))
    
    def set_menu(self, menu_type):
        """Set the current menu type"""
        if menu_type in self.menu_items:
            self.current_menu = menu_type
            self.selected_item = 0
    
    def render(self):
        """Render the current menu"""
        if self.current_menu == "main":
            self.render_main_menu()
        elif self.current_menu == "pause":
            self.render_pause()
        elif self.current_menu == "options":
            self.render_options()
        elif self.current_menu == "controls":
            self.render_controls()
        elif self.current_menu == "graphics":
            self.render_submenu("GRAPHICS", (0, 100, 200))
        elif self.current_menu == "sound":
            self.render_submenu("SOUND", (200, 100, 0))
        elif self.current_menu == "gameplay":
            self.render_submenu("GAMEPLAY", (100, 0, 200))
    
    def render_submenu(self, title, color):
        """Render a submenu with the given title and color"""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Draw background
        pygame.draw.rect(self.screen, (color[0]//4, color[1]//4, color[2]//4), (0, 0, self.width, self.height))
        
        # Draw title
        title_text = self.title_font.render(title, True, color)
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 100))
        
        # Draw menu items
        self._render_menu_items(self.current_menu)

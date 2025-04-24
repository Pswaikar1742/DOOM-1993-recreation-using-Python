"""
HUD (Heads-Up Display) class for DOOM recreation
"""
import math
import gc
import pygame

class HUD:
    """HUD class that renders player status information"""
    
    def __init__(self, screen, player):
        """Initialize the HUD"""
        self.screen = screen
        self.player = player
        
        # Screen dimensions
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Load fonts
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.message_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.kill_feed_font = pygame.font.SysFont("Arial", 20)
        
        # Kill feed
        self.kill_feed = []
        self.kill_feed_duration = 3.0  # seconds
        
        # Load HUD elements
        self.hud_elements = {}
        self._load_hud_elements()
        
        # Message display
        self.message = None
        self.message_timer = 0
    
    def _load_hud_elements(self):
        """Load HUD elements like health bar, ammo counter, etc."""
        # Try to load textures from the game
        try:
            # Get game instance
            from engine.game import Game
            game_instances = [obj for obj in gc.get_objects() if isinstance(obj, Game)]
            if game_instances:
                game = game_instances[0]
                
                # Load face textures
                if "face_normal" in game.textures:
                    self.hud_elements["face"] = game.textures["face_normal"]
                if "face_hurt" in game.textures:
                    self.hud_elements["face_hurt"] = game.textures["face_hurt"]
                
                # Load item textures
                for item in ["health", "armor", "ammo"]:
                    if item in game.textures:
                        self.hud_elements[item] = game.textures[item]
        except:
            pass
        
        # Create fallback elements if textures not loaded
        if "face" not in self.hud_elements:
            # Create face image placeholder
            face = pygame.Surface((50, 50))
            face.fill((200, 200, 0))  # Yellow placeholder
            pygame.draw.circle(face, (0, 0, 0), (15, 15), 5)  # Left eye
            pygame.draw.circle(face, (0, 0, 0), (35, 15), 5)  # Right eye
            pygame.draw.arc(face, (0, 0, 0), (10, 25, 30, 20), 0, math.pi, 3)  # Smile
            self.hud_elements["face"] = face
        
        if "face_hurt" not in self.hud_elements:
            # Create hurt face image placeholder
            face_hurt = pygame.Surface((50, 50))
            face_hurt.fill((200, 100, 0))  # Orange placeholder
            pygame.draw.line(face_hurt, (0, 0, 0), (10, 10), (20, 20), 3)  # Left eye X
            pygame.draw.line(face_hurt, (0, 0, 0), (20, 10), (10, 20), 3)  # Left eye X
            pygame.draw.line(face_hurt, (0, 0, 0), (30, 10), (40, 20), 3)  # Right eye X
            pygame.draw.line(face_hurt, (0, 0, 0), (40, 10), (30, 20), 3)  # Right eye X
            pygame.draw.arc(face_hurt, (0, 0, 0), (10, 30, 30, 15), math.pi, 2*math.pi, 3)  # Frown
            self.hud_elements["face_hurt"] = face_hurt
        
        # Create health bar surface
        health_bar = pygame.Surface((200, 20))
        health_bar.fill((100, 0, 0))  # Dark red background
        self.hud_elements["health_bar_bg"] = health_bar
        
        # Create armor bar surface
        armor_bar = pygame.Surface((200, 20))
        armor_bar.fill((0, 0, 100))  # Dark blue background
        self.hud_elements["armor_bar_bg"] = armor_bar
    
    def show_message(self, message, duration=2.0):
        """Show a message on the screen for a specified duration"""
        self.message = message
        self.message_timer = duration
    
    def update(self, dt):
        """Update HUD elements that need to be updated over time"""
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = None
                
        # Update kill feed timers
        for kill in self.kill_feed[:]:
            kill['timer'] -= dt
            if kill['timer'] <= 0:
                self.kill_feed.remove(kill)
    
    def add_kill_feed(self, enemy_type):
        """Add a kill message to the kill feed"""
        self.kill_feed.insert(0, {
            'text': f"Killed {enemy_type}",
            'timer': self.kill_feed_duration
        })
        # Keep only the last 5 kills
        if len(self.kill_feed) > 5:
            self.kill_feed = self.kill_feed[:5]

    def _render_kill_feed(self):
        """Render the kill feed in top right corner"""
        y_offset = 10
        for kill in self.kill_feed:
            # Calculate alpha based on remaining time (fade out effect)
            alpha = min(255, int(255 * (kill['timer'] / self.kill_feed_duration)))
            
            # Render kill text
            kill_text = self.kill_feed_font.render(kill['text'], True, (255, 0, 0))
            kill_text.set_alpha(alpha)
            
            # Position in top right
            x = self.width - kill_text.get_width() - 20
            self.screen.blit(kill_text, (x, y_offset))
            y_offset += kill_text.get_height() + 5

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
        for i in range(0, self.width, 4):
            for j in range(0, 120, 4):
                if (i + j) % 8 == 0:
                    pygame.draw.rect(hud_bg, (50, 50, 50), (i, j, 2, 2))
        
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
        crosshair_size = 10
        crosshair_color = (255, 0, 0)
        pygame.draw.line(self.screen, crosshair_color, 
                        (self.width // 2 - crosshair_size, self.height // 2),
                        (self.width // 2 + crosshair_size, self.height // 2), 2)
        pygame.draw.line(self.screen, crosshair_color, 
                        (self.width // 2, self.height // 2 - crosshair_size),
                        (self.width // 2, self.height // 2 + crosshair_size), 2)
        
        # Render message if active
        if self.message and self.message_timer > 0:
            self._render_message()
    
    def _render_message(self):
        """Render a message on the screen"""
        # Create message text
        message_text = self.message_font.render(self.message, True, (255, 255, 0))
        
        # Create background for message
        padding = 10
        msg_bg = pygame.Surface((message_text.get_width() + padding * 2, 
                                message_text.get_height() + padding * 2))
        msg_bg.fill((0, 0, 0))
        msg_bg.set_alpha(200)
        
        # Position message at top center of screen
        msg_x = self.width // 2 - message_text.get_width() // 2
        msg_y = 50
        
        # Draw message background and text
        self.screen.blit(msg_bg, (msg_x - padding, msg_y - padding))
        self.screen.blit(message_text, (msg_x, msg_y))
    
    def _render_health(self):
        """Render the health bar"""
        # Health bar background
        health_bar_bg = self.hud_elements["health_bar_bg"]
        self.screen.blit(health_bar_bg, (20, self.height - 90))
        
        # Health bar fill
        health_percent = max(0, self.player.health / self.player.max_health)
        health_width = int(200 * health_percent)
        health_bar = pygame.Surface((health_width, 20))
        health_bar.fill((255, 0, 0))  # Bright red
        self.screen.blit(health_bar, (20, self.height - 90))
        
        # Health text
        health_text = self.font.render(f"{self.player.health}%", True, (255, 255, 255))
        self.screen.blit(health_text, (230, self.height - 90))
    
    def _render_armor(self):
        """Render the armor bar"""
        # Armor bar background
        armor_bar_bg = self.hud_elements["armor_bar_bg"]
        self.screen.blit(armor_bar_bg, (20, self.height - 60))
        
        # Armor bar fill
        armor_percent = max(0, self.player.armor / self.player.max_armor)
        armor_width = int(200 * armor_percent)
        armor_bar = pygame.Surface((armor_width, 20))
        armor_bar.fill((0, 0, 255))  # Bright blue
        self.screen.blit(armor_bar, (20, self.height - 60))
        
        # Armor text
        armor_text = self.font.render(f"{self.player.armor}%", True, (255, 255, 255))
        self.screen.blit(armor_text, (230, self.height - 60))
    
    def _render_ammo(self):
        """Render the ammo counter"""
        # Only show bullets ammo
        if "bullets" in self.player.ammo:
            ammo_count = self.player.ammo["bullets"]
            max_ammo = self.player.max_ammo.get("bullets", 0)
            
            ammo_text = self.font.render(f"{ammo_count}/{max_ammo}", True, (255, 255, 255))
            self.screen.blit(ammo_text, (self.width - 150, self.height - 60))
            
            ammo_type_text = self.small_font.render("BULLETS", True, (200, 200, 200))
            self.screen.blit(ammo_type_text, (self.width - 150, self.height - 85))
    
    def _render_face(self):
        """Render the face status icon"""
        # Face changes based on health
        if self.player.health < 30 and "face_hurt" in self.hud_elements:
            face = self.hud_elements["face_hurt"]
        else:
            face = self.hud_elements["face"]
        self.screen.blit(face, (self.width // 2 - 25, self.height - 75))
    
    def _render_weapon(self):
        """Render the current weapon icon"""
        # Show current weapon name
        current_weapon = getattr(self.player, "current_weapon", "pistol")
        weapon_text = self.font.render(current_weapon.upper(), True, (255, 255, 255))
        self.screen.blit(weapon_text, (self.width - 150, self.height - 30))
    
    def _render_keys(self):
        """Render the keys the player has collected"""
        # This will show which keys the player has
        # For now, just placeholder text
        keys_text = self.small_font.render("KEYS: ", True, (200, 200, 200))
        self.screen.blit(keys_text, (20, self.height - 30))

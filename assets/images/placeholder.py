"""
Script to generate placeholder images for testing
"""
import os
import pygame
import numpy as np

def create_placeholder_images():
    """Create placeholder images for testing"""
    print("Starting to create placeholder images...")
    
    # Initialize pygame
    print("Initializing pygame...")
    pygame.init()
    
    # Create wall textures
    print("Creating wall textures...")
    create_wall_textures()
    
    # Create weapon sprites
    print("Creating weapon sprites...")
    create_weapon_sprites()
    
    # Create enemy sprites
    print("Creating enemy sprites...")
    create_enemy_sprites()
    
    # Create item sprites
    print("Creating item sprites...")
    create_item_sprites()
    
    # Create UI elements
    print("Creating UI elements...")
    create_ui_elements()
    
    print("Placeholder images created successfully!")

def create_wall_textures():
    """Create placeholder wall textures"""
    # Wall texture size
    size = 64
    
    # Create different wall textures
    textures = {
        "wall1": (200, 0, 0),    # Red wall
        "wall2": (0, 200, 0),    # Green wall
        "wall3": (0, 0, 200),    # Blue wall
        "door": (200, 200, 0),   # Yellow door
    }
    
    for name, color in textures.items():
        # Create surface
        surface = pygame.Surface((size, size))
        surface.fill(color)
        
        # Add some detail
        pygame.draw.rect(surface, (min(color[0] + 50, 255), 
                                  min(color[1] + 50, 255), 
                                  min(color[2] + 50, 255)), 
                        (5, 5, size - 10, size - 10))
        
        # Add grid lines
        for i in range(0, size, 16):
            pygame.draw.line(surface, (50, 50, 50), (0, i), (size, i), 1)
            pygame.draw.line(surface, (50, 50, 50), (i, 0), (i, size), 1)
        
        # Save image
        print(f"Saving {name}.png...")
        try:
            pygame.image.save(surface, f"{name}.png")
            print(f"Saved {name}.png successfully")
        except Exception as e:
            print(f"Error saving {name}.png: {e}")

def create_weapon_sprites():
    """Create placeholder weapon sprites"""
    # Weapon sprite size
    width, height = 200, 150
    
    # Create different weapon sprites
    weapons = {
        "pistol_idle": (150, 150, 150),
        "pistol_fire1": (200, 200, 0),
        "pistol_fire2": (250, 250, 0),
        "shotgun_idle": (100, 100, 100),
        "shotgun_fire1": (200, 100, 0),
        "shotgun_fire2": (250, 150, 0),
    }
    
    for name, color in weapons.items():
        # Create surface
        surface = pygame.Surface((width, height))
        surface.fill((0, 0, 0))  # Black background
        surface.set_colorkey((0, 0, 0))  # Make black transparent
        
        # Draw weapon shape
        if "pistol" in name:
            # Draw pistol shape
            pygame.draw.rect(surface, color, (width // 2 - 10, height - 60, 20, 40))
            pygame.draw.rect(surface, color, (width // 2 - 20, height - 40, 40, 20))
            
            # If firing, add muzzle flash
            if "fire" in name:
                flash_size = int(name[-1]) * 10
                pygame.draw.circle(surface, (255, 255, 0), 
                                 (width // 2, height - 70), flash_size)
        
        elif "shotgun" in name:
            # Draw shotgun shape
            pygame.draw.rect(surface, color, (width // 2 - 40, height - 50, 80, 20))
            pygame.draw.rect(surface, color, (width // 2 - 10, height - 70, 20, 50))
            
            # If firing, add muzzle flash
            if "fire" in name:
                flash_size = int(name[-1]) * 15
                pygame.draw.circle(surface, (255, 200, 0), 
                                 (width // 2, height - 80), flash_size)
        
        # Save image
        pygame.image.save(surface, f"{name}.png")

def create_enemy_sprites():
    """Create placeholder enemy sprites"""
    # Enemy sprite size
    width, height = 64, 64
    
    # Create different enemy sprites
    enemies = {
        "imp_idle1": (200, 0, 0),
        "imp_walk1": (200, 50, 0),
        "imp_attack1": (250, 0, 0),
        "demon_idle1": (150, 0, 150),
        "demon_walk1": (200, 0, 200),
        "demon_attack1": (250, 0, 250),
    }
    
    for name, color in enemies.items():
        # Create surface
        surface = pygame.Surface((width, height))
        surface.fill((0, 0, 0))  # Black background
        surface.set_colorkey((0, 0, 0))  # Make black transparent
        
        # Draw enemy shape
        if "imp" in name:
            # Draw imp shape (humanoid)
            pygame.draw.circle(surface, color, (width // 2, height // 4), width // 6)  # Head
            pygame.draw.rect(surface, color, (width // 3, height // 3, width // 3, height // 2))  # Body
            
            # If attacking, add attack animation
            if "attack" in name:
                pygame.draw.line(surface, (255, 0, 0), 
                               (width // 2, height // 2), 
                               (width, height // 2), 5)
        
        elif "demon" in name:
            # Draw demon shape (more monstrous)
            pygame.draw.circle(surface, color, (width // 2, height // 3), width // 4)  # Head
            pygame.draw.rect(surface, color, (width // 4, height // 2, width // 2, height // 2))  # Body
            
            # Add horns
            pygame.draw.line(surface, (100, 0, 100), 
                           (width // 3, height // 4), 
                           (width // 4, 0), 3)
            pygame.draw.line(surface, (100, 0, 100), 
                           (2 * width // 3, height // 4), 
                           (3 * width // 4, 0), 3)
            
            # If attacking, add attack animation
            if "attack" in name:
                pygame.draw.rect(surface, (255, 0, 0), 
                               (width // 4, 2 * height // 3, width // 2, height // 6))
        
        # Save image
        pygame.image.save(surface, f"{name}.png")

def create_item_sprites():
    """Create placeholder item sprites"""
    # Item sprite size
    size = 32
    
    # Create different item sprites
    items = {
        "health": (0, 200, 0),    # Green health pack
        "armor": (0, 0, 200),     # Blue armor
        "ammo": (200, 200, 0),    # Yellow ammo
        "key_red": (200, 0, 0),   # Red key
        "key_blue": (0, 0, 200),  # Blue key
        "key_yellow": (200, 200, 0),  # Yellow key
    }
    
    for name, color in items.items():
        # Create surface
        surface = pygame.Surface((size, size))
        surface.fill((0, 0, 0))  # Black background
        surface.set_colorkey((0, 0, 0))  # Make black transparent
        
        # Draw item shape
        if "health" in name:
            # Draw health pack (cross)
            pygame.draw.rect(surface, color, (size // 3, size // 8, size // 3, 3 * size // 4))
            pygame.draw.rect(surface, color, (size // 8, size // 3, 3 * size // 4, size // 3))
        
        elif "armor" in name:
            # Draw armor (shield)
            pygame.draw.polygon(surface, color, [
                (size // 2, size // 8),
                (size - size // 8, size // 3),
                (size - size // 8, 2 * size // 3),
                (size // 2, size - size // 8),
                (size // 8, 2 * size // 3),
                (size // 8, size // 3)
            ])
        
        elif "ammo" in name:
            # Draw ammo box
            pygame.draw.rect(surface, color, (size // 8, size // 4, 3 * size // 4, size // 2))
            pygame.draw.rect(surface, (50, 50, 50), (size // 4, size // 3, size // 2, size // 3))
        
        elif "key" in name:
            # Draw key
            pygame.draw.circle(surface, color, (size // 3, size // 3), size // 6)
            pygame.draw.rect(surface, color, (size // 3, size // 3, size // 2, size // 8))
            pygame.draw.rect(surface, color, (2 * size // 3, size // 3, size // 8, size // 3))
        
        # Save image
        pygame.image.save(surface, f"{name}.png")

def create_ui_elements():
    """Create placeholder UI elements"""
    # Create HUD elements
    
    # Face
    face = pygame.Surface((64, 64))
    face.fill((200, 200, 0))  # Yellow background
    pygame.draw.circle(face, (0, 0, 0), (20, 20), 5)  # Left eye
    pygame.draw.circle(face, (0, 0, 0), (44, 20), 5)  # Right eye
    pygame.draw.arc(face, (0, 0, 0), (15, 30, 34, 20), 0, 3.14, 3)  # Smile
    pygame.image.save(face, "face_normal.png")
    
    # Hurt face
    face_hurt = pygame.Surface((64, 64))
    face_hurt.fill((200, 100, 0))  # Orange background
    pygame.draw.line(face_hurt, (0, 0, 0), (15, 15), (25, 25), 3)  # Left eye X
    pygame.draw.line(face_hurt, (0, 0, 0), (25, 15), (15, 25), 3)  # Left eye X
    pygame.draw.line(face_hurt, (0, 0, 0), (39, 15), (49, 25), 3)  # Right eye X
    pygame.draw.line(face_hurt, (0, 0, 0), (49, 15), (39, 25), 3)  # Right eye X
    pygame.draw.arc(face_hurt, (0, 0, 0), (15, 35, 34, 20), 3.14, 6.28, 3)  # Frown
    pygame.image.save(face_hurt, "face_hurt.png")
    
    # Logo
    logo = pygame.Surface((400, 150))
    logo.fill((100, 0, 0))  # Dark red background
    font = pygame.font.SysFont("Arial", 72, bold=True)
    text = font.render("DOOM", True, (255, 0, 0))
    logo.blit(text, (100, 40))
    pygame.image.save(logo, "logo.png")

if __name__ == "__main__":
    create_placeholder_images()

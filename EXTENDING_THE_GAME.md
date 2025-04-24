# Extending the DOOM Python Recreation

This guide provides instructions and best practices for extending the DOOM Python Recreation with new features. Whether you want to add new enemies, weapons, levels, or gameplay mechanics, this document will help you understand how to integrate your additions with the existing codebase.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Adding New Enemies](#adding-new-enemies)
3. [Adding New Weapons](#adding-new-weapons)
4. [Creating New Levels](#creating-new-levels)
5. [Adding New Items](#adding-new-items)
6. [Extending the HUD](#extending-the-hud)
7. [Adding New Game Mechanics](#adding-new-game-mechanics)
8. [Performance Considerations](#performance-considerations)
9. [Testing Your Changes](#testing-your-changes)
10. [Contributing Guidelines](#contributing-guidelines)

## Getting Started

Before you start extending the game, make sure you understand the existing codebase:

1. Read the [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md) file to understand the overall architecture.
2. Review the [ARCHITECTURE.md](ARCHITECTURE.md) file to see how components interact.
3. For rendering-specific features, read [RAYCASTING_EXPLAINED.md](RAYCASTING_EXPLAINED.md).
4. Run the game and experiment with existing features to understand how they work.

## Adding New Enemies

To add a new enemy type to the game:

1. **Create Sprites**: Add sprite images for the new enemy in `assets/images/`.
   - Follow the naming convention: `enemy_type_state.png` (e.g., `cacodemon_idle1.png`).
   - Create sprites for different states: idle, walk, attack, pain, death.

2. **Add Sound Effects**: Add sound effects in `assets/sounds/`.
   - Follow the naming convention: `enemy_type_action.wav` (e.g., `cacodemon_sight.wav`).
   - Create sounds for: sight, attack, pain, death.

3. **Update Enemy Class**: Modify `engine/enemy.py` to include the new enemy type.
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

4. **Update Game Asset Loading**: Modify `engine/game.py` to load the new enemy assets.
   ```python
   # Load enemy textures
   for enemy in ["imp", "demon", "cacodemon"]:  # Add new enemy type
       for state in ["idle1", "walk1", "attack1", "pain1", "death1"]:
           texture_path = os.path.join(texture_dir, f"{enemy}_{state}.png")
           if os.path.exists(texture_path):
               self.textures[f"{enemy}_{state}"] = pygame.image.load(texture_path).convert_alpha()
   
   # Load enemy sounds
   for enemy in ["imp", "demon", "cacodemon"]:  # Add new enemy type
       for state in ["sight", "attack", "pain", "death"]:
           sound_path = os.path.join(sound_dir, f"{enemy}_{state}.wav")
           if os.path.exists(sound_path):
               self.sounds[f"{enemy}_{state}"] = pygame.mixer.Sound(sound_path)
   ```

5. **Add to Map Files**: Update map files to include the new enemy type.
   ```
   # Enemy spawns
   ENEMIES
   imp,5,10
   demon,15,10
   cacodemon,20,15  # New enemy type
   END_ENEMIES
   ```

## Adding New Weapons

To add a new weapon to the game:

1. **Create Sprites**: Add sprite images for the new weapon in `assets/images/`.
   - Follow the naming convention: `weapon_state.png` (e.g., `chaingun_idle.png`).
   - Create sprites for different states: idle, fire1, fire2, reload.

2. **Add Sound Effects**: Add sound effects in `assets/sounds/`.
   - Follow the naming convention: `weapon_action.wav` (e.g., `chaingun_fire.wav`).

3. **Update Weapon Class**: Modify `engine/weapon.py` to include the new weapon type.
   ```python
   def _set_properties(self):
       """Set weapon properties based on type"""
       # Default properties...
       
       # Type-specific properties
       if self.type == "fist":
           # Existing fist properties...
       elif self.type == "pistol":
           # Existing pistol properties...
       elif self.type == "chaingun":  # New weapon type
           self.damage = 10
           self.fire_rate = 8.0
           self.ammo_type = "bullets"
           self.ammo_per_shot = 1
           self.sprites = {
               "idle": ["chaingun_idle"],
               "fire": ["chaingun_fire1", "chaingun_fire2"]
           }
   ```

4. **Update WeaponManager**: Modify the `_create_weapons` method in `WeaponManager` class.
   ```python
   def _create_weapons(self):
       """Create all weapons"""
       weapon_types = ["fist", "pistol", "chaingun"]  # Add new weapon type
       
       for weapon_type in weapon_types:
           self.weapons[weapon_type] = Weapon(weapon_type)
   ```

5. **Update Game Asset Loading**: Modify `engine/game.py` to load the new weapon assets.
   ```python
   # Load weapon textures
   for weapon in ["pistol", "chaingun"]:  # Add new weapon type
       for state in ["idle", "fire1", "fire2"]:
           texture_path = os.path.join(texture_dir, f"{weapon}_{state}.png")
           if os.path.exists(texture_path):
               self.textures[f"{weapon}_{state}"] = pygame.image.load(texture_path).convert_alpha()
   
   # Load weapon sounds
   for sound in ["pistol_fire", "chaingun_fire", "no_ammo"]:  # Add new weapon sound
       sound_path = os.path.join(sound_dir, f"{sound}.wav")
       if os.path.exists(sound_path):
           self.sounds[sound] = pygame.mixer.Sound(sound_path)
   ```

6. **Add Weapon Pickup**: Add the weapon as a pickup item in map files.
   ```
   # Item spawns
   ITEMS
   health,3,3
   ammo,17,3
   chaingun,10,10  # New weapon pickup
   END_ITEMS
   ```

## Creating New Levels

To create a new level:

1. **Create a Map File**: Create a new map file in `assets/maps/` (e.g., `e1m2.txt`).
   - Follow the existing map format with MAP, ENEMIES, and ITEMS sections.
   - Use numbers for wall types and special characters for player start position.

2. **Define Wall Layout**: Design your level layout using the grid-based system.
   ```
   MAP
   222222222222222222222222222222
   211111111111111111111111111112
   210000000000000000000000000012
   # ... more map rows ...
   END_MAP
   ```

3. **Add Enemy Spawns**: Define where enemies should appear.
   ```
   ENEMIES
   imp,5,10
   demon,15,10
   # ... more enemy spawns ...
   END_ENEMIES
   ```

4. **Add Item Spawns**: Define where items should appear.
   ```
   ITEMS
   health,3,3
   ammo,17,3
   # ... more item spawns ...
   END_ITEMS
   ```

5. **Update Level Selection**: If you want to add level selection, modify the menu system in `ui/menu.py` to include the new level.

## Adding New Items

To add a new item type:

1. **Create Sprites**: Add sprite images for the new item in `assets/images/`.
   - Follow the naming convention: `item_name.png` (e.g., `armor_green.png`).

2. **Update Map Class**: Modify `engine/map.py` to handle the new item type.

3. **Update Player Class**: Modify `engine/player.py` to handle picking up the new item.
   ```python
   def pickup_item(self, item_type):
       """Handle item pickups from the map"""
       if item_type == "health":
           self.add_health(25)
       elif item_type == "armor":
           self.add_armor(50)
       elif item_type == "armor_green":  # New item type
           self.add_armor(100)
       elif item_type == "ammo":
           self.add_ammo("bullets", 20)
   ```

4. **Update Game Asset Loading**: Modify `engine/game.py` to load the new item assets.
   ```python
   # Load item textures
   for item in ["health", "armor", "armor_green", "ammo"]:  # Add new item type
       texture_path = os.path.join(texture_dir, f"{item}.png")
       if os.path.exists(texture_path):
           self.textures[item] = pygame.image.load(texture_path).convert_alpha()
   ```

5. **Add to Map Files**: Update map files to include the new item.
   ```
   # Item spawns
   ITEMS
   health,3,3
   armor_green,17,3  # New item type
   END_ITEMS
   ```

## Extending the HUD

To extend the HUD with new elements:

1. **Create HUD Graphics**: Add new HUD element images in `assets/images/`.

2. **Update HUD Class**: Modify `ui/hud.py` to include the new HUD elements.
   ```python
   def _load_hud_elements(self):
       """Load HUD elements like health bar, ammo counter, etc."""
       # Existing code...
       
       # Load new HUD elements
       for hud_element in ["face_normal", "face_hurt", "new_element"]:  # Add new element
           texture_path = os.path.join(texture_dir, f"{hud_element}.png")
           if os.path.exists(texture_path):
               self.hud_elements[hud_element] = pygame.image.load(texture_path).convert_alpha()
   ```

3. **Create Render Method**: Add a new render method for the new HUD element.
   ```python
   def _render_new_element(self):
       """Render the new HUD element"""
       if "new_element" in self.hud_elements:
           element = self.hud_elements["new_element"]
           self.screen.blit(element, (x_position, y_position))
   ```

4. **Update Main Render Method**: Modify the `render` method to call your new render method.
   ```python
   def render(self):
       """Render the HUD elements"""
       # Existing code...
       
       # Render new element
       self._render_new_element()
   ```

## Adding New Game Mechanics

To add new game mechanics:

1. **Identify Affected Components**: Determine which components need to be modified.

2. **Update Game Logic**: Modify the relevant files to implement the new mechanics.

3. **Add New Assets**: Create any new assets needed for the mechanics.

4. **Update Input Handling**: If the mechanic requires new input, update the input handling in `engine/game.py` and `engine/controller.py`.

5. **Update HUD**: If the mechanic needs to be displayed on the HUD, update `ui/hud.py`.

Example: Adding a sprint mechanic

```python
# In engine/player.py
def __init__(self, map_obj):
    # Existing code...
    self.stamina = 100
    self.max_stamina = 100
    self.sprint_speed = 7.0  # Faster than run_speed

def update(self, keys, mouse_dx, controller_input, dt):
    # Existing code...
    # Handle sprint
    if keys[pygame.K_LSHIFT] and self.stamina > 0:
        speed = self.sprint_speed
        self.stamina = max(0, self.stamina - 20 * dt)
    else:
        speed = self.run_speed if keys[pygame.K_LSHIFT] else self.move_speed
        self.stamina = min(self.max_stamina, self.stamina + 10 * dt)

# In ui/hud.py
def _render_stamina(self):
    """Render the stamina bar"""
    # Stamina bar background
    stamina_bar_bg = pygame.Surface((200, 10))
    stamina_bar_bg.fill((50, 50, 50))
    self.screen.blit(stamina_bar_bg, (20, self.height - 30))
    
    # Stamina bar fill
    stamina_percent = max(0, self.player.stamina / self.player.max_stamina)
    stamina_width = int(200 * stamina_percent)
    stamina_bar = pygame.Surface((stamina_width, 10))
    stamina_bar.fill((255, 255, 0))  # Yellow
    self.screen.blit(stamina_bar, (20, self.height - 30))

def render(self):
    # Existing code...
    self._render_stamina()
```

## Performance Considerations

When extending the game, keep these performance considerations in mind:

1. **Asset Optimization**: Keep textures and sounds at a reasonable size.
2. **Efficient Algorithms**: Use efficient algorithms for new game mechanics.
3. **Limit Object Count**: Don't spawn too many enemies or items at once.
4. **Use Distance Culling**: Don't render objects that are too far away.
5. **Profile Your Code**: Use profiling tools to identify performance bottlenecks.

## Testing Your Changes

Before submitting your changes:

1. **Test Thoroughly**: Make sure your additions work correctly and don't break existing functionality.
2. **Check Performance**: Ensure your changes don't significantly impact performance.
3. **Test on Different Systems**: If possible, test on different operating systems and hardware.
4. **Get Feedback**: Have others test your changes and provide feedback.

## Contributing Guidelines

When contributing to the project:

1. **Follow the Coding Style**: Match the existing coding style for consistency.
2. **Document Your Code**: Add comments and docstrings to explain your code.
3. **Update Documentation**: Update relevant documentation files to reflect your changes.
4. **Create a Pull Request**: Submit your changes as a pull request with a clear description of what you've added or changed.
5. **Be Open to Feedback**: Be willing to make changes based on feedback from the project maintainers.

By following these guidelines, you can successfully extend the DOOM Python Recreation with new features while maintaining compatibility with the existing codebase.

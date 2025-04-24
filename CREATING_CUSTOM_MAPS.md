# Creating Custom Maps for DOOM Python Recreation

This guide provides detailed instructions on how to create custom maps for the DOOM Python Recreation. Creating your own levels is a great way to extend the game and share your creativity with others.

## Table of Contents

1. [Map File Format](#map-file-format)
2. [Creating a Basic Map](#creating-a-basic-map)
3. [Map Symbols and Their Meanings](#map-symbols-and-their-meanings)
4. [Adding Enemies](#adding-enemies)
5. [Adding Items](#adding-items)
6. [Testing Your Map](#testing-your-map)
7. [Advanced Map Features](#advanced-map-features)
8. [Map Design Tips](#map-design-tips)
9. [Example Maps](#example-maps)
10. [Sharing Your Maps](#sharing-your-maps)

## Map File Format

Maps in the DOOM Python Recreation are defined in text files with a simple format. Each map file consists of three main sections:

1. **MAP**: Defines the layout of walls and empty spaces.
2. **ENEMIES**: Defines enemy spawn positions and types.
3. **ITEMS**: Defines item spawn positions and types.

Here's the basic structure of a map file:

```
# Map name and description
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

## Creating a Basic Map

To create a basic map:

1. **Create a New Text File**: Create a new text file in the `assets/maps/` directory with a name like `custom1.txt`.

2. **Define the Map Header**: Add a comment at the top with the map name and description.
   ```
   # Custom Map 1 - My First DOOM Map
   ```

3. **Start the Map Section**: Add the MAP marker to start the map section.
   ```
   MAP
   ```

4. **Define the Map Grid**: Create a grid of characters representing walls and empty spaces. The grid should be rectangular (all rows the same length).
   ```
   222222222222222222222222222222
   211111111111111111111111111112
   210000000000000000000000000012
   210001111001111000111100111012
   210001000000010000100000001012
   21000100P000010000100000001012
   210001000000010000100000001012
   210001111000000000100000001012
   210000000000000000100000001012
   210000000000000000100000001012
   210000222222200000100000001012
   210000200000200000100000001012
   210000200000200000100000001012
   210000200000200000100000001012
   210000200000200000100000001012
   210000222222200000100000001012
   210000000000000000100000001012
   210000000000000000100000001012
   210000000000000000100000001012
   210000000000000000100000001012
   210000000000000000100000001012
   210000000000000000100000001012
   210000000000000000100000001012
   210000000000000000100000001012
   210000000000000000100000001012
   210000000000000000100000001012
   210000000000000000100000001012
   210000000000000000100000001012
   210000000000000000111111111112
   222222222222222222222222222222
   ```

5. **End the Map Section**: Add the END_MAP marker to end the map section.
   ```
   END_MAP
   ```

6. **Add Enemy Spawns**: Define where enemies should appear.
   ```
   ENEMIES
   imp,5,10
   demon,15,10
   imp,10,15
   END_ENEMIES
   ```

7. **Add Item Spawns**: Define where items should appear.
   ```
   ITEMS
   health,3,3
   ammo,17,3
   armor,10,10
   END_ITEMS
   ```

8. **Save the File**: Save the file in the `assets/maps/` directory.

## Map Symbols and Their Meanings

The map grid uses the following symbols:

- **0**: Empty space (floor)
- **1**: Wall type 1 (standard wall)
- **2**: Wall type 2 (different texture)
- **3**: Door
- **P**: Player start position
- **E**: Enemy spawn point (alternative to ENEMIES section)
- **I**: Item spawn point (alternative to ITEMS section)

## Adding Enemies

Enemies are defined in the ENEMIES section with the format: `type,x,y`

Available enemy types:
- **imp**: Basic enemy with medium speed and low health
- **demon**: Stronger enemy with slower speed and higher health

Example:
```
ENEMIES
imp,5,10
demon,15,10
imp,10,15
demon,20,20
END_ENEMIES
```

The coordinates (x,y) refer to the grid position in the map, with (0,0) being the top-left corner.

## Adding Items

Items are defined in the ITEMS section with the format: `type,x,y`

Available item types:
- **health**: Restores player health
- **armor**: Adds armor protection
- **ammo**: Provides ammunition
- **shotgun**: Gives the player a shotgun weapon

Example:
```
ITEMS
health,3,3
ammo,17,3
armor,10,10
shotgun,5,5
END_ITEMS
```

## Testing Your Map

To test your custom map:

1. **Modify the Game Code**: Temporarily modify `engine/map.py` to load your custom map:
   ```python
   def __init__(self, level_num):
       """Initialize the map with a specific level"""
       self.level_num = level_num
       
       # Load the map data
       # Change this line to load your custom map
       # self.load_map()
       self.load_custom_map("custom1.txt")  # Load your custom map
   
   def load_custom_map(self, filename):
       """Load a custom map file"""
       map_file = f"assets/maps/{filename}"
       # Rest of the loading code is the same as load_map()
       # ...
   ```

2. **Run the Game**: Start the game and your custom map should load.

3. **Debug and Iterate**: If there are issues with your map, check the console for error messages, fix the issues, and try again.

## Advanced Map Features

### Multiple Wall Types

You can use different numbers (1, 2, 3) for different wall types, which will use different textures:

```
222222
211112
213132
211112
222222
```

### Secret Areas

Create secret areas by placing items in hidden rooms that require the player to find a way to access them:

```
2222222222
2100000002
2100000002
2100222002
2100200002
2100200002
2100222002
2100000002
2100000002
2222222222
```

### Complex Layouts

Create more complex layouts with corridors, rooms, and open areas:

```
222222222222222222222222
210000000000000000000012
210000000000000000000012
210000222222222222000012
210000200000000002000012
210000200000000002000012
210000200000000002000012
210000200000000002000012
210000222222222222000012
210000000000000000000012
210000000000000000000012
222222222222222222222222
```

## Map Design Tips

1. **Start Small**: Begin with a small, simple map to get familiar with the format.

2. **Balance Enemy Placement**: Don't place too many enemies close together, as this can make the game too difficult.

3. **Create Interesting Spaces**: Mix open areas with corridors and rooms to create varied gameplay.

4. **Strategic Item Placement**: Place health and ammo where players might need them after combat.

5. **Test Thoroughly**: Play through your map multiple times to ensure it's balanced and fun.

6. **Consider Flow**: Think about how the player will move through the map and ensure there's a logical progression.

7. **Add Secrets**: Hidden areas with valuable items add exploration value to your map.

8. **Use Comments**: Add comments in your map file to explain special areas or design choices.

## Example Maps

Here are some example maps to inspire your creations:

### Simple Arena

```
# Simple Arena
MAP
222222222222222222222222
210000000000000000000012
210000000000000000000012
210000000000000000000012
210000000000000000000012
210000000P00000000000012
210000000000000000000012
210000000000000000000012
210000000000000000000012
210000000000000000000012
222222222222222222222222
END_MAP

ENEMIES
imp,5,5
imp,15,5
demon,10,8
END_ENEMIES

ITEMS
health,3,3
ammo,17,3
armor,10,2
END_ITEMS
```

### Maze

```
# Maze
MAP
222222222222222222222222
200000000000000000000002
202222222222222222222202
202000000000000000000202
202022222222222222220202
202020000000000000020202
202020222222222222020202
202020200000000002020202
202020202222222202020202
202020200000000202020202
202020222222220202020202
202020000000020202020202
202022222222220202020202
202000000000000202020202
202222222222222202020202
200000000000000002020202
222222222222222222020202
2P0000000000000000020202
222222222222222222220202
200000000000000000000202
202222222222222222222202
200000000000000000000002
222222222222222222222222
END_MAP

ENEMIES
imp,3,3
imp,19,3
demon,10,10
imp,3,19
imp,19,19
END_ENEMIES

ITEMS
health,1,1
health,21,1
health,1,21
health,21,21
ammo,10,5
ammo,5,10
ammo,15,10
armor,10,15
END_ITEMS
```

### Multi-Room Level

```
# Multi-Room Level
MAP
2222222222222222222222222222222222222
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2000000P00000002000000000000000000002
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2222222222222222222222222222222000002
2000000000000000000000000000002000002
2000000000000000000000000000002000002
2000000000000000000000000000002000002
2000000000000000000000000000002000002
2000000000000000000000000000002000002
2000000000000000000000000000002000002
2000000000000000000000000000002000002
2000000000000000000000000000002000002
2000000000000000000000000000002000002
2222222222222222222222222222222000002
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2000000000000002000000000000000000002
2222222222222222222222222222222222222
END_MAP

ENEMIES
imp,5,5
demon,25,5
imp,5,25
demon,25,25
imp,15,15
END_ENEMIES

ITEMS
health,3,3
health,33,3
health,3,27
health,33,27
ammo,15,5
ammo,25,15
ammo,15,25
armor,15,15
shotgun,5,15
END_ITEMS
```

## Sharing Your Maps

To share your custom maps with others:

1. **Package Your Map File**: Make sure your map file is complete and tested.

2. **Document Your Map**: Create a README file that explains your map's concept, difficulty level, and any special features.

3. **Share the File**: Share your map file through forums, social media, or file-sharing platforms.

4. **Installation Instructions**: Provide clear instructions for others to install your map:
   - Place the map file in the `assets/maps/` directory
   - Modify `engine/map.py` to load the custom map (as described in the Testing section)

By following this guide, you can create and share your own custom maps for the DOOM Python Recreation, extending the game with your own creative levels and challenges.

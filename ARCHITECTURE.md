# DOOM Python Recreation - Architecture

This document provides a visual overview of the architecture and component relationships in the DOOM Python Recreation project.

## System Architecture

```
                                +-------------------+
                                |      main.py      |
                                | (Entry Point)     |
                                +--------+----------+
                                         |
                                         v
                     +-------------------+-------------------+
                     |              engine/game.py           |
                     |         (Main Game Controller)        |
                     +-------------------+-------------------+
                                         |
                     +-------------------+-------------------+
                     |                                       |
         +-----------v-----------+               +-----------v-----------+
         |    Game Components    |               |     UI Components     |
         +-----------------------+               +-----------------------+
         |                       |               |                       |
+--------v-------+    +----------v---------+     +---------v--------+    +--------v--------+
|   raycasting   |    |       player       |     |        hud       |    |      menu       |
+----------------+    +--------------------+     +------------------+    +-----------------+
|  - 3D Rendering |    | - Movement        |     | - Health Display |    | - Main Menu     |
|  - Wall Textures|    | - Collision       |     | - Ammo Counter   |    | - Pause Menu    |
|  - Sprites      |    | - Combat          |     | - Face Display   |    | - Options       |
+--------+-------+    +----------+---------+     +---------+--------+    +-----------------+
         |                       |                         |
         |                       |                         |
+--------v-------+    +----------v---------+     +---------v--------+
|      map       |    |       weapon       |     |    controller    |
+----------------+    +--------------------+     +------------------+
| - Level Loading |    | - Weapon Types    |     | - Xbox Controller|
| - Collision     |    | - Firing Logic    |     | - Input Mapping  |
| - Enemy Spawns  |    | - Ammo Management |     | - Vibration      |
+--------+-------+    +--------------------+     +------------------+
         |
         |
+--------v-------+
|     enemy      |
+----------------+
| - AI States    |
| - Pathfinding  |
| - Combat       |
+----------------+
```

## Data Flow

```
+-------------+     +-------------+     +-------------+
|   Input     | --> |    Game     | --> |   Render    |
|   System    |     |    Logic    |     |   System    |
+-------------+     +-------------+     +-------------+
| - Keyboard  |     | - Update    |     | - Raycaster |
| - Mouse     |     |   Positions |     | - HUD       |
| - Controller|     | - Collision |     | - Sprites   |
|             |     | - AI        |     | - Menus     |
+-------------+     +-------------+     +-------------+
```

## Component Relationships

### Player Interactions

```
                  +----------------+
                  |     Player     |
                  +-------+--------+
                          |
          +---------------+---------------+
          |               |               |
+---------v------+ +------v-------+ +----v-----------+
|    Weapons     | |     Map      | |    Enemies     |
+----------------+ +--------------+ +----------------+
| - Fire Weapon  | | - Collision  | | - Take Damage  |
| - Switch Weapon| | - Item Pickup| | - Attack Player|
+----------------+ +--------------+ +----------------+
```

### Rendering Pipeline

```
+----------------+     +----------------+     +----------------+
|    Player      | --> |   Raycaster    | --> |    Screen      |
|    Position    |     |                |     |    Buffer      |
+----------------+     +-------+--------+     +----------------+
                               |
                 +-------------+-------------+
                 |             |             |
        +--------v-----+ +-----v------+ +----v---------+
        |    Walls     | |  Sprites   | |     HUD      |
        +--------------+ +------------+ +--------------+
        | - Texturing  | | - Enemies  | | - Health Bar |
        | - Shading    | | - Items    | | - Ammo Count |
        +--------------+ +------------+ +--------------+
```

## State Management

```
+----------------+
|   Game State   |
+-------+--------+
        |
+-------v--------+
|  State Machine  |
+----------------+
|                |
+-------+--------+
        |
+-------v--------+     +----------------+     +----------------+
|   Main Game    | <-> |  Pause Menu    | <-> |  Main Menu     |
+----------------+     +----------------+     +----------------+
```

## Map Format Structure

```
+----------------+
|   Map File     |
+-------+--------+
        |
+-------v--------+
|  Map Section   |
+----------------+
| 1 = Wall Type 1|
| 2 = Wall Type 2|
| 3 = Door       |
| 0 = Empty Space|
| P = Player     |
+----------------+
        |
+-------v--------+     +----------------+
| Enemy Section  |     |  Item Section  |
+----------------+     +----------------+
| type,x,y       |     | type,x,y       |
+----------------+     +----------------+
```

## Class Hierarchy

```
                  +----------------+
                  |     Entity     |
                  +-------+--------+
                          |
          +---------------+---------------+
          |                               |
+---------v------+                 +------v-------+
|     Player     |                 |    Enemy     |
+----------------+                 +--------------+
                                           |
                                   +-------+-------+
                                   |               |
                           +-------v-----+ +-------v-----+
                           |     Imp     | |    Demon    |
                           +-------------+ +-------------+
```

## Asset Management

```
+----------------+
|    Assets      |
+-------+--------+
        |
+-------v--------+     +----------------+     +----------------+
|    Images      |     |    Sounds      |     |     Maps       |
+----------------+     +----------------+     +----------------+
| - Wall Textures|     | - Weapon Sounds|     | - Level Data   |
| - Sprites      |     | - Enemy Sounds |     | - Enemy Spawns |
| - HUD Elements |     | - UI Sounds    |     | - Item Spawns  |
+----------------+     +----------------+     +----------------+
```

## Game Loop

```
+----------------+
|    Game Loop   |
+-------+--------+
        |
        v
+-------+--------+
| Process Input  |
+-------+--------+
        |
        v
+-------+--------+
|  Update State  |
+-------+--------+
        |
        v
+-------+--------+
|    Render      |
+-------+--------+
        |
        v
+-------+--------+
| Maintain FPS   |
+-------+--------+
        |
        v
+-------+--------+
|   Repeat Loop  |
+----------------+
```

This architectural overview provides a visual representation of how the different components of the DOOM Python Recreation project interact with each other. The modular design allows for easy maintenance and extension of the codebase.

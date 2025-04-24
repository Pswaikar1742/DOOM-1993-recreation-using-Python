# DOOM Python Recreation

![DOOM Python](doom/assets/images/logo.png)

A recreation of the classic DOOM (1993) game using Python and Pygame. This project implements the core mechanics and feel of the original game while using modern programming techniques and libraries.

## Overview

This project is a faithful recreation of the iconic DOOM game, featuring:

- Raycasting engine for pseudo-3D rendering
- Player movement and combat mechanics
- Enemy AI with different enemy types (Imps, Demons)
- Weapon system with multiple weapons
- Classic DOOM-style HUD and menus
- Xbox controller support
- Sound effects and basic ambient audio

## Screenshots

(Screenshots would be placed here)

## Requirements

- Python 3.8+
- Pygame 2.5.0+
- Inputs 0.5+ (for controller support)
- NumPy 1.24.0+

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/doom-python.git
   cd doom-python
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the game:
   ```
   python run.py
   ```

## Controls

### Keyboard/Mouse

- **WASD**: Movement
- **Mouse**: Look around
- **Left Click**: Shoot
- **1-2**: Switch weapons
- **E**: Use/Interact
- **Space**: Jump
- **Shift**: Run
- **Esc**: Pause menu

### Xbox Controller

- **Left Stick**: Movement
- **Right Stick**: Look around
- **Right Trigger**: Shoot
- **Left Trigger**: Aim
- **A**: Jump
- **X**: Use/Interact
- **Y**: Switch weapon
- **B**: Melee attack
- **Start**: Pause menu

## Project Structure

- `assets/`: Game assets (images, sounds, maps)
  - `images/`: Textures and sprites
  - `sounds/`: Sound effects
  - `maps/`: Level definitions
- `engine/`: Game engine components
  - `player.py`: Player movement and combat
  - `enemy.py`: Enemy AI and behavior
  - `weapon.py`: Weapon mechanics
  - `map.py`: Map loading and collision detection
  - `raycasting.py`: 3D rendering engine
  - `controller.py`: Xbox controller support
- `ui/`: User interface components
  - `menu.py`: Game menus
  - `hud.py`: Heads-up display
- `main.py`: Main entry point
- `run.py`: Setup and launcher script

## Code Documentation

For detailed documentation of the codebase, architecture, and implementation details, see [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md).

## Features

### Raycasting Engine

The game uses a raycasting technique similar to the original DOOM to create a pseudo-3D environment. This approach casts rays from the player's viewpoint to determine what is visible and at what distance, creating the illusion of 3D space.

### Enemy AI

Enemies use a state machine to control their behavior:
- **Idle**: Standing still until they detect the player
- **Chase**: Moving toward the player
- **Attack**: Attacking when in range
- **Pain**: Reacting to being hit
- **Dead**: Death animation and removal

### Weapon System

The weapon system supports multiple weapons with different properties:
- **Pistol**: Basic starting weapon
- **Shotgun**: More powerful but slower firing rate

Each weapon has its own damage, fire rate, and ammunition type.

### Map System

Maps are loaded from text files with a simple format:
- Numbers represent different wall types
- Special characters mark player start positions and enemy spawns
- Additional sections define enemy and item placements

## Development

This is a recreation of DOOM (1993) using Python and modern libraries. The goal is to create a faithful recreation of the original game while adding modern features like controller support.

### Future Enhancements

- More enemy types
- Additional weapons
- More levels
- Multiplayer support
- Custom map editor

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is for educational purposes only. DOOM is a registered trademark of id Software LLC, a ZeniMax Media company.

## Acknowledgments

- id Software for creating the original DOOM
- The Pygame community for the excellent game development library
- All contributors to this project

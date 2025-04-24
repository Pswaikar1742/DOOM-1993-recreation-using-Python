#!/usr/bin/env python3
"""
DOOM 1993 Recreation in Python
Main entry point for the game
"""
import sys
import pygame
import numpy as np
from engine.game import Game

def main():
    """Main function to initialize and run the game"""
    # Initialize pygame
    pygame.init()
    
    # Create game instance
    game = Game()
    
    try:
        # Run the game loop
        game.run()
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        # Clean up
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()

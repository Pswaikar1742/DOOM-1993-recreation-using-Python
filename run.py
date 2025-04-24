#!/usr/bin/env python3
"""
DOOM Python Recreation
Run script to start the game
"""
import os
import sys
import subprocess

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import pygame
        import numpy
        import inputs
        return True
    except ImportError as e:
        print(f"Missing required package: {e}")
        return False

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    subprocess.call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def generate_assets():
    """Generate placeholder assets if they don't exist"""
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if placeholder images exist
    if not os.path.exists(os.path.join(script_dir, "assets", "images", "wall1.png")):
        print("Generating placeholder images...")
        # Change to the images directory
        os.chdir(os.path.join(script_dir, "assets", "images"))
        # Run the placeholder script
        subprocess.call([sys.executable, "placeholder.py"])
        # Change back to the script directory
        os.chdir(script_dir)
    
    # Check if placeholder sounds exist
    if not os.path.exists(os.path.join(script_dir, "assets", "sounds", "pistol_fire.wav")):
        print("Generating placeholder sounds...")
        # Change to the sounds directory
        os.chdir(os.path.join(script_dir, "assets", "sounds"))
        # Run the placeholder script
        subprocess.call([sys.executable, "placeholder.py"])
        # Change back to the script directory
        os.chdir(script_dir)

def main():
    """Main function"""
    # Check if requirements are installed
    if not check_requirements():
        print("Would you like to install the required packages? (y/n)")
        choice = input().lower()
        if choice == "y":
            install_requirements()
        else:
            print("Cannot run the game without required packages.")
            return
    
    # Generate placeholder assets
    generate_assets()
    
    # Run the game
    print("Starting DOOM Python Recreation...")
    subprocess.call([sys.executable, "main.py"])

if __name__ == "__main__":
    main()

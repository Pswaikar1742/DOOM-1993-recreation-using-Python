"""
Script to generate placeholder sound effects for testing
"""
import os
import math
import wave
import struct
import numpy as np

def create_placeholder_sounds():
    """Create placeholder sound effects for testing"""
    # Create weapon sounds
    create_weapon_sounds()
    
    # Create enemy sounds
    create_enemy_sounds()
    
    # Create player sounds
    create_player_sounds()
    
    # Create ambient sounds
    create_ambient_sounds()
    
    print("Placeholder sounds created successfully!")

def create_wave_file(filename, frequency, duration, volume=0.5, sample_rate=44100):
    """Create a simple wave file with the given parameters"""
    # Calculate the number of frames
    num_frames = int(duration * sample_rate)
    
    # Create the wave file
    with wave.open(f"{filename}.wav", "w") as wav_file:
        # Set parameters
        wav_file.setparams((1, 2, sample_rate, num_frames, "NONE", "not compressed"))
        
        # Generate frames
        for i in range(num_frames):
            # Calculate the value at this frame
            t = i / sample_rate
            value = int(volume * 32767.0 * math.sin(2 * math.pi * frequency * t))
            
            # Write the frame
            wav_file.writeframes(struct.pack('h', value))

def create_noise_file(filename, duration, volume=0.5, sample_rate=44100):
    """Create a noise wave file with the given parameters"""
    # Calculate the number of frames
    num_frames = int(duration * sample_rate)
    
    # Create the wave file
    with wave.open(f"{filename}.wav", "w") as wav_file:
        # Set parameters
        wav_file.setparams((1, 2, sample_rate, num_frames, "NONE", "not compressed"))
        
        # Generate frames
        for i in range(num_frames):
            # Generate random noise
            value = int(volume * 32767.0 * (2 * np.random.random() - 1))
            
            # Write the frame
            wav_file.writeframes(struct.pack('h', value))

def create_weapon_sounds():
    """Create placeholder weapon sounds"""
    # Pistol shot
    create_wave_file("pistol_fire", 440, 0.2, 0.8)
    
    # Shotgun shot
    create_noise_file("shotgun_fire", 0.3, 0.9)
    
    # Chaingun shot
    create_wave_file("chaingun_fire", 220, 0.1, 0.7)
    
    # Rocket launch
    create_wave_file("rocket_fire", 110, 0.5, 0.9)
    
    # Plasma shot
    create_wave_file("plasma_fire", 880, 0.2, 0.6)
    
    # BFG charge
    create_wave_file("bfg_charge", 55, 1.0, 0.5)
    
    # BFG fire
    create_noise_file("bfg_fire", 1.0, 1.0)
    
    # No ammo click
    create_wave_file("no_ammo", 220, 0.1, 0.3)

def create_enemy_sounds():
    """Create placeholder enemy sounds"""
    # Imp sight
    create_wave_file("imp_sight", 220, 0.5, 0.5)
    
    # Imp attack
    create_wave_file("imp_attack", 330, 0.3, 0.7)
    
    # Imp pain
    create_wave_file("imp_pain", 440, 0.2, 0.6)
    
    # Imp death
    create_wave_file("imp_death", 110, 0.8, 0.8)
    
    # Demon sight
    create_wave_file("demon_sight", 110, 0.7, 0.6)
    
    # Demon attack
    create_wave_file("demon_attack", 165, 0.4, 0.8)
    
    # Demon pain
    create_wave_file("demon_pain", 220, 0.3, 0.7)
    
    # Demon death
    create_wave_file("demon_death", 55, 1.0, 0.9)

def create_player_sounds():
    """Create placeholder player sounds"""
    # Player pain
    create_wave_file("player_pain", 440, 0.3, 0.6)
    
    # Player death
    create_wave_file("player_death", 110, 1.0, 0.8)
    
    # Player jump
    create_wave_file("player_jump", 660, 0.2, 0.4)
    
    # Player land
    create_wave_file("player_land", 220, 0.3, 0.5)
    
    # Player pickup
    create_wave_file("player_pickup", 880, 0.2, 0.4)

def create_ambient_sounds():
    """Create placeholder ambient sounds"""
    # Door open
    create_wave_file("door_open", 220, 0.5, 0.5)
    
    # Door close
    create_wave_file("door_close", 110, 0.5, 0.5)
    
    # Switch
    create_wave_file("switch", 440, 0.2, 0.4)
    
    # Explosion
    create_noise_file("explosion", 0.8, 0.9)
    
    # Ambient background
    create_wave_file("ambient", 55, 5.0, 0.2)

if __name__ == "__main__":
    create_placeholder_sounds()

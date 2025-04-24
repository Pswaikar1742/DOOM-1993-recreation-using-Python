"""
Controller class for DOOM recreation
Handles Xbox controller input
"""
import pygame
import threading
import time
from inputs import get_gamepad, devices

class Controller:
    """Controller class that handles Xbox controller input"""
    
    def __init__(self):
        """Initialize the controller"""
        self.input_state = {
            # Analog sticks
            'left_stick_x': 0.0,
            'left_stick_y': 0.0,
            'right_stick_x': 0.0,
            'right_stick_y': 0.0,
            
            # Triggers
            'left_trigger': 0.0,
            'right_trigger': 0.0,
            
            # Buttons
            'a': False,
            'b': False,
            'x': False,
            'y': False,
            'lb': False,
            'rb': False,
            'start': False,
            'back': False,
            
            # D-pad
            'dpad_up': False,
            'dpad_down': False,
            'dpad_left': False,
            'dpad_right': False
        }
        
        # Check if controller is connected
        self.controller_connected = False
        self.check_controller()
        
        # Start controller input thread if controller is connected
        if self.controller_connected:
            self.running = True
            self.input_thread = threading.Thread(target=self._controller_input_loop)
            self.input_thread.daemon = True
            self.input_thread.start()
    
    def check_controller(self):
        """Check if a controller is connected"""
        try:
            # Check if any gamepads are connected
            if devices:
                for device in devices:
                    if 'Microsoft X-Box' in device.name or 'RedGear' in device.name or 'gamepad' in device.name.lower() or 'controller' in device.name.lower():
                        self.controller_connected = True
                        print(f"Controller detected: {device.name}")
                        return
            
            # If we get here, no controller was found
            self.controller_connected = False
            print("No compatible controller detected")
        except Exception as e:
            print(f"Error checking for controller: {e}")
            self.controller_connected = False
    
    def _controller_input_loop(self):
        """Background thread to continuously read controller input"""
        while self.running:
            try:
                # Get events from the gamepad
                events = get_gamepad()
                
                for event in events:
                    self._process_controller_event(event)
            
            except Exception as e:
                print(f"Controller input error: {e}")
                time.sleep(0.1)  # Avoid busy-waiting if there's an error
    
    def _process_controller_event(self, event):
        """Process a single controller event"""
        # Debug controller events to help identify mappings
        # print(f"Controller event: {event.code} - {event.state}")
        
        # Analog sticks - support multiple possible mappings
        if event.code in ['ABS_X', 'ABS_0']:
            # Left stick X axis
            self.input_state['left_stick_x'] = self._normalize_stick_input(event.state)
        
        elif event.code in ['ABS_Y', 'ABS_1']:
            # Left stick Y axis (inverted because Y is positive downward)
            self.input_state['left_stick_y'] = -self._normalize_stick_input(event.state)
        
        elif event.code in ['ABS_RX', 'ABS_Z', 'ABS_3']:
            # Right stick X axis
            self.input_state['right_stick_x'] = self._normalize_stick_input(event.state)
        
        elif event.code in ['ABS_RY', 'ABS_RZ', 'ABS_4']:
            # Right stick Y axis (inverted)
            self.input_state['right_stick_y'] = -self._normalize_stick_input(event.state)
        
        # Triggers - support multiple possible mappings
        elif event.code in ['ABS_Z', 'ABS_2', 'BTN_TL2']:
            # Left trigger
            if isinstance(event.state, bool):
                self.input_state['left_trigger'] = 1.0 if event.state else 0.0
            else:
                self.input_state['left_trigger'] = event.state / 255.0
        
        elif event.code in ['ABS_RZ', 'ABS_5', 'BTN_TR2']:
                # Right trigger
                if isinstance(event.state, bool):
                    self.input_state['right_trigger'] = 1.0 if event.state else 0.0
                else:
                    self.input_state['right_trigger'] = event.state / 255.0


        
        # Buttons - support multiple possible mappings
        elif event.code in ['BTN_SOUTH', 'BTN_A', 'BTN_0']:
            # A button
            self.input_state['a'] = bool(event.state)
            # A button can be used for interaction or jumping
            self.input_state['interact'] = bool(event.state)
        
        elif event.code in ['BTN_EAST', 'BTN_B', 'BTN_1']:
            # B button
            self.input_state['b'] = bool(event.state)
            # B button can be used for secondary action
            self.input_state['secondary_action'] = bool(event.state)
        
        elif event.code in ['BTN_WEST', 'BTN_X', 'BTN_2']:
            # X button
            self.input_state['x'] = bool(event.state)
            # X button can be used for reloading
            self.input_state['reload'] = bool(event.state)
        
        elif event.code in ['BTN_NORTH', 'BTN_Y', 'BTN_3']:
            # Y button
            self.input_state['y'] = bool(event.state)
            # Y button can be used for weapon switching
            self.input_state['switch_weapon'] = bool(event.state)
        
        elif event.code in ['BTN_TL', 'BTN_4']:
            # Left bumper
            self.input_state['lb'] = bool(event.state)
            # Left bumper can be used for previous weapon
            self.input_state['prev_weapon'] = bool(event.state)
        
        elif event.code in ['BTN_TR', 'BTN_5']:
            # Right bumper
            self.input_state['rb'] = bool(event.state)
            # Right bumper is now used for firing
            self.input_state['fire'] = bool(event.state)
            # Also track for next weapon if needed
            self.input_state['next_weapon'] = bool(event.state)




        
        elif event.code in ['BTN_START', 'BTN_8', 'BTN_7']:
            # Start button
            self.input_state['start'] = bool(event.state)
        
        elif event.code in ['BTN_SELECT', 'BTN_6', 'BTN_9']:
            # Back/Select button
            self.input_state['back'] = bool(event.state)
        
        # D-pad - support multiple possible mappings
        elif event.code in ['ABS_HAT0X', 'ABS_6']:
            # D-pad X axis
            self.input_state['dpad_left'] = event.state == -1
            self.input_state['dpad_right'] = event.state == 1
            
            # D-pad left/right can be used for weapon switching
            if event.state == -1:
                self.input_state['prev_weapon'] = True
                self._vibrate(0.3, 0.1)  # Light vibration for weapon switch
            elif event.state == 1:
                self.input_state['next_weapon'] = True
                self._vibrate(0.3, 0.1)  # Light vibration for weapon switch
            else:
                self.input_state['prev_weapon'] = False
                self.input_state['next_weapon'] = False
        
        elif event.code in ['ABS_HAT0Y', 'ABS_7']:
            # D-pad Y axis
            self.input_state['dpad_up'] = event.state == -1
            self.input_state['dpad_down'] = event.state == 1
        
        # Individual D-pad buttons (some controllers use these)
        elif event.code == 'BTN_DPAD_UP':
            self.input_state['dpad_up'] = bool(event.state)
        elif event.code == 'BTN_DPAD_DOWN':
            self.input_state['dpad_down'] = bool(event.state)
        elif event.code == 'BTN_DPAD_LEFT':
            self.input_state['dpad_left'] = bool(event.state)
            if bool(event.state):
                self.input_state['prev_weapon'] = True
                self._vibrate(0.3, 0.1)  # Light vibration for weapon switch
            else:
                self.input_state['prev_weapon'] = False
        elif event.code == 'BTN_DPAD_RIGHT':
            self.input_state['dpad_right'] = bool(event.state)
            if bool(event.state):
                self.input_state['next_weapon'] = True
                self._vibrate(0.3, 0.1)  # Light vibration for weapon switch
            else:
                self.input_state['next_weapon'] = False
    
    def _normalize_stick_input(self, value):
        """Normalize analog stick input to range -1.0 to 1.0 with deadzone"""
        # Normalize to -1.0 to 1.0
        normalized = value / 32768.0
        
        # Apply deadzone
        deadzone = 0.15
        if abs(normalized) < deadzone:
            return 0.0
        
        # Adjust for deadzone
        return (normalized - deadzone * (1 if normalized > 0 else -1)) / (1.0 - deadzone)
    
    def handle_event(self, event):
        """Handle pygame events for controller connection/disconnection"""
        # Check for controller connection/disconnection events
        if event.type == pygame.JOYDEVICEADDED:
            self.check_controller()
            if self.controller_connected and not hasattr(self, 'input_thread'):
                self.running = True
                self.input_thread = threading.Thread(target=self._controller_input_loop)
                self.input_thread.daemon = True
                self.input_thread.start()
        
        elif event.type == pygame.JOYDEVICEREMOVED:
            self.controller_connected = False
            if hasattr(self, 'input_thread'):
                self.running = False
                self.input_thread.join(timeout=1.0)
                delattr(self, 'input_thread')
    
    def get_input(self):
        """Get the current controller input state"""
        if not self.controller_connected:
            return None
        
        return self.input_state.copy()
    
    def _vibrate(self, intensity=0.5, duration=0.2):
        """Vibrate the controller (if supported)"""
        try:
            # Try to use pygame's joystick rumble feature
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            for joystick in joysticks:
                if joystick.get_init() and hasattr(joystick, 'rumble'):
                    joystick.rumble(intensity, intensity, int(duration * 1000))
                    return
        except Exception as e:
            # Silently fail if vibration is not supported
            pass
    
    def shutdown(self):
        """Shutdown the controller input thread"""
        if hasattr(self, 'input_thread'):
            self.running = False
            self.input_thread.join(timeout=1.0)

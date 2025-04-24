"""
Base Entity class for all game objects
"""
class Entity:
    """Base class for all game entities"""
    
    def __init__(self, x, y):
        """Initialize entity with position"""
        self.x = x
        self.y = y
        self.size = 0.5  # Default hitbox size
        self.health = 100  # Default health
        self.alive = True
        self.map = None  # Will be set by game when added to map
        
    def update(self, dt):
        """Update entity state"""
        pass  # To be overridden by subclasses
        
    def take_damage(self, amount):
        """Handle taking damage"""
        self.health -= amount
        if self.health <= 0:
            self.alive = False
            
    def collides_with(self, other):
        """Check collision with another entity"""
        if not self.alive or not other.alive:
            return False
            
        dx = self.x - other.x
        dy = self.y - other.y
        distance = (dx*dx + dy*dy) ** 0.5
        return distance < (self.size + other.size)

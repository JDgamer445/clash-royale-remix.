import pygame
import sys
import random

# Settings
WIDTH, HEIGHT = 450, 700
FPS = 60
ELIXIR_SPEED = 0.8  # Fast generation for Remix!

class Unit:
    def __init__(self, x, y, team, hp, speed, damage, color):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.team = team  # "player" or "enemy"
        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.color = color
        self.fighting = False

    def update(self, others):
        self.fighting = False
        # Check for enemies in front
        for other in others:
            if other.team != self.team and self.rect.colliderect(other.rect):
                self.fighting = True
                other.hp -= self.damage / FPS # Deal damage over time
                break
        
        # Move if not fighting
        if not self.fighting:
            direction = -1 if self.team == "player" else 1
            self.rect.y += self.speed * direction

    def draw(self, screen):
        # Draw Unit
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        # Draw Health Bar
        hp_width = (self.hp / self.max_hp) * 30
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, 30, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, hp_width, 5))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    units = []
    elixir = 5.0
    enemy_timer = 0

    while True:
        screen.fill((50, 150, 50)) # Arena Green
        
        # 1. Input / Spawning
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and elixir >= 3:
                    units.append(Unit(WIDTH//2-15, HEIGHT-100, "player", 100, 2, 20, (0, 100, 255)))
                    elixir -= 3
                if event.key == pygame.K_2 and elixir >= 5:
                    units.append(Unit(WIDTH//2-15, HEIGHT-100, "player", 300, 0.8, 40, (0, 0, 150)))
                    elixir -= 5

        # 2. Simple AI Opponent
        enemy_timer += 1
        if enemy_timer > 120: # Spawn enemy every 2 seconds
            units.append(Unit(WIDTH//2-15, 100, "enemy", 100, 1.5, 15, (200, 0, 0)))
            enemy_timer = 0

        # 3. Update Logic
        elixir = min(elixir + (ELIXIR_SPEED / FPS), 10)
        for u in units[:]:
            u.update(units)
            if u.hp <= 0: units.remove(u)

        # 4. Draw Everything
        # Towers
        pygame.draw.rect(screen, (100, 100, 100), (WIDTH//2-40, 20, 80, 60)) # Enemy King
        pygame.draw.rect(screen, (100, 100, 100), (WIDTH//2-40, HEIGHT-80, 80, 60)) # Player King
        
        for u in units: u.draw(screen)
        
        # UI
        text = font.render(f"ELIXIR: {int(elixir)} | [1] Knight (3) [2] Giant (5)", True, (255, 255, 255))
        screen.blit(text, (10, HEIGHT - 25))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

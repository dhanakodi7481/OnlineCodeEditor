import random
import time
from abc import ABC, abstractmethod

# ==========================================
# 1. ABSTRACTION: THE BASE TEMPLATE
# ==========================================
class GameEntity(ABC):
    """Abstract Base Class for all living things in the game."""
    def __init__(self, name, health, attack_power):
        self._name = name
        self._health = health  # Protected: Encapsulation
        self._max_health = health
        self._attack_power = attack_power
        self.is_alive = True

    @property
    def name(self):
        return self._name

    @abstractmethod
    def take_turn(self, targets):
        """Must be implemented by subclasses to define AI behavior."""
        pass

    def receive_damage(self, amount):
        self._health -= amount
        print(f"  [DAMAGE] {self.name} took {amount} damage! (Remaining: {max(0, self._health)})")
        if self._health <= 0:
            self._health = 0
            self.is_alive = False
            print(f"  [DEATH] {self.name} has been defeated!")

    def heal(self, amount):
        if self.is_alive:
            self._health = min(self._health + amount, self._max_health)
            print(f"  [HEAL] {self.name} recovered {amount} HP!")

# ==========================================
# 2. COMPOSITION: EQUIPMENT & INVENTORY
# ==========================================
class Weapon:
    def __init__(self, name, bonus_damage):
        self.name = name
        self.bonus_damage = bonus_damage

class Inventory:
    def __init__(self):
        self.items = []
        self.weapon = None

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f"  [EQUIP] {weapon.name} equipped! (+{weapon.bonus_damage} ATK)")

# ==========================================
# 3. INHERITANCE: CHARACTER ROLES
# ==========================================
class Hero(GameEntity):
    def __init__(self, name, health, attack_power, hero_class):
        super().__init__(name, health, attack_power)
        self.hero_class = hero_class
        self.level = 1
        self.xp = 0
        self.inventory = Inventory() # Composition

    def gain_xp(self, amount):
        self.xp += amount
        print(f"  [XP] {self.name} gained {amount} XP!")
        if self.xp >= 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp = 0
        self._max_health += 20
        self._health = self._max_health
        self._attack_power += 5
        print(f"  [LEVEL UP] {self.name} reached Level {self.level}!")

    def take_turn(self, enemies):
        if not enemies: return
        target = random.choice(enemies)
        damage = self._attack_power
        if self.inventory.weapon:
            damage += self.inventory.weapon.bonus_damage
        
        print(f"  [ACTION] {self.name} ({self.hero_class}) attacks {target.name}!")
        target.receive_damage(damage)

class Mage(Hero):
    def __init__(self, name):
        super().__init__(name, health=80, attack_power=20, hero_class="Mage")
        self.mana = 50

    # Polymorphism: Different turn behavior for Mage
    def take_turn(self, enemies):
        if self.mana >= 20:
            print(f"  [SPELL] {self.name} casts Fireball on all enemies!")
            for enemy in enemies:
                enemy.receive_damage(self._attack_power + 10)
            self.mana -= 20
        else:
            super().take_turn(enemies)

class Paladin(Hero):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=10, hero_class="Paladin")

    def take_turn(self, enemies):
        # Paladin heals self slightly then attacks
        self.heal(5)
        super().take_turn(enemies)

# ==========================================
# 4. ENEMY TYPES (INHERITANCE)
# ==========================================
class Monster(GameEntity):
    def __init__(self, name, health, attack_power, monster_type):
        super().__init__(name, health, attack_power)
        self.type = monster_type

    def take_turn(self, heroes):
        if not heroes: return
        target = random.choice(heroes)
        print(f"  [ENEMY] {self.name} ({self.type}) bites {target.name}!")
        target.receive_damage(self._attack_power)

class Boss(Monster):
    def __init__(self, name):
        super().__init__(name, health=300, attack_power=30, monster_type="BOSS")

    def take_turn(self, heroes):
        print(f"  [BOSS ACTION] {self.name} unleashes a Roar!")
        for hero in heroes:
            hero.receive_damage(15)

# ==========================================
# 5. ENGINE: SYSTEM MANAGEMENT CLASS
# ==========================================
class BattleSimulator:
    def __init__(self):
        self.heroes = []
        self.monsters = []
        self.round_number = 1

    def initialize_world(self):
        """Sets up the objects without user input."""
        print("--- Initializing Game World ---")
        
        # Create Hero Objects
        h1 = Mage("Gandalf")
        h2 = Paladin("Arthur")
        h1.inventory.equip_weapon(Weapon("Staff of Power", 10))
        h2.inventory.equip_weapon(Weapon("Excalibur", 15))
        
        self.heroes = [h1, h2]

        # Create Monster Objects
        self.monsters = [
            Monster("Goblin A", 40, 8, "Scout"),
            Monster("Goblin B", 40, 8, "Scout"),
            Boss("Dragon Lord")
        ]

    def check_battle_status(self):
        self.heroes = [h for h in self.heroes if h.is_alive]
        self.monsters = [m for m in self.monsters if m.is_alive]
        
        if not self.heroes:
            print("\n[GAME OVER] The Monsters have won...")
            return False
        if not self.monsters:
            print("\n[VICTORY] The Heroes have cleared the dungeon!")
            return False
        return True

    def run_simulation(self):
        self.initialize_world()
        
        while self.check_battle_status():
            print(f"\n--- ROUND {self.round_number} ---")
            time.sleep(1)

            # Hero Phase
            print("\n[HERO PHASE]")
            for hero in self.heroes:
                if hero.is_alive and self.monsters:
                    hero.take_turn(self.monsters)

            # Monster Phase
            print("\n[MONSTER PHASE]")
            for monster in self.monsters:
                if monster.is_alive and self.heroes:
                    monster.take_turn(self.heroes)

            self.round_number += 1
            if self.round_number > 50: # Failsafe
                break

        self.print_summary()

    def print_summary(self):
        print("\n" + "="*30)
        print("BATTLE FINAL SUMMARY")
        print("="*30)
        print(f"Total Rounds: {self.round_number}")
        print(f"Survivors: {[h.name for h in self.heroes]}")
        print("="*30)

# ==========================================
# 6. EXECUTION
# ==========================================
if __name__ == "__main__":
    sim = BattleSimulator()
    sim.run_simulation()
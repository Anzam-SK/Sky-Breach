import pygame
import sys
import os
import random
import math

# --- Configuration & Setup ---
pygame.init()
pygame.mixer.init()  # Initialize the sound mixer
# Increase available sound channels to prevent warning sound from being cut off
pygame.mixer.set_num_channels(32)
CLOCK = pygame.time.Clock()
FPS = 60

# Define Paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "Final image")
MUSIC_DIR = os.path.join(PROJECT_ROOT, "Aircraft music")

# Image Filenames
BG_MENU = "Game pic.png"
BG_LEVEL1 = "background3.png"
BG_LEVEL2 = "background4.png"
BG_LEVEL3 = "background5.png"
SHOP_BG_IMG = "shop.png"
START_BTN_IMG = "Start.png"
EXIT_BTN_IMG = "Exit.png"
RESUME_BTN_IMG = "Resume.png"
STORE_BTN_IMG = "Store.png"
HERO_IMG = "plane1.png"
BULLET_IMG = "bullet0.png"
ENEMY_BULLET_IMG = "bullet.png"
BLUE_BULLET_IMG = "blue_bullet.png"
METEOR1_IMG = "meteor1.png"
METEOR2_IMG = "meteor2.png"
METEOR4_IMG = "meteor_4.png"
METEOR_BIG_IMG = "meteor_2.png"
SCORE_COIN_IMG = "score_coin.png"
MYSTERY_BOX_IMG = "mystery_box.png"
ENEMY1_IMG = "enemy1_1.png"
ENEMY1_2_IMG = "enemy1_2.png"
ENEMY1_3_IMG = "enemy1_3.png"
E1_IMG = "e1.png"
B1_IMG = "b1.png"
B2_IMG = "b2.png"
B3_IMG = "b3.png"
ENEMY2_1_IMG = "enemy2_1.png"
ENEMY2_2_IMG = "enemy2_2.png"
BOSS_IMG = "boss.png"
BOSS2_IMG = "boss2.png"
BOSS3_IMG = "boss3.png"
MISSILE_IMG = "Missile.png"
BOSS_BULLET_IMG = "bullet_refill.png"

# Audio Filenames
INTERFACE_MUSIC = "interfaace.mp3"
GAME_BG_MUSIC = "Game bg.mp3"
COIN_SFX_FILENAME = "Coin collection.mp3"
METEOR_BLAST_SFX = "meteor blast.wav"
ENEMY_BLAST_SFX = "Enermy blast.wav"
SHOOT_SFX = "shoot.mp3"
LASER_SFX = "lasery.mp3"
BOSS_SHOOT_SFX = "boss1shoot.mp3"
BOSS2_SHOOT_SFX = "boss2shoot.mp3"
ENEMY_SHOOT_SFX = "enemy shoot.mp3"
GAME_OVER_SFX = "Game Over.mp3"
WARNING_SFX = "warning.mp3"
FLYING_ROCKET_SFX = "flying rocket.mp3"

# Special Assets
SHIELD_PLANE1_IMG = "sheild plane1.png"
SHIELD_PLANE2_IMG = "p2sheild.png"
SHIELD_PLANE3_IMG = "Sheildplane3.png"
CLONE_IMG = "clone.png"

# Shop Item Filenames
ITEM_ROCKET_IMG = "Rocket launcher.png"
ITEM_NUCLEAR_IMG = "Nuclear blast.png"
ITEM_SHIELD_IMG = "Sheild.png"
ITEM_HEAL_IMG = "heal.png"
ITEM_LASER_IMG = "lasery.png"
ITEM_CLONE_IMG = "c5.png"
ITEM_PLANE2_IMG = "p2.png"
ITEM_PLANE3_IMG = "plane3.png"

# Game Settings
# NOTE: Button sizes are now determined dynamically to preserve aspect ratio
SCROLL_SPEED = 2
PLAYER_SCALE = 0.35
BULLET_SCALE = 0.1
SHOP_ITEM_SIZE = (100, 100)
LEVEL1_DURATION = 45000
LEVEL2_DURATION = 75000
LEVEL3_DURATION = 105000

# Drop Rates
BASE_COIN_RATE = 0.5
BASE_MBOX_RATE = 0.20

# Custom Events
SPAWN_METEOR_EVENT = pygame.USEREVENT + 1
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 2
SPAWN_TRAIN_EVENT = pygame.USEREVENT + 3


def load_image(filename, do_convert=True):
    path = os.path.join(ASSETS_DIR, filename)
    try:
        image = pygame.image.load(path)
        if do_convert:
            image = image.convert_alpha()
        return image
    except (FileNotFoundError, pygame.error):
        print(f"Warning: Could not find image at {path}. Using placeholder.")
        surface = pygame.Surface((40, 40))
        surface.fill((255, 0, 255))
        return surface


# New Helper to scale images while keeping aspect ratio
def scale_image_keep_ratio(image, target_width):
    w, h = image.get_size()
    aspect_ratio = h / w
    new_height = int(target_width * aspect_ratio)
    return pygame.transform.smoothscale(image, (target_width, new_height))


def load_sound(filename):
    path = os.path.join(MUSIC_DIR, filename)
    try:
        sound = pygame.mixer.Sound(path)
        return sound
    except (FileNotFoundError, pygame.error):
        print(f"Warning: Could not find sound file at {path}")
        return None


def play_music(filename, loops=-1):
    path = os.path.join(MUSIC_DIR, filename)
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops)
    except (FileNotFoundError, pygame.error):
        print(f"Warning: Could not find music file at {path}")


def stop_music():
    pygame.mixer.music.stop()


def draw_popup(surface, text, target_rect, fixed_size=None):
    font = pygame.font.SysFont('Arial', 30, bold=True)
    text_surf = font.render(text, True, (255, 255, 255))

    if fixed_size:
        box_width, box_height = fixed_size
    else:
        padding = 20
        box_width = text_surf.get_width() + padding
        box_height = text_surf.get_height() + padding

    if not isinstance(target_rect, pygame.Rect):
        target_rect = pygame.Rect(surface.get_width() // 2, surface.get_height() // 2, 1, 1)

    box_x = target_rect.centerx - (box_width // 2)
    box_y = target_rect.centery - (box_height // 2)

    s = pygame.Surface((box_width, box_height))
    s.set_alpha(200)
    s.fill((0, 0, 0))
    surface.blit(s, (box_x, box_y))

    pygame.draw.rect(surface, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)

    text_x = box_x + (box_width - text_surf.get_width()) // 2
    text_y = box_y + (box_height - text_surf.get_height()) // 2
    surface.blit(text_surf, (text_x, text_y))

    pygame.display.update()


def draw_entity_health_bar(surface, sprite, color):
    if not hasattr(sprite, 'max_hp') or not hasattr(sprite, 'hp'):
        return

    bar_w = max(20, sprite.rect.width * 0.8)
    bar_h = 4

    bar_x = sprite.rect.centerx - (bar_w // 2)
    bar_y = sprite.rect.top - 10

    draw_hp = max(0, sprite.hp)
    ratio = draw_hp / sprite.max_hp

    bg_surface = pygame.Surface((bar_w, bar_h))
    bg_surface.set_alpha(150)
    bg_surface.fill((50, 50, 50))
    surface.blit(bg_surface, (bar_x, bar_y))

    if ratio > 0:
        fg_w = int(bar_w * ratio)
        fg_surface = pygame.Surface((fg_w, bar_h))
        fg_surface.set_alpha(200)
        fg_surface.fill(color)
        surface.blit(fg_surface, (bar_x, bar_y))


def draw_hud(surface, score, player, screen_width, screen_height, icons, boss=None):
    font_small = pygame.font.SysFont('Arial', 16, bold=True)
    font_large = pygame.font.SysFont('Arial', 24, bold=True)
    font_mini = pygame.font.SysFont('Arial', 14, bold=True)

    def draw_transparent_bg(x, y, w, h, color, alpha):
        s = pygame.Surface((w, h))
        s.set_alpha(alpha)
        s.fill(color)
        surface.blit(s, (x, y))

    bar_width = 80
    bar_height = 15
    x = 10
    y = 10

    display_hp = max(0, player.hp)
    health_pct = max(0, display_hp / player.max_hp)

    if health_pct <= 0.2:
        fill_color = (220, 20, 20)
    else:
        fill_color = (120, 120, 140)

    draw_transparent_bg(x, y, bar_width, bar_height, (20, 20, 20), 80)

    fill_width = int(bar_width * health_pct)
    pygame.draw.rect(surface, fill_color, (x, y, fill_width, bar_height))
    pygame.draw.rect(surface, (200, 200, 200), (x, y, bar_width, bar_height), 2)

    hp_text = font_small.render(f"{int(display_hp)}/{player.max_hp}", True, (255, 255, 255))
    surface.blit(hp_text, (x + bar_width + 10, y - 2))

    if boss and boss.alive():
        boss_bar_w = 400
        boss_bar_h = 20
        bx = (screen_width - boss_bar_w) // 2
        by = 50

        boss_pct = max(0, boss.hp / boss.max_hp)
        draw_transparent_bg(bx, by, boss_bar_w, boss_bar_h, (50, 0, 0), 150)
        pygame.draw.rect(surface, (255, 50, 50), (bx, by, int(boss_bar_w * boss_pct), boss_bar_h))
        pygame.draw.rect(surface, (255, 255, 255), (bx, by, boss_bar_w, boss_bar_h), 2)

        boss_text = font_small.render(f"BOSS (Lvl {boss.level})", True, (255, 255, 255))
        surface.blit(boss_text, (bx + boss_bar_w // 2 - boss_text.get_width() // 2, by + 2))

    coin_icon = icons['coin']
    surface.blit(coin_icon, (x, y + 25))

    coin_color = (255, 215, 0)
    score_surf = font_large.render(f"{score}", True, coin_color)
    shadow_surf = font_large.render(f"{score}", True, (0, 0, 0))
    surface.blit(shadow_surf, (x + 37, y + 27))
    surface.blit(score_surf, (x + 35, y + 25))

    # UPDATED ABILITIES LIST with NEW KEYS
    abilities = [
        ("W", 'rocket', player.rockets, False),
        ("A", 'nuke', player.nukes, False),
        ("S", 'heal', player.potions, False),
        ("R-Clk", 'shield', player.shields, player.shield_active),  # Shield is still right click
        ("D", 'laser', player.lasers, player.laser_active),
        ("F", 'clone', player.clones, player.clone_active)
    ]

    slot_height = 30
    slot_width = 60
    padding = 5
    margin_right = 10
    start_y = 10

    for i, (key, icon_key, count, is_active) in enumerate(abilities):
        slot_y = start_y + i * (slot_height + padding)
        slot_x = screen_width - slot_width - margin_right

        bg_col = (50, 100, 50) if is_active else (20, 20, 20)
        draw_transparent_bg(slot_x, slot_y, slot_width, slot_height, bg_col, 80)

        border_color = (255, 255, 0) if is_active else ((200, 200, 200) if count > 0 else (80, 80, 80))
        width = 2 if is_active else 1
        pygame.draw.rect(surface, border_color, (slot_x, slot_y, slot_width, slot_height), width)

        icon = icons[icon_key]
        scaled_icon = pygame.transform.smoothscale(icon, (20, 20))

        icon_x = slot_x + 5
        icon_y = slot_y + (slot_height - 20) // 2
        surface.blit(scaled_icon, (icon_x, icon_y))

        text_col = (255, 255, 255) if count > 0 else (150, 150, 150)
        text_str = f"[{key}] {count}"
        text_surf = font_mini.render(text_str, True, text_col)

        text_x = icon_x + 20 + 5
        text_y = slot_y + (slot_height - text_surf.get_height()) // 2
        surface.blit(text_surf, (text_x, text_y))


# --- Class Definitions ---

class Button:
    def __init__(self, x, y, image):
        # We NO LONGER accept width/height here.
        # The image must be pre-scaled before creating the button to preserve ratios.
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action


class StoreItem:
    def __init__(self, center_x, center_y, image, price, name, item_id):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)
        self.price = price
        self.name = name
        self.item_id = item_id
        self.clicked = False
        self.click_area = self.rect.inflate(40, 40)

    def draw(self, surface, current_coins, allow_input=True):
        is_bought = False
        pos = pygame.mouse.get_pos()
        surface.blit(self.image, self.rect)
        font = pygame.font.SysFont('Arial', 18, bold=True)

        if current_coins >= self.price:
            text_color = (0, 255, 0)
        else:
            text_color = (255, 0, 0)

        price_surf = font.render(f"{self.price} Coins", True, text_color)
        name_surf = font.render(self.name, True, (255, 255, 255))

        surface.blit(name_surf, (self.rect.centerx - name_surf.get_width() // 2, self.rect.bottom + 5))
        surface.blit(price_surf, (self.rect.centerx - price_surf.get_width() // 2, self.rect.bottom + 25))

        if self.click_area.collidepoint(pos) and allow_input:
            pygame.draw.rect(surface, (255, 255, 0), self.click_area, 2)
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                if current_coins >= self.price:
                    is_bought = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return is_bought


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, damage):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.damage = damage

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, target_x, target_y, damage=5, speed=None):
        super().__init__()
        self.image = pygame.transform.rotate(image, 180)  # Flip to face down
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        base_speed = 7 * 0.6
        self.speed = speed if speed is not None else base_speed
        self.damage = damage

        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)

        if dist != 0:
            self.dx = (dx / dist) * self.speed
            self.dy = (dy / dist) * self.speed
        else:
            self.dx = 0
            self.dy = self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.top > 2000 or self.rect.bottom < -500:
            self.kill()


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, image, damage):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 12
        self.damage = damage * 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, image, base_damage):
        super().__init__()
        self.image = pygame.transform.scale(image, (20, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 15
        self.damage = base_damage * 0.60

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, animation_frames):
        super().__init__()
        self.frames = animation_frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.animation_speed = 3
        self.tick_count = 0

    def update(self):
        self.tick_count += 1
        if self.tick_count >= self.animation_speed:
            self.tick_count = 0
            self.frame_index += 1
            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, center, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = 4

    def update(self, screen_height):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()


class MysteryBox(pygame.sprite.Sprite):
    def __init__(self, center, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = 3

    def update(self, screen_height):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, screen_width, assets, explosion_assets, level=1):
        super().__init__()
        self.level = level
        # Level 2/3 Logic
        if level == 3:
            r = random.random()
            if r < 0.40:
                self.type = 1
            elif r < 0.80:
                self.type = 2
            elif r < 0.90:
                self.type = 4
            else:
                self.type = 5
        elif level == 2:
            r = random.random()
            if r < 0.45:
                self.type = 1
            elif r < 0.90:
                self.type = 2
            else:
                self.type = 4
        else:
            self.type = random.choice([1, 2])

        if self.type == 1:
            self.image = assets['meteor1']
            self.hp = 1
            self.speed = 3
            self.explosion_frames = explosion_assets['normal']
        elif self.type == 2:
            self.image = assets['meteor2']
            self.hp = 1
            self.speed = 2
            self.explosion_frames = explosion_assets['normal']
        elif self.type == 4:
            self.image = assets['meteor4']
            if self.level == 2:
                self.hp = 3
            else:
                self.hp = 1
            self.speed = 2.5
            self.explosion_frames = explosion_assets['normal']
        elif self.type == 5:
            self.image = assets['meteor_big']
            self.hp = 10
            self.speed = 2
            self.explosion_frames = explosion_assets['normal']

        self.max_hp = self.hp

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)

    def update(self, screen_height):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, image, shoot_sfx, bullet_img, explosion_frames, speed=None, hp=1, damage=5,
                 scale_factor=1.0, movement_type="normal", bullet_speed=None,
                 center_pos=None, radius=0, angle=0):
        super().__init__()
        if scale_factor != 1.0:
            w = int(image.get_width() * scale_factor)
            h = int(image.get_height() * scale_factor)
            self.image = pygame.transform.smoothscale(image, (w, h))
        else:
            self.image = image

        self.rect = self.image.get_rect()

        self.movement_type = movement_type
        self.bullet_speed = bullet_speed
        self.explosion_frames = explosion_frames

        # Rotational Movement Attributes
        self.center_pos = center_pos if center_pos else [0, 0]
        self.radius = radius
        self.angle = angle
        self.angular_speed = 0.05

        # Normal Movement init
        if self.movement_type == "normal":
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            base_speed = random.randint(4, 6) * 0.75
            self.dx = 0
            self.dy = speed if speed else base_speed
        elif self.movement_type == "train_left":
            self.rect.x = -50
            self.rect.y = 50
            self.dx = 3
            self.dy = 1
            self.speed = 0
        elif self.movement_type == "train_right":
            self.rect.x = screen_width + 50
            self.rect.y = 50
            self.dx = -3
            self.dy = 1
            self.speed = 0
        elif self.movement_type == "rotate":
            self.dx = 0
            self.dy = 2
            self.rect.centerx = self.center_pos[0] + self.radius * math.cos(self.angle)
            self.rect.centery = self.center_pos[1] + self.radius * math.sin(self.angle)

        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.bullet_img = bullet_img
        self.shoot_sfx = shoot_sfx

        self.shoot_timer = random.randint(30, 90)
        self.fired_bullets = pygame.sprite.Group()

    def update(self, screen_width, screen_height, bullet_group, player_x, player_y):
        # Movement
        if self.movement_type == "normal":
            if self.rect.y < 50:
                self.rect.y += self.dy
        elif "train" in self.movement_type:
            self.rect.x += self.dx
            self.rect.y += self.dy
            if self.rect.right < -100 or self.rect.left > screen_width + 100 or self.rect.top > screen_height:
                self.kill()
        elif self.movement_type == "rotate":
            self.center_pos[1] += self.dy
            self.angle += self.angular_speed
            self.rect.centerx = self.center_pos[0] + self.radius * math.cos(self.angle)
            self.rect.centery = self.center_pos[1] + self.radius * math.sin(self.angle)
            if self.center_pos[1] - self.radius > screen_height:
                self.kill()

        # Shooting Logic
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(60, 120)

            start_x = self.rect.centerx
            start_y = self.rect.bottom

            target_x_val = player_x
            target_y_val = player_y

            if self.movement_type == "rotate":
                target_x_val = self.rect.centerx + math.cos(self.angle) * 1000
                target_y_val = self.rect.centery + math.sin(self.angle) * 1000
                start_y = self.rect.centery

            bullet = EnemyBullet(start_x, start_y, self.bullet_img, target_x_val, target_y_val,
                                 damage=self.damage, speed=self.bullet_speed)
            bullet_group.add(bullet)
            self.fired_bullets.add(bullet)
            if self.shoot_sfx:
                self.shoot_sfx.play()


class Boss(pygame.sprite.Sprite):
    def __init__(self, screen_width, image, missile_img, bullet_img, shoot_sfx, level=1):
        super().__init__()
        self.level = level
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.y = -200

        # Stats based on Level
        if self.level == 1:
            self.max_hp = 200
        elif self.level == 2:
            self.max_hp = 400  # 2x Level 1 HP
        elif self.level == 3:
            self.max_hp = 500  # 2.5x of Level 1 HP (200 * 2.5 = 500)

        self.hp = self.max_hp
        self.speed = 2
        self.move_dir = 1

        self.missile_img = missile_img
        self.bullet_img = bullet_img
        self.shoot_sfx = shoot_sfx

        self.bullet_timer = 0
        self.missile_timer = 0
        self.shoot_pause_timer = 0

        # Track shots for burst logic
        self.shots_fired_count = 0

        self.fired_projectiles = pygame.sprite.Group()

    def update(self, screen_width, bullet_group, player_x, player_y):
        # Entrance
        if self.rect.y < 50:
            self.rect.y += 2  # Entrance speed
        else:
            # Strafe
            self.rect.x += self.speed * self.move_dir
            if self.rect.right >= screen_width or self.rect.left <= 0:
                self.move_dir *= -1

        # Shoot Bullets (Dual Wing)
        # Check if we are currently pausing our shots
        if self.shoot_pause_timer > 0:
            self.shoot_pause_timer -= 1
        else:
            self.bullet_timer += 1
            if self.bullet_timer >= 20:
                self.bullet_timer = 0

                # Boss 2 Bullet Damage = 2x Boss 1 Damage.
                # Boss 3 damage logic: > Level 2.
                # Level 1 = 15. Level 2 = 30. Level 3 = 40.
                if self.level == 1:
                    bullet_dmg = 15
                elif self.level == 2:
                    bullet_dmg = 30
                else:
                    bullet_dmg = 38  # 2.5x of Boss 1 (15) = 37.5 -> 38

                if self.level == 2:
                    # Boss 2: Shoot 3 bullets (Left, Center, Right)
                    offsets = [-100, 0, 100]
                    for offset in offsets:
                        bx = self.rect.centerx + offset
                        b = EnemyBullet(bx, self.rect.bottom - 20, self.bullet_img, bx,
                                        self.rect.bottom + 100, bullet_dmg)
                        bullet_group.add(b)
                        self.fired_projectiles.add(b)

                elif self.level == 3:
                    # Boss 3: Shoot 4 bullets evenly spread
                    for i in range(4):
                        margin = 40
                        available_width = self.rect.width - (2 * margin)
                        step = available_width / 3
                        bx = self.rect.left + margin + (i * step)
                        b = EnemyBullet(bx, self.rect.bottom - 20, self.bullet_img, bx,
                                        self.rect.bottom + 100, bullet_dmg)
                        bullet_group.add(b)
                        self.fired_projectiles.add(b)
                else:
                    # Level 1: Standard 2 wing bullets
                    b1 = EnemyBullet(self.rect.left + 20, self.rect.bottom - 20, self.bullet_img, self.rect.left + 20,
                                     self.rect.bottom + 100, bullet_dmg)
                    b2 = EnemyBullet(self.rect.right - 20, self.rect.bottom - 20, self.bullet_img, self.rect.right - 20,
                                     self.rect.bottom + 100, bullet_dmg)
                    bullet_group.add(b1, b2)
                    self.fired_projectiles.add(b1, b2)

                # Play shoot sound
                if self.shoot_sfx:
                    self.shoot_sfx.play()

                self.shots_fired_count += 1

                # GUARANTEED PAUSE logic:
                burst_limit = random.randint(6, 8)
                if self.shots_fired_count >= burst_limit:
                    self.shoot_pause_timer = 120
                    self.shots_fired_count = 0
                # Random chance for early pause (optional variety)
                elif random.random() < 0.05:
                    self.shoot_pause_timer = 60
                    self.shots_fired_count = 0

        # Shoot Missiles
        self.missile_timer += 1
        if self.missile_timer >= 120:
            self.missile_timer = 0
            if random.random() < 0.7:
                missile_dmg = 30  # Base for L1/L2
                if self.level == 3:
                    missile_dmg = 45  # Increased for L3 (was 30)

                if self.level == 2:
                    # Boss 2: 2 Rockets (Wings)
                    m1 = EnemyBullet(self.rect.left, self.rect.centery, self.missile_img, player_x, player_y,
                                     missile_dmg)
                    m2 = EnemyBullet(self.rect.right, self.rect.centery, self.missile_img, player_x, player_y,
                                     missile_dmg)
                    bullet_group.add(m1, m2)
                    self.fired_projectiles.add(m1, m2)
                elif self.level == 3:
                    # Boss 3: 3 Rockets (Left, Center, Right)
                    m1 = EnemyBullet(self.rect.left, self.rect.centery, self.missile_img, player_x, player_y,
                                     missile_dmg)
                    m2 = EnemyBullet(self.rect.centerx, self.rect.centery, self.missile_img, player_x, player_y,
                                     missile_dmg)
                    m3 = EnemyBullet(self.rect.right, self.rect.centery, self.missile_img, player_x, player_y,
                                     missile_dmg)
                    bullet_group.add(m1, m2, m3)
                    self.fired_projectiles.add(m1, m2, m3)
                else:
                    # Boss 1: 1 Rocket (Center)
                    m = EnemyBullet(self.rect.centerx, self.rect.centery, self.missile_img, player_x, player_y,
                                    missile_dmg)
                    bullet_group.add(m)
                    self.fired_projectiles.add(m)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, clone_frames):
        super().__init__()
        self.base_image = image
        self.image = image
        self.clone_frames = clone_frames  # Store the list of frames
        self.clone_frame_index = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Stats
        self.hp = 100
        self.max_hp = 100
        self.bullet_damage = 1

        # Inventory
        self.nukes = 0
        self.rockets = 0
        self.shields = 0
        self.potions = 0
        self.lasers = 0
        self.clones = 0

        # State
        self.shield_active = False
        self.shield_timer = 0

        self.laser_active = False
        self.laser_timer = 0

        self.clone_active = False
        self.clone_timer = 0

        # Plane Management
        self.current_plane_type = 'plane1'
        self.owned_planes = ['plane1']
        self.plane_images = {}
        self.shield_images = {}

        # Clone Offset Distance
        self.clone_offset = 70  # Reduced from 100

    def update(self, screen_width, screen_height):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height))

        # Timers
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.deactivate_shield()

        if self.laser_active:
            self.laser_timer -= 1
            if self.laser_timer <= 0:
                self.laser_active = False

        if self.clone_active:
            self.clone_timer -= 1
            if self.clone_timer <= 0:
                self.clone_active = False

            # Animate Clones
            if self.clone_frames:
                self.clone_frame_index += 0.4  # Adjust animation speed
                if self.clone_frame_index >= len(self.clone_frames):
                    self.clone_frame_index = 0

    def get_clone_rects(self):
        if not self.clone_active or not self.clone_frames:
            return []

        # Get rect of current frame
        current_frame = self.clone_frames[int(self.clone_frame_index)]

        l_rect = current_frame.get_rect(center=(self.rect.centerx - self.clone_offset, self.rect.centery))
        r_rect = current_frame.get_rect(center=(self.rect.centerx + self.clone_offset, self.rect.centery))
        return [l_rect, r_rect]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.clone_active and self.clone_frames:
            current_frame = self.clone_frames[int(self.clone_frame_index)]
            clones = self.get_clone_rects()
            for c_rect in clones:
                surface.blit(current_frame, c_rect)

    def activate_shield(self, duration_seconds=7):
        if self.shields > 0 and not self.shield_active:
            self.shields -= 1
            self.shield_active = True
            self.shield_timer = duration_seconds * 60
            if self.current_plane_type in self.shield_images:
                center = self.rect.center
                self.image = self.shield_images[self.current_plane_type]
                self.rect = self.image.get_rect()
                self.rect.center = center

    def deactivate_shield(self):
        self.shield_active = False
        center = self.rect.center
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.center = center

    def activate_laser(self, duration_seconds=5):
        if self.lasers > 0 and not self.laser_active:
            self.lasers -= 1
            self.laser_active = True
            self.laser_timer = duration_seconds * 60

    def activate_clones(self, duration_seconds=5):
        if self.clones > 0 and not self.clone_active:
            self.clones -= 1
            self.clone_active = True
            self.clone_timer = duration_seconds * 60

    def use_potion(self):
        if self.potions > 0:
            self.potions -= 1
            self.hp = self.max_hp
            print("Potion used! Health fully restored.")

    def switch_plane(self, plane_type):
        if plane_type in self.plane_images and plane_type in self.owned_planes:
            self.current_plane_type = plane_type
            self.base_image = self.plane_images[plane_type]
            center = self.rect.center
            if self.shield_active:
                self.image = self.shield_images[plane_type]
            else:
                self.image = self.base_image
            self.rect = self.image.get_rect()
            self.rect.center = center

            if plane_type == 'plane1':
                self.max_hp = 100
                self.bullet_damage = 1
            elif plane_type == 'plane2':
                self.max_hp = 150
                self.bullet_damage = 5
            elif plane_type == 'plane3':
                self.max_hp = 200
                # 1.75x of Plane 1 (which is 1) -> 1.75 damage
                self.bullet_damage = 1.75

    def reset_stats(self):
        self.hp = 100
        self.max_hp = 100
        self.bullet_damage = 1
        self.nukes = 0
        self.rockets = 0
        self.shields = 0
        self.potions = 0
        self.lasers = 0
        self.clones = 0
        self.shield_active = False
        self.laser_active = False
        self.clone_active = False
        self.current_plane_type = 'plane1'
        self.owned_planes = ['plane1']

        # --- Main Execution ---


def main():
    bg_level1_raw = load_image(BG_LEVEL1, do_convert=False)
    screen_width = bg_level1_raw.get_width()
    screen_height = bg_level1_raw.get_height()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sky Breach Game")

    bg_level1_img = bg_level1_raw.convert_alpha()
    bg_menu_raw = load_image(BG_MENU)
    bg_menu_img = pygame.transform.smoothscale(bg_menu_raw, (screen_width, screen_height))

    # Load and scale Level 2 Background
    bg_level2_raw = load_image(BG_LEVEL2)
    bg_level2_img = pygame.transform.smoothscale(bg_level2_raw, (screen_width, screen_height))

    # Load and scale Level 3 Background
    bg_level3_raw = load_image(BG_LEVEL3)
    bg_level3_img = pygame.transform.smoothscale(bg_level3_raw, (screen_width, screen_height))

    bg_shop_raw = load_image(SHOP_BG_IMG)
    bg_shop_img = pygame.transform.smoothscale(bg_shop_raw, (screen_width, screen_height))

    # --- BUTTON ASSETS LOADING & SCALING ---
    # We define a target width and calculate height dynamically to preserve aspect ratio
    TARGET_BTN_WIDTH = 185

    start_raw = load_image(START_BTN_IMG)
    start_img = scale_image_keep_ratio(start_raw, TARGET_BTN_WIDTH)

    exit_raw = load_image(EXIT_BTN_IMG)
    exit_img = scale_image_keep_ratio(exit_raw, TARGET_BTN_WIDTH)

    resume_raw = load_image(RESUME_BTN_IMG)
    resume_img = scale_image_keep_ratio(resume_raw, TARGET_BTN_WIDTH)

    store_raw = load_image(STORE_BTN_IMG)
    store_img = scale_image_keep_ratio(store_raw, TARGET_BTN_WIDTH)

    # Transparency for Menu Buttons
    BUTTON_ALPHA = 240  # Less transparent (Solid-like)
    start_img.set_alpha(BUTTON_ALPHA)
    exit_img.set_alpha(BUTTON_ALPHA)
    resume_img.set_alpha(BUTTON_ALPHA)
    store_img.set_alpha(BUTTON_ALPHA)

    hero_raw = load_image(HERO_IMG)
    hero_width = int(hero_raw.get_width() * PLAYER_SCALE)
    hero_height = int(hero_raw.get_height() * PLAYER_SCALE)
    hero_img = pygame.transform.smoothscale(hero_raw, (hero_width, hero_height))

    # Boss Assets
    boss_raw = load_image(BOSS_IMG)
    # INCREASED SIZE: 1.7x player size (Was 1.35x, increased by ~25%)
    boss_w = int(hero_width * 1.7)
    boss_h = int(hero_height * 1.7)
    boss_img = pygame.transform.smoothscale(boss_raw, (boss_w, boss_h))

    # Boss 2 Assets
    boss2_raw = load_image(BOSS2_IMG)
    # Boss 2 Size: 2.9x Player Size (Reduced by 15% from 3.4x)
    boss2_w = int(hero_width * 2.9)
    boss2_h = int(hero_height * 2.9)
    boss2_img = pygame.transform.smoothscale(boss2_raw, (boss2_w, boss2_h))

    # Boss 3 Assets
    boss3_raw = load_image(BOSS3_IMG)
    # Boss 3 Size: 4x Player Size (Per recent instruction)
    boss3_w = int(hero_width * 4.0)
    boss3_h = int(hero_height * 4.0)
    boss3_img = pygame.transform.smoothscale(boss3_raw, (boss3_w, boss3_h))

    # Bullets & Missiles
    bullet_raw = load_image(BULLET_IMG)
    bullet_width = 20
    bullet_height = 20
    bullet_img = pygame.transform.smoothscale(bullet_raw, (bullet_width, bullet_height))

    # Enemy Bullet (16px)
    enemy_bullet_raw = load_image(ENEMY_BULLET_IMG)
    enemy_bullet_size = 16
    enemy_bullet_img = pygame.transform.smoothscale(enemy_bullet_raw, (enemy_bullet_size, enemy_bullet_size))

    # Blue Bullet for Level 2 Enemy (20px)
    blue_bullet_raw = load_image(BLUE_BULLET_IMG)
    blue_bullet_img = pygame.transform.smoothscale(blue_bullet_raw, (20, 20))

    missile_raw = load_image(MISSILE_IMG)
    missile_img = pygame.transform.smoothscale(missile_raw, (30, 60))

    boss_bullet_raw = load_image(BOSS_BULLET_IMG)
    boss_bullet_img = pygame.transform.smoothscale(boss_bullet_raw, (20, 40))

    meteor_target_width = int(hero_width * 0.6)
    meteor_target_height = int(hero_height * 0.6)

    # ADJUSTED SIZE for Meteor 4 (Was 5.0, now 3.5x as per 'decrease' instruction)
    # New instruction: increase to 2.5x of current size.
    # Current size was `m4_width = int(meteor_target_width * 0.7)`
    # New size = `0.7 * 2.5` = `1.75`
    m4_width = int(meteor_target_width * 1.75)
    m4_height = int(meteor_target_height * 1.75)

    # Size for Meteor 2 (Level 3 Giant) -> 3x of its current size.
    # Current size was `m_big_width = int(m4_width * 1.2)` (relative to old small m4)
    # Wait, the prompt says "increase the size of meteor_2.png to 3x of it's current size".
    # Previous code had `m_big_width = int(m4_width * 1.2)` where `m4_width` was 0.7 * target.
    # So current big was `0.7 * 1.2 = 0.84 * target`.
    # New big should be `0.84 * 3 = 2.52 * target`.
    m_big_width = int(meteor_target_width * 2.52)
    m_big_height = int(meteor_target_height * 2.52)

    explosion_target_width = int(meteor_target_width * 1.3)
    explosion_target_height = int(meteor_target_height * 1.3)

    # BIG Explosion Dimensions (Proportional to Meteor 4)
    explosion_big_width = int(m4_width * 1.3)
    explosion_big_height = int(m4_height * 1.3)

    # HUGE Explosion Dimensions (Proportional to Meteor 2 Giant)
    explosion_huge_width = int(m_big_width * 1.3)
    explosion_huge_height = int(m_big_height * 1.3)

    coin_target_width = int(hero_width * 0.4)
    coin_target_height = int(hero_height * 0.4)
    # Mystery Box Size set to 60% of player size (reasonable visibility)
    mbox_target_width = int(hero_width * 0.6)
    mbox_target_height = int(hero_height * 0.6)

    coin_raw = load_image(SCORE_COIN_IMG)
    coin_img = pygame.transform.smoothscale(coin_raw, (coin_target_width, coin_target_height))

    m1_raw = load_image(METEOR1_IMG)
    m2_raw = load_image(METEOR2_IMG)
    m4_raw = load_image(METEOR4_IMG)
    m_big_raw = load_image(METEOR_BIG_IMG)

    meteor_assets = {
        'meteor1': pygame.transform.smoothscale(m1_raw, (meteor_target_width, meteor_target_height)),
        'meteor2': pygame.transform.smoothscale(m2_raw, (meteor_target_width, meteor_target_height)),
        'meteor4': pygame.transform.smoothscale(m4_raw, (m4_width, m4_height)),
        'meteor_big': pygame.transform.smoothscale(m_big_raw, (m_big_width, m_big_height))
    }

    # Load All Explosion Sequences
    # Sequence 0 (Default): explosion0-8
    explosion0_frames = []
    for i in range(9):
        filename = f"explosion{i}.png"
        frame_raw = load_image(filename)
        frame_scaled = pygame.transform.smoothscale(frame_raw, (explosion_target_width, explosion_target_height))
        explosion0_frames.append(frame_scaled)

    # Sequence 1 (Meteors): explosion1_0 - explosion1_8
    explosion1_frames = []
    for i in range(9):
        filename = f"explosion1_{i}.png"
        frame_raw = load_image(filename)
        frame_scaled = pygame.transform.smoothscale(frame_raw, (explosion_target_width, explosion_target_height))
        explosion1_frames.append(frame_scaled)

    # Sequence 1 BIG (For Meteor 4) - Same images, bigger scale
    explosion1_big_frames = []
    for i in range(9):
        filename = f"explosion1_{i}.png"
        frame_raw = load_image(filename)
        frame_scaled = pygame.transform.smoothscale(frame_raw, (explosion_big_width, explosion_big_height))
        explosion1_big_frames.append(frame_scaled)

    # Sequence 1 HUGE (For Meteor 2/Giant)
    explosion1_huge_frames = []
    for i in range(9):
        filename = f"explosion1_{i}.png"
        frame_raw = load_image(filename)
        frame_scaled = pygame.transform.smoothscale(frame_raw, (explosion_huge_width, explosion_huge_height))
        explosion1_huge_frames.append(frame_scaled)

    # New Meteor Explosion Sequence (ex1 - ex5)
    ex_frames = []
    for i in range(1, 6):  # ex1.png to ex5.png
        filename = f"ex{i}.png"
        raw = load_image(filename)
        ex_frames.append(raw)

    # Scale new meteor explosions (used for small enemies)
    enemy_small_explosion = []
    for raw in ex_frames:
        scaled = pygame.transform.smoothscale(raw, (explosion_target_width, explosion_target_height))
        enemy_small_explosion.append(scaled)

    # Bundle Explosion Assets for Meteors using explosion1 frames
    meteor_explosion_assets = {
        'normal': explosion1_frames,
        'big': explosion1_big_frames,
        'huge': explosion1_huge_frames
    }

    # Sequence 2 (Player/Boss): explosion2_0 - explosion2_18
    explosion2_frames = []
    for i in range(19):
        filename = f"explosion2_{i}.png"
        frame_raw = load_image(filename)
        # Scaled larger for boss/player death - INCREASED SIZE (2.5x player size)
        frame_scaled = pygame.transform.smoothscale(frame_raw, (int(hero_width * 2.5), int(hero_height * 2.5)))
        explosion2_frames.append(frame_scaled)

    # Sequence 3 (Enemy 2_1): explosion3_0 - explosion3_18
    explosion3_frames = []
    for i in range(19):
        filename = f"explosion3_{i}.png"
        frame_raw = load_image(filename)
        frame_scaled = pygame.transform.smoothscale(frame_raw, (int(hero_width * 1.5), int(hero_height * 1.5)))
        explosion3_frames.append(frame_scaled)

    def load_shop_icon(fname):
        raw = load_image(fname)
        return pygame.transform.smoothscale(raw, SHOP_ITEM_SIZE)

    def load_hud_icon(fname):
        raw = load_image(fname)
        return pygame.transform.smoothscale(raw, (30, 30))

    # Pre-load Sounds
    coin_sfx = load_sound(COIN_SFX_FILENAME)
    meteor_sfx = load_sound(METEOR_BLAST_SFX)  # Used for meteors? No, overwritten by Enemy blast as requested
    enemy_sfx = load_sound(ENEMY_BLAST_SFX)  # Used for enemies AND meteors as requested
    shoot_sfx = load_sound(SHOOT_SFX)
    laser_sfx = load_sound(LASER_SFX)
    boss_shoot_sfx = load_sound(BOSS_SHOOT_SFX)
    boss2_shoot_sfx = load_sound(BOSS2_SHOOT_SFX)
    enemy_shoot_sfx = load_sound(ENEMY_SHOOT_SFX)
    game_over_sfx = load_sound(GAME_OVER_SFX)

    # Load Music Tracks (Assuming user has these files or placeholders)
    # Using existing load_sound for simplicity if they are SFX, or pygame.mixer.music if long tracks.
    # The requirement asks for switching. Pygame music is best for bgm.
    # We will try to load them. If fail, catch error.

    # Store sound/music objects or paths
    warning_sfx = load_sound(WARNING_SFX)
    # Ensure Warning SFX is loud
    if warning_sfx:
        warning_sfx.set_volume(1.0)

    game_over_event_sfx = load_sound(GAME_OVER_SFX)  # Reuse the loaded game_over_sfx
    flying_rocket_sfx = load_sound(FLYING_ROCKET_SFX)

    img_rocket = load_shop_icon(ITEM_ROCKET_IMG)
    img_nuclear = load_shop_icon(ITEM_NUCLEAR_IMG)
    img_shield = load_shop_icon(ITEM_SHIELD_IMG)
    img_heal = load_shop_icon(ITEM_HEAL_IMG)
    img_laser = load_shop_icon(ITEM_LASER_IMG)
    img_clone = load_shop_icon(ITEM_CLONE_IMG)

    hud_icons = {
        'rocket': load_hud_icon(ITEM_ROCKET_IMG),
        'nuke': load_hud_icon(ITEM_NUCLEAR_IMG),
        'shield': load_hud_icon(ITEM_SHIELD_IMG),
        'heal': load_hud_icon(ITEM_HEAL_IMG),
        'laser': load_hud_icon(ITEM_LASER_IMG),
        'clone': load_hud_icon(ITEM_CLONE_IMG),
        'coin': load_hud_icon(SCORE_COIN_IMG)
    }

    mbox_raw = load_image(MYSTERY_BOX_IMG)
    mbox_img = pygame.transform.smoothscale(mbox_raw, (mbox_target_width, mbox_target_height))

    laser_raw = load_image(ITEM_LASER_IMG)

    rocket_raw = load_image(ITEM_ROCKET_IMG)
    # Rocket sizing based on hero size
    rocket_game_w = int(hero_width * 0.5)
    rocket_game_h = int(hero_height * 0.5)
    rocket_game_img = pygame.transform.smoothscale(rocket_raw, (rocket_game_w, rocket_game_h))

    # --- CLONE ANIMATION LOADING ---
    clone_frames = []
    clone_w = int(hero_width * 0.65)
    clone_h = int(hero_height * 0.65)

    # Try loading sequence c1.png to c14.png
    for i in range(1, 15):
        fname = f"c{i}.png"
        try:
            raw = load_image(fname)
            scaled = pygame.transform.smoothscale(raw, (clone_w, clone_h))
            clone_frames.append(scaled)
        except:
            pass

    # Fallback if no frames loaded (just in case)
    if not clone_frames:
        clone_raw = load_image(CLONE_IMG)
        scaled = pygame.transform.smoothscale(clone_raw, (clone_w, clone_h))
        clone_frames.append(scaled)

    real_plane1 = hero_img

    plane2_raw = load_image(ITEM_PLANE2_IMG)
    # Enhance Plane 2 Size (1.4x bigger than Plane 1)
    p2_w = int(hero_width * 1.4)
    p2_h = int(hero_height * 1.4)
    real_plane2 = pygame.transform.smoothscale(plane2_raw, (p2_w, p2_h))

    plane3_raw = load_image(ITEM_PLANE3_IMG)
    # Size Plane 3 same as Plane 2? or Standard? Let's use standard hero size + a bit?
    # Keeping it 1.2x for visual distinction
    p3_w = int(hero_width * 1.2)
    p3_h = int(hero_height * 1.2)
    real_plane3 = pygame.transform.smoothscale(plane3_raw, (p3_w, p3_h))

    s1_raw = load_image(SHIELD_PLANE1_IMG)
    shield_plane1 = pygame.transform.smoothscale(s1_raw, (hero_width, hero_height))

    s2_raw = load_image(SHIELD_PLANE2_IMG)
    # Match Shield Plane 2 size to enhanced Plane 2
    shield_plane2 = pygame.transform.smoothscale(s2_raw, (p2_w, p2_h))

    s3_raw = load_image(SHIELD_PLANE3_IMG)
    shield_plane3 = pygame.transform.smoothscale(s3_raw, (p3_w, p3_h))

    # --- Enemy Assets ---
    # Level 1 Enemy
    enemy1_raw = load_image(ENEMY1_IMG)
    enemy_w = int(hero_width * 0.52)
    enemy_h = int(hero_height * 0.52)
    enemy1_img = pygame.transform.smoothscale(enemy1_raw, (enemy_w, enemy_h))

    # Level 1 New Vertical Enemy E1
    e1_raw = load_image(E1_IMG)
    # e1 size to be 92% of player plane size (15% increase from 80%)
    e1_w = int(hero_width * 0.92)
    e1_h = int(hero_height * 0.92)
    e1_img = pygame.transform.smoothscale(e1_raw, (e1_w, e1_h))

    # Level 1 New Bullet B1
    b1_raw = load_image(B1_IMG)
    b1_img = pygame.transform.smoothscale(b1_raw, (20, 20))

    # Level 2/3 New Bullet B2 (Replacing Blue Bullet for Enemy 2 variants)
    b2_raw = load_image(B2_IMG)
    b2_img = pygame.transform.smoothscale(b2_raw, (20, 20))

    # New Bullet B3
    b3_raw = load_image(B3_IMG)
    b3_img = pygame.transform.smoothscale(b3_raw, (20, 20))

    # Level 3 New Enemy 1.2 (Standard Size)
    enemy1_2_raw = load_image(ENEMY1_2_IMG)
    enemy1_2_img = pygame.transform.smoothscale(enemy1_2_raw, (enemy_w, enemy_h))

    # Level 2 Enemies
    enemy1_3_raw = load_image(ENEMY1_3_IMG)
    enemy1_3_img = pygame.transform.smoothscale(enemy1_3_raw, (enemy_w, enemy_h))  # Same size as enemy1_1

    enemy2_1_raw = load_image(ENEMY2_1_IMG)
    # 30% larger than enemy1_1 -> Update to match p2 size per instruction
    # p2_w and p2_h are already defined
    enemy2_1_w = p2_w
    enemy2_1_h = p2_h
    enemy2_1_img = pygame.transform.smoothscale(enemy2_1_raw, (enemy2_1_w, enemy2_1_h))

    # Level 3 New Enemy 2.2 (Size like 2.1 which is now p2 size)
    enemy2_2_raw = load_image(ENEMY2_2_IMG)
    enemy2_2_img = pygame.transform.smoothscale(enemy2_2_raw, (enemy2_1_w, enemy2_1_h))

    col1_x = int(screen_width * (1 / 6))
    col2_x = int(screen_width * 0.5)
    col3_x = int(screen_width * (5 / 6))

    row1_y = int(screen_height * 0.33)
    row2_y = int(screen_height * 0.66)

    shop_items = [
        StoreItem(col1_x, row1_y, img_rocket, 2, "Rocket (x1)", "rocket"),
        StoreItem(col2_x, row1_y, img_nuclear, 3, "Nuke (x1)", "nuke"),
        StoreItem(col3_x, row1_y, img_shield, 3, "Shield (x1)", "shield"),
        StoreItem(col1_x, row2_y - 30, img_heal, 4, "Heal (x1)", "heal"),
        StoreItem(col2_x, row2_y - 30, img_laser, 5, "Laser (x1)", "laser"),
        StoreItem(col3_x, row2_y - 30, img_clone, 6, "Clone (x1)", "clone")
    ]

    center_x = screen_width // 2

    # --- MENU LAYOUT: Vertical Center Column ---
    # Centering the block of 3 buttons vertically
    center_y = screen_height // 2

    # ADJUSTED: Gap set to 4 to tightly group the buttons
    gap = 4

    # We use the height of the actual start button image as a reference
    btn_h = start_img.get_height()

    total_menu_height = (btn_h * 3) + (gap * 2)

    # ADJUSTED: Increased offset to +150 to ensure Start/Resume buttons are below the "Sky Breach" title
    menu_start_y = center_y - (total_menu_height // 2) + 150

    start_btn_x = (screen_width - start_img.get_width()) // 2
    start_btn_y = menu_start_y

    store_btn_x = (screen_width - store_img.get_width()) // 2
    store_btn_y = start_btn_y + btn_h + gap

    exit_btn_x = (screen_width - exit_img.get_width()) // 2
    exit_btn_y = store_btn_y + btn_h + gap

    # Passing just coordinates and image. Button class does not scale anymore.
    start_btn = Button(start_btn_x, start_btn_y, start_img)
    exit_btn = Button(exit_btn_x, exit_btn_y, exit_img)
    store_btn = Button(store_btn_x, store_btn_y, store_img)

    # Resume button (same position as Start button for consistency)
    resume_btn_x = (screen_width - resume_img.get_width()) // 2
    resume_btn = Button(resume_btn_x, start_btn_y, resume_img)

    player = Player(100, screen_height // 2, hero_img, clone_frames)  # Pass frames instead of single image

    player.plane_images['plane1'] = real_plane1
    player.plane_images['plane2'] = real_plane2
    player.plane_images['plane3'] = real_plane3
    player.shield_images['plane1'] = shield_plane1
    player.shield_images['plane2'] = shield_plane2
    player.shield_images['plane3'] = shield_plane3

    player.owned_planes = ['plane1', 'plane2', 'plane3']

    bullet_group = pygame.sprite.Group()
    meteor_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    enemy_bullet_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    mystery_box_group = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()

    game_state = "MENU"
    previous_state = "MENU"
    current_level = 1
    bg_scroll = 0
    player_score = 0

    current_music_file = None

    font_large = pygame.font.SysFont('Arial', 40, bold=True)
    font_small = pygame.font.SysFont('Arial', 20)

    # Enemy 2 Bullet Speed Calculation
    base_enemy_bullet_speed = 7 * 0.6  # 4.2
    enemy2_bullet_speed = base_enemy_bullet_speed * 1.15  # 4.83

    level_start_time = 0
    level_complete = False  # Flag for transition
    boss_spawned = False

    # State flags for death animations
    player_exploding = False
    boss_exploding = False
    active_boss_explosion = None

    # Warning sound logic
    warning_played = False  # Initialized here to be safe

    # Mouse release flag for store input handling
    mouse_released_in_store = False

    run = True

    while run:
        CLOCK.tick(FPS)
        current_time = pygame.time.get_ticks()

        # --- Music State Machine ---
        target_music = None
        if game_state in ["MENU", "STORE", "LEVEL_2_MENU", "LEVEL_3_MENU", "GAME_WIN"]:
            target_music = INTERFACE_MUSIC
        elif game_state == "PLAYING" and not player_exploding and not boss_exploding:
            # Stop music if player dead or boss dying (will be handled by their specific logic)
            target_music = GAME_BG_MUSIC

        # Only switch if track changed (and not None)
        if target_music and target_music != current_music_file:
            play_music(target_music)
            current_music_file = target_music
        elif not target_music and current_music_file:
            stop_music()
            current_music_file = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # --- Spawn Logic Handling ---
            # Adjusted spawn logic: In Level 2 & 3, minions spawn even if Boss is present.
            spawn_allowed = False
            if not level_complete and game_state == "PLAYING" and not player_exploding and not boss_exploding:
                if not boss_spawned:
                    spawn_allowed = True
                elif current_level >= 1:  # Minions support boss in ALL LEVELS now
                    spawn_allowed = True

            if spawn_allowed:
                if event.type == SPAWN_METEOR_EVENT:
                    new_meteor = Meteor(screen_width, meteor_assets, meteor_explosion_assets, level=current_level)
                    meteor_group.add(new_meteor)

                if event.type == SPAWN_ENEMY_EVENT:
                    # Spawn Logic based on Level (Vertical/Single Spawns)
                    if current_level == 1:
                        # Level 1 Vertical: Spawn e1 from above shooting b2 (SWAPPED)
                        # HP logic: Lvl 1 -> 2 hits
                        new_enemy = Enemy(screen_width, e1_img, enemy_shoot_sfx, b2_img, enemy_small_explosion, hp=2)
                        enemy_group.add(new_enemy)
                    elif current_level == 2:
                        # Level 2 Vertical: Random chance for enemy2_1 shooting b1 (SWAPPED)
                        if random.random() < 0.6:
                            # 40% chance for e1 (added per request to have e1 in lvl 2)
                            if random.random() < 0.4:
                                # e1 in Level 2. HP logic: Lvl 2 -> 1 hit
                                new_enemy = Enemy(screen_width, e1_img, enemy_shoot_sfx, b2_img, enemy_small_explosion,
                                                  hp=1)
                            else:
                                new_enemy = Enemy(screen_width, enemy2_1_img, enemy_shoot_sfx, b1_img,
                                                  # Changed to b1_img
                                                  explosion3_frames, speed=None, damage=8, hp=3,
                                                  bullet_speed=enemy2_bullet_speed)
                            enemy_group.add(new_enemy)
                    elif current_level == 3:
                        # Level 3 Vertical: enemy2_1, enemy2_2 or e1
                        r = random.random()
                        if r < 0.3:
                            # Spawn e1 in Level 3. HP logic: Lvl 3 -> 1 hit
                            new_enemy = Enemy(screen_width, e1_img, enemy_shoot_sfx, b2_img, enemy_small_explosion,
                                              hp=1)
                        elif r < 0.65:
                            # enemy2_1 in Level 3. HP = 2
                            new_enemy = Enemy(screen_width, enemy2_1_img, enemy_shoot_sfx, b1_img,  # Changed to b1_img
                                              explosion3_frames, speed=None, damage=15, hp=2,
                                              bullet_speed=enemy2_bullet_speed)
                        else:
                            # enemy2_2 in Level 3. HP = 3
                            new_enemy = Enemy(screen_width, enemy2_2_img, enemy_shoot_sfx, b1_img,  # Changed to b1_img
                                              explosion3_frames, speed=None, damage=20, hp=3,
                                              bullet_speed=enemy2_bullet_speed)
                        enemy_group.add(new_enemy)

                if event.type == SPAWN_TRAIN_EVENT:
                    # In Level 3, if Boss is present, Vector troops appear "very less".
                    spawn_train = True
                    if current_level == 3 and boss_spawned:
                        # Only 20% chance to spawn train during boss fight
                        if random.random() > 0.2:
                            spawn_train = False

                    if spawn_train:
                        side = random.choice(["left", "right"])
                        train_speed = 3 * 0.8
                        start_x = -50 if side == "left" else screen_width + 50

                        train_count = 0
                        train_img = None
                        train_bullet = bullet_img  # Default bullet
                        train_explosion = enemy_small_explosion  # Default explosion

                        if current_level == 1:
                            # Level 1 Vector: 3x enemy1_1 -> shoots bullet.png (enemy_bullet_img)
                            train_count = 3
                            train_img = enemy1_img
                            train_bullet = enemy_bullet_img  # bullet.png
                        elif current_level == 2:
                            # Randomly choose between Enemy1_1 (Vector) and Enemy1_3 (Circle)
                            if random.random() < 0.5:
                                # Enemy 1.1 - Vector
                                train_count = 3
                                train_img = enemy1_img
                                train_bullet = enemy_bullet_img
                            else:
                                # Enemy 1.3 - Circle (Handled by is_circle_spawn check later)
                                train_count = 4
                                train_img = enemy1_3_img
                                train_bullet = b3_img
                        elif current_level == 3:
                            # Level 3 Vector: Random Mix
                            r = random.random()
                            if r < 0.33:
                                # enemy1_1 -> bullet.png
                                train_count = 3
                                train_img = enemy1_img
                                train_bullet = enemy_bullet_img
                            elif r < 0.66:
                                # enemy1_3 -> b3.png
                                train_count = 4
                                train_img = enemy1_3_img
                                train_bullet = b3_img
                            else:
                                # enemy1_2 -> b3.png
                                train_count = 6  # 6 enemies per request
                                train_img = enemy1_2_img
                                train_bullet = b3_img

                        # Check specifically for Level 2/3 circle logic for enemy1_3
                        is_circle_spawn = False
                        if current_level == 2:
                            # Level 2 was "4 enemy1_3" -> Circle
                            if train_img == enemy1_3_img:
                                is_circle_spawn = True
                        elif current_level == 3:
                            if train_img == enemy1_3_img:
                                is_circle_spawn = True

                        # Check for Level 3 Cross Spawn logic for enemy1_2
                        is_cross_spawn = False
                        if current_level == 3 and train_img == enemy1_2_img:
                            is_cross_spawn = True

                        if train_img:
                            if is_circle_spawn:
                                # Spawn 4 enemies in circle formation
                                center_pos = [random.randint(100, screen_width - 100), -100]
                                radius = 80
                                for i in range(4):
                                    angle = (math.pi / 2) * i  # 0, 90, 180, 270 degrees
                                    # HP is 1 for all small enemies in train/circle as per request
                                    e = Enemy(screen_width, train_img, enemy_shoot_sfx, train_bullet, train_explosion,
                                              movement_type="rotate", center_pos=list(center_pos), radius=radius,
                                              angle=angle, hp=1)
                                    enemy_group.add(e)
                            elif is_cross_spawn:
                                # Spawn 6 enemies: 3 Left->Right, 3 Right->Left
                                # Left -> Right Group
                                for i in range(3):
                                    e = Enemy(screen_width, train_img, enemy_shoot_sfx, train_bullet, train_explosion,
                                              speed=train_speed, movement_type="train_left", hp=1)
                                    e.rect.x = -50 - (i * 80)  # Stagger horizontally offscreen
                                    e.rect.y = 50 + (i * 60)  # Stagger vertically
                                    enemy_group.add(e)

                                # Right -> Left Group
                                for i in range(3):
                                    e = Enemy(screen_width, train_img, enemy_shoot_sfx, train_bullet, train_explosion,
                                              speed=train_speed, movement_type="train_right", hp=1)
                                    e.rect.x = screen_width + 50 + (i * 80)  # Stagger horizontally offscreen
                                    e.rect.y = 50 + (i * 60)  # Stagger vertically to match or criss-cross
                                    enemy_group.add(e)

                            else:
                                # Spawn Vector/Train formation (Standard)
                                # Determine spacing based on enemy type
                                spacing_x = 100
                                spacing_y = 50

                                for i in range(train_count):
                                    # HP is 1 for all small enemies in train/circle as per request
                                    e = Enemy(screen_width, train_img, enemy_shoot_sfx, train_bullet, train_explosion,
                                              speed=train_speed, movement_type=f"train_{side}", hp=1)
                                    # Horizontal spacing:
                                    x_offset = spacing_x * i if side == "left" else -spacing_x * i
                                    e.rect.x = start_x + x_offset
                                    # Vertical spacing:
                                    e.rect.y = 50 - (spacing_y * i)
                                    enemy_group.add(e)

            if event.type == pygame.MOUSEBUTTONDOWN and game_state == "PLAYING":
                # Check bounds/state before processing input
                if not level_complete and not player_exploding and not boss_exploding:
                    # Left Click: Shoot
                    if event.button == 1:
                        if player.laser_active:
                            if laser_sfx: laser_sfx.play()  # Play Laser Sound
                            offset = 25
                            l1 = Laser(player.rect.centerx - offset, player.rect.top, laser_raw, player.bullet_damage)
                            l2 = Laser(player.rect.centerx + offset, player.rect.top, laser_raw, player.bullet_damage)
                            bullet_group.add(l1)
                            bullet_group.add(l2)
                        else:
                            if shoot_sfx: shoot_sfx.play()  # Play Normal Shoot Sound
                            bullet = Bullet(player.rect.centerx, player.rect.top, bullet_img, player.bullet_damage)
                            bullet_group.add(bullet)

                        if player.clone_active:
                            clone_shoot_offset = 70
                            # 50% damage for clones
                            c_dmg = player.bullet_damage * 0.5
                            c1 = Bullet(player.rect.centerx - clone_shoot_offset, player.rect.top, bullet_img,
                                        c_dmg)
                            c2 = Bullet(player.rect.centerx + clone_shoot_offset, player.rect.top, bullet_img,
                                        c_dmg)
                            bullet_group.add(c1)
                            bullet_group.add(c2)

                    # Right Click: Activate Shield
                    elif event.button == 3:
                        if player.shields > 0 and not player.shield_active:
                            player.activate_shield(4)

            # --- KEY MAPPING UPDATES ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state == "PLAYING":
                        game_state = "PAUSE"
                        pygame.mouse.set_visible(True)
                    elif game_state == "PAUSE":
                        game_state = "PLAYING"
                        pygame.mouse.set_visible(False)
                    elif game_state == "STORE":
                        game_state = previous_state
                        # Reset store input flag when leaving store
                        mouse_released_in_store = False

                if game_state == "PLAYING" and not level_complete and not player_exploding and not boss_exploding:
                    # 'A' KEY -> NUCLEAR
                    if event.key == pygame.K_a:
                        if player.nukes > 0:
                            player.nukes -= 1
                            # Wipe screen
                            for m in meteor_group:
                                m.kill()
                                if enemy_sfx: enemy_sfx.play()  # Meteor Sound (using enemy_sfx as requested)
                                expl = Explosion(m.rect.center, meteor_explosion_assets['normal'])
                                explosion_group.add(expl)
                            for e in enemy_group:
                                e.kill()
                                if enemy_sfx: enemy_sfx.play()  # Sound
                                expl = Explosion(e.rect.center, e.explosion_frames)
                                explosion_group.add(expl)

                            # Boss Nuke Damage (3x Base Bullet Damage)
                            for b in boss_group:
                                # Nuke NO LONGER damages boss per instruction
                                pass

                            draw_popup(screen, "NUKE BLAST!", player.rect)

                    # 'W' KEY -> ROCKET
                    if event.key == pygame.K_w:
                        if player.rockets > 0:
                            player.rockets -= 1
                            rocket = Rocket(player.rect.centerx, player.rect.top, rocket_game_img, player.bullet_damage)
                            bullet_group.add(rocket)
                            if flying_rocket_sfx: flying_rocket_sfx.play()

                    # 'S' KEY -> HEAL
                    if event.key == pygame.K_s:
                        player.use_potion()

                    # 'D' KEY -> LASER
                    if event.key == pygame.K_d:
                        player.activate_laser(5)

                    # 'F' KEY -> CLONE
                    if event.key == pygame.K_f:
                        player.activate_clones(5)

                    if event.key == pygame.K_1:
                        player.switch_plane('plane1')

                    if event.key == pygame.K_2:
                        player.switch_plane('plane2')

                    if event.key == pygame.K_3:
                        player.switch_plane('plane3')

        # --- STATE MACHINE ---

        if game_state == "MENU":
            screen.blit(bg_menu_img, (0, 0))

            if start_btn.draw(screen):
                # FIXED POPUP: Using button dimensions (Scaled down to 80% for better look)
                popup_w = int(start_img.get_width() * 0.8)
                popup_h = int(start_img.get_height() * 0.8)
                draw_popup(screen, "Get Ready!", start_btn.rect, fixed_size=(popup_w, popup_h))
                pygame.time.delay(1000)
                game_state = "PLAYING"
                current_level = 1
                bg_scroll = 0

                # --- FRESH START LOGIC ---
                # Reset ALL stats and inventory to 0 for a fresh game
                player.reset_stats()
                player_score = 0  # Reset Coins
                player.switch_plane('plane1')  # Reset visual to basic plane

                # Reset Level Logic
                level_start_time = pygame.time.get_ticks()
                boss_spawned = False
                level_complete = False
                player_exploding = False
                boss_exploding = False
                active_boss_explosion = None
                warning_played = False  # Re-initialized here as well

                # Initialize Timers for Level 1 - CRITICAL FIX FOR LEVEL 1 TRAINS
                pygame.time.set_timer(SPAWN_METEOR_EVENT, 1500)
                pygame.time.set_timer(SPAWN_ENEMY_EVENT, 2500)
                pygame.time.set_timer(SPAWN_TRAIN_EVENT, 5000)  # Added train timer for Level 1

                pygame.mouse.set_visible(False)

            if store_btn.draw(screen):
                game_state = "STORE"
                previous_state = "MENU"
                mouse_released_in_store = False  # Reset click flag

            if exit_btn.draw(screen):
                popup_w = int(exit_img.get_width() * 0.8)
                popup_h = int(exit_img.get_height() * 0.8)
                draw_popup(screen, "Goodbye!", exit_btn.rect, fixed_size=(popup_w, popup_h))
                pygame.time.delay(1000)
                run = False

        elif game_state == "STORE":
            screen.blit(bg_shop_img, (0, 0))

            title_surf = font_large.render("STORE", True, (255, 255, 255))
            screen.blit(title_surf, (center_x - title_surf.get_width() // 2, 50))

            coin_surf = font_large.render(f"Coins: {player_score}", True, (255, 215, 0))
            screen.blit(coin_surf, (screen_width - coin_surf.get_width() - 20, 20))

            instr_surf = font_small.render("Press ESC to go back", True, (200, 200, 200))
            screen.blit(instr_surf, (20, 20))

            # Store Click Logic fix: check if mouse is released before allowing purchase
            if pygame.mouse.get_pressed()[0] == 0:
                mouse_released_in_store = True

            for item in shop_items:
                if item.draw(screen, player_score, allow_input=mouse_released_in_store):
                    player_score -= item.price
                    # Play Coin SFX on purchase
                    if coin_sfx: coin_sfx.play()
                    print(f"Bought {item.name}")

                    if item.item_id == "rocket":
                        player.rockets += 1
                    elif item.item_id == "nuke":
                        player.nukes += 1
                    elif item.item_id == "shield":
                        player.shields += 1
                    elif item.item_id == "heal":
                        player.potions += 1
                    elif item.item_id == "laser":
                        player.lasers += 1
                    elif item.item_id == "clone":
                        player.clones += 1

                # --- NEW: Play Sound on Collect ---
                if collected_coins:
                    if coin_sfx:
                        coin_sfx.play()
                    player_score += len(collected_coins)

                collected_boxes = pygame.sprite.spritecollide(player, mystery_box_group, True)
                for box in collected_boxes:
                    reward_type = random.choice(['rocket', 'nuke', 'shield', 'heal', 'laser', 'clone'])
                    if reward_type == 'rocket':
                        player.rockets += 1
                    elif reward_type == 'nuke':
                        player.nukes += 1
                    elif reward_type == 'shield':
                        player.shields += 1
                    elif reward_type == 'heal':
                        player.potions += 1
                    elif reward_type == 'laser':
                        player.lasers += 1
                    elif reward_type == 'clone':  # Fixed variable name here (was item.item_id)
                        player.clones += 1
                    draw_popup(screen, f"GOT {reward_type.upper()}!", player.rect)

                if player.clone_active:
                    clone_rects = player.get_clone_rects()

        elif game_state == "PAUSE":
            screen.blit(bg_menu_img, (0, 0))

            if resume_btn.draw(screen):
                game_state = "PLAYING"
                pygame.mouse.set_visible(False)
                # Note: Not adjusting timer, so 45s includes pause time currently

            if store_btn.draw(screen):
                game_state = "STORE"
                previous_state = "PAUSE"
                mouse_released_in_store = False

            if exit_btn.draw(screen):
                popup_w = int(exit_img.get_width() * 0.8)
                popup_h = int(exit_img.get_height() * 0.8)
                draw_popup(screen, "Goodbye!", exit_btn.rect, fixed_size=(popup_w, popup_h))
                pygame.time.delay(1000)
                run = False

        elif game_state == "LEVEL_2_MENU":
            # Level 2 Transition Screen
            screen.blit(bg_menu_img, (0, 0))

            # Welcome Text
            welcome_surf = font_large.render("Welcome to Level 2", True, (100, 255, 100))
            screen.blit(welcome_surf, (center_x - welcome_surf.get_width() // 2, screen_height - 100))

            # Buttons (Reuse Logic)
            if resume_btn.draw(screen):  # Acts as "Start Level 2"
                draw_popup(screen, "Starting Lvl 2", resume_btn.rect,
                           fixed_size=(resume_img.get_width(), resume_img.get_height()))
                pygame.time.delay(1000)

                game_state = "PLAYING"
                current_level = 2

                # Reset Position & States
                player.rect.centerx = screen_width // 2
                player.rect.bottom = screen_height - 50
                player.shield_active = False

                # Unlock Plane 2 if not owned (due to reset logic) and switch
                if 'plane2' not in player.owned_planes:
                    player.owned_planes.append('plane2')

                # FORCE SWITCH TO PLANE 2
                player.switch_plane('plane2')
                # Heal to new max HP
                player.hp = player.max_hp

                # Reset Boss/Level Logic
                level_start_time = pygame.time.get_ticks()
                boss_spawned = False
                level_complete = False
                player_exploding = False
                boss_exploding = False
                active_boss_explosion = None
                warning_played = False

                # Clear any lingering objects from transition
                bullet_group.empty()

                pygame.mouse.set_visible(False)
                # Ensure timers are running
                # INCREASED DIFFICULTY: Faster meteor spawns (800ms) for "continuous drop" feeling
                pygame.time.set_timer(SPAWN_METEOR_EVENT, 800)
                pygame.time.set_timer(SPAWN_ENEMY_EVENT, 1500)  # More frequent in Level 2
                pygame.time.set_timer(SPAWN_TRAIN_EVENT, 5000)  # Train spawns every 5s

            if store_btn.draw(screen):
                game_state = "STORE"
                previous_state = "LEVEL_2_MENU"
                mouse_released_in_store = False

            if exit_btn.draw(screen):
                popup_w = int(exit_img.get_width() * 0.8)
                popup_h = int(exit_img.get_height() * 0.8)
                draw_popup(screen, "Goodbye!", exit_btn.rect, fixed_size=(popup_w, popup_h))
                pygame.time.delay(1000)
                run = False

        elif game_state == "LEVEL_3_MENU":
            # Level 3 Transition Screen
            screen.blit(bg_menu_img, (0, 0))

            # Welcome Text
            welcome_surf = font_large.render("Welcome to Level 3", True, (100, 100, 255))
            screen.blit(welcome_surf, (center_x - welcome_surf.get_width() // 2, screen_height - 100))

            # Use same pattern: Resume (Start), Store, Exit
            if resume_btn.draw(screen):
                draw_popup(screen, "Starting Lvl 3", resume_btn.rect,
                           fixed_size=(resume_img.get_width(), resume_img.get_height()))
                pygame.time.delay(1000)

                game_state = "PLAYING"
                current_level = 3

                # Reset Pos
                player.rect.centerx = screen_width // 2
                player.rect.bottom = screen_height - 50
                player.shield_active = False

                if 'plane3' not in player.owned_planes:
                    player.owned_planes.append('plane3')

                # FORCE SWITCH TO PLANE 3
                player.switch_plane('plane3')
                player.hp = player.max_hp

                # Reset Logic
                level_start_time = pygame.time.get_ticks()
                boss_spawned = False
                level_complete = False
                player_exploding = False
                boss_exploding = False
                active_boss_explosion = None
                bullet_group.empty()
                pygame.mouse.set_visible(False)
                warning_played = False

                # Timers same as L2
                pygame.time.set_timer(SPAWN_METEOR_EVENT, 800)
                pygame.time.set_timer(SPAWN_ENEMY_EVENT, 1500)
                pygame.time.set_timer(SPAWN_TRAIN_EVENT, 5000)

            if store_btn.draw(screen):
                game_state = "STORE"
                previous_state = "LEVEL_3_MENU"
                mouse_released_in_store = False

            if exit_btn.draw(screen):
                popup_w = int(exit_img.get_width() * 0.8)
                popup_h = int(exit_img.get_height() * 0.8)
                draw_popup(screen, "Goodbye!", exit_btn.rect, fixed_size=(popup_w, popup_h))
                pygame.time.delay(1000)
                run = False

        elif game_state == "GAME_WIN":
            # Victory Screen
            screen.blit(bg_menu_img, (0, 0))

            # Congratulations Text
            win_surf = font_large.render("CONGRATULATIONS!", True, (255, 215, 0))
            # Optional drop shadow for readability
            win_shadow = font_large.render("CONGRATULATIONS!", True, (0, 0, 0))

            cx = screen_width // 2
            cy = screen_height // 2

            screen.blit(win_shadow, (cx - win_surf.get_width() // 2 + 2, cy - 100 + 2))
            screen.blit(win_surf, (cx - win_surf.get_width() // 2, cy - 100))

            # Only Exit Button in middle
            exit_btn.rect.centerx = cx
            exit_btn.rect.top = cy + 50

            if exit_btn.draw(screen):
                popup_w = int(exit_img.get_width() * 0.8)
                popup_h = int(exit_img.get_height() * 0.8)
                draw_popup(screen, "Goodbye!", exit_btn.rect, fixed_size=(popup_w, popup_h))
                pygame.time.delay(1000)
                run = False

        elif game_state == "PLAYING":
            # --- Draw Background based on Level ---
            bg_scroll += SCROLL_SPEED
            if bg_scroll > screen_height:
                bg_scroll = 0

            if current_level == 1:
                screen.blit(bg_level1_img, (0, bg_scroll))
                screen.blit(bg_level1_img, (0, bg_scroll - screen_height))
                duration = LEVEL1_DURATION
            elif current_level == 2:
                screen.blit(bg_level2_img, (0, bg_scroll))
                screen.blit(bg_level2_img, (0, bg_scroll - screen_height))
                duration = LEVEL2_DURATION
            elif current_level == 3:
                screen.blit(bg_level3_img, (0, bg_scroll))
                screen.blit(bg_level3_img, (0, bg_scroll - screen_height))
                duration = LEVEL3_DURATION

            # --- Check Boss Spawn ---
            if not boss_spawned and not level_complete and not player_exploding and not boss_exploding:

                # --- WARNING SOUND LOGIC ---
                # Check for warning sound 2 seconds before boss
                time_elapsed = current_time - level_start_time
                if duration - time_elapsed <= 2000:
                    if not warning_played:
                        if warning_sfx: warning_sfx.play()
                        warning_played = True

                if current_time - level_start_time > duration:
                    # FAILSAFE: If warning hasn't played (lag?), play it NOW before boss spawns
                    if not warning_played:
                        if warning_sfx: warning_sfx.play()
                        warning_played = True

                    boss_spawned = True
                    # Clear screen for boss - TOTAL ISOLATION ONLY FOR LEVEL 1
                    if current_level == 1:
                        meteor_group.empty()
                        enemy_group.empty()
                        enemy_bullet_group.empty()
                        mystery_box_group.empty()

                        boss = Boss(screen_width, boss_img, missile_img, boss_bullet_img, boss_shoot_sfx, level=1)
                        boss_group.add(boss)
                    elif current_level == 2:
                        # For Level 2, we keep enemies spawning (handled in event loop logic above)
                        boss = Boss(screen_width, boss2_img, missile_img, boss_bullet_img, boss2_shoot_sfx, level=2)
                        boss_group.add(boss)
                    elif current_level == 3:
                        # For Level 3, keep spawning enemies. Reuse Boss 2 Asset but tougher (Level 3 stats in Boss class)
                        boss = Boss(screen_width, boss3_img, missile_img, boss_bullet_img, boss2_shoot_sfx, level=3)
                        boss_group.add(boss)

            # --- Update Logic (Active or Transition) ---
            if not level_complete and not player_exploding:
                player.update(screen_width, screen_height)
            elif level_complete and not boss_exploding and not player_exploding:
                # Cinematic Exit: Fly UP (Smoother transition)
                player.rect.y -= 8
                # When off screen, trigger transition
                if player.rect.bottom < -50:
                    if current_level == 1:
                        game_state = "LEVEL_2_MENU"
                        pygame.mouse.set_visible(True)
                    elif current_level == 2:
                        game_state = "LEVEL_3_MENU"
                        pygame.mouse.set_visible(True)
                    else:
                        # End of content for now
                        draw_popup(screen, "YOU WIN!", player.rect)
                        pygame.time.delay(3000)
                        run = False

            bullet_group.update()

            # Update Enemies/Meteors only if boss isn't present (or keep them?)
            # Usually nice to have 1v1. We cleared them above, so update calls are safe.
            meteor_group.update(screen_height)
            enemy_group.update(screen_width, screen_height, enemy_bullet_group, player.rect.centerx,
                               player.rect.centery)

            if not boss_exploding:
                boss_group.update(screen_width, enemy_bullet_group, player.rect.centerx, player.rect.centery)

            enemy_bullet_group.update()  # Updates boss bullets too
            explosion_group.update()
            coin_group.update(screen_height)
            mystery_box_group.update(screen_height)

            # --- Player vs Meteors ---
            if not player_exploding:
                hits = pygame.sprite.groupcollide(meteor_group, bullet_group, False, True)
                for meteor, bullets_hit in hits.items():
                    total_damage = sum([b.damage for b in bullets_hit])
                    meteor.hp -= total_damage
                    if meteor.hp <= 0:
                        meteor.kill()

                        # Use enemy_sfx (Enermy blast.wav) for ALL explosions per new instruction
                        if enemy_sfx: enemy_sfx.play()

                        expl = Explosion(meteor.rect.center, meteor_explosion_assets['normal'])
                        explosion_group.add(expl)

                        # Drop Logic based on Level
                        drop_chance_coin = BASE_COIN_RATE
                        drop_chance_mbox = BASE_MBOX_RATE

                        if current_level == 2:
                            drop_chance_coin *= 0.75
                            drop_chance_mbox *= 0.75
                        elif current_level == 3:
                            drop_chance_coin *= 0.05
                            drop_chance_mbox *= 0.05

                        if random.random() < drop_chance_coin:
                            coin = Coin(meteor.rect.center, coin_img)
                            coin_group.add(coin)
                        if random.random() < drop_chance_mbox:
                            mbox = MysteryBox(meteor.rect.center, mbox_img)
                            mystery_box_group.add(mbox)

            # --- Player vs Enemies ---
            if not player_exploding:
                enemy_hits = pygame.sprite.groupcollide(enemy_group, bullet_group, False, True)
                for enemy, bullets_hit in enemy_hits.items():
                    total_damage = sum([b.damage for b in bullets_hit])
                    enemy.hp -= total_damage
                    if enemy.hp <= 0:
                        # Clean up enemy's bullets
                        for b in enemy.fired_bullets:
                            b.kill()
                        enemy.kill()
                        if enemy_sfx: enemy_sfx.play()  # Enemy Sound
                        expl = Explosion(enemy.rect.center, enemy.explosion_frames)
                        explosion_group.add(expl)

                        # Drop Logic based on Level (Reused vars)
                        drop_chance_coin = BASE_COIN_RATE
                        drop_chance_mbox = BASE_MBOX_RATE

                        if current_level == 2:
                            drop_chance_coin *= 0.75
                            drop_chance_mbox *= 0.75
                        elif current_level == 3:
                            drop_chance_coin *= 0.05
                            drop_chance_mbox *= 0.05

                        if random.random() < drop_chance_coin:
                            coin = Coin(enemy.rect.center, coin_img)
                            coin_group.add(coin)
                        if random.random() < drop_chance_mbox:
                            mbox = MysteryBox(enemy.rect.center, mbox_img)
                            mystery_box_group.add(mbox)

            # --- Player vs Boss ---
            if not player_exploding and not boss_exploding:
                boss_hits = pygame.sprite.groupcollide(boss_group, bullet_group, False, True)
                for boss, bullets_hit in boss_hits.items():
                    # Apply special damage calculation logic for Boss
                    total_damage = 0
                    for b in bullets_hit:
                        if isinstance(b, Rocket):
                            total_damage += player.bullet_damage * 2  # Rocket vs Boss = 2x Base Damage
                        else:
                            total_damage += b.damage  # Standard damage for bullets/lasers

                    boss.hp -= total_damage

                    if boss.hp <= 0:
                        boss.kill()
                        if enemy_sfx: enemy_sfx.play()  # Boss Explosion Sound (Reused enemy blast)

                        # Boss Bonus Logic
                        if current_level == 1:
                            player_score += 10
                            draw_popup(screen, "BOSS DOWN! +10 Gold", boss.rect)
                        elif current_level == 2:
                            player_score += 15
                            draw_popup(screen, "BOSS DOWN! +15 Gold", boss.rect)
                        else:
                            draw_popup(screen, "VICTORY!", boss.rect)

                        # Boss Death Explosion (Big Sequence)
                        # We use active_boss_explosion to track it
                        expl = Explosion(boss.rect.center, explosion2_frames)
                        expl.animation_speed = 5
                        explosion_group.add(expl)
                        active_boss_explosion = expl

                        boss_exploding = True  # Trigger boss death state

                        # Use Game Over SFX for Level 3 Victory / Boss Death
                        if current_level == 3:
                            if game_over_event_sfx: game_over_event_sfx.play()
                        else:
                            # Standard boss death sound
                            if enemy_sfx: enemy_sfx.play()

                        # Clean up hazards - Only clear hazards if transitioning or safe
                        enemy_bullet_group.empty()
                        # We might want to clear enemies too for the cinematics
                        enemy_group.empty()
                        mystery_box_group.empty()

            if not player_exploding:
                collected_coins = pygame.sprite.spritecollide(player, coin_group, True)

                # --- NEW: Play Sound on Collect ---
                if collected_coins:
                    if coin_sfx:
                        coin_sfx.play()
                    player_score += len(collected_coins)

                collected_boxes = pygame.sprite.spritecollide(player, mystery_box_group, True)
                for box in collected_boxes:
                    reward_type = random.choice(['rocket', 'nuke', 'shield', 'heal', 'laser', 'clone'])
                    if reward_type == 'rocket':
                        player.rockets += 1
                    elif reward_type == 'nuke':
                        player.nukes += 1
                    elif reward_type == 'shield':
                        player.shields += 1
                    elif reward_type == 'heal':
                        player.potions += 1
                    elif reward_type == 'laser':
                        player.lasers += 1
                    elif reward_type == 'clone':  # Fixed variable name here (was item.item_id)
                        player.clones += 1
                    draw_popup(screen, f"GOT {reward_type.upper()}!", player.rect)

                if player.clone_active:
                    clone_rects = player.get_clone_rects()
                    for c_rect in clone_rects:
                        # Manually check collisions since these are rects, not sprites
                        for coin in coin_group:
                            if c_rect.colliderect(coin.rect):
                                coin.kill()
                                player_score += 1
                                if coin_sfx:
                                    coin_sfx.play()

            # --- Collision: Player taking damage ---
            if not player_exploding and not boss_exploding:
                # 1. From Meteors
                crash_hits = pygame.sprite.spritecollide(player, meteor_group, True)
                for meteor in crash_hits:
                    if not player.shield_active: player.hp -= 20

                    # Sound Logic for Collision
                    if enemy_sfx: enemy_sfx.play()

                    expl = Explosion(meteor.rect.center, meteor.explosion_frames)
                    explosion_group.add(expl)

                # 2. From Enemy Bodies
                enemy_crash_hits = pygame.sprite.spritecollide(player, enemy_group, True)
                for enemy in enemy_crash_hits:
                    if not player.shield_active: player.hp -= 20
                    # Enemy dies on crash, so clean up bullets
                    for b in enemy.fired_bullets:
                        b.kill()
                    if enemy_sfx: enemy_sfx.play()
                    expl = Explosion(enemy.rect.center, enemy.explosion_frames)
                    explosion_group.add(expl)

                # 3. From Boss Body - MUTUAL DAMAGE LOGIC
                boss_crash_list = pygame.sprite.spritecollide(player, boss_group, False)
                if boss_crash_list and not player.shield_active:
                    player.hp -= 2  # Player takes heavy damage per frame
                    for b in boss_crash_list:
                        b.hp -= 0.5  # Boss takes light chip damage per frame

                # 4. From Bullets (Enemy & Boss)
                bullet_hits = pygame.sprite.spritecollide(player, enemy_bullet_group, True)
                for bullet in bullet_hits:
                    if not player.shield_active:
                        player.hp -= bullet.damage

                    # Game Over check
            if player.hp <= 0 and not player_exploding:
                # Initiate Player Death Sequence
                player_exploding = True

                # Player Death Explosion (Big Sequence)
                expl = Explosion(player.rect.center, explosion2_frames)
                expl.animation_speed = 5
                explosion_group.add(expl)

                # We track this specific explosion to know when it finishes
                active_player_explosion = expl

                # Stop BG music and Play Game Over Sound
                stop_music()
                if game_over_event_sfx:
                    game_over_event_sfx.play()

                # Hide Player (Move offscreen)
                player.rect.center = (-1000, -1000)

            # --- Drawing ---

            # If player is alive or exploding, we draw relevant stuff
            if not player_exploding:
                player.draw(screen)

            meteor_group.draw(screen)
            enemy_group.draw(screen)
            boss_group.draw(screen)
            bullet_group.draw(screen)
            enemy_bullet_group.draw(screen)
            explosion_group.draw(screen)
            coin_group.draw(screen)
            mystery_box_group.draw(screen)

            # Show Boss HP in HUD if active (and not exploded yet)
            active_boss = boss_group.sprites()[0] if boss_group else None
            draw_hud(screen, player_score, player, screen_width, screen_height, hud_icons, active_boss)

            # Draw Health Bars for Enemies
            for enemy in enemy_group:
                # Yellow for enemies (R, G, B) = (255, 255, 0)
                draw_entity_health_bar(screen, enemy, (255, 255, 0))

                # Draw Health Bars for Meteors
            for meteor in meteor_group:
                # Orange for meteors (R, G, B) = (255, 165, 0)
                draw_entity_health_bar(screen, meteor, (255, 165, 0))

                # --- Logic to Wait for Explosions to Finish ---

            # 1. Player Death Finish Logic
            if player_exploding:
                # Check if the specific explosion sprite is still alive
                if active_player_explosion is not None and not active_player_explosion.alive():
                    # Animation finished
                    pygame.time.delay(1000)  # Short pause after explosion

                    # Create a dummy rect in the center of the screen for the popup
                    center_rect = pygame.Rect(screen_width // 2, screen_height // 2, 1, 1)
                    draw_popup(screen, "GAME OVER!", center_rect)

                    pygame.time.delay(2000)
                    game_state = "MENU"
                    # Reset Groups
                    bullet_group.empty()
                    meteor_group.empty()
                    enemy_group.empty()
                    enemy_bullet_group.empty()
                    explosion_group.empty()
                    coin_group.empty()
                    mystery_box_group.empty()
                    boss_group.empty()
                    pygame.time.set_timer(SPAWN_METEOR_EVENT, 0)
                    pygame.time.set_timer(SPAWN_ENEMY_EVENT, 0)
                    pygame.mouse.set_visible(True)
                    player_exploding = False  # Reset flag

            # 2. Boss Death Finish Logic
            if boss_exploding:
                # Check if boss explosion finished
                if active_boss_explosion is not None and not active_boss_explosion.alive():
                    boss_exploding = False
                    level_complete = True
                    if flying_rocket_sfx: flying_rocket_sfx.play()
                    # Now the loop will hit the "Cinematic Exit" block at top of update logic

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()










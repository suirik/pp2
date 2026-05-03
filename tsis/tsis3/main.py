import pygame, sys, random, time, os
import persistence
from racer import Player, Enemy, Collectible, get_asset

# Инициализация
pygame.init()
pygame.mixer.init()
print(get_asset("Player.png"))

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer KBTU Edition")
clock = pygame.time.Clock()

# Цвета
RED, WHITE, BLACK, YELLOW, BLUE = (255,0,0), (255,255,255), (0,0,0), (255,255,0), (0,200,255)

# 🔧 ЗАГЛУШКА (чтобы не падало)
def play_music():
    pass

# Загружаем настройки
settings = persistence.load_json(
    'settings.json',
    {"sound": True, "color": "Player.png", "diff": 1}
)

def draw_text(text, size, y, color=WHITE, x=WIDTH//2):
    font = pygame.font.SysFont("Verdana", size, bold=True)
    surf = font.render(str(text), True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)

def button(text, y):
    mx, my = pygame.mouse.get_pos()
    rect = pygame.Rect(WIDTH//2 - 110, y - 25, 220, 50)
    on_hover = rect.collidepoint(mx, my)
    draw_text(text, 30, y, YELLOW if on_hover else WHITE)

    if on_hover and pygame.mouse.get_pressed()[0]:
        return True
    return False


def leaderboard_screen():
    time.sleep(0.2)
    running = True

    while running:
        screen.fill(BLACK)
        draw_text("TOP 10 PILOTS", 35, 60, YELLOW)

        data = persistence.load_json('leaderboard.json', [])
        sorted_data = sorted(data, key=lambda x: x.get('score', 0), reverse=True)[:10]

        for idx, entry in enumerate(sorted_data):
            name = entry.get('name', 'Unknown')
            score = entry.get('score', 0)
            draw_text(f"{idx+1}. {name}: {int(score)}", 20, 130 + idx*35)

        if button("BACK", 530):
            running = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


def settings_screen():
    time.sleep(0.2)
    running = True

    while running:
        screen.fill(BLACK)
        draw_text("SETTINGS", 40, 100, YELLOW)

        m_txt = "MUSIC: ON" if settings['sound'] else "MUSIC: OFF"
        if button(m_txt, 220):
            settings['sound'] = not settings['sound']
            persistence.save_json('settings.json', settings)
            play_music()
            time.sleep(0.2)

        diffs = {1: "EASY", 2: "MEDIUM", 3: "HARD"}
        if button(f"DIFF: {diffs[settings['diff']]}", 300):
            settings['diff'] = 1 if settings['diff'] == 3 else settings['diff'] + 1
            persistence.save_json('settings.json', settings)
            time.sleep(0.2)

        if button("BACK", 450):
            running = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


def game_run(username):
    try:
        road = pygame.transform.scale(
            pygame.image.load(get_asset("road.png")),
            (WIDTH, HEIGHT)
        )
    except:
        road = pygame.Surface((WIDTH, HEIGHT))
        road.fill((50, 50, 50))

    road_y = 0

    player = Player(settings['color'])
    speed = 4 + (settings['diff'] * 2)

    enemies = pygame.sprite.Group(Enemy(speed))
    items = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(*enemies)

    score, dist = 0, 0
    effect_timer = 0
    effect_msg = ""

    while True:
        road_y += speed
        if road_y >= HEIGHT:
            road_y = 0

        screen.blit(road, (0, road_y))
        screen.blit(road, (0, road_y - HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if random.randint(1, 80) == 1:
            itype = random.choice(['coinn', 'oil', 'shield', 'boost', 'heal'])
            item = Collectible(itype, speed)
            items.add(item)
            all_sprites.add(item)

        player.move()
        enemies.update()
        items.update()

        dist += speed / 50

        if pygame.sprite.spritecollide(player, enemies, False):
            if player.shield:
                player.shield = False
                effect_msg = "SHIELD BROKEN!"
                effect_timer = 60
                for e in enemies:
                    e.rect.y = -200
            else:
                screen.fill(RED)
                draw_text("CRASH!", 60, HEIGHT//2)
                pygame.display.update()
                time.sleep(2)

                final_score = int(score + dist)
                persistence.update_leaderboard(username, final_score, dist)
                return

        hits = pygame.sprite.spritecollide(player, items, True)
        for h in hits:
            effect_timer = 60

            if h.type == 'coinn':
                score += 100
                effect_msg = "+100 SCORE"
            elif h.type == 'oil':
                speed = max(4, speed - 3)
                effect_msg = "SLOW"
            elif h.type == 'shield':
                player.shield = True
                effect_msg = "SHIELD"
            elif h.type == 'boost':
                speed += 4
                effect_msg = "BOOST"
            elif h.type == 'heal':
                score += 500
                effect_msg = "BONUS"

        for s in all_sprites:
            screen.blit(s.image, s.rect)

        if player.shield:
            pygame.draw.circle(screen, BLUE, player.rect.center, 55, 3)

        draw_text(f"Score: {int(score + dist)}", 20, 30)

        if effect_timer > 0:
            draw_text(effect_msg, 25, 100, YELLOW)
            effect_timer -= 1

        pygame.display.update()
        clock.tick(60)


def input_name_screen():
    name = ""

    while True:
        screen.fill(BLACK)
        draw_text("ENTER NAME:", 25, 200)
        draw_text(name, 35, 300, YELLOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += event.unicode

        pygame.display.update()
        clock.tick(60)


def main_menu():
    play_music()

    while True:
        screen.fill(BLACK)
        draw_text("RACER 2026", 50, 100, YELLOW)

        if button("PLAY", 220):
            user = input_name_screen()
            if user:
                game_run(user)

        if button("LEADERBOARD", 290):
            leaderboard_screen()

        if button("SETTINGS", 360):
            settings_screen()

        if button("QUIT", 430):
            pygame.quit()
            sys.exit()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main_menu() 
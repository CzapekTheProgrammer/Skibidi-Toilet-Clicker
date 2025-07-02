import pygame
import sys
import base64
import io

pygame.init()

WIDTH, HEIGHT = 400, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("skibidi clicker")

font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

score = 0
points_per_click = 1
upgrade_cost = 10

auto_clicker_level = 0
auto_clicker_cost = 50
auto_clicker_rate = 1  # points per second added per level

# Your decal base64 image
base64_data = """
/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIADgAHwMBIgACEQEDEQH/xAAbAAACAwEBAQAAAAAAAAAAAAAGBwAEBQIDAf/EADEQAAIBAwIEBAQFBQAAAAAAAAECAwQFEQAhBhITMSJBUYEUYZGhByMkwfBCcXKisf/EABgBAAMBAQAAAAAAAAAAAAAAAAECAwAE/8QAHREAAgIDAQEBAAAAAAAAAAAAAAECERIhQTFRA//aAAwDAQACEQMRAD8AlmnEF5pyTgODH9Rt99GtBMOqxUggouD69z+40sLhXQUc0XVqEhcnKFmx289Vr3JxJxRUMeH5ulbosBIqebpmRsZc7d/Fkd/LXFBXFWWknk6HMZdV5pv1CDP9OlZwtTcXcOVVPNdKpnoKhxHJTzSl2UscKRnsc47Htpgl1qIWLuy84HiU4K48hrOuOzU16KK3Wh+K7lPUTM6U6tyqQccqj+f91tI1Za6xpbFXxRU6TLHHCqjpMud+YHfO+cj013LE9l4Kg6Q5WrpDGzj03yPfl+50PztGklLPIzIiHcqcbaZ71wMHsKqiquE0nxF1uw5EnzLBGqflASDl5BjOwB7nvolqbdDfOHpIrVdZXWQjlnXCshDA4IA22B+ul1A8NRUVMsExlaTOXc59s/fRJ+G88i3urpUY9NqbmZR2LBlwfoTpFHo36S3Re4gt7VnAP5K80tDN1MeeATzf6sT7aX0jO8BXkJx5aa9ouBoqhhPEr00o5ZQvcehA+WuKr8PbLdXNVarl8OrnLRqwAB/xPb220U/pPwV1Afh6eQhDGrHwA7E5+WmlwLY3slvluVbF+rrCoSI7FVHYf37k+w1ctPA1jsEqVlbUGsqEOYw7A4PyA2B+etSraWqYyEY5RhEXso9NLOdKkFLJ2zDNHIVyE++vajta9XxymLmBJ5Hxqamp5MpSNWC308cqyl3kZfCrO3YnbV2OnjLgMsZJ32181NI2w0f/2Q==
"""
image_data = base64.b64decode(base64_data)
image_file = io.BytesIO(image_data)
button_image = pygame.image.load(image_file).convert_alpha()
button_image = pygame.transform.smoothscale(button_image, (150, 100))
button_rect = button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))

upgrade_button_rect = pygame.Rect(WIDTH // 2 - 130, HEIGHT - 140, 260, 60)
auto_clicker_button_rect = pygame.Rect(WIDTH // 2 - 130, HEIGHT - 70, 260, 60)

def draw_button(surface, rect, base_text, cost, mouse_pos):
    color = (140, 190, 140) if rect.collidepoint(mouse_pos) else (100, 150, 100)
    pygame.draw.rect(surface, color, rect, border_radius=10)
    full_text = f"{base_text} - Cost: {cost}"
    txt_surf = font.render(full_text, True, (255, 255, 255))
    text_x = rect.x + (rect.width - txt_surf.get_width()) // 2
    text_y = rect.y + (rect.height - txt_surf.get_height()) // 2
    surface.blit(txt_surf, (text_x, text_y))

auto_clicker_timer = 0

running = True
while running:
    dt = clock.tick(60) / 1000  # seconds passed since last frame
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                score += points_per_click
            elif upgrade_button_rect.collidepoint(event.pos):
                if score >= upgrade_cost:
                    score -= upgrade_cost
                    points_per_click += 1
                    upgrade_cost = int(upgrade_cost * 1.5)
            elif auto_clicker_button_rect.collidepoint(event.pos):
                if score >= auto_clicker_cost:
                    score -= auto_clicker_cost
                    auto_clicker_level += 1
                    auto_clicker_cost = int(auto_clicker_cost * 2)

    # Auto-clicker adds points over time
    if auto_clicker_level > 0:
        auto_clicker_timer += dt
        if auto_clicker_timer >= 0.25:
            score += auto_clicker_level * auto_clicker_rate
            auto_clicker_timer = 0

    screen.fill((30, 30, 30))

    # Draw decal button
    screen.blit(button_image, button_rect)

    # Show score (centered above decal button)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, button_rect.top - 50))

    # Show points per click (below decal button)
    ppc_text = font.render(f"Points per Click: {points_per_click}", True, (255, 255, 255))
    screen.blit(ppc_text, (WIDTH // 2 - ppc_text.get_width() // 2, button_rect.bottom + 10))

    # Show auto-clicker level
    ac_text = font.render(f"Auto-Clicker Level: {auto_clicker_level}", True, (255, 255, 255))
    screen.blit(ac_text, (WIDTH // 2 - ac_text.get_width() // 2, button_rect.bottom + 35))

    # Draw upgrade buttons with centered auto-updating text
    draw_button(screen, upgrade_button_rect, "Upgrade (+1 click)", upgrade_cost, mouse_pos)
    draw_button(screen, auto_clicker_button_rect, f"Auto-Clicker (+{auto_clicker_rate}/s)", auto_clicker_cost, mouse_pos)

    pygame.display.flip()

pygame.quit()
sys.exit()

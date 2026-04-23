import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    mode = 'blue'
    draw_type = 'brush' # brush, rect, circle, eraser
    points = []

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held: return
                # Color selection
                if event.key == pygame.K_r: mode = 'red'
                if event.key == pygame.K_g: mode = 'green'
                if event.key == pygame.K_b: mode = 'blue'
                # Tool selection
                if event.key == pygame.K_e: draw_type = 'eraser'
                if event.key == pygame.K_p: draw_type = 'brush'
                if event.key == pygame.K_s: draw_type = 'rect'
                if event.key == pygame.K_c: draw_type = 'circle'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    start_pos = event.pos
                    if draw_type == 'rect':
                        pygame.draw.rect(screen, get_color(mode), (start_pos[0], start_pos[1], 50, 50))
                    elif draw_type == 'circle':
                        pygame.draw.circle(screen, get_color(mode), start_pos, 25)
            
            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                if pygame.mouse.get_pressed()[0]: # Dragging
                    if draw_type == 'brush':
                        draw_line_between(screen, position, last_pos, radius, get_color(mode))
                    elif draw_type == 'eraser':
                        draw_line_between(screen, position, last_pos, radius, (0,0,0))
                last_pos = position

        pygame.display.flip()
        clock.tick(60)

def get_color(mode):
    if mode == 'red': return (255, 0, 0)
    if mode == 'green': return (0, 255, 0)
    if mode == 'blue': return (0, 0, 255)
    return (255, 255, 255)

def draw_line_between(screen, start, end, width, color):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    iterations = max(abs(dx), abs(dy))
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1.0 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

main()
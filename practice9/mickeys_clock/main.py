import pygame
from clock import MickeyClock

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Mickey Mouse Clock")
    
    clock_timer = pygame.time.Clock()
    mickey_clock = MickeyClock(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        
        
        mickey_clock.draw()

        pygame.display.flip()
        clock_timer.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

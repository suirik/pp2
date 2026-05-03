"""
main.py – Entry point for TSIS 3 Racer.

Run:
    python main.py

Flow:
    Username  →  Main Menu  →  [Play / Leaderboard / Settings / Quit]
                    ↓ Play
                 RacerGame
                    ↓ game over
                 GameOverScreen  →  Retry (back to Play) | Main Menu
"""

import pygame
import sys

from persistence import (
    load_settings, save_settings,
    add_leaderboard_entry,
)
from ui import (
    UsernameScreen,
    MainMenuScreen,
    SettingsScreen,
    GameOverScreen,
    LeaderboardScreen,
)
from racer import RacerGame, SCREEN_W, SCREEN_H


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Racer – TSIS 3")

    # ── Load persistent data ──────────────────────────────────────────────────
    settings = load_settings()

    # ── Ask for username once per session ────────────────────────────────────
    username = UsernameScreen(screen).run()

    # ── Main application loop ─────────────────────────────────────────────────
    while True:
        action = MainMenuScreen(screen).run()

        if action == MainMenuScreen.QUIT:
            break

        elif action == MainMenuScreen.LEADERBOARD:
            LeaderboardScreen(screen).run()

        elif action == MainMenuScreen.SETTINGS:
            SettingsScreen(screen, settings).run()
            # settings dict was mutated in-place and already saved by SettingsScreen

        elif action == MainMenuScreen.PLAY:
            # Inner play loop: supports Retry without going back to main menu
            play_again = True
            while play_again:
                # Start one game session
                game             = RacerGame(screen, settings, username)
                score, distance, coins = game.run()

                # Save to leaderboard
                add_leaderboard_entry(username, score, distance, coins)

                # Game Over screen
                result = GameOverScreen(screen).run(score, distance, coins, username)
                if result == GameOverScreen.RETRY:
                    play_again = True        # loop back and play again
                else:
                    play_again = False       # return to main menu

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
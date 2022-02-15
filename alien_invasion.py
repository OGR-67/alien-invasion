import sys
import pygame


from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game ressources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()

        # Create an instance to store game statistics and create scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()
        self._create_stars()

        # Make the "Play" button.
        self.play_button = Button(self, "Play")

        # Sounds.
        self.main_theme = pygame.mixer.Sound("sounds/Space Heroes.ogg")
        self.main_theme.set_volume(0.5)
        self.main_theme.play(9999)
        self.sound_explosion = pygame.mixer.Sound("sounds/explosion.wav")
        self.sound_explosion.set_volume(0.3)
        self.sound_laser = pygame.mixer.Sound("sounds/laser7.mp3")
        self.sound_laser.set_volume(0.8)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self.clock.tick(60)
            self._update_screen()

    def _check_events(self):
        """Respond to keypress and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.record_high_score()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def record_high_score(self):
        with open("high_score.txt", 'w') as file_objet:
            file_objet.write(str(self.stats.high_score))

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset game settings.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_images()

            self.reset_level()

            # Hide mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        # Ship Controls.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        # Ship fire.
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            self.sound_laser.play()

        # Game controls.
        elif event.key == pygame.K_q:
            self.record_high_score()
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        # Ship Controls.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
            then update position of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen.
        self._check_alien_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        self.sound_explosion.play()
        if self.stats.ships_left > 0:
            # Decrement ships left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.reset_level()

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.stats.game_over = True

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullets and alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            self.sound_explosion.play()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet and speed up next
            # wave.
            self.reset_level()
            self.settings.increase_speed()

            # increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def reset_level(self):
        self.ship.center_ship()
        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()

    def _create_fleet(self):
        """Create a fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_alien_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _create_stars(self):
        for time in range(self.settings.star_number):
            star = Star(self)
            self.stars.add(star)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()

        # Draw Play button if game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        if self.stats.game_over:
            self.screen.blit(self.sb.game_over_image, self.sb.game_over_rect)

        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()

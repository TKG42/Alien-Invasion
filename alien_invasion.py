# Plan projects before writing code. Write one before each project. 
# Alien Invasion project chapters 12 - 14

# NOTE: Create and use a Git repository (+ pushing online) during code refactoring.

import sys
from time import sleep

import pygame
import random
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from powerup import PowerUp

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        # 3 lines below produce full screen mode. TESTED - DO NOT USE. Only as reference. Not compatible with G9
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get.rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # 3 Lines below for windowed mode. Comment out to switch to fullscreen.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics, and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button
        self.normal_button = Button(self, "Normal", (0, 255, 0), 0)
        self.hard_button = Button(self, "Hard", (255, 255, 0), 60)
        self.nightmare_button = Button(self, "Nightmare", (255, 0, 0), 120)

        # NOTE: For more sound files, use a dictionary. Example below
        # self.sounds = {"laser: pygame.mixer.Sound('sounds/LaserGun.wav)"}
        # self.sounds["laser"].play()
        pygame.mixer.init()
        self.ship_laser_sound = pygame.mixer.Sound('sounds/LaserGun.wav')
        self.level_success_sound = pygame.mixer.Sound('sounds/success.wav')
        self.player_hit_sound = pygame.mixer.Sound('sounds/player_hit.wav')
        self.game_over_sound = pygame.mixer.Sound('sounds/game_over.wav')
        self.powerup_bullet_sound = pygame.mixer.Sound('sounds/blaster.wav')
        self.powerup_sound = pygame.mixer.Sound('sounds/powerup.wav')

        # Initialize powerups group
        self.powerups = pygame.sprite.Group() 

        # Initialize power up states and timers
        self.powerup_active = False
        self.powerup_start_time = 0
        self.powerup_duration = 5000 # duration in milliseconds
        self.powerup_counter = 0
        self.powerup_spawned_this_level = False

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_powerups()
                self._update_powerup_timer()
                
            self._update_screen() 
    
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:                                                            
                    with open('files/high_score.txt', 'w') as file_object:
                        # print(f"Writing high score: {self.stats.high_score}")   # NOTE: debug print
                        file_object.write(str(self.stats.high_score))
                except Exception as e:
                    print(f"Error writing high score: {e}")                     # NOTE: catch and print errors, debugging
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _start_game(self):
        """Handles start game state."""
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.normal_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        nightmare_button_clicked = self.nightmare_button.rect.collidepoint(mouse_pos)
        p_pressed = pygame.key.get_pressed() 
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self._start_game()
        elif hard_button_clicked and not self.stats.game_active:
            self.settings.initialize_hard_dynamic_settings()
            self._start_game()
        elif nightmare_button_clicked and not self.stats.game_active:
            self.settings.initialize_nightmare_dynamic_settings()
            self._start_game()
        elif p_pressed[pygame.K_p] and not self.stats.game_active: 
            self._start_game()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)    
            
    def _check_keydown_events(self, event):
        """Responds to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            try:                                                            
                with open('files/high_score.txt', 'w') as file_object:
                    # print(f"Writing high score: {self.stats.high_score}")   # NOTE: debug print
                    file_object.write(str(self.stats.high_score))
            except Exception as e:
                    print(f"Error writing high score: {e}")   
            sys.exit()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Responds to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            powerup_active = self.check_if_powerup_active() 
            new_bullet = Bullet(self, powerup_active)
            self.bullets.add(new_bullet)

            # play ship laser shot sound or powerup sound
            if self.powerup_active:
                self.powerup_bullet_sound.play()
            else:
                self.ship_laser_sound.play()

    def check_if_powerup_active(self) :
        """Check if the powerup is active."""
        return self.powerup_active # This could be a boolean attribute you toggle.

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
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True) 
        # Change self.bullets boolean pair to False for super bullets that rip through everything

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.powerup_counter += len(aliens)
            if self.powerup_counter >= random.randint(3, 15):
                self.powerup_counter = 0
                self._create_powerup()

        if not self.aliens:
            self._start_new_level()
    
    def _create_powerup(self):
        """Create a power-up and add it to the power-ups group."""
        if not self.powerups and not self.powerup_spawned_this_level: # Make sure only one powerup is present
            powerup = PowerUp(self)
            powerup.rect.x = random.randint(0, self.settings.screen_width - powerup.rect.width)
            powerup.rect.y = self.ship.rect.y - powerup.rect.height + 50 # Align with the ships y position. 
            self.powerups.add(powerup)
            self.powerup_spawned_this_level = True

    def _update_powerups(self):
        """Update the position of power-ups and get rid of old power-ups."""
        for powerup in self.powerups.copy():        
            if pygame.sprite.spritecollideany(self.ship, self.powerups):
                self.powerup_sound.play()
                self._powerup_collected()
                self.powerups.remove(powerup)
                # Brief pause
                sleep(0.5)

    def _powerup_collected(self):
        """Handle powerup collection."""
        self.powerup_start_time = pygame.time.get_ticks()
        self.powerup_active = True
        # TODO: start a timer for the power-up duration

    def _update_powerup_timer(self):
        """Update the power up state based on the timer."""
        if self.powerup_active and pygame.time.get_ticks() - self.powerup_start_time > self.powerup_duration:
            self._end_powerup()

    def _end_powerup(self):
        """Revert changes made by the power up"""
        self.powerup_active = False

    def _start_new_level(self):
        """starts new level if there are no more aliens"""
        # Destroy existing bullets and create new fleet.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level.
        self.stats.level += 1
        self.sb.prep_level()

        # Reset powerup flag
        self.powerup_spawned_this_level = False

        # Play sound to indicate new level starting
        self.level_success_sound.play()

    def _update_aliens(self):
        """Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Play ship hit sound
            self.player_hit_sound.play()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship. 
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            # Play game over sound
            self.game_over_sound.play()

            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of row of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
            
    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
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

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop. 
        # The fill() method always takes one argument: a color.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw power up
        self.powerups.draw(self.screen)

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.normal_button.draw_button()
            self.hard_button.draw_button()
            self.nightmare_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()



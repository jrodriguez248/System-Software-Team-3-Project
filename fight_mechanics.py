import pygame
import random
from classes.stats import player_stats, enemy_stats

# Constants
FONT_SIZE_HEALTH = 12
FONT_SIZE_CHARS = 36

'''
Section of code determines outcome of actions during a fight event
'''
# Determines damage output of sword based on hunger and tool level
def fighting_action():
    tool_sword = player_stats.tool_sword
    player_hunger = player_stats.player_hunger

    if tool_sword == 1:
        flat_damage = random.randint(5, 10)
    elif tool_sword == 2:
        flat_damage = random.randint(10, 15)
    else:
        flat_damage = random.randint(20, 30)

    if player_hunger >= 75:
        efficacy = 1.0
    elif player_hunger >= 50:
        efficacy = 0.75
    elif player_hunger >= 25:
        efficacy = 0.50
    else:
        efficacy = 0.25

    attack_damage_result = flat_damage * efficacy

    return round(attack_damage_result)
#Determines damage dealt to player by enemy after a fight action event was initated
def enemy_attack():
    enemy_damage = random.randint(1, 3)
    return enemy_damage
#Determines if players flee attempt in fight is successful
def runaway_calc():
    runaway_chance = random.randint(1, 25)
    if player_stats.player_hunger >= runaway_chance:
        return True
    else:
        return False

'''
Section of code initializes and sets up fight event when triggered by chance in the world_map file
'''
def fight_encounter():
    # Pygame setup
    pygame.display.set_caption("Enemy Encounter")
    screen = pygame.display.set_mode((500, 500))

    # Pygame font setup
    font_health = pygame.font.Font(None, FONT_SIZE_HEALTH)
    font_chars = pygame.font.Font(None, FONT_SIZE_CHARS)

    # Text surfaces
    player_text = font_chars.render("P", True, (0, 0, 0))
    enemy_text = font_chars.render("E", True, (0, 0, 0))
    fight_button_text = font_chars.render("FIGHT", True, (0, 0, 0))
    run_button_text = font_chars.render("RUN", True, (0, 0, 0))

    # Health and hunger bars
    player_health_bar = font_health.render(f"Health: {player_stats.player_health}", True, (255, 0, 0))
    enemy_health_bar = font_health.render(f"Health: {enemy_stats.enemy_health}", True, (255, 0, 0))
    player_hunger_bar = font_health.render(f"Hunger: {player_stats.player_hunger}", True, (255, 0, 0))

    # Calculate text sizes
    player_text_size = player_text.get_size()
    enemy_text_size = enemy_text.get_size()

    # Calculate health and hunger bar positions
    player_health_bar_pos = (50 - player_health_bar.get_width() / 2, 50 + player_text_size[1])
    enemy_health_bar_pos = (350 - enemy_health_bar.get_width() / 2, 50 + enemy_text_size[1])
    player_hunger_bar_pos = (
    50 - player_hunger_bar.get_width() / 2, player_health_bar_pos[1] + player_health_bar.get_height() + 5)

    # Button locations
    button_width = FONT_SIZE_CHARS * 4  # Adjust button width as needed
    button_height = FONT_SIZE_CHARS + 10  # Adjust button height as needed
    fight_button_location = ((250 - button_width) / 2, 400)
    run_button_location = ((250 - button_width) / 2 + 250, 400)

    # Main loop
    running_fight = True
    while running_fight:
        screen.fill((255, 255, 255))

        # Draw player and enemy text
        screen.blit(player_text, (50, 50))
        screen.blit(enemy_text, (350, 50))

        # Draw health and hunger bars
        screen.blit(player_health_bar, player_health_bar_pos)
        screen.blit(enemy_health_bar, enemy_health_bar_pos)
        screen.blit(player_hunger_bar, player_hunger_bar_pos)

        # Draw buttons
        pygame.draw.rect(screen, (200, 200, 200), (fight_button_location, (button_width, button_height)))
        pygame.draw.rect(screen, (200, 200, 200), (run_button_location, (button_width, button_height)))
        screen.blit(fight_button_text, (fight_button_location[0] + (button_width - fight_button_text.get_width()) / 2,
                                        fight_button_location[1] + (button_height - FONT_SIZE_CHARS) / 2))
        screen.blit(run_button_text, (run_button_location[0] + (button_width - run_button_text.get_width()) / 2,
                                      run_button_location[1] + (button_height - FONT_SIZE_CHARS) / 2))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                '''
                Sub-section of code that calls for damage/hunger outcome when fight button event is clicked
                '''
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if fight_button_location[0] < mouse_pos[0] < fight_button_location[0] + button_width and \
                        fight_button_location[1] < mouse_pos[1] < fight_button_location[1] + button_height:
                    # Handles health/hunger tracking and damage exchange on fight button event click
                    damage_dealt = fighting_action()
                    enemy_stats.enemy_health -= damage_dealt
                    damage_recieved = enemy_attack()
                    player_stats.player_health -= damage_recieved
                    if player_stats.player_hunger > 0:
                        player_stats.player_hunger -= 3
                        if player_stats.player_hunger < 0:
                            player_stats.player_hunger = 0
                    #Ends fight event if player health or enemy health is fully depleted
                    if enemy_stats.enemy_health <= 0:
                        running_fight = False
                        enemy_stats.enemy_health = 100
                    elif player_stats.player_health <= 0:
                        running_fight = False
                        player_stats.player_health = 100
                        enemy_stats.enemy_health = 100

                    # Update player and enemy health display
                    player_health_bar = font_health.render(f"Health: {player_stats.player_health}", True, (255, 0, 0))
                    enemy_health_bar = font_health.render(f"Health: {enemy_stats.enemy_health}", True, (255, 0, 0))
                    player_hunger_bar = font_health.render(f"Hunger: {player_stats.player_hunger}", True, (255, 0, 0))



                    '''
                    Sub-section of code that calls for damage and chance outcome if RUN button is clicked
                    '''
                elif run_button_location[0] < mouse_pos[0] < run_button_location[0] + button_width and \
                        run_button_location[1] < mouse_pos[1] < run_button_location[1] + button_height:
                    # Handle run button click
                    flee_attempt = runaway_calc()
                    if flee_attempt == True:
                        running_fight = False
                        enemy_stats.enemy_health = 100
                    else:
                        damage_recieved = enemy_attack()
                        player_stats.player_health -= damage_recieved
                        if player_stats.player_health <= 0:
                            running_fight = False
                            player_stats.player_health = 100
                            enemy_stats.enemy_health = 100

                    # Update player and enemy health display
                    player_health_bar = font_health.render(f"Health: {player_stats.player_health}", True, (255, 0, 0))
                    enemy_health_bar = font_health.render(f"Health: {enemy_stats.enemy_health}", True, (255, 0, 0))


        pygame.display.flip()

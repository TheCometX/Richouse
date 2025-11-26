from functions import System, Preference, textbox_handling
import json
import pygame 
import sys



# Main module excuted when game starts
def main() -> None:
    # Initialization of pygame and its features
    pygame.init()
    pygame.mixer.init()

    clock = pygame.time.Clock()

    # Create the title
    pygame.display.set_caption("Richouse")

    # Start the music
    pygame.mixer.music.load("/Users/viniciusferrari/Documents/Richouse/Media/stealth-battle.mp3")
    pygame.mixer.music.play(loops=-1)

    #Set the mouse coursor invisible in screen
    pygame.mouse.set_visible(False)

    # Get the user data from local flatfile database, JSON type
    with open("/Users/viniciusferrari/Documents/Richouse/Distribution-code/LocalUserInfo.json", "r") as f:
        userData = json.load(f)

    # Check for registered username
    username = userData[0]["username"]
    if username == "":
        preferences = Preference() # Give default preferences
        system = System(preferences=preferences) # Create the system object, it will be resposible for screens
        system.render_screen(nextScreen="username") # Render the screen to register an username
    else:
        controls = userData[0]["controls"]
        preferences = Preference(username=username, up=controls["up"], down=controls["down"],
                                 left=controls["left"], right=controls["right"], interact=controls["interact"], 
                                 use=controls["use"], volume=userData[0]["volume"]) # Uses the preferences 
                                                                                                               # from database
        system = System(preferences=preferences) # Create the system object, it will be resposible for screens
        system.render_screen(nextScreen="menu") # Render the menu screen
    pygame.mixer.music.set_volume(preferences.volume)
    game_loop(system=system, clock=clock) # Redirect to the function with the game loop

def game_loop(system: System, clock: pygame.time.Clock) -> None:
    while True:
        # Update screen elements, i.e. background, buttons and textbox.
        system.update_screen() 
        if system.screenName in ["baker", "usbourne", "hacking", "lockpick", "fingerprint", "pause"]: # Only happen in gameplay screens
            system.gameplay.update_status() # Update and print the time and lives
            system.gameplay.player.display_inventory() # Display the inventory
            system.gameplay.guard.move() # Update guard postion
            system.gameplay.player.check_collision() # Check any collisions with the player
            if system.gameplay.player.lives == 0: # Finish the mission if player lose all lives
                system.render_screen(nextScreen="game-over") # Fail screen
        input(system=system) # Where the input will be handled
        pygame.display.flip() # Change the frame
        clock.tick(60) # Limit the fps to 60

def input(system: System) -> None:
    # Get the events to be handled
    for event in pygame.event.get():
        # Essential to maintain pygame working
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Handle any key pressed, no matters if key still pressed, it will hanlde once per press
        elif event.type == pygame.KEYDOWN:
            # Different handling accorgin to the screen
            match system.screenName:
                case "menu":
                    system.button.selection_menu(key=event.key) # Uses a method to handle the buttons
                case "username":
                    textbox_handling(system=system, key=event.key) # Uses a function to handle the texbox
                # Just to enable me to return to menu screen at this stage
                case "start":
                    system.button.selection_start(key=event.key) # Use a method to handle the buttons
                case "rank":
                    # Return to menu in case of ESC be pressed
                    if event.key == pygame.K_ESCAPE:
                        system.render_screen(nextScreen="menu")
                case "options":
                    system.button.selection_options(event=event) # Uses Button method to do the selection
                case "baker" | "usbourne":
                    match event.key:
                        case system.preferences.buttonInteract: # Button used to search
                            system.gameplay.player.interact() # Player method
                        case system.preferences.buttonUse: # Button used to start the minigames 
                            system.gameplay.player.use() # Player method
                        case pygame.K_ESCAPE: # Button to open the pause screen
                            system.render_screen(nextScreen="pause") # System method
                case "pause":
                    system.button.selection_pause(key=event.key) # Button method
                case "mission-completed":
                    if event.key == pygame.K_RETURN: # Button used to continue to menu
                        system.render_screen(nextScreen="menu") # System method 
                case "lockpick":
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] and len(system.minigame.userSequence) < 4:
                        system.minigame.userSequence.append(event.key)
                    if len(system.minigame.userSequence) == 4:
                        system.minigame.check()
                    if event.key == pygame.K_ESCAPE:
                        system.render_screen(nextScreen=system.gameplay.map)
                case "fingerprint":
                    if pygame.key.name(event.key).isnumeric() and len(system.minigame.userSequence) < 3:
                        system.minigame.userSequence.append(int(pygame.key.name(event.key)))
                    if len(system.minigame.userSequence) == 3:
                        system.minigame.check()
                    if event.key == pygame.K_ESCAPE:
                        system.render_screen(nextScreen=system.gameplay.map)
                case "game-over":
                    if event.key == pygame.K_RETURN:
                        system.render_screen(nextScreen="menu")
                case "hacking":
                    if pygame.key.name(event.key).isalpha() and len(system.minigame.userSequence) < 3:
                        system.minigame.userSequence.append(pygame.key.name(event.key))
                    if len(system.minigame.userSequence) == 3:
                        system.minigame.check()
                    if event.key == pygame.K_ESCAPE:
                        system.render_screen(nextScreen=system.gameplay.map)
    if system.screenName in ["baker", "usbourne"]: # Limit the action to gameplay screens
        system.gameplay.player.movement() # Player Method

if __name__ == '__main__':
    main()
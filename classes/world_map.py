'''

Approach:
    Create map class
    Handles movement
    Has functions to check if you are near an ore, tree, building, or boat
    Has render function (takes screen as input)
    Handles resource mining:
        At initialization, all mining sites are assigned a resource object
        When a resource is mined, it will use the object corresponding to that deposit
        If the resource is successfully mined, the resource spot will be removed
    Camera panning
    Map is a 2D array of strings, where characters can stack (which allows things like grass under the player, or grass under an ore)

Map Key:
    P - Player
    w - Water
    | - Wall
    . - Ground (safe)
    * - Tall Grass (hostile)
    B - Blacksmith
    S - Shop
    H - Inn
    U - Boat
    O - Ore Deposit
    T - Tree

'''

import pygame
from classes.resource import resource
from random import randint

class world_map:
    def __init__(self) -> None:
        # Initialize variables
        self.data: list[list[str]] = None # Stores the map data in a 2D array of strings
        self.map_size: tuple[int, int] = None # Width and height of map
        self.player_position: tuple[int, int] = (33, 15) # Location of player
        self.resources: list[resource] = [] # Properties for all resources that have been spawned

        self.initialize()


    def initialize(self):
        '''
        Loads map from map_data.txt and generates (or regernates) resources.

        Can be used to create map at the beginning of the game, or reset the map
        to reaload the resources.
        '''

        # Reset variables
        if self.data != None:
            self.data.clear()
        if self.resources != None:
            self.resources.clear()

        # Load map data
        self.load_map_from_file()

        # Add player to map
        self.add_char_to_tile('P', self.player_position)

        # Generate trees
        NUM_TREES = 10
        for i in range(NUM_TREES):
            # Find a valid tile to insert the tree
            valid_tile = False
            while not valid_tile:
                location = (randint(0, self.map_size[0]-1), randint(0, self.map_size[1]-1))
                if not self.is_obstacle(location):
                    valid_tile = True

            # Insert tree at valid location
            self.add_char_to_tile('T', location)

            # Add tree to list of resources
            self.resources.append(resource('wood', location))

        # Generate ore (same as generating trees)
        NUM_ORE_DEPOSITS = 10
        for i in range(NUM_ORE_DEPOSITS):
            # Find a valid tile to insert the ore deposit
            valid_tile = False
            while not valid_tile:
                location = (randint(0, self.map_size[0]-1), randint(0, self.map_size[1]-1))
                if not self.is_obstacle(location):
                    valid_tile = True

            # Insert ore deposit at valid location
            self.add_char_to_tile('O', location)

            # Add ore deposit to list of resources
            ore_type = 'iron' if randint(0, 1) == 0 else 'copper'
            self.resources.append(resource(ore_type, location))


    def load_map_from_file(self):
        '''
        Loads text-based map from map_data.txt into self.data as a 2D array of strings

        Note: Make sure the input map has no player (P) or resources such as ore (O) or trees (T), because
        we need to know what kind of terrain is underneath them.
        '''


        # Load map form file
        with open('./content/map_data.txt') as f:
            lines = f.readlines()

            self.map_size = (len(lines[0]), len(lines))

            # Initialize 2D data array
            self.data = [['' for x in range(self.map_size[0])] for y in range(self.map_size[1])]

            y = 0
            for line in lines:
                x = 0
                for value in line:
                    self.data[y][x] = value
                    x += 1
                y += 1


    def get_tile(self, location: tuple[int, int]) -> str:
        '''
        Returns the top character at a certain map position.
        
        (returns top character because each tile may have multiple characters stacked on top of each other)
        '''

        tile_string = self.data[location[1]][location[0]]
        return tile_string[len(tile_string)-1] # Return character at the end of the tile string (tile string may look like this '*P' where the player is on top of tall grass)
    

    def is_obstacle(self, location: tuple[int, int]):
        '''
        Returns true if the character at the provided location blocks character movement.
        '''

        tile = self.get_tile(location)
        return tile == 'P' or tile == 'w' or tile == '|' or tile == 'B' or tile == 'S' or tile == 'H' or tile == 'U' or tile == 'O' or tile == 'T'


    def is_resource(self, location: tuple[int, int]):
        '''
        Returns true if tile is either 'O' or 'T'.
        '''

        tile = self.get_tile(location)
        return tile == 'O' or tile == 'T'


    def get_resource(self, location: tuple[int, int]):
        '''
        Returns the resource object for the resource at the given location (or none if location
        does not have a resource associated with it).
        '''
        
        for resource in self.resources:
            if resource.location == location:
                return resource
            
        return None


    def add_char_to_tile(self, value: str, location: tuple[int, int]):
        '''
        Adds the value (should be a single character) to the end of the data string at the provided location
        '''

        self.data[location[1]][location[0]] = self.data[location[1]][location[0]] + value


    def remove_top_char_from_tile(self, location: tuple[int, int]):
        '''
        Removes the top character from the data string at the provided location.

        Example:
        ```
        # before: data[2][4] = '.P'
        remove_top_char_from_tile((2, 4))
        # after: data[2][4] = '.'
        ```
        '''

        self.data[location[1]][location[0]] = self.data[location[1]][location[0]][:-1]


    def render(self, screen: pygame.Surface, font: pygame.font.Font, render_regeion: tuple[int, int] = (21, 11), line_spacing: int = 26):
        # Create string that contains entire screen
        for y in range(render_regeion[1]):
            line = ''
            world_y = y - render_regeion[1]//2 + self.player_position[1]
            for x in range(render_regeion[0]):
                world_x = x - render_regeion[0]//2 + self.player_position[0]
                
                location = (world_x, world_y)

                # Render empty space in locations that are outside of the map
                if location[0] < 0 or location[0] >= self.map_size[0] or location[1] < 0 or location[1] >= self.map_size[1]:
                    line += ' '
                else:
                    line += self.get_tile(location)

            img = font.render(line, True, (255, 255, 255))
            screen.blit(img, (0, y * line_spacing))


    def move_player(self, direction: str):
        '''
        Moves the player in a specified direction.

        Accepted directions: 'n', 's', 'e', 'w'
        '''

        # Get move-to location
        if direction == 'n':
            move_to = (self.player_position[0], self.player_position[1]-1)
        elif direction == 's':
            move_to = (self.player_position[0], self.player_position[1]+1)
        elif direction == 'e':
            move_to = (self.player_position[0]+1, self.player_position[1])
        elif direction == 'w':
            move_to = (self.player_position[0]-1, self.player_position[1])
        else:
            print('world_map -> move_player: Error: invalid direction')

        # Validate location
        if self.is_obstacle(move_to):
            return

        # Move player to new location
        self.remove_top_char_from_tile(self.player_position)
        self.player_position = move_to
        self.add_char_to_tile('P', self.player_position)

import pygame
from classes.resource import Resource
from random import randint

class world_map:
    '''
    The `world_map` class handles loading, storing, rendering, and updating
    the world map. It also handles resource generation and player movement.

    Map Key:
        P: Player
        w: Water
        |: Wall
        .: Ground (safe)
        *: Tall Grass (hostile)
        B: Blacksmith
        S: Shop
        H: Inn
        U: Boat
        O: Ore Deposit
        T: Tree
    '''

    # Initialization
    def __init__(self) -> None:
        # Initialize variables
        self.__data: list[list[str]] = None # Stores the map data in a 2D array of strings
        self.__map_size: tuple[int, int] = None # Width and height of map
        self.__player_position: tuple[int, int] = (33, 15) # Location of player
        self.__resources: list[Resource] = [] # Properties for all resources that have been spawned

        self.initialize()

    def initialize(self):
        '''
        Loads map from map_data.txt and generates (or regernates) resources.

        Can be used to create map at the beginning of the game, or reset the map
        to reaload the resources.
        '''

        # Reset variables
        if self.__data != None:
            self.__data.clear()
        if self.__resources != None:
            self.__resources.clear()

        # Load map data
        self.load_map_from_file()

        # Add player to map
        self.add_char_to_tile('P', self.__player_position)

        # Generate trees
        NUM_TREES = 10
        for i in range(NUM_TREES):
            # Find a valid tile to insert the tree
            valid_tile = False
            while not valid_tile:
                location = (randint(0, self.__map_size[0]-1), randint(0, self.__map_size[1]-1))
                tile = self.get_tile(location)
                if not self.is_obstacle(tile):
                    valid_tile = True

            # Insert tree at valid location
            self.add_char_to_tile('T', location)

            # Add tree to list of resources
            self.__resources.append(Resource('wood', location))

        # Generate ore (same as generating trees)
        NUM_ORE_DEPOSITS = 10
        for i in range(NUM_ORE_DEPOSITS):
            # Find a valid tile to insert the ore deposit
            valid_tile = False
            while not valid_tile:
                location = (randint(0, self.__map_size[0]-1), randint(0, self.__map_size[1]-1))
                tile = self.get_tile(location)
                if not self.is_obstacle(tile):
                    valid_tile = True

            # Insert ore deposit at valid location
            self.add_char_to_tile('O', location)

            # Add ore deposit to list of resources
            ore_type = 'iron' if randint(0, 1) == 0 else 'copper'
            self.__resources.append(Resource(ore_type, location))

    def load_map_from_file(self):
        '''
        Loads text-based map from map_data.txt into self.__data as a 2D array of strings

        Note: Make sure the input map has no player (P) or resources such as ore (O) or trees (T), because
        we need to know what kind of terrain is underneath them.
        '''


        # Load map form file
        with open('./content/map_data.txt') as f:
            lines = f.readlines()

            self.__map_size = (len(lines[0]), len(lines))

            # Initialize 2D data array
            self.__data = [['' for x in range(self.__map_size[0])] for y in range(self.__map_size[1])]

            y = 0
            for line in lines:
                x = 0
                for value in line:
                    self.__data[y][x] = value
                    x += 1
                y += 1


    # Map editing
    def add_char_to_tile(self, value: str, location: tuple[int, int]):
        '''
        Adds the value (should be a single character) to the end of the data string at the provided location
        '''

        self.__data[location[1]][location[0]] = self.__data[location[1]][location[0]] + value

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

        self.__data[location[1]][location[0]] = self.__data[location[1]][location[0]][:-1]

    def remove_resource(self, location: tuple[int, int]):
        '''
        Removes resource from specified location, including the map letter, and the resoruce data
        '''

        for i in range(len(self.__resources)):
            if self.__resources[i].location == location:
                self.remove_top_char_from_tile(self.__resources[i].location)
                self.__resources.pop(i)
                return
            
        print('world_map.py -> remove_resource: Warning: No resource was removed at the specified location')


    # Rendering
    def render(self, screen: pygame.Surface, font: pygame.font.Font, render_regeion: tuple[int, int] = (21, 11), line_spacing: int = 26):
        # Create string that contains entire screen
        for y in range(render_regeion[1]):
            line = ''
            world_y = y - render_regeion[1]//2 + self.__player_position[1]
            for x in range(render_regeion[0]):
                world_x = x - render_regeion[0]//2 + self.__player_position[0]
                
                location = (world_x, world_y)

                # Render empty space in locations that are outside of the map
                if location[0] < 0 or location[0] >= self.__map_size[0] or location[1] < 0 or location[1] >= self.__map_size[1]:
                    line += ' '
                else:
                    line += self.get_tile(location)

            img = font.render(line, True, (255, 255, 255))
            screen.blit(img, (0, y * line_spacing))


    # Movement
    def move_player(self, direction: str):
        '''
        Moves the player in a specified direction.

        Accepted directions: 'n', 's', 'e', 'w'
        '''

        # Get move-to location
        if direction == 'n':
            move_to = (self.__player_position[0], self.__player_position[1]-1)
        elif direction == 's':
            move_to = (self.__player_position[0], self.__player_position[1]+1)
        elif direction == 'e':
            move_to = (self.__player_position[0]+1, self.__player_position[1])
        elif direction == 'w':
            move_to = (self.__player_position[0]-1, self.__player_position[1])
        else:
            print('world_map -> move_player: Error: invalid direction')
            return

        # Validate location
        potential_tile = self.get_tile(move_to)
        if self.is_obstacle(potential_tile):
            return

        # Move player to new location
        self.remove_top_char_from_tile(self.__player_position)
        self.__player_position = move_to
        self.add_char_to_tile('P', self.__player_position)


    # Querying
    def get_tile(self, location: tuple[int, int]) -> str:
        '''
        Returns the top character at a certain map position.
        
        (returns top character because each tile may have multiple characters stacked on top of each other)
        '''

        tile_string = self.__data[location[1]][location[0]]
        return tile_string[len(tile_string)-1] # Return character at the end of the tile string (tile string may look like this '*P' where the player is on top of tall grass)
    
    def is_resource(self, char: str):
        '''
        Returns true if provided string is either 'O' or 'T'.
        '''

        return char == 'O' or char == 'T'

    def is_building(self, char: str):
        '''
        Returns true if provided string is either 'B', 'S', or 'H'
        '''

        return char == 'B' or char == 'S' or char == 'H'

    def is_interactable(self, char: str):
        '''
        Returns true if the provided letter is something the player can interact with.
        '''

        return self.is_building(char) or self.is_resource(char) or char == 'U'

    def is_obstacle(self, char: str):
        '''
        Returns true if the provided character would block character movement.
        '''

        return self.is_building(char) or self.is_resource(char) or char == 'P' or char == 'w' or char == '|' or char == 'U'

    def get_nearby_resource(self):
        '''
        Returns resource object of a nearby resource (returns None if there are no nearby resources)
        '''

        for resource in self.__resources:
            if location_nearby(resource.location, self.__player_position):
                return resource

        return None

    def get_nearby_interactable(self):
        '''
        Returns any nearby interactable letter. Returns empty string ('') if there is nothing interactable nearby.
        '''
        
        for x in range(-1, 2):
            for y in range(-1, 2):
                # Ignore tile directly on top of player
                if x == 0 and y == 0:
                    continue

                location = (self.__player_position[0]+x, self.__player_position[1]+y)
                tile = self.get_tile(location)
                if self.is_interactable(tile):
                    return tile
                
        return ''


def location_nearby(location_1: tuple[int, int], location_2: tuple[int, int]):
    '''
    Returns true if the two locations are directly next to each other virtically, horizontally, or diaginally. 
    '''
    
    x_offset = location_1[0] - location_2[0]
    y_offset = location_1[1] - location_2[1]

    return x_offset >= -1 and x_offset <= 1 and y_offset >= -1 and y_offset <= 1

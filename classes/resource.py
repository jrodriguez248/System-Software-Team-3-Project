'''
Resource classes for ores and trees.
'''

class Resource:
    def __init__(self, type: str, location: tuple[int, int]) -> None:
        '''
        Available types: 'iron', 'copper', 'wood'
        '''

        # Ensure the resource type is valid
        if not (type == 'iron' or type == 'copper' or type == 'wood'):
            print('resources.py: Error: resource type is invalid')

        self.health: float = 1.0 # Gets destroyed when health reaches zero
        self.type: str = type
        self.location = location

    def mine(self, amount: float):
        self.health = max(self.health - amount, 0.0)

    def is_mined(self) -> bool:
        return self.health == 0.0

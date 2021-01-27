"""
CSSE1001 Assignment 2
Semester 2, 2020
"""
from utils import *

# Fill these in with your details
__author__ = "{{user.name}} ({{user.id}})"
__email__ = ""
__date__ = ""


# Write your code here
class Player:
	def __init__(self, count:int):
		self.move_count = count
		self.collidable = True
		self._position = None
		self._inventory = []

	def get_id(self):
		return "O"

	def set_collide(self, collidable:bool):
		 self.collidable = collidable

	def can_collide(self):
		return self.collidable

	def set_position(self, position):
		self._position = position

	def get_position(self):
		return self._position

	def change_move_count(self, number):
		self.move_count += number

	def moves_remaining(self):
		return self.move_count

	def decrease_move(self):
		self.move_count -= 1


	def add_item(self, item): #item: Entity
		self._inventory.append(item)

	def get_inventory (self):
		return self._inventory

	def __str__(self) :
		return "Player('O')"

	def  __repr__(self):
		return "Player('O')"


class Key:
	def __init__(self):
		self.collidable = True

	def get_id(self):
		return "K"

	def set_collide(self, collidable: bool):
		 self.collidable = collidable

	def can_collide(self):
		return self.collidable

	def on_hit(self, game):
		player_entity = game.get_player()
		player_position  =  player_entity.get_position()
		key_entity_position  = game.get_positions(KEY)[0]

		if key_entity_position is not None:
			if player_position == key_entity_position:
				player_entity.add_item(game.get_game_information()[key_entity_position])
				del game.get_game_information()[key_entity_position]

	def __str__(self) :
		return "Key('K')"

	def  __repr__(self):
		return "Key('K')"


class MoveIncrease:

	def __init__(self):
		self.moves = 5
		self.collidable = True

	def get_id(self):
		return "M"

	def set_collide(self, collidable: bool):
		 self.collidable = collidable

	def can_collide(self):
		return self.collidable

	def on_hit(self, game):
		player_entity = game.get_player()
		player_position  =  player_entity.get_position()
		move_increase_entity_position  = game.get_positions(MOVE_INCREASE)[0]
		if move_increase_entity_position is not None:
			if player_position == move_increase_entity_position:
				player_entity.change_move_count(self.moves)
				del game.get_game_information()[move_increase_entity_position]
				#{ k:v for k, v in game.get_game_information() if str(v) == "MoveIncrease('M')" }

	def __str__(self) :
		return "MoveIncrease('M')"

	def  __repr__(self):
		return "MoveIncrease('M')"


class Wall:
	def __init__(self):
		self.collidable = False

	def get_id(self):
		return "#"

	def set_collide(self, collidable: bool):
		 self.collidable = collidable

	def can_collide(self):
		return self.collidable

	def __str__(self) :
		return "Wall('#')"

	def  __repr__(self):
		return "Wall('#')"


class Item(MoveIncrease, Key):
	def get_id(self):
		pass

	def set_collide(self, collidable:bool):
		 self.collidable = collidable

	def can_collide(self):
		return self.collidable

	def on_hit(self, game):
		pass


class Door:

	def __init__(self):
		self.collidable = True

	def get_id(self):
		return "D"

	def set_collide(self, collidable:bool):
		 self.collidable = collidable

	def can_collide(self):
		return self.collidable

	def on_hit(self, game):
		door_position = game.get_positions(DOOR)[0]
		my_position = game.get_player().get_position()

		found = False

		if door_position  == my_position:
			for entity in game.get_player().get_inventory():
				if str(entity) == "Key('K')":
					game.set_win(True)
					game.set_game_over(True)
					found  = True
		if not found:
			print('You don\'t have the key!')

	def __str__(self) :
		return "Door('D')"

	def  __repr__(self):
		return "Door('D')"



class Entity(Door, Item, Player, Wall):

	def __init__(self):
		self.collidable = True

	def get_id(self):
		return "Entity"

	def set_collide(self, collidable: bool):
		 self.collidable = collidable

	def can_collide(self):
		return self.collidable

	def __str__(self) :
		return "Entity('Entity')"

	def  __repr__(self):
		return "Entity('Entity')"



class GameLogic:
    def __init__(self, dungeon_name="game2.txt"):
        """Constructor of the GameLogic class.

        Parameters:
            dungeon_name (str): The name of the level.
        """
        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)

        #you need to implement the Player class first.
        self._player = Player(GAME_LEVELS[dungeon_name])

        #you need to implement the init_game_information() method for this.
        self._game_information = self.init_game_information()

        self._win = False

        self._gameOver  =  False

    def get_positions(self, entity):
        """ Returns a list of tuples containing all positions of a given Entity
             type.

        Parameters:
            entity (str): the id of an entity.

        Returns:
            )list<tuple<int, int>>): Returns a list of tuples representing the
            positions of a given entity id.
        """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row,col))

        return positions

    # Write your code here

    def init_game_information(self):
        entities_position = {}
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                entity = None
                if  char == "O":
                	self._player.set_position((row,col))
                elif char == "K":
                	entity = Key()
                elif char == "D":
                	entity = Door()
                elif char ==  "#":
                	entity = Wall()
                elif char == "M":
                	entity = MoveIncrease()

                if entity is  not None:
                	entities_position[(row,col)] = entity

        return entities_position

    def get_dungeon_size(self):
    	return self._dungeon_size

    def get_game_information(self):
        return self._game_information

    def get_player(self):
    	return self._player

    def get_entity(self, position):
    	if position in self.get_game_information():
    		return self.get_game_information()[position]
    	else:
    		return None




    def new_position(self, direction):
    	old_position =  self._player.get_position()

    	row = old_position[0]
    	col = old_position[1]
    	if direction ==  "W" and row >=0:
    		row-=1
    	elif direction ==  "S"  and row < self.get_dungeon_size():
    		row+=1
    	elif  direction == "D" and col < self.get_dungeon_size():
    		col+=1
    	elif  direction == "A" and col >= 0:
    		col-=1
    	position = (row,col)
    	return position

    def get_entity_in_direction(self, direction):
    	position = self.new_position(direction)
    	return self.get_entity(position)

    def collision_check(self, direction):
    	entity =  self.get_entity_in_direction(direction)
    	if entity is not  None:
    		if entity.can_collide():
    			return True	#key or door
    		else:
    			return False
    	return None

    def investigate_entity(self,direction):
        self._player.decrease_move()
        entity = self.get_entity_in_direction(direction)
        if entity is not  None:
            print(str(entity), ' is on the ',direction, ' side.')

    def move_player(self, direction):
        self._player.decrease_move()
        old_position  = self._player.get_position()
        position =  self.new_position(direction)
        if self.collision_check(direction)  is None :
            self._player.set_position(position)        	
        elif self.collision_check(direction):
            self._player.set_position(position)  
            entity =  self.get_entity(position)
            if entity.can_collide():
                entity.on_hit(self)  
        else:
            print(INVALID)


    def check_game_over(self):
        if self._gameOver or self._player.moves_remaining() < 1:
            self.set_game_over(True)
            return True
        else:
            False


    def set_game_over(self,value):
        self._gameOver = value

    def set_win(self, win):
        self._win  = win

    def won(self):
        return  self._win

class GameApp:

    def __init__(self):
        self._gameLogic =GameLogic()
        self._gameDisplay =  Display(self._gameLogic.get_game_information(), self._gameLogic.get_dungeon_size())


    def play(self):
        while(not self._gameLogic.check_game_over()):
        	self.draw()
        	user_input = input("Please input an action:")
        	if user_input == "W" or user_input ==  "S" or user_input  == "D" or user_input == "A":
        		self._gameLogic.move_player(user_input)
        	elif  user_input  == "I W" or user_input ==  "I S" or user_input  == "I D" or user_input == "I A":
        		self._gameLogic.investigate_entity(user_input[len(user_input)-1])
        	elif user_input == "H":
        		print(HELP_MESSAGE)
        	elif user_input == "Q":
        		confirm = input("Are you sure you want to quit? (y/n):")
        		if confirm == "y ":
        			exit()
        	else:
        		print(INVALID)

        if self._gameLogic.won():
        	print(WIN_TEXT)
        else:
        	print("You have lost all your strength and honour.")

    def draw(self):
        self._gameDisplay.display_game(self._gameLogic.get_player().get_position())
        self._gameDisplay.display_moves(self._gameLogic.get_player().moves_remaining())




def main():
    game  = GameApp()
    game.play()

if __name__ == "__main__":
    main()

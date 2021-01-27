
from utils import *
import tkinter as tk
from tkinter import messagebox
import time
from PIL import ImageTk
import PIL.Image

TASK_ONE = "CAVE"
TASK_TWO = "FOREST"

PLAYER = "O"
KEY = "K"
DOOR = "D"
WALL = "#"
MOVE_INCREASE = "M"
SPACE = " "

GAME_NAME = "Key Cave Adventure Game"

GAME_LEVELS = {
    # dungeon layout: max moves allowed
    "game1.txt": 7,
    "game2.txt": 12,
    "game3.txt": 19,
}


DIRECTIONS = {
    "W": (-1, 0),
    "S": (1, 0),
    "D": (0, 1),
    "A": (0, -1)
}


def load_game(filename):
    """Create a 2D array of string representing the dungeon to display.

    Parameters:
        filename (str): A string representing the name of the level.

    Returns:
        (list<list<str>>): A 2D array of strings representing the
            dungeon.
    """
    dungeon_layout = []

    with open(filename, 'r') as file:
        file_contents = file.readlines()

    for i in range(len(file_contents)):
        line = file_contents[i].strip()
        row = []
        for j in range(len(file_contents)):
            row.append(line[j])
        dungeon_layout.append(row)

    return dungeon_layout


class AbstractGrid(tk.Canvas):

    def __init__(self, master, rows, cols, width, height, **kwargs):
        tk.Canvas.__init__(self, width=width, height=height)
        self._cell_size = (width/rows, height/cols)
        # width/rows is cell width and height/cols is cell height
        self.pack(anchor='center', side='left')

    def get_bbox(self, position):
        """ Returns the bounding box for the (row, col) position
        """
        x1 = int(position[1]*self._cell_size[0])
        y1 = int(position[0]*self._cell_size[1])
        return (x1, y1, x1+self._cell_size[0], y1+self._cell_size[1])

    def pixel_to_position(self, pixel):
        """ Converts the x, y pixel position (in graphics units) to a (row, col) position
        """
        return (int(pixel[0]/self._cell_size[0]), int(pixel[1]/self._cell_size[1]))

    def get_position_center(self, position):
        """ Gets the graphics coordinates for the center of the cell at the given (row, col) position
        """
        # position[1] represent column number and position[0] represent row number
        x = int((position[1]*self._cell_size[0]) + self._cell_size[0]/2)
        y = int((position[0]*self._cell_size[1]) + self._cell_size[1]/2)
        return (x, y)

    def annotate_position(self, position, text):
        """ Annotates the cell at the given (row, col) position with the provided text
        """
        x, y = self.get_position_center(position)
        self.create_text(x, y, text=f"{text}", anchor=tk.CENTER)


class DungeonMap(AbstractGrid):
    def __init__(self, master, size, width=600, **kwargs):
        AbstractGrid.__init__(self, master=master, rows=size, cols=size,
                              width=width, height=width, kwargs=kwargs)

        """
        size is the number of rows (equal to the number of columns) in the grid, and width is the number of pixels for the width and height of the grid
        """

    def draw_grid(self, dungeon, player_position):
        self.delete('all')
        # dungeon type - dict<tuple<int, int>: Entity>: game_information

        for position in dungeon:
            entity = dungeon[position].get_id()

            cell_coordinates = self.get_bbox(position)
            if entity == WALL:
                self.create_rectangle(cell_coordinates, fill='dark grey')
            elif entity == DOOR:
                self.create_rectangle(cell_coordinates, fill='red')
                self.annotate_position(text="Nest", position=position)
            elif entity == KEY:
                self.create_rectangle(cell_coordinates, fill='yellow')
                self.annotate_position(text="Trash", position=position)
            elif entity == MOVE_INCREASE:
                self.create_rectangle(cell_coordinates, fill='orange')
                self.annotate_position(text="Banana", position=position)

            player_coordinates = self.get_bbox(player_position)
            player_cell_center_coordinaates = self.get_position_center(
                player_position)
            self.create_rectangle(player_coordinates, fill='spring green')
            self.create_text(player_cell_center_coordinaates[0], player_cell_center_coordinaates[1],
                             text="Ibis", anchor=tk.CENTER)

def draw_grid(self, dungeon, player_position):
        self.delete('all')
        # dungeon type - dict<tuple<int, int>: Entity>: game_information

        for position in dungeon:
            entity = dungeon[position].get_id()

            cell_coordinates = self.get_bbox(position)
            if entity == WALL:
                self.create_rectangle(cell_coordinates, fill='dark grey')
            elif entity == DOOR:
                self.create_rectangle(cell_coordinates, fill='red')
                self.annotate_position(text="Nest", position=position)
            elif entity == KEY:
                self.create_rectangle(cell_coordinates, fill='yellow')
                self.annotate_position(text="Trash", position=position)
            elif entity == MOVE_INCREASE:
                self.create_rectangle(cell_coordinates, fill='orange')
                self.annotate_position(text="Banana", position=position)

            player_coordinates = self.get_bbox(player_position)
            player_cell_center_coordinaates = self.get_position_center(
                player_position)
            self.create_rectangle(player_coordinates, fill='spring green')
            self.create_text(player_cell_center_coordinaates[0], player_cell_center_coordinaates[1],
                             text="Ibis", anchor=tk.CENTER)
class KeyPad(AbstractGrid):
    def __init__(self, master, width=200, height=100, **kwargs):
        AbstractGrid.__init__(self, master=master, rows=3, cols=2,
                              width=width, height=height, kwargs=kwargs)

        """ Create Keypad UI
        """
        for row in range(2):
            for col in range(3):
                if row == 0 and (col == 0 or col == 2):
                    continue
                self.create_rectangle(self.get_bbox(
                    (row, col)), fill='dark grey')
                if row == 0 and col == 1:
                    self.annotate_position(text="N", position=(row, col))
                elif row == 1:
                    if col == 0:
                        self.annotate_position(text="W", position=(row, col))
                    if col == 1:
                        self.annotate_position(text="S", position=(row, col))
                    if col == 2:
                        self.annotate_position(text="E", position=(row, col))

    def pixel_to_direction(self, pixel):
        """ Converts the x, y pixel position to the direction of the arrow depictedat that position
        """

        position = self.pixel_to_position(pixel=pixel)
        direction = ' '
        if position[1] == 0 and position[0] == 1:
            direction = 'W'
        elif position[1] == 1:
            if position[0] == 0:
                direction = 'A'
            if position[0] == 1:
                direction = 'S'
            if position[0] == 2:
                direction = 'D'
        return direction


class StatusBar(tk.Frame):
    def __init__(self, parent=None, **kw):
        tk.Frame.__init__(self, parent, kw)
        self.initUi(parent)

    def initUi(self, parent):
        # Parent Status bar frame widget
        status_bar_frame = tk.Frame(parent)
        status_bar_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        moves_frame = tk.Frame(status_bar_frame)
        moves_frame.pack(side=tk.RIGHT)

        buttons_frame = tk.Frame(status_bar_frame)
        buttons_frame.pack(side=tk.LEFT)

        timer_frame = tk.Frame(status_bar_frame)
        timer_frame.pack(side=tk.BOTTOM, expand=1)

        self.new_game_btn = tk.Button(buttons_frame, text="New Game")
        self.quit_btn = tk.Button(buttons_frame, text="Quit")

        image_clock_file = open("images/clock.png", "rb")
        image_clock = PIL.Image.open(image_clock_file)
        image_clock.thumbnail((54, 54), PIL.Image.ANTIALIAS)
        photo_clock = ImageTk.PhotoImage(image_clock)

        clock_label = tk.Label(timer_frame, image=photo_clock)
        clock_label.image = photo_clock
        clock_label.pack(fill="both", expand="yes", side="left")

        self.time_elapsed_heading = tk.Label(timer_frame, text='Time elapsed')
        self.timer = Timer(timer_frame)

        image_lightning_file = open("images/lightning.gif", "rb")
        image_lightning = PIL.Image.open(image_lightning_file)
        image_lightning.thumbnail((54, 54), PIL.Image.ANTIALIAS)
        photo_lightning = ImageTk.PhotoImage(image_lightning)

        lightning_label = tk.Label(moves_frame, image=photo_lightning)
        lightning_label.image = photo_lightning
        lightning_label.pack(fill="both", expand="yes", side="left")
        self.moves_left_heading = tk.Label(moves_frame, text='Moves Left')
        self.remaining_moves = tk.Label(moves_frame, text="12 moves remaining")

        self.new_game_btn.pack(side=tk.BOTTOM)
        self.quit_btn.pack(side=tk.BOTTOM)

        self.time_elapsed_heading.pack(side=tk.BOTTOM)
        self.timer.pack(side=tk.BOTTOM)

        self.moves_left_heading.pack(side=tk.BOTTOM)
        self.remaining_moves.pack(side=tk.BOTTOM)


class Timer(tk.Frame):
    def __init__(self, parent=None, **kw):
        tk.Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = tk.StringVar()
        self.makeWidgets()
        self.Start()

    def makeWidgets(self):
        """ Make the time label. """
        l = tk.Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        l.pack(pady=2, padx=2)

    def _update(self):
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def Start(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def Reset(self):
        """ Reset the timer. """
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)

    def Stop(self):                                    
        """ Stop the timer, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0


class Entity:
    """A generic entity within the game
    """

    def __init__(self):
        """Constructor for class Entity
        """
        self._id = "Entity"
        self.collidable = True

    def get_id(self):
        """Returns a string that represents the Entity’s ID.
        """
        return self._id

    def set_id(self, entity):
        """Sets the ID of Entity.

        Args:
            entity (str): New _id value for the Entity
        """
        self._id = entity

    def set_collide(self, collidable):
        """Set the collision state for the Entity to be True

        Args:
            collidable (bool): Collision state we want to set.
        """
        self.collidable = collidable

    def can_collide(self):
        """Returns the collidable state of entity
        """
        return self.collidable

    def __str__(self):
        """Returns the string representation of the Entity

        Returns:
            str: String representation of Entity
        """
        return f"Entity('{self.get_id()}')"

    def __repr__(self):
        """returns representation of the Entity.
        (Same as __str__) 

        Returns:
            str: representation of Entity
        """
        return str(self)


class Wall(Entity):
    """A Wall is a special type of an Entity within the game.
    """

    def __init__(self):
        """Constructor for the wall class
        """
        super().__init__()
        self.set_id(WALL)
        self.set_collide(False)

    def __str__(self):
        """returns string representation for Wall 

        Returns:
            str: String representation for wall
        """
        return f"Wall('{self.get_id()}')"


class Door(Entity):
    """Door is a special Entity within the game.
    """

    def __init__(self):
        """Constructor for Door 
        """
        super().__init__()
        self.set_id(DOOR)

    def on_hit(self, game):
        """Sets the game to win state if the user 
        inventory contains a Key

        Args:
            game (GameLogic): instance of GameLogic class
        """
        door_position = game.get_positions(DOOR)[0]
        my_position = game.get_player().get_position()

        found = False

        if door_position == my_position:
            for entity in game.get_player().get_inventory():
                if entity.get_id() == KEY:
                    game.set_win(True)
                    found = True
        if not found:
            print('You don\'t have the key!')

    def __str__(self):
        """returns string representation for Door

        Returns:
            str: String representation for Door
        """
        return f"Door('{self.get_id()}')"


class Player(Entity):
    """Player is a special type of entity within the game.
    """

    def __init__(self, move_count):
        """constructor for class Player

        Args:
            move_count (int): Number of moves alloted to Player at start.
        """
        super().__init__()
        self.set_id(PLAYER)

        self.move_count = move_count
        self.position = None
        self.inventory = []

    def set_position(self, position):
        """Sets the position of the Player

        Args:
            position (tuple<int, int>): Tuple containing position of Player 
        """
        self.position = position

    def get_position(self):
        """Returns the position of the Player.

        Returns:
            tuple<int, int>: position in the form of tuple
        """
        return self.position

    def change_move_count(self, number: int):
        """Updates the move count of the Player

        Args:
            number (int): Number to increment the count with
        """

        self.move_count += number

    def moves_remaining(self):
        """Returns the moves available to Player

        Returns:
            int: available_moves
        """
        return self.move_count

    def add_item(self, item: Entity):
        """Adds item to the Player's inventory.

        Args:
            item (Entity): Item to be added in Inventory
        """
        self.inventory.append(item)

    def get_inventory(self):
        """returns Player's Inventory

        Returns:
            List: Player Inventory
        """
        return self.inventory

    def __str__(self):
        """String Representation of Player class

        Returns:
            str: String implementation
        """
        return f"Player('{self._id}')"


class Item(Entity):
    """An Item is a special type of an Entity within the game. This is an abstract class.
    By default the Item Entity can be collided with.
    """

    def __init__(self):
        """Constructor for Item class
        """
        super().__init__()

    def on_hit(self, game):
        """This is an abstract method and needs to be implemented
        by base classes.

        Args:
            game (GameLogic): instance of GameLogic class

        Raises:
            NotImplementedError: Raises error due to abstract class
        """
        raise NotImplementedError

    def __str__(self):
        """String representation of class Item

        Returns:
            str: String representation 
        """
        return f"Item('{self.get_id()}')"


class Key(Item):
    """Key is a special type of Item within the game
    """

    def __init__(self):
        """constructor for class Key
        """
        super().__init__()
        self.set_id(KEY)

    def on_hit(self, game) -> None:
        """Adds Key into the player's inventory and
        removes from game_information.

        Args:
            game (GameLogic): instance of GameLogic class
        """
        player = game.get_player()
        player.add_item(self)
        game.get_game_information().pop(player.get_position())

    def __str__(self) -> str:
        """String Representation of class Key

        Returns:
            str: String Representation
        """
        return f"Key('{self._id}')"


class MoveIncrease(Item):
    """MoveIncrease is a special type of Item within the game.
    """

    def __init__(self, moves=5):
        """constructor for class MoveIncrease

        Args:
            moves (int, optional): Number of moves we want to increment. Defaults to 5.
        """
        super().__init__()
        self.set_id(MOVE_INCREASE)
        self.moves = moves

    def on_hit(self, game) -> None:
        """Increase the move_count of the game player.

        Args:
            game (GameLogic): Instance of class GameLogic
        """
        player = game.get_player()
        player.change_move_count(self.moves)
        game.get_game_information().pop(player.get_position())

    def __str__(self):
        """String representation of class MoveIncrease

        Returns:
            str: String Representation
        """
        return f"MoveIncrease('{self._id}')"


class GameLogic:
    """It contains methods, all the game information and how the game should play out.
    """

    def __init__(self, dungeon_name="game2.txt"):
        """Constructor of the GameLogic class.

        Parameters:
            dungeon_name (str): The entity of the level.
        """
        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)

        self._player = Player(GAME_LEVELS[dungeon_name])

        self._game_information = self.init_game_information()

        self._win = False

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
                    positions.append((row, col))

        return positions

    def get_dungeon_size(self):
        """Returns the dungeon size 

        Returns:
            int: dungeon size
        """
        return self._dungeon_size

    def init_game_information(self):
        """Updates game_information with the data of positions and Entity
        as Key Value pair.

        Returns:
            dict<tuple<int, int>: Entity>: game_information
        """
        entities_position = {}
        # {(row, col): Entity, ...}
        for row in range(0, self._dungeon_size):
            for col in range(0, self._dungeon_size):
                position = (row, col)
                char = self._dungeon[row][col]
                entity = None
                if char == WALL:
                    entity = Wall()
                elif char == KEY:
                    entity = Key()
                elif char == PLAYER:
                    self._player.set_position(position)
                elif char == DOOR:
                    entity = Door()
                elif char == MOVE_INCREASE:
                    entity = MoveIncrease()

                if entity:
                    entities_position[position] = entity
        return entities_position

    def get_game_information(self):
        """Returns game_information

        Returns:
            dict<tuple<int, int>: Entity>: game_information
        """
        return self._game_information

    def get_player(self):
        """Returns the game Player

        Returns:
            Player: Player instance used in class
        """
        return self._player

    def get_entity(self, position):
        """Returns Entity at position specified.
        if position not in game_information return None.

        Args:
            position tuple<int, int>: position we want get entity at

        Returns:
            Entity: Instance of Entity 
        """
        return self._game_information.get(position, None)

    def get_entity_in_direction(self, direction):
        """Returns an Entity in the given direction of the Player’s position. 
        If there is no Entity in the given direction or if the direction is 
        off map then this function should return None.

        Args:
            direction (DIRECTIONS): directions for navigation

        Returns:
            Entity: instance of class Entity
        """
        new_p = self.new_position(direction)
        return self.get_entity(new_p)

    def collision_check(self, direction):
        """ Returns False if a player can travel in the given direction, they 
        won’t collide. True, they will collide, otherwise.

        Args:
            direction (DIRECTIONS): direction in which we want to check collision
        """
        entity = self.get_entity_in_direction(direction)

        if entity:
            if entity.can_collide():
                return False
            else:
                return True
        elif entity == None:
            return False

    def new_position(self, direction):
        """Returns a tuple of integers that represents the new position given the direction.

        Args:
            direction (str): Direction in which we want to get new position

        Returns:
            tuple<int, int>: New position for Player
        """
        d = DIRECTIONS[direction]
        position = self.get_player().get_position()
        new_p = (d[0]+position[0], d[1]+position[1])

        return new_p

    def move_player(self, direction):
        """Update the Player’s position to place them one position in the given direction.

        Args:
            direction (tuple<int, int>): direction in which we want to move
        """
        player = self.get_player()
        new_p = self.new_position(direction)
        player.set_position(new_p)

    def check_game_over(self):
        """: Return True if the game has been lost and False otherwise. 

        Returns:
            bool: game_over_state
        """
        if self.get_player().moves_remaining():
            return False
        return True

    def set_win(self, win):
        """Set the game’s win state to be True or False

        Args:
            win bool: Value we want to update
        """
        self._win = win

    def won(self):
        """Return game’s win state.

        Returns:
            bool: win state
        """
        return self._win


class GameApp:
    """GameApp acts as a communicator between the GameLogic and the Display
    """

    def __init__(self, master, status_bar, task=TASK_ONE, dungeon_name="game2.txt"):
        """Constructor of the GameApp class.
        """
        self._game_logic = GameLogic()
        self._dungeon_map = DungeonMap(
            master=master, size=self._game_logic.get_dungeon_size(), bg='light gray')
        self._master = master
        self._keypad = KeyPad(master=master, width=200, height=100)
        self._status_bar = status_bar

    def on_direction_change(self, direction):
        if direction in list(DIRECTIONS.keys()):
            # get collision state
            collision = self._game_logic.collision_check(direction)
            entity = self._game_logic.get_entity_in_direction(direction)
            if not collision:
                self._game_logic.move_player(direction)
                if entity and entity.get_id() in [KEY, MOVE_INCREASE, DOOR]:
                    entity.on_hit(self._game_logic)

            self._dungeon_map.draw_grid(dungeon=self._game_logic.get_game_information(
            ), player_position=self._game_logic.get_player().get_position())
            if self._game_logic.won():
                self._status_bar.timer.Stop()
                tk.messagebox.showinfo(
                    "You won!", "You have finished the level!")

                exit(0)

    def play(self):
        """Method defined to play the game according to user input.
        """
        while(not self._game_logic.check_game_over()):
            self._dungeon_map.draw_grid(dungeon=self._game_logic.get_game_information(
            ), player_position=self._game_logic.get_player().get_position())

            def key(event):
                self._master.focus_set()

                direction = event.char.upper()
                self.on_direction_change(direction)

            def callback(event):
                self._master.focus_set()

                direction = self._keypad.pixel_to_direction((event.x, event.y))
                self.on_direction_change(direction)

            self._master.bind("<Button-1>", callback)
            self._master.bind("<Key>", key)

            self._master.mainloop()
            # action = input("Please input an action: ").strip().split()
            if action[0] in VALID_ACTIONS:
                if action[0] in list(DIRECTIONS.keys()):
                    direction = action[0]
                    # get collision state
                    collision = self._game_logic.collision_check(direction)
                    entity = self._game_logic.get_entity_in_direction(
                        direction)
                    if not collision:
                        self._game_logic.move_player(action[0])
                        if entity and entity.get_id() in [KEY, MOVE_INCREASE, DOOR]:
                            entity.on_hit(self._game_logic)
                    else:
                        print(INVALID)

                elif action[0] == "I":
                    if action[1] in list(DIRECTIONS.keys()):
                        entity = self._game_logic.get_entity_in_direction(
                            action[1])
                        print(f"{entity} is on the {action[1]} side.")
                    else:
                        print(INVALID)
                        continue

                elif action[0] == QUIT:
                    confirm = input("Are you sure you want to quit? (y/n): ")
                    if confirm.lower() in ["y", "n"]:
                        if confirm == "y":
                            return
                        continue
                    else:
                        print(INVALID)
                        continue
                elif action[0] == HELP:
                    print(HELP_MESSAGE)
                    continue

            else:
                print(INVALID)
                continue

            self._game_logic.get_player().change_move_count(-1)

            if self._game_logic.won():
                print(WIN_TEXT)
                return
        print(LOSE_TEST)

    def draw(self):
        """display the dungeon,player_position and moves remaining.
        """
        self._display.display_game(
            self._game_logic.get_player().get_position())
        self._display.display_moves(
            self._game_logic.get_player().moves_remaining())


def main():
    """Creates instance of GameApp and calls the play method on it.
    """
    master = tk.Tk()
    master.title(GAME_NAME)
    label_widget = tk.Label(master, text=GAME_NAME, bg='green',
                            background="spring green", font='Helvetica 18')
    label_widget.pack(fill=tk.BOTH)

    status_bar = StatusBar(master)
    status_bar.pack(side=tk.BOTTOM)
    game = GameApp(master=master, status_bar=status_bar)
    game.play()


if __name__ == "__main__":
    main()

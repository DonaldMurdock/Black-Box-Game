#Donald Taylor
#8/7/2020
#Implementation of the Black Box game.

class BlackBoxGame:
    """Represents Black Box Game. Has data members for storing the gameboard, score of the player, number of atoms,
    a list of incorrect guesses, and a dictionary that stores each atom and whether or not it has been guessed.
    """

    def __init__(self, atom_locations):
        """Creates a BlackBoxGame object with data members for the board, player score, number of atoms, incorrect guesses,
        and a dictionary containing each atom and whether or not it has been guessed.

        The function takes a list of atom locations as a parameter and places the atoms on the board. The atoms are
        represented by an 'X'. It uses the given atom locations to initialize the number of atoms and puts them all in
        a dictionary where they are associated with 'UNGUESSED'
        """
        self._board = []
        self._score = 25
        self._num_of_atoms = 0
        self._incorrect_guesses = []
        self._ray_entries_and_exits = []
        self._atoms_dict = {}


        for i in range(10):                                     #Construct empty gameboard
            self._board.append([])
            for j in range(10):
                self._board[i].append('')

        for loc in atom_locations:                              #Place atoms on board
            self._board[loc[0]][loc[1]] = 'X'
            self._num_of_atoms = self._num_of_atoms + 1         #and count them
            self._atoms_dict[loc] = 'UNGUESSED'                 #and add them to the dictionary as UNGUESSED

    def get_atoms_dict(self):
        """Returns the atoms dictionary
        """
        return self._atoms_dict

    def is_valid_coordinate(self, coordinate):
        """Takes a tuple containing (row, column) as a coordinate.
        Returns True if the coordinate is valid and False otherwise
        """
        row = coordinate[0]
        column = coordinate[1]

        if row < 0 or row > 9:                  #Check for invalid coordinates
            return False
        if column < 0 or column > 9:
            return False

        return True

    def has_atom(self, coordinate):
        """Takes a tuple containing (row, column) as a coordinate.
        Returns True if there is an atom at the given coordinate, and False otherwise"""

        if not self.is_valid_coordinate(coordinate):
            return False

        row = coordinate[0]
        column = coordinate[1]

        if self._board[row][column] == '':
            return False
        else:
            return True


    def print_board(self):
        """Prints the current game board. X's represent atoms.
        """

        print('   0  1  2  3  4  5  6  7  8  9')       #Column numbers

        for i in range(10):
            row = str(i) + '  '
            for j in range(10):                        #Creates each row
                if self.has_atom((i,j)):
                    row = row + 'X' + '  '             #With X for Atoms
                else:
                    row = row + '   '                  #If a space doesn't have an atom we had spaces
            print(row)

    def get_score(self):
        """Returns the player's current score
        """
        return self._score

    def decrease_score(self, amt):
        """Decreases the player's score by 1 or 5, taken as a parameter
        """
        self._score = self._score - amt

    def guess_atom(self, row, column):
        """If there is an atom at the specified location the method will return True. It will change the atom in
        the dictionary from 'UNGUESSED' to 'GUESSED'. If the atom has already been guessed it will return True and
        nothing will be changed.

        If there is no atom at the location the method will return False and decrease 5
        points from the player's score. If the player has already guessed this location, the method will return False
        but the score will remain unchanged
        """

        if self.has_atom((row, column)):                          #If the guess is correct
            self._atoms_dict[(row,column)] = 'GUESSED'
            return True

        else:                                                   #If the guess is incorrect
            if (row,column) in self._incorrect_guesses:         #If it's already been guessed return false
                return False
            else:
                self._incorrect_guesses.append((row,column))    #else add it to our list of incorrect guesses
                self.decrease_score(5)                          #and decrease the score by 5
                return False

    def atoms_left(self):
        """Returns the number of atoms that remain to be guessed.
        """
        num_of_atoms_left = 0
        for atom in self._atoms_dict:
            if self._atoms_dict[atom] == 'UNGUESSED':
                num_of_atoms_left = num_of_atoms_left + 1
        return num_of_atoms_left

    def is_border(self, coordinate):
        """Takes a tuple containing (row,column) as a parameter. Determines if the coordinate is a border coordinate. Returns
        True if it is and False otherwise"""
        row = coordinate[0]
        column = coordinate[1]

        if row in [0,9]:
            return True
        if column in [0,9]:
            return True
        return False

    def is_non_corner_border(self, coordinate):
        """Takes a row and column as a parameter. Determines if the coordinate is a border coordinate and not a corner.
         Returns True if it is and False otherwise.
         """
        row = coordinate[0]
        column = coordinate[1]

        if row == 0:
            if column <=0 or column >= 9:
                return False
            return True
        if row == 9:
            if column <= 0 or column >= 9:
                return False
            return True
        if column == 0:
            if row <= 0 or row >= 9:
                return False
            return True
        if column == 9:
            if row <= 0 or row >= 9:
                return False
            return True
        return False

    def shoot_ray(self, row, column):
        """Takes a row and column as parameters. If the starting position is invalid it returns False.

        Shoots a ray from the starting location. If the ray hits an atom the method returns None.

        Otherwise the ray returns a tuple containing (row, column) of the exit location of the ray.
        """

        if self.is_non_corner_border((row, column)) == False:           #If the starting location is invalid
            return False

        ray = Ray(row, column)
        if ray.get_location() not in self._ray_entries_and_exits:       #If the player hasn't guessed this location yet
            self.decrease_score(1)                                      #decrease the score
            self._ray_entries_and_exits.append(ray.get_location())      #and save the location

        while True:
            if self.has_atom(ray.get_fwd()):            #Check in front for atom
                return None
            while self.has_atom(ray.get_fwd_left()):    #Check forward left for atom
                ray.turn_right()
            while self.has_atom(ray.get_fwd_right()):   #Check forwward right for atom
                ray.turn_left()
            if self.is_border(ray.get_location()):      #If i'm in the border
                if not self.is_border(ray.get_fwd()) and self.is_valid_coordinate(ray.get_fwd()):   #And i'm facing inside the gameboard
                    ray.move()                          #move
            else:                                       #I'm i'm not in the border
                ray.move()                              #move
            if self.is_border(ray.get_location()):      #If i moved into the border
                if ray.get_location() not in self._ray_entries_and_exits:  # If the player hasn't guessed this location yet
                    self.decrease_score(1)                                 # decrease the score
                    self._ray_entries_and_exits.append(ray.get_location())   # and save the location
                return ray.get_location()                                  #Return the location
                break


class Ray:
    """Represents a ray for the Black Box Game. Ray's have data members for location and direction, and methods
    for moving around the game board
    """
    def __init__(self,row, column):
        """Creates a ray at the location given as parameters. The direction of the ray is initialized based on the
        location.
        """
        self._row = row
        self._column = column

        if row == 9:
            self._direction = 'NORTH'
        if row == 0:
            self._direction = 'SOUTH'
        if column == 0:
            self._direction = 'EAST'
        if column == 9:
            self._direction = 'WEST'

    def get_location(self):
        """Returns a tuple with (row, column) of the current location
        """
        return (self._row, self._column)

    def move(self):
        """Moves the ray forward one space in whatever direction it's facing.
        """

        if self._direction == 'NORTH':
            self._row = self._row - 1
        if self._direction == 'SOUTH':
            self._row = self._row + 1
        if self._direction == 'EAST':
            self._column = self._column + 1
        if self._direction == 'WEST':
            self._column = self._column - 1

    def turn_right(self):
        """Turns the ray to the right.
        """
        if self._direction == 'NORTH':
            self._direction = 'EAST'
            return
        if self._direction == 'SOUTH':
            self._direction = 'WEST'
            return
        if self._direction == 'EAST':
            self._direction = 'SOUTH'
            return
        if self._direction == 'WEST':
            self._direction = 'NORTH'
            return

    def turn_left(self):
        """Turns the ray to the left.
        """
        if self._direction == 'NORTH':
            self._direction = 'WEST'
            return
        if self._direction == 'SOUTH':
            self._direction = 'EAST'
            return
        if self._direction == 'EAST':
            self._direction = 'NORTH'
            return
        if self._direction == 'WEST':
            self._direction = 'SOUTH'
            return

    def get_fwd(self):
        """Returns a tuple containing the coordinate directly in front of the ray
        """
        if self._direction == 'NORTH':
            return (self._row - 1, self._column)
        if self._direction == 'SOUTH':
            return (self._row + 1, self._column)
        if self._direction == 'EAST':
            return (self._row, self._column + 1)
        if self._direction == 'WEST':
            return (self._row, self._column - 1)

    def get_fwd_left(self):
        """Returns a tuple containing the coordinate diagonally forward and left of the ray
        """
        if self._direction == 'NORTH':
            return (self._row - 1, self._column - 1)
        if self._direction == 'SOUTH':
            return (self._row + 1, self._column + 1)
        if self._direction == 'EAST':
            return (self._row - 1, self._column + 1)
        if self._direction == 'WEST':
            return (self._row + 1, self._column - 1)

    def get_fwd_right(self):
        """Returns a tuple containing the coordinate diagonally forward and right of the ray
        """
        if self._direction == 'NORTH':
            return (self._row - 1, self._column + 1)
        if self._direction == 'SOUTH':
            return (self._row + 1, self._column - 1)
        if self._direction == 'EAST':
            return (self._row + 1, self._column + 1)
        if self._direction == 'WEST':
            return (self._row - 1, self._column - 1)


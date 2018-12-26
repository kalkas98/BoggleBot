import random

CUBE_SIDES = 6
MIN_WORD_LENGTH = 3
DICTIONARY_FILE = "words.txt"
BOARD_SIZE = 4

# possible letters at every cube, used to generate a board which is
# not completely random where words are easier to form
CUBES = [
   "AAEEGN", "ABBJOO", "ACHOPS", "AFFKPS",
   "AOOTTW", "CIMOTU", "DEILRX", "DELRVY",
   "DISTTY", "EEGHNW", "EEINSU", "EHRTVW",
   "EIOSST", "ELRTTY", "HIMNQU", "HLNNRZ"
]


class Boggle:
    """
    Contains functionality for playing a game of boggle
    """

    def __init__(self):

        self.word_list = set(line.strip() for line in open(DICTIONARY_FILE))

        self.points_list = {}
        self.visited = [[], [], [], []]
        self.board = [[], [], [], []]
        self.guessed = []
        self.init_board()
        # Reset Game()

    def reset_game(self):
        """Resets the game state"""
        self.points_list = {}
        self.guessed = []
        self.visited = [[], [], [], []]
        self.board = [[], [], [], []]
        self.init_board()

    def init_board(self):
        """Initializes the letters at the board and initializes self.visited"""
        for i in range(0, BOARD_SIZE):
            for n in range(0, BOARD_SIZE):
                seed = random.randint(0, CUBE_SIDES-1)

                self.board[i] += \
                    [CUBES[i*BOARD_SIZE + n][seed]]
                self.visited[i] += [False]

    def is_on_board(self, word):
        """
        Determines if you can form a given word on the board
        :param word: a given word as a string
        :return: returns true if the given word can be formed on the board
        """
        for i in range(0, BOARD_SIZE):
            for n in range(0, BOARD_SIZE):
                if self.is_on_board_helper(word, i, n):
                    return True
        return False

    def is_on_board_helper(self, word, row, column):
        """
        Determines if a given word can be formed on the word
        :param word: a word asa string
        :param row: row at which the previous letter was
        :param column: column at which the previous letter was
        :return: returns true if the given word could be found on the board
        """
        if not word:
            return True
        else:
            for i in range(row-1,row+2):
                for n in range(column-1,column+2):
                    in_bounds = (i > -1) and (n > -1) and (i < BOARD_SIZE) and (n < BOARD_SIZE)
                    if in_bounds and word[0].lower() == self.board[i][n].lower() and not self.visited[i][n]:
                        self.visited[i][n] = True
                        is_on_board = self.is_on_board_helper(word[1:], i, n)
                        self.visited[i][n] = False

                        if is_on_board:
                            return True
            return False

    def get_remaining_words(self):
        """Returns a list of all remaining words that can be formed on the board"""
        words = []
        for i in range(0,BOARD_SIZE):
            for n in range(0,BOARD_SIZE):
                self.get_remaining_words_helper(i, n, self.board[i][n], words)

        return words

    def get_remaining_words_string(self):
        """Returns all remaining words as a string"""
        words = self.get_remaining_words()
        word_string = ""
        for word in words:
            word_string += word + " "
        return word_string

    def get_remaining_words_helper(self, row, column, word, words):
        """
        Recursive helper function for determining all possible words that can be found on the board
        this function is pretty slow and should probably make use of a trie data structure
        :param row: row att which the previous letter was found
        :param column: column at which the previous letter was found
        :param word: word which the function is looking to form on the board
        :param words: list which the function append words to
        :return: a list containing possible words on the board
        """
        self.visited[row][column] = True
        if self.is_valid(word):
            words += [word.lower()]
            self.guessed += [word.lower()]

        for i in range(row-1,row+2):
            for n in range(column-1,column+2):
                in_bounds = (i > -1) and (n > -1) and (i < BOARD_SIZE) and (n < BOARD_SIZE)

                if in_bounds and not self.visited[i][n] and self.word_starts_with(word + self.board[i][n]):
                    #print(word+self._board[i][n])
                    self.get_remaining_words_helper(i, n, word + self.board[i][n], words)
        self.visited[row][column] = False

    def word_starts_with(self, word):
        """Returns true if there exists an english word that starts with the given word"""
        for real_word in self.word_list:
            if len(real_word)>3 and real_word.lower().startswith(word.lower()):
                return True
        return False

    def is_valid(self, word):
        """
        Returns true if the given word is a valid word that is can be formed on the board,
        an english word
        and has not been played already
        """
        return self.is_valid_word_length(word) and self.is_in_lexicon(word.lower()) and not self.has_been_played(word.lower())

    def is_valid_word_length(self, word):
        """Returns true if the given word is of a valid word length"""
        return len(word) >= MIN_WORD_LENGTH

    def is_in_lexicon(self, word):
        """Returns true if the given word is in the english dictionary"""
        return word in self.word_list

    def has_been_played(self,word):
        """Returns true if the given word has already been played"""
        for guessed_word in self.guessed:
            if word.lower() == guessed_word.lower():
                return True
        return False

    def play_word(self, word, player):
        """
        Plays a word and gives points to the palyer based on the length of th guessed word
        :param word: the word which is guessed
        :param player: the player name
        """
        self.guessed += [word.lower()]
        if player in self.points_list:
            self.points_list[player] += len(word) - MIN_WORD_LENGTH+1
        else:
            self.points_list[player] = len(word) - MIN_WORD_LENGTH+1

    def print_board(self):
        """Prints the board to the console"""
        for i in range(0, BOARD_SIZE):
            for n in range(0, BOARD_SIZE):
                print(self.board[i][n], end=" ")
            print("", end="\n")

    def get_score_string(self):
        """Returns a string containing each player name and their  score"""
        scores=""
        for player, score in self.points_list.items():
            scores += player + " : " + str(score) + "\n"
        return scores

    def get_chat_board(boggle):
        """Returns a discord chat representation of the given boggle game"""
        board = ""
        for i in range(0, BOARD_SIZE):
            for n in range(0, BOARD_SIZE):
                board += ":regional_indicator_"+boggle.board[i][n].lower()+": "
            board += "\n"
        return board

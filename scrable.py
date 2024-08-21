import tkinter as tk
import random
from collections import Counter

# Define the Scrabble tiles and their point values
tile_values = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8,
    'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1,
    'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
}

# Generate a list of tiles with random distribution of letters from A-Z
tiles = []
for letter, freq in tile_values.items():
    tiles.extend([letter] * freq)

# Add two blank tiles
tiles.extend([' '] * 2)

# Shuffle the tiles
random.shuffle(tiles)

# Create the main window
root = tk.Tk()
root.title("Scrabble")

# Create a frame to hold the board and trays
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

# Create a frame to hold the board
board_frame = tk.Frame(main_frame)
board_frame.grid(row=0, column=1, padx=10)

# Create the board cells
board_cells = []
for i in range(15):
    row = []
    for j in range(15):
        cell = tk.Label(board_frame, text="", relief="sunken", width=2, font=("Arial", 16))
        cell.grid(row=i, column=j)
        row.append(cell)
    board_cells.append(row)

# Create the letter trays
letter_trays = []
for player in range(2):
    tray_frame = tk.Frame(main_frame)
    tray_frame.grid(row=0, column=player*2, padx=10)
    tray = []
    for i in range(7):
        label = tk.Label(tray_frame, text="", relief="raised", width=2, font=("Arial", 16))
        label.grid(row=0, column=i)
        label.bind("<Button-1>", lambda event, label=label: pick_tile(label, player))
        tray.append(label)
    letter_trays.append(tray)

# Function to draw a tile from the bag
def draw_tile():
    if tiles:
        return tiles.pop()
    else:
        return ""

# Function to pick a tile from the tray
def pick_tile(label, player):
    tile = label.cget("text")
    if tile:
        label.config(text="")
        for row in board_cells:
            for cell in row:
                cell.bind("<Button-1>", lambda event, tile=tile, cell=cell, player=player: place_tile(tile, cell, player, label))

# Function to place a tile on the board
def place_tile(tile, cell, player, tray_label):
    if not any(label.cget("text") for row in board_cells for label in row):  # First move
        if cell == board_cells[7][7]:  # Center square
            cell.config(text=tile, bg="green")
        else:
            return  # First move must be on the center square
    else:
        cell.config(text=tile)
    cell.unbind("<Button-1>")
    next_player = (player + 1) % 2
    tray_label.config(text=draw_tile())  # Replace the picked tile with a new one
    if next_player == 0:  # If it's the first player's turn next
        for label in letter_trays[1]:
            if label.cget("text") == "":
                label.config(text=draw_tile())  # Refill the second player's tray
    end_turn(player)  # End the current player's turn

# Function to challenge a word
def challenge_word(player):
    word = input(f"Player {player + 1}, enter the word you want to challenge: ")
    if word_is_valid(word):
        print(f"The word '{word}' is valid.")
    else:
        print(f"The word '{word}' is invalid. Player {player + 1} loses their turn.")

# Function to check word validity (using a simple word list)
def word_is_valid(word):
    # Replace this with your own word validation logic
    with open("word_list.txt", "r") as file:
        word_list = [line.strip() for line in file]
    return word.upper() in word_list

# Function to check if the game has ended
def check_end_game():
    if not any(tiles) and all(not label.cget("text") for tray in letter_trays for label in tray):
        print("Game over!")
        # Calculate final scores and determine the winner
        player_scores = [calculate_score(player) for player in range(2)]
        if player_scores[0] > player_scores[1]:
            print("Player 1 wins!")
        elif player_scores[0] < player_scores[1]:
            print("Player 2 wins!")
        else:
            print("It's a tie!")
        root.quit()

# Function to calculate the score for a player
def calculate_score(player):
    score = 0
    for row in board_cells:
        for cell in row:
            letter = cell.cget("text")
            if letter:
                score += tile_values.get(letter, 0)
    return score

# Function to end the current player's turn
def end_turn(player):
    next_player = (player + 1) % 2
    print(f"Player {player + 1}, end of turn.")
    for label in letter_trays[next_player]:
        if not label.cget("text"):
            label.config(text=draw_tile())
    check_end_game()

# Bind challenge function to a key (e.g., "C" key)
root.bind("c", lambda event, player=0: challenge_word(player))
root.bind("C", lambda event, player=0: challenge_word(player))
root.bind("c", lambda event, player=1: challenge_word(player))
root.bind("C", lambda event, player=1: challenge_word(player))

# Bind end turn function to a key (e.g., "Enter" key)
root.bind("<Return>", lambda event, player=0: end_turn(player))
root.bind("<Return>", lambda event, player=1: end_turn(player))

# Set up premium squares
for i in range(15):
    for j in range(15):
        cell = board_cells[i][j]
        if (i == 7 and j == 7) or (i == 7 and j == 3) or (i == 7 and j == 11) or (i == 3 and j == 7) or (i == 11 and j == 7):
            cell.config(bg="red")  # Triple Word Score
        elif (i == 5 and j == 5) or (i == 5 and j == 9) or (i == 9 and j == 5) or (i == 9 and j == 9):
            cell.config(bg="pink")  # Triple Letter Score
        elif (i == 4 and j == 4) or (i == 4 and j == 10) or (i == 10 and j == 4) or (i == 10 and j == 10) or \
             (i == 7 and j == 0) or (i == 7 and j == 14) or (i == 0 and j == 7) or (i == 14 and j == 7):
            cell.config(bg="green")  # Double Word Score
        elif (i == 3 and j == 3) or (i == 3 and j == 11) or (i == 11 and j == 3) or (i == 11 and j == 11) or \
             (i == 6 and j == 6) or (i == 6 and j == 8) or (i == 8 and j == 6) or (i == 8 and j == 8) or \
             (i == 2 and j == 6) or (i == 2 and j == 8) or (i == 6 and j == 2) or (i == 6 and j == 12) or \
             (i == 8 and j == 2) or (i == 8 and j == 12) or (i == 12 and j == 6) or (i == 12 and j == 8):
            cell.config(bg="blue")  # Double Letter Score

# Draw initial tiles
for player in range(2):
    for label in letter_trays[player]:
        label.config(text=draw_tile())

# Start the main event loop
root.mainloop()

import gym
import numpy as np
import random

class ScrabbleEnv(gym.Env):
    def __init__(self, num_players=2):
        self.num_players = num_players
        self.board_size = 15
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.bag = self.generate_tile_bag()
        self.tile_values = {0: 0, 1: 1, 2: 3, 3: 3, 4: 4, 5: 5, 8: 8, 10: 10}
        self.player_scores = [0] * self.num_players
        self.current_player = 0
        self.player_tiles = [[] for _ in range(self.num_players)]
        self.action_space = gym.spaces.Discrete(self.board_size * self.board_size + len(self.bag))
        self.observation_space = gym.spaces.Discrete(2)  # Only two discrete observations: 0 and 1

    def reset(self):
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.player_scores = [0] * self.num_players
        self.current_player = 0
        self.player_tiles = [[] for _ in range(self.num_players)]
        self.bag = self.generate_tile_bag()
        random.shuffle(self.bag)
        for _ in range(7):
            for player in range(self.num_players):
                self.player_tiles[player].append(self.bag.pop())
        return self._discretize_observation()

    def step(self, action):
        if action < self.board_size * self.board_size:
            row = action // self.board_size
            col = action % self.board_size
            if self.board[row, col] == 0:
                word = self.get_word(row, col, self.current_player)
                if word:
                    score = self.calculate_score(word)
                    self.board[row, col] = self.player_tiles[self.current_player].pop(0)
                    self.player_scores[self.current_player] += score
                    self.current_player = (self.current_player + 1) % self.num_players
                    for _ in range(7 - len(self.player_tiles[self.current_player])):
                        if self.bag:
                            self.player_tiles[self.current_player].append(self.bag.pop(random.randint(0, len(self.bag) - 1)))
                        else:
                            break
                    return self._discretize_observation(), score, False, {}
        else:
            tile_index = action - self.board_size * self.board_size
            if tile_index < len(self.bag):
                self.player_tiles[self.current_player].append(self.bag.pop(tile_index))
                self.current_player = (self.current_player + 1) % self.num_players
                for _ in range(7 - len(self.player_tiles[self.current_player])):
                    if self.bag:
                        self.player_tiles[self.current_player].append(self.bag.pop(random.randint(0, len(self.bag) - 1)))
                    else:
                        break
                return self._discretize_observation(), 0, False, {}

        return self._discretize_observation(), 0, False, {}

    def _discretize_observation(self):
        # For simplicity, we'll use a binary observation: 0 if current player is 0, 1 if current player is 1
        return int(self.current_player)

    def generate_tile_bag(self):
        bag = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 5, 8, 8, 10, 10] * 4
        return bag

    def get_word(self, row, col, player):
        word = ""
        # Check horizontally
        for c in range(self.board_size):
            if self.board[row, c] != 0:
                word += chr(self.board[row, c] + 96)
            else:
                break
        # Check vertically
        for r in range(self.board_size):
            if self.board[r, col] != 0:
                word += chr(self.board[r, col] + 96)
            else:
                break
        return word if len(word) > 1 else ""

    def calculate_score(self, word):
        return len(word)

# Create the Scrabble environment
env = ScrabbleEnv()

# Q-learning parameters
alpha = 0.1  # Learning rate
gamma = 0.6  # Discount factor
epsilon = 0.1  # Epsilon for epsilon-greedy policy

# Initialize Q-table
num_states = env.observation_space.n
num_actions = env.action_space.n
q_table = np.zeros((num_states, num_actions))

# Q-learning algorithm
num_episodes = 10
for episode in range(num_episodes):
    state = env.reset()
    done = False
    while not done:
        # Epsilon-greedy policy
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()  # Explore action space
        else:
            action = np.argmax(q_table[state])  # Exploit learned values

        next_state, reward, done, _ = env.step(action)

        # Update Q-table
        q_table[state, action] = q_table[state, action] + alpha * (reward + gamma * np.max(q_table[next_state]) - q_table[state, action])

        state = next_state

# Test the learned policy
total_reward = 0
num_test_episodes = 3
for _ in range(num_test_episodes):
    state = env.reset()
    done = False
    while not done:
        action = np.argmax(q_table[state])
        state, reward, done, _ = env.step(action)
        total_reward += reward

average_reward = total_reward / num_test_episodes
print("Average reward over {} test episodes: {:.2f}".format(num_test_episodes, average_reward))

def human_play(env, q_table):
    state = env.reset()
    done = False
    while not done:
        env.render()  # Display the current state of the environment
        print("Your Turn:")
        action = int(input("Enter your action (0 to 224 for placing a tile, 225 to 264 for exchanging tiles): "))
        next_state, reward, done, _ = env.step(action)
        state = next_state

# Create the Scrabble environment
env = ScrabbleEnv()

# Human vs. Computer gameplay loop
while True:
    human_play(env, q_table)
    # After human plays, let the computer agent take its turn
    action = np.argmax(q_table[state])
    state, reward, done, _ = env.step(action)
    if done:
        break

# Display final scores
print("Final scores:", env.player_scores)
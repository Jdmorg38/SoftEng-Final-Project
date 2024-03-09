import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import PhotoImage
import random
import pygame


class WanderingInTheWoodsGame:
    # Initialize the game with the main window passed as an argument
    def __init__(self, game):

        self.game = game
        self.game_status = True
        self.game.title("Wandering in the Woods (K-2)")

        self.grid_size = 4  # Define the size of the grid
        self.cells = {}  # Dictionary to store cell widgets

        # Initialize the step counter
        self.steps_player1 = 0
        self.steps_player2 = 0

        self.step_counter_labels = {}
        for player in range(1, 3):
            self.step_counter_labels[player] = tk.Label(self.game, text=f"Player {player} Steps: 0")
            self.step_counter_labels[player].pack()

        self.move_speed = 1000
        self.speed_slider = tk.Scale(self.game, from_=10, to=2000, orient=tk.HORIZONTAL,
                                     label="Adjust Speed (Milliseconds)", length=500, command=self.update_speed)
        self.speed_slider.set(self.move_speed)
        self.speed_slider.pack()

        # Create a frame to hold the grid of cells
        self.grid_frame = tk.Frame(self.game)
        self.grid_frame.pack()

        pygame.mixer.init()

        # Create the grid cells and store them in the cells dictionary
        cell_size = 50
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = tk.Canvas(self.grid_frame, width=cell_size, height=cell_size)
                cell.create_rectangle(0, 0, cell_size, cell_size, fill="light green", outline="black")
                cell.grid(row=i, column=j)
                self.cells[(i, j)] = cell

        # Initialize player positions
        self.players = {}
        self.player1 = (0, 0)
        self.player2 = (self.grid_size - 1, self.grid_size - 1)

    # Update the grid to show player positions
    def player_posit(self):
        cell_size = 50
        # Clear all cells
        for cell in self.cells.values():
            cell.create_rectangle(0, 0, cell_size, cell_size, fill="light green", outline="black")
        # Place the players on the grid
        player1_cell = self.cells[self.player1]
        player1_cell.create_text(cell_size // 2, cell_size // 2, text="P1", fill="black")
        player2_cell = self.cells[self.player2]
        player2_cell.create_text(cell_size // 2, cell_size // 2, text="P2", fill="black")

    # Move a player in a random direction
    def player_move(self, player):
        directions = ([(0, 1), (1, 0), (0, -1), (-1, 0)])
        random.shuffle(directions)  # Randomize the directions to move
        for ix, jy in directions:
            new_posit = (player[0] + ix, player[1] + jy)
            if (0 <= new_posit[0] < self.grid_size) and (0 <= new_posit[1] < self.grid_size):
                if player == self.player1:
                    self.player1 = new_posit
                    self.steps_player1 += 1  # Increment the counter
                    self.step_counter_labels[1].config(text=f"Player 1 Steps: {self.steps_player1}")
                else:
                    self.player2 = new_posit
                    self.steps_player2 += 1  # Increment the counter
                    self.step_counter_labels[2].config(text=f"Player 2 Steps: {self.steps_player2}")
                break

    # Check if players have met and prompt for replay
    def meeting_check(self):
        if self.player1 == self.player2:
            self.game_status = False
            pygame.mixer.music.stop()
            met_sound = pygame.mixer.Sound("C:/Users/Justin/Software Engineeringf/announcement-sound-4-21464.mp3")
            met_sound.play()
            met_cell = self.cells[self.player1]
            cell_size = 50  # This should match the cell_size used elsewhere
            met_cell.create_rectangle(0, 0, cell_size, cell_size, fill="red", outline="black")
            user_input = messagebox.askyesno("Game Over", "Players met! Do you want to play again?")
            if user_input:
                self.play_again()
            else:
                self.game.quit()

    # Reset the game to its initial state
    def play_again(self):
        # Reset the game to the initial state
        self.background_music()
        cell_size = 50
        for position, cell in self.cells.items():
            cell.delete("all")
            cell.create_rectangle(0, 0, cell_size, cell_size, fill="light green", outline="black")
        self.player1 = (0, 0)
        self.player2 = (self.grid_size - 1, self.grid_size - 1)
        self.player_posit()
        self.moves = 0
        self.game_status = True
        self.play_game()
        self.steps_player1 = 0  # Resets the step counter when restarting the game for player 1
        self.steps_player2 = 0  # Resets the step counter when restarting the game for player 2
        self.step_counter_labels[1].config(text=f"Player 1 Steps: {self.steps_player1}")
        self.step_counter_labels[2].config(text=f"Player 2 Steps: {self.steps_player2}")

    # Prepare the game to start or restart
    def start(self):
        self.game_status = True
        self.moves = 0
        self.play_game()

    # Main game loop
    def play_game(self):
        if self.game_status:
            # Move each player and update positions
            self.player_move(self.player1)
            self.player_move(self.player2)
            self.player_posit()
            # Check if players have met
            self.meeting_check()
            self.game.after(self.move_speed, self.play_game)

    def update_speed(self, speed):
        self.move_speed = 1000  # Initial Speed
        self.move_speed = int(speed)

    def background_music(self):
        pygame.mixer.music.load(
            'C:/Users/Justin/Software Engineeringf/Wallpaperchosic.com.mp3')  # Specify your music file path
        pygame.mixer.music.play(loops=-1)


class Grade3to5(WanderingInTheWoodsGame):
    # Initial setup for the game with parameters specific to grades 3-5
    def __init__(self, game, width, height, num_players):
        super().__init__(game)  # Calls the constructor of the parent class
        self.num_players = num_players
        self.grid_width = width
        self.grid_height = height
        self.game.title("Wandering in the Woods (3-5)")
        self.players = {}  # Dictionary to keep track of players and their positions
        self.cells = {}  # Dictionary to keep track of cell widgets

    # Sets up the game grid based on specified dimensions
    def setup_grid(self):
        max_cell_size = 500
        # Calculate cell size to fit the grid within a max dimension
        cell_size = min(max_cell_size // max(self.grid_width, self.grid_height), 50)

        if self.grid_width is None or self.grid_height is None:
            messagebox.showinfo("Cancelled", "Grid size setup cancelled. Exiting game.")
            self.game.quit()
            return

        # Clear existing cells and create new ones for the updated grid
        self.cells.clear()
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Create cells for the new gri
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                cell = tk.Canvas(self.grid_frame, width=cell_size, height=cell_size)
                cell.create_rectangle(0, 0, cell_size, cell_size, fill="light green", outline="black")
                cell.grid(row=i, column=j)
                self.cells[(i, j)] = cell

    # Set up players based on user input for starting positions
    def setup_players(self):
        self.players.clear()  # Clear existing player positions

        if num_players is None:
            messagebox.showinfo("Cancelled", "Player setup cancelled.")
            return

        # Loop to get starting positions for all players
        for player in range(1, num_players + 1):
            valid_position = False
            while not valid_position:
                position_str = simpledialog.askstring("Player Position",
                                                      f"Enter starting position for Player {player} (format: x,y):")
                if position_str:
                    try:
                        x, y = map(int, position_str.split(','))
                        position = (x, y)
                        # Check if the position is within bounds and not occupied
                        if (0 <= x < self.grid_width) and (0 <= y < self.grid_height) and (
                                (x, y) not in self.players.values()):
                            self.players[player] = position
                            valid_position = True
                        else:
                            tk.messagebox.showerror("Error",
                                                    "Invalid position. Position out of grid bounds or occupied by another player.")
                    except ValueError:
                        tk.messagebox.showerror("Error", "Invalid format. Please enter coordinates in the format x,y.")
                else:
                    break  # User cancelled the dialog, break the loop
        self.player_posit()  # Update the grid to show the initial positions of players

    # Updates the display to show current player positions
    def player_posit(self):
        for posit, canvas in self.cells.items():
            canvas.delete("all")  # Clear the canvas
            canvas.create_rectangle(0, 0, 50, 50, fill="light green", outline="black")
            # Display player ID on their current position
            if posit in self.players.values():
                player_id = [key for key, value in self.players.items() if value == posit][0]
                canvas.create_text(25, 25, text=f"P{player_id}", fill="black")

    # Updates player groupings based on current positions
    def update_player_group(self):
        self.player_groups = {player: {player} for player in self.players}
        for player1, posit1 in self.players.items():
            for player2, posit2 in self.players.items():
                if player1 != player2 and posit1 == posit2:
                    self.player_groups[player1].update(self.player_groups[player2])
                    self.player_groups[player2] = self.player_groups[player1]

    # Moves players according to the game rules
    def player_move(self, player):
        if player not in self.players:
            print(f"Player ID {player} not found in players dictionary.")
            return

        self.update_player_group()

        group = self.player_groups[player]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)  # Randomize the directions to move

        for dx, dy in directions:
            valid_move = True
            new_positions = {}
            for member in group:
                current_position = self.players[member]
                new_position = (current_position[0] + dx, current_position[1] + dy)
                if 0 <= new_position[0] < self.grid_width and 0 <= new_position[1] < self.grid_height:
                    new_positions[member] = new_position
                else:
                    valid_move = False
                    break
            if valid_move:
                for member, new_position in new_positions.items():
                    self.players[member] = new_position
                break

    # Checks if players have met and handles the game state accordingly
    def meeting_check(self):
        self.update_player_group()
        all_met = len(set(frozenset(group) for group in self.player_groups.values())) == 1

        if all_met:
            self.game_status = False
            pygame.mixer.music.stop()
            for met_position in set(self.players.values()):
                met_cell = self.cells[met_position]
                met_cell.create_rectangle(0, 0, 50, 50, fill="red", outline="black")
            user_input = messagebox.askyesno("Game Over", "Players met! Do you want to play again?")
            if user_input:
                self.play_again()
            else:
                self.game.quit()
        else:
            # Highlight met positions without ending the game
            met_positions = set(pos for pos in self.players.values() if list(self.players.values()).count(pos) > 1)
            for met_position in met_positions:
                met_cell = self.cells[met_position]
                met_cell.create_rectangle(0, 0, 50, 50, fill="orange", outline="black")

    # Starts or restarts the game
    def start(self):
        self.game_status = True  # Mark game as active
        self.background_music()  # Play background music
        self.player_posit()  # Show initial player positions
        super().play_game()  # Begin the game loop

    # Main game loop to move players and check for meetings
    def play_game(self):
        if not self.game_status:
            return

        for player in self.players.keys():
            self.player_move(player)  # Move each player

        self.player_posit()  # Update positions on the grid
        self.meeting_check()  # Check for player meetings
        self.game.after(self.move_speed, self.play_game)  # Schedule next game tick

    # Handles game reset for a new round
    def play_again(self):
        # Reset game settings and start a new round
        self.background_music()
        self.setup_grid()
        self.setup_players()
        self.moves = 0
        self.game_status = True
        self.play_game()
        self.steps_player1 = 0  # Resets the step counter when restarting the game for player 1
        self.steps_player2 = 0  # Resets the step counter when restarting the game for player 2
        self.step_counter_labels[1].config(text=f"Player 1 Steps: {self.steps_player1}")
        self.step_counter_labels[2].config(text=f"Player 2 Steps: {self.steps_player2}")


class Grade6to8(Grade3to5):
    def __init__(self, game, width, height, num_players):
        super().__init__(game, width, height, num_players)

    def player_move(self, player):
        self.update_player_group()

        if player not in self.players:
            print(f"Player ID {player} not found in players dictionary.")
            return

        group = self.player_groups[player]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)  # Randomize the directions to move

        for dx, dy in directions:
            valid_move = True
            new_positions = {}
            for member in group:
                current_position = self.players[member]
                new_position = (current_position[0] + dx, current_position[1] + dy)
                if 0 <= new_position[0] < self.grid_width and 0 <= new_position[1] < self.grid_height:
                    new_positions[member] = new_position
                else:
                    valid_move = False
                    break
            if valid_move:
                for member, new_position in new_positions.items():
                    self.players[member] = new_position
                break

    def player_move_v2(self, player):
        current_posit = self.players[player]
        # next_posit = (current_posit[0] + self.)


# If this script is run directly, create the game window and start the game
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    version = simpledialog.askstring("Chose Game Version", "Enter the grade range you want to play (K-2, 3-5, or 6-8):")
    if version == "K-2":
        game = WanderingInTheWoodsGame(root)
        game.background_music()
        game.player_posit()
        root.deiconify()
        game.start()
    elif version == "3-5":
        grid_width = simpledialog.askinteger("Grid Width", "Enter grid width:", minvalue=1, maxvalue=20, parent=root)
        grid_height = simpledialog.askinteger("Grid Height", "Enter grid height:", minvalue=1, maxvalue=20, parent=root)
        num_players = simpledialog.askinteger("Number of Players", "Enter the number of players (2-4):", minvalue=2,
                                              maxvalue=4, parent=root)
        game = Grade3to5(root, grid_width, grid_height, num_players)
        game.setup_grid()
        game.setup_players()
        root.deiconify()
        game.start()
    elif version == "6-8":
        grid_width = simpledialog.askinteger("Grid Width", "Enter grid width:", minvalue=1, maxvalue=20, parent=root)
        grid_height = simpledialog.askinteger("Grid Height", "Enter grid height:", minvalue=1, maxvalue=20, parent=root)
        num_players = simpledialog.askinteger("Number of Players", "Enter the number of players (2-4):", minvalue=2,
                                              maxvalue=4, parent=root)
        game = Grade6to8(root, grid_width, grid_height, num_players)
        game.setup_grid()
        game.setup_players()
        root.deiconify()
        game.start()
    else:
        messagebox.showerror("Invalid input", "Please enter a valid input (K-2, 3-5, or 6-8)")

    root.mainloop()

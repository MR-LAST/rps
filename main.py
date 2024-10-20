import tkinter as tk
import random
import heapq
import time

# Constants
MOVES = ['rock', 'paper', 'scissors']
WIN_CONDITIONS = {
    'rock': 'scissors',
    'paper': 'rock',
    'scissors': 'paper'
}

class AStarRPS:
    def __init__(self, opponent_history):
        self.opponent_history = opponent_history

    def heuristic(self, move, opponent_last_move):
        if not opponent_last_move:
            return random.choice(MOVES)
        if WIN_CONDITIONS[move] == opponent_last_move:
            return 0
        elif WIN_CONDITIONS[opponent_last_move] == move:
            return 2
        return 1

    def a_star_search(self):
        if not self.opponent_history:
            return random.choice(MOVES)
        opponent_last_move = self.opponent_history[-1]
        priority_queue = []
        for move in MOVES:
            cost = self.heuristic(move, opponent_last_move)
            heapq.heappush(priority_queue, (cost, move))
        return heapq.heappop(priority_queue)[1]

    def make_move(self):
        return self.a_star_search()

class RockPaperScissorsGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock Paper Scissors with A* AI")
        self.geometry("400x400")
        
        self.opponent_history = []
        self.ai = AStarRPS(self.opponent_history)
        self.user_move = None
        self.result_text = tk.StringVar()
        self.countdown_text = tk.StringVar()
        
        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Rock Paper Scissors Game", font=("Arial", 18)).pack(pady=10)

        # Buttons for user input
        tk.Button(self, text="Rock", width=10, command=lambda: self.set_user_move('rock')).pack(pady=5)
        tk.Button(self, text="Paper", width=10, command=lambda: self.set_user_move('paper')).pack(pady=5)
        tk.Button(self, text="Scissors", width=10, command=lambda: self.set_user_move('scissors')).pack(pady=5)

        # Countdown label
        self.countdown_label = tk.Label(self, textvariable=self.countdown_text, font=("Arial", 24), fg="blue")
        self.countdown_label.pack(pady=10)

        # Result label
        self.result_label = tk.Label(self, textvariable=self.result_text, font=("Arial", 16))
        self.result_label.pack(pady=10)

    def set_user_move(self, move):
        self.user_move = move
        self.countdown_text.set("")
        self.result_text.set("")
        self.start_countdown()

    def start_countdown(self):
        for i in range(3, 0, -1):
            self.update_countdown(i)
            time.sleep(1)
        self.play_round()

    def update_countdown(self, count):
        self.countdown_text.set(f"Starting in {count}...")
        self.update()  # Refresh the GUI

    def play_round(self):
        # AI makes a move
        ai_move = self.ai.make_move()

        # Determine the result
        if WIN_CONDITIONS[self.user_move] == ai_move:
            result = "You win!"
        elif WIN_CONDITIONS[ai_move] == self.user_move:
            result = "AI wins!"
        else:
            result = "It's a draw!"

        # Update opponent history
        self.opponent_history.append(self.user_move)

        # Display the result and AI's move
        self.result_text.set(f"AI chose: {ai_move}. {result}")
        self.countdown_text.set("")

# Run the game
if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.mainloop()

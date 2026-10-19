import tkinter as tk

from solver import solve_history
from screen_reader import capture_screen
from board_detector import detect_tiles, remove_duplicates, organize_grid
from tile_reader import read_color, read_letter


# Display colors are independent of the website's theme.
DISPLAY_COLORS = {
    "green": "#538D4E",
    "yellow": "#B59F3B",
    "gray": "#3A3A3C",
    "empty": "#242424",
    "unknown": "#8B3A3A"
}


class WordleApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Wordle Solver")
        self.root.geometry("430x780")
        self.root.resizable(False, False)
        self.root.configure(bg="#181818")
        self.root.attributes("-topmost", True)

        self.status = tk.StringVar(value="Ready to scan.")

        self.board = [
            [("", "empty") for _ in range(5)]
            for _ in range(6)
        ]

        title = tk.Label(
            root,
            text="WORDLE SOLVER",
            font=("Arial", 20, "bold"),
            bg="#181818",
            fg="white"
        )
        title.pack(pady=(22, 5))

        subtitle = tk.Label(
            root,
            text="Automatic board reader",
            font=("Arial", 10),
            bg="#181818",
            fg="#AAAAAA"
        )
        subtitle.pack(pady=(0, 18))

        self.canvas = tk.Canvas(
            root,
            width=370,
            height=440,
            bg="#181818",
            highlightthickness=0
        )
        self.canvas.pack()

        self.draw_board()

        self.scan_button = tk.Button(
            root,
            text="SCAN WORDLE",
            font=("Arial", 12, "bold"),
            bg="#538D4E",
            fg="white",
            activebackground="#467A42",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.start_scan
        )
        self.scan_button.pack(
            fill="x",
            padx=35,
            pady=(10, 12),
            ipady=9
        )

        self.status_label = tk.Label(
            root,
            textvariable=self.status,
            font=("Arial", 10),
            bg="#181818",
            fg="#CCCCCC",
            wraplength=360
        )
        self.status_label.pack()

        # Solver results
        self.suggestion = tk.StringVar(value="—")
        self.remaining_count = tk.StringVar(value="—")
        self.solver_status = tk.StringVar(value="Scan the board to begin.")

        solver_frame = tk.Frame(
            root,
            bg="#242424",
            padx=15,
            pady=12
        )

        solver_frame.pack(
            fill="x",
            padx=20,
            pady=(10, 15)
        )

        tk.Label(
            solver_frame,
            text="RECOMMENDED NEXT GUESS",
            font=("Arial", 9, "bold"),
            bg="#242424",
            fg="#AAAAAA"
        ).pack()

        tk.Label(
            solver_frame,
            textvariable=self.suggestion,
            font=("Consolas", 25, "bold"),
            bg="#242424",
            fg="#FFFFFF"
        ).pack(pady=5)

        tk.Label(
            solver_frame,
            textvariable=self.remaining_count,
            font=("Arial", 11),
            bg="#242424",
            fg="#CCCCCC"
        ).pack()

        tk.Label(
            solver_frame,
            textvariable=self.solver_status,
            font=("Arial", 9),
            bg="#242424",
            fg="#AAAAAA",
            wraplength=350
        ).pack(pady=(5, 0))

    def get_guess_history(self):

        symbols = {
            "green": "G",
            "yellow": "Y",
            "gray": "X"
        }

        history = []
        empty_row_found = False

        for row_number, row in enumerate(self.board, start=1):

            colors = [color for letter, color in row]

            # A completely empty row is fine.
            if all(color == "empty" for color in colors):
                empty_row_found = True
                continue

            # Completed rows cannot appear after an empty row.
            if empty_row_found:
                raise ValueError(
                    f"Unexpected tiles after empty row {row_number - 1}."
                )

            # Never send partially submitted or unknown feedback.
            if any(color not in symbols for color in colors):
                raise ValueError(
                    f"Row {row_number} contains incomplete or unknown feedback."
                )

            letters = [letter for letter, color in row]

            # Reject missing or uncertain OCR results.
            if any(
                    len(letter) != 1 or
                    letter.upper() not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    for letter in letters
            ):
                raise ValueError(
                    f"Row {row_number} contains an unreadable letter."
                )

            guess = "".join(letters).lower()

            feedback = "".join(
                symbols[color]
                for color in colors
            )

            history.append((guess, feedback))

        return history

    def draw_board(self):

        self.canvas.delete("all")

        tile_size = 62
        gap = 9

        for row_index, row in enumerate(self.board):

            for col_index, (letter, color) in enumerate(row):

                x = 8 + col_index * (tile_size + gap)
                y = 7 + row_index * (tile_size + gap)

                fill = DISPLAY_COLORS.get(
                    color,
                    DISPLAY_COLORS["unknown"]
                )

                self.canvas.create_rectangle(
                    x,
                    y,
                    x + tile_size,
                    y + tile_size,
                    fill=fill,
                    outline="#565656",
                    width=1
                )

                self.canvas.create_text(
                    x + tile_size / 2,
                    y + tile_size / 2,
                    text=letter,
                    fill="white",
                    font=("Arial", 23, "bold")
                )

    def start_scan(self):

        self.status.set("Preparing to capture Wordle...")
        self.scan_button.config(state="disabled")

        # Hide this application so it cannot cover the board.
        self.root.iconify()

        # Give the operating system time to minimize the window.
        self.root.after(500, self.scan_board)

    def scan_board(self):
        try:
            image = capture_screen()

            tiles = detect_tiles(image)
            tiles = remove_duplicates(tiles)

            if len(tiles) != 30:
                raise ValueError(
                    f"Expected 30 tiles, detected {len(tiles)}."
                )

            grid = organize_grid(tiles)

            new_board = []

            for row in grid:

                new_row = []

                for tile in row:

                    color = read_color(image, tile)
                    letter = read_letter(image, tile, color)

                    new_row.append((letter, color))

                new_board.append(new_row)

            self.board = new_board
            self.draw_board()

            # Convert the detected board into solver-compatible feedback.
            history = self.get_guess_history()

            print("\nGuess history:", history)

            # Run the existing solver.
            result = solve_history(history)

            remaining = result["remaining"]

            self.remaining_count.set(
                f"{len(remaining)} possible answers remaining"
            )

            if result["solved"]:

                self.suggestion.set("SOLVED!")
                self.solver_status.set("Wordle completed successfully.")

            elif not remaining:

                self.suggestion.set("—")
                self.solver_status.set(
                    "No possible answers remain. Check OCR and feedback."
                )

            else:

                self.suggestion.set(
                    result["suggestion"].upper()
                )

                if result["score"] is not None:
                    self.solver_status.set(
                        f"Guess score: {result['score']}"
                    )
                else:
                    self.solver_status.set("Ready for your next guess.")

            # Print detailed results for debugging.
            print("\nDetected board:")

            for row in self.board:
                print(row)

            has_unknown = any(
                color == "unknown" or letter == "?"
                for row in self.board
                for letter, color in row
            )

            if has_unknown:
                self.status.set(
                    "Scan complete, but some tiles need verification."
                )
            else:
                self.status.set("Board scanned successfully!")


        except Exception as error:
            self.suggestion.set("—")

            self.remaining_count.set("—")

            self.solver_status.set("Scan results could not be processed.")

        finally:

            # Restore the application even if scanning fails.
            self.root.deiconify()
            self.root.lift()

            self.scan_button.config(state="normal")


if __name__ == "__main__":

    root = tk.Tk()
    app = WordleApp(root)
    root.mainloop()
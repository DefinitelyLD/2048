import colors as col
import tkinter
import random

class Game(tkinter.Frame):
    def __init__(self):
        tkinter.Frame.__init__(self)
        self.grid()
        self.master.title("2048 Game")

        self.main_grid = tkinter.Frame(self, bg = col.GRID_COLOR, width=800, height=800)
        self.main_grid.grid(pady=(100,0))

        self.init_GUI()
        self.start_game()

        #Key binds
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)
        self.master.bind("<Return>", self.restart_game)

        self.mainloop()

    def init_GUI(self):
        #create grid
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tkinter.Frame(self.main_grid, bg = col.EMPTY_CELL_COLOR, bd=5, width=200, height=200)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tkinter.Label(self.main_grid, bg=col.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        #create score
        score_frame = tkinter.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor="center")
        tkinter.Label(
            score_frame,
            text="Score",
            font=col.SCORE_LABEL_FONT
        ).grid(row=0)
        self.score_label = tkinter.Label(score_frame, text="0", font=col.SCORE_FONT)
        self.score_label.grid(row=1)


    def start_game(self):
        #create matrix
        self.matrix = [[0] * 4 for k in range(4)]

        #spawn 2 random starting cells
        row = random.randint(0,3)
        column = random.randint(0,3)
        self.matrix[row][column] = 2
        self.cells[row][column]["frame"].configure(bg = col.TILE_COLORS[2])
        self.cells[row][column]["number"].configure(
            bg=col.TILE_COLORS[2],
            fg=col.NUMBER_COLORS[2],
            font= col.CELL_NUMBER_FONT,
            text="2"
        )
        while(self.matrix[row][column] != 0):
            row = random.randint(0, 3)
            column = random.randint(0, 3)
        self.matrix[row][column] = 2
        self.cells[row][column]["frame"].configure(bg=col.TILE_COLORS[2])
        self.cells[row][column]["number"].configure(
            bg=col.TILE_COLORS[2],
            fg=col.NUMBER_COLORS[2],
            font=col.CELL_NUMBER_FONT,
            text="2"
        )

        self.score = 0

    def stack_tiles(self):
        new_matrix = [[0] * 4 for k in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine_tiles(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2 # result * 2
                    self.matrix[i][j + 1] = 0 #clear combined
                    self.score += self.matrix[i][j] #add score

    def reverse_matrix(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append((self.matrix[i][3-j]))
        self.matrix = new_matrix


    def transpose_matrix(self):
        new_matrix = [[0] * 4 for k in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    #Add 2 tiles after each move:
    def add_new_tile(self):
        if any(0 in row for row in self.matrix):
            row = random.randint(0, 3)
            column = random.randint(0, 3)
            while (self.matrix[row][column] != 0):
                row = random.randint(0, 3)
                column = random.randint(0, 3)
            self.matrix[row][column] = random.choice([2, 4])

    #Updating GUI
    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=col.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=col.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=col.TILE_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=col.TILE_COLORS[cell_value],
                        fg=col.NUMBER_COLORS[cell_value],
                        font=col.CELL_NUMBER_FONT,
                        text=str(cell_value)
                )
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    #Implementing controls
    def move_left(self, event):
        self.stack_tiles()
        self.combine_tiles()
        self.stack_tiles()
        self.add_new_tile()
        self.update_GUI()
        self.gg()

    def move_right(self, event):
        self.reverse_matrix()
        self.stack_tiles()
        self.combine_tiles()
        self.stack_tiles()
        self.reverse_matrix()
        self.add_new_tile()
        self.update_GUI()
        self.gg()

    def move_up(self, event):
        self.transpose_matrix()
        self.stack_tiles()
        self.combine_tiles()
        self.stack_tiles()
        self.transpose_matrix()
        self.add_new_tile()
        self.update_GUI()
        self.gg()

    def move_down(self, event):
        self.transpose_matrix()
        self.reverse_matrix()
        self.stack_tiles()
        self.combine_tiles()
        self.stack_tiles()
        self.reverse_matrix()
        self.transpose_matrix()
        self.add_new_tile()
        self.update_GUI()
        self.gg()


    def restart_game(self, event):
        self.create_frame("Game over!(Press Return)", col.LOSE_BG, col.GRID_COLOR)
        self.init_GUI()
        self.start_game()

    #check if game is over
    def gg(self):
        if any(2048 in row for row in self.matrix):
            self.create_frame("You win!(Press Return)", col.WIN_BG, col.GAME_OVER_FONT_COLOR)
        elif not any(0 in row for row in self.matrix) and not self.any_vertical_move_left() and not self.any_vertical_move_left():
            self.create_frame("Game over!(Press Return)", col.LOSE_BG, col.GAME_OVER_FONT_COLOR)

    def create_frame(self, text, bg_color, text_color):
        frame = tkinter.Frame(self.main_grid)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tkinter.Label(
            frame,
            text= text,
            bg= bg_color,
            fg= text_color,
            font=col.GAME_OVER_FONT
        ).pack()

    def any_horizontal_move_left(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False

    def any_vertical_move_left(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False

def main():
    Game()

if __name__ == "__main__":
    main()
from tkinter import *
import colors as co
import random as r

class Game_2048():
    def __init__(self, height, width, grid_size):
        self.height = height
        self.width = width
        self.grid_size = grid_size
        self.setup()
    
    def setup(self):
        self.window = Tk()
        self.window.title("2048")

        # binding keys
        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)
        self.window.bind('<Down>', self.downKey)
        self.window.bind('<Up>', self.upKey)

        self.main_canvas = Canvas(self.window, height = self.height, width = self.width, bd = 3, bg = co.MAIN_CANVAS)
        self.main_canvas.pack()

        self.main_grid = Frame(self.main_canvas, bg = co.GRID_COLOR, bd = 3)
        self.main_grid.grid(pady = (80, 0))
        self.createGrid()

        self.score_frame = Frame(self.main_canvas, bg = co.MAIN_CANVAS)
        self.score_frame.place(relx = 0, rely = 0, relheight = 77/545, relwidth = 1)

        self.score_title_label = Label(self.score_frame,  text = 'Score: ', bg = co.MAIN_CANVAS, fg = co.GRID_COLOR, font = co.SCORE_LABEL_FONT, anchor = 'e')
        self.score_title_label.place(relx = 0, rely = 0, relheight = 1, relwidth = 0.5)

        self.score_label = Label(self.score_frame,  text = '0', bg = co.MAIN_CANVAS, fg = co.GRID_COLOR, font = co.SCORE_LABEL_FONT,  anchor = 'w')
        self.score_label.place(relx = 0.5, rely = 0, relheight = 1, relwidth = 0.5)

    def createGrid(self):
        self.cell_list = []
        for r in range(self.grid_size):
            row = []
            for c in range(self.grid_size):
                self.cell_frame = Frame(self.main_grid, bg = co.EMPTY_CELL_COLOR, height = self.height / self.grid_size, width = self.width / self.grid_size)
                self.cell_frame.grid(row = r, column = c, padx = 3, pady = 3)

                self.cell_number = Label(self.main_grid, bg = co.EMPTY_CELL_COLOR)
                self.cell_number.grid(row = r, column = c)

                cell_data = {"frame": self.cell_frame, "number": self.cell_number}
                row.append(cell_data)

            self.cell_list.append(row)

        self.startGame()

    # this function is responsible for creating the game
    def startGame(self):
        self.added_score = 0
        self.matrix = [[0] * self.grid_size for i in range(self.grid_size)]
        
        row = r.randint(0, self.grid_size - 1)
        column = r.randint(0, self.grid_size - 1)

        self.matrix[row][column] = 2
        self.cell_list[row][column]["frame"].configure(bg = co.CELL_COLORS[2])
        self.cell_list[row][column]["number"].configure(text = "2", bg = co.CELL_COLORS[2], fg = co.CELL_NUMBER_COLORS[2], font = co.CELL_NUMBER_FONTS[2])

        while self.matrix[row][column] != 0:
            row = r.randint(0, self.grid_size - 1)
            column = r.randint(0, self.grid_size - 1)

        self.matrix[row][column] = 2
        self.cell_list[row][column]["frame"].configure(bg = co.CELL_COLORS[2])
        self.cell_list[row][column]["number"].configure(text = "2", bg = co.CELL_COLORS[2], fg = co.CELL_NUMBER_COLORS[2], font = co.CELL_NUMBER_FONTS[2])

    def stack(self):
        new_matrix = [[0] * self.grid_size for i in range(self.grid_size)]

        for i in range(self.grid_size):
            fill_position = 0
            for j in range(self.grid_size):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
                
        self.matrix = new_matrix.copy()

    def combine(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                if self.matrix[i][j] != 0 and self.matrix[i][j+1] == self.matrix[i][j]:
                    self.matrix[i][j] = self.matrix[i][j] + self.matrix[i][j+1]
                    self.matrix[i][j+1] = 0
                    self.added_score += self.matrix[i][j]
                    

    def reverse(self):
        new_matrix = [[0] * self.grid_size for i in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                new_matrix[i][j] = self.matrix[i][(self.grid_size - 1) - j]

        self.matrix = new_matrix

    def transpose(self):
        new_matrix = [[0] * self.grid_size for i in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                new_matrix[i][j] = self.matrix[j][i]
    
        self.matrix = new_matrix
        
    def leftKey(self, dummy):
        self.stack()
        self.combine()
        self.stack()
        self.addNewTile()
        self.updateUI()
        self.gameOver()

    def rightKey(self, dummy):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.addNewTile()
        self.updateUI()
        self.gameOver()

    def upKey(self, dummy):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.addNewTile()
        self.updateUI()
        self.gameOver()

    def downKey(self, dummy):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.addNewTile()
        self.updateUI()
        self.gameOver()

    def updateUI(self):
        for row in range(self.grid_size):
            for column in range(self.grid_size):
                cell_value = self.matrix[row][column]
                if cell_value == 0:
                    self.cell_list[row][column]["frame"].configure(bg = co.EMPTY_CELL_COLOR)
                    self.cell_list[row][column]["number"].configure(text = '', bg = co.EMPTY_CELL_COLOR)
                else:
                    self.cell_list[row][column]["frame"].configure(bg = co.CELL_COLORS[cell_value])
                    self.cell_list[row][column]["number"].configure(text = str(cell_value), bg = co.CELL_COLORS[cell_value], fg = co.CELL_NUMBER_COLORS[cell_value], font = co.CELL_NUMBER_FONTS[cell_value])

        self.score_label.configure(text = str(self.added_score))

    def addNewTile(self):
        column = r.randint(0, self.grid_size - 1)
        row = r.randint(0, self.grid_size - 1)

        while self.matrix[row][column] != 0:
            row = r.randint(0, self.grid_size - 1)
            column = r.randint(0, self.grid_size - 1)

        self.matrix[row][column] = r.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])

    def zeroExist(self):
        for i in range(self.grid_size):
            if 0 in self.matrix[i]:
                return True
        return False

    def horizontalMoveExists(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size - 1):
                if self.matrix[r][c] == self.matrix[r][c + 1]:
                    return True
        return False

    def verticalMoveExists(self):
        for r in range(self.grid_size - 1):
            for c in range(self.grid_size):
                if self.matrix[r][c] == self.matrix[r + 1][c]:
                    return True
        return False

    def gameOver(self):
        if (not self.zeroExist()) and (not self.horizontalMoveExists()) and (not self.verticalMoveExists()):
            print("game over")

    def mainloop(self):
        self.window.mainloop()
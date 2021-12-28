class LifeGeneration:
    # fill in this class yourself
    def __init__(self, state=[]):
        self.state = state

    def __str__(self):
        ret = ""

    def width(self):    #determine the width of the board
        return len(self.state[0])

    def height(self):   #determine the height of the board
        return len(self.state)

    def is_alive(self,x,y): #determines if a specific cell is dead or alive
        if self.state[y][x]:
            return True
        else:
            return False

    def neighbours(self,x,y): #returns an array of x and y coordinates of neighbour cells
        maxy = self.height() - 1
        maxx = self.width() - 1
        states = []
        n = [[x2, y2] for x2 in range(x - 1, x + 2) for y2 in range(y - 1, y + 2) if (-1 < x <= maxx and -1 < y <= maxy and (x != x2 or y != y2) and (0 <= x2 <= maxx) and (0 <= y2 <= maxy))]
        for i in range(0,len(n)):
            x = n[i][0]
            y = n[i][1]
            states.append(self.is_alive(x,y))
        return states

    def will_stay_alive(self,x,y):
        neighbours = self.neighbours(x,y).count(True)
        if neighbours == 2 or neighbours == 3:
            return True
        else:
            return False

    def will_become_alive(self,x,y):
        neighbours = self.neighbours(x, y).count(True)
        if neighbours == 3:
            return True
        else:
            return False

    def next_generation(self):
        newgen = []
        for y in range(0,self.height()):
            newrow = []
            for x in range(0,self.width()):
                if self.is_alive(x,y):
                    newrow.append(self.will_stay_alive(x,y))
                else:
                    newrow.append(self.will_become_alive(x,y))
            newgen.append(newrow)
        return LifeGeneration(newgen)

    def is_all_dead(self):
        nelements = sum([len(row) for row in self.state])
        if self.state.count(False) == nelements:
            return True
        else:
            return False

    def board(self):
        return self.state


class LifeHistory:
    # fill in this class yourself
    def __init__(self, initial_gen=LifeGeneration):
        self.history = [initial_gen]

    def __str__(self):
        rez = ""
        boards = self.all_boards()
        for i in range(0,len(boards)-1):
            res = f"{i}"
            res += "\n"
            board = boards[i]
            res += printboard(board)
            rez += res
            rez += "\n =========== \n"
        return rez

    def printboard(self,board):
        ret = ""
        nr_rows = len(board)
        for j in range(nr_rows):
            ret += row_to_str(board[j])
            ret += "\n"
        return ret

    def row_to_str(row):
        return "".join(['x' if v else ' ' for v in row])

    def play_step(self):
        newgen = LifeGeneration(self.history[-1].next_generation().board())
        self.history.append(newgen)

    def nr_generations(self):
        return len(self.history)

    def get_generation(self, i):
        if i <= self.nr_generations():
            return self.history[i]

    def flat(self, arr): #expects a 2D array, returns a single D arr
        newarr = []
        for i in range(0, len(arr)-1):
            for j in range(0,len(arr[i])-1):
                newarr.append(arr[i][j])
        return newarr

    def dies_out(self):
        arr = self.flat(self.history[-1].board())
        if True in arr:
            return False
        else:
            return True

    def is_identical_to(self, gen):
        currboard = self.history[-1].board()        #take the current board
        print(self.printboard(currboard))
        print(self.printboard(gen))
        strlast = "".join(map(str, self.flat(currboard)))
        strcomp = "".join(map(str, self.flat(gen)))
        print(strlast==strcomp)
        if strlast != strcomp:
            return False
        else:
            return True

    def period(self): #take current generation as n, then determine is there is a p, identical to n. Then self.nr_generaion
        currboard = self.history[-1].board()        #take the current board
        nboards = len(self.history)
        print("Aantal boarden",nboards)
        for i in range(nboards-2,0,-1):
            if nboards > 2:     #hierna kijken!!!
                print(i)
                focusboard = self.get_generation(i).board()
                # print(self.printboard(focusboard))
                # print(self.printboard(currboard))
                test = self.is_identical_to(focusboard)
                if test == True:
                    return self.nr_generations()-i-1

        return None

    def play_out(self, max_steps):
        continuing = True
        counter = 0
        while self.nr_generations() < max_steps and continuing:
            counter += 1
            print("Dit is generatie", counter)
            if self.period() != None or self.dies_out() == True:
                continuing = False
            self.play_step()


    def all_boards(self):
        boards = []
        for i in range(0,self.nr_generations()):
            boards.append(self.history[i].board())
        return boards



def read_test_boards_from_file(filename):
    boards_str = open(filename).read().split("=========\n")
    return [to_bool_matrix(board) for board in boards_str]

def to_bool_matrix(s):
    res = []
    for line in s.splitlines():
        row = []
        for c in line:
            row.append(c == "x")
        res.append(row)
    return res

def row_to_str(row):
    return "".join(['x' if v else ' ' for v in row])

def printboard(gen):
    res = ""
    board = gen.board()
    nr_rows = len(board)
    for j in range(nr_rows):
        res += row_to_str(board[j])
        res += "\n"
    return res
input1 = read_test_boards_from_file("tests/period14.txt")

l = LifeHistory(LifeGeneration(input1[0]))
l.play_out(100)
print("Periode", l.period())
print("Het aantal generaties: ", l.nr_generations())
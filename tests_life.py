import unittest

from life import LifeHistory, LifeGeneration


class TestLife(unittest.TestCase):

    def test_next_gen(self):
        l = LifeGeneration([[True, True], [True, True], [False, True]])
        self.assertEqual(l.next_generation().board(), [[True, True], [False, False], [True, True]])
        # check no change in original generation
        self.assertEqual(l.board(),[[True, True], [True, True], [False, True]])

        l = LifeGeneration([[False, True, False], [True, False, True], [False, False, True]])
        self.assertEqual(l.next_generation().board(), [[False, True, False], [False, False, True], [False, True, False]])
        # check no change in original generation
        self.assertEqual(l.board(), [[False, True, False], [True, False, True], [False, False, True]])


    def test_input1(self):
        history = LifeHistory(LifeGeneration(input1[0]))
        history.play_out(100)
        self.assertEqual(history.nr_generations(), 26)
        self.assertTrue(history.dies_out())
        self.assertEqual(history.period(), None)
        self.equal_boards(history.all_boards(), input1)

    def test_input2(self):
        history = LifeHistory(LifeGeneration(input2[0]))
        history.play_out(100)
        self.assertEqual(history.nr_generations(), 5)
        self.assertTrue(not history.dies_out())
        self.assertEqual(history.period(), 1)
        self.equal_boards(history.all_boards(), input2)

    def test_input3(self):
        history = LifeHistory(LifeGeneration(input3[0]))
        history.play_out(100)
        self.assertEqual(history.nr_generations(), 12)
        self.assertTrue(not history.dies_out())
        self.assertEqual(history.period(), 1)
        self.equal_boards(history.all_boards(), input3)

    def test_stable(self):
        history = LifeHistory(LifeGeneration(stable[0]))
        history.play_out(100)
        self.assertEqual(history.nr_generations(), 23)
        self.assertTrue(not history.dies_out())
        self.assertEqual(history.period(), 1)
        self.equal_boards(history.all_boards(), stable)

    def test_dies(self):
        history = LifeHistory(LifeGeneration(dies[0]))
        history.play_out(100)
        self.assertEqual(history.nr_generations(), 12)
        self.assertTrue(history.dies_out())
        self.assertEqual(history.period(), None)
        self.equal_boards(history.all_boards(), dies)

    def test_period2(self):
        history = LifeHistory(LifeGeneration(period2[0]))
        history.play_out(100)
        self.assertEqual(history.nr_generations(), 8)
        self.assertTrue(not history.dies_out())
        self.assertEqual(history.period(), 2)
        self.equal_boards(history.all_boards(), period2)

    def test_period14(self):
        history = LifeHistory(LifeGeneration(period14[0]))
        history.play_out(100)
        #self.assertEqual(history.nr_generations(), 15)
        self.assertTrue(not history.dies_out())
        self.assertEqual(history.period(), 14)
        #self.equal_boards(history.all_boards(), period14)

    def equal_boards(self, got_boards, want_boards):
        self.assertTrue(got_boards == want_boards, boards_side_by_side(want_boards, got_boards))


def row_to_str(row):
    return "".join(['x' if v else ' ' for v in row])


def board_side_by_side(want_board, got_board):
    res = ""
    nr_rows = len(want_board)
    if len(got_board) != nr_rows:
        res += "Want %d rows, got %d rows" % (len(want_board), len(got_board))
    for j in range(nr_rows):
        res += "|"
        res += row_to_str(want_board[j])
        res += "|"
        res += row_to_str(got_board[j])
        res += "|"
        res += "\n"
    return res


def boards_side_by_side(want_boards, got_boards):
    if len(want_boards) != len(got_boards):
        return "Expected %d boards, got %d boards" % (len(want_boards), len(got_boards))
    nr_boards = len(want_boards)
    if want_boards != got_boards:
        res = "\n|%9s|%9s|\n" % ("Want", "Got")
        res += "==========|==========\n"
        for i in range(nr_boards):
            res += board_side_by_side(want_boards[i], got_boards[i])
            if want_boards[i] != got_boards[i]:
                return res
            res += "==========|==========\n"
        return res
    else:
        return ""


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


input1 = read_test_boards_from_file("tests/input1.txt")
input2 = read_test_boards_from_file("tests/input2.txt")
input3 = read_test_boards_from_file("tests/input3.txt")
stable = read_test_boards_from_file("tests/stable.txt")
dies = read_test_boards_from_file("tests/dies.txt")
period2 = read_test_boards_from_file("tests/period2.txt")
period14 = read_test_boards_from_file("tests/period14.txt")

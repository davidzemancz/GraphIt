import copy

class Matrix:
    def __init__(self, matrix = []):
        self.__array = matrix

    @property
    def array(self):
       return self.__array

    @array.setter
    def array(self, value):
       self.__array = value
        
    def get_count_cols(self):
        return len(self.array[0]) if len(self.array) > 0 else 0

    def get_count_rows(self):
        return self.array.count()

    def load(self, input): # m.load "(1,2,3;4,5,6;7,8,9)"
        matrix = []

        input = input[1:-1]

        rows = input.split(";")
        for row in rows:
            values = row.split(",")
            matrix_row = []
            for value in values:
                matrix_row.append(float(value))
            matrix.append(matrix_row)

        self.array.clear()
        self.array = matrix

        return self

    def REF(self): # m.ref "(1,2,3;4,5,6;7,8,9)"
        matrix = self.array     
       
        r = 0
        for i in range(len(matrix)): # Prochazim radky
            pivot = matrix[i][r]

            i_next = i + 1
            while pivot == 0 and i_next < len(matrix): # Pokud je na pivotu 0, prohodim aktualni a nasledujci radek
                matrix[i],matrix[i_next] = matrix[i_next],matrix[i_next]
                i_next += 1

            for j in range(i + 1, len(matrix)): # Prochazim radky po aktualnim radkem
                ratio = matrix[j][r] / pivot
                for k in range(len(matrix[i])): # Prochazim sloupce
                    matrix[j][k] = matrix[j][k] - ratio * matrix[i][k] 
            r += 1

        return self

    def RREF(self): # m.rref "(1,2,3;4,5,6;7,8,9)"
        matrix = self.array
       
        r = 0
        for i in range(len(matrix)): # Prochazim radky
            pivot = matrix[i][r]

            i_next = i + 1
            while pivot == 0 and i_next < len(matrix): # Pokud je na pivotu 0, prohodim aktualni a nasledujci radek
                matrix[i],matrix[i_next] = matrix[i_next],matrix[i_next]
                pivot = matrix[i][r]
                i_next += 1

            if pivot == 0:
                break

            for k in range(len(matrix[i])): # Na pozici aktulniho pivota dam 1
                matrix[i][k] = matrix[i][k] / pivot

            pivot = matrix[i][r] # = 1
            if pivot != 1:
                raise Exception("Pivot is not one")

            for j in range(len(matrix)): # Prochazim vsechny radky krom aktualniho
                if j == i:
                    continue
                ratio = matrix[j][r] / pivot
                for k in range(len(matrix[i])): # Prochazim sloupce
                    matrix[j][k] = matrix[j][k] - ratio * matrix[i][k] 
            r += 1

        return self

    def can_multiply(self, matrix: Matrix, dir = "l"):
        if dir == "l":
            return self.get_count_cols() == matrix.get_count_rows()
        if dir == "r":
            return matrix.get_count_cols() == self.get_count_rows()

    def multiply_left(self, matrix: Matrix):
        return self

    def multiply_right(self, matrix: Matrix):
        return self

    def add(self, matrix: Matrix):
        for i in range(self.array):
            for j in range(self.array[i]):
                self.array[i, j] += matrix.get_value(i, j)
        return self

    def get_value(self, row, column):
        if len(self.array) >= row:
            if len(self.array[row]) >= column:
                return self.array[row][column]
        return 0

    def transpose(self):
        matrix = self.array
        
        for i in range(self.get_count_cols()):
            new_row = []
            for j in range(self.get_count_rows()):
                new_row.append(matrix[j][i])
            new_matrix.append(new_row)
           
        self.matrix = new_matrix
        return self

    def inverse(self):
        return self

    def rank(self):
        return 0

    def clone(self):
        return copy.deepcopy(self)
    


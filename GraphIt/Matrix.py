class Matrix:
    def __init__(self, matrix = [[]]):
        self.set_matrix(matrix)

    def get_matrix(self):
        return self.__matrix

    def set_matrix(self, matrix):
        self.__matrix = matrix

    def load(self, input): # "(1,2,3;4,5,6;7,8,9)"
        matrix = []

        input = input[1:-1]

        rows = input.split(";")
        for row in rows:
            values = row.split(",")
            matrix_row = []
            for value in values:
                matrix_row.append(float(value))
            matrix.append(matrix_row)

        self.set_matrix(matrix)

        return self

    def REF(self):
        matrix = self.get_matrix() 
        
        # Seradim radky podle pivotu
        r = 0
        for i in range(len(matrix)): # Prochazim radky
            # TODO
            r += 1

        r = 0
        for i in range(len(matrix)): # Prochazim radky
            pivot = matrix[i][r]
            for j in range(i + 1, len(matrix)): # Prochazim radky po aktualnim radkem
                ratio = matrix[j][r] / pivot
                for k in range(len(matrix[i])): # Prochazim sloupce
                    matrix[j][k] = matrix[j][k] - ratio * matrix[i][k] 
            r += 1

        return self

    def RREF():
        return self

    def multiply_left():
        return self

    def multiply_right():
        return self

    def add():
        return self

    def subtract():
        return self

    def transpose(self):
        matrix = self.get_matrix()
        
        rows_count = len(matrix) # Pocet radku
        if rows_count == 0:
           return self

        columns_count = len(matrix[0]) # Delka radku = pocet sloupcu
        new_matrix = []

        for i in range(columns_count):
            new_row = []
            for j in range(rows_count):
                new_row.append(matrix[j][i])
            new_matrix.append(new_row)
           
        self.set_matrix(new_matrix)
        return self

    def inverse():
        return self

    def rank():
        return 0

    def clone():
        return Matrix(get_arr())
    


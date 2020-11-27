class Matrix:
    def __init__(self, matrix = [[]]):
        self.matrix = matrix

    @property
    def matrix(self):
       return self.__matrix

    @matrix.setter
    def matrix(self, value):
       self.__matrix = value
        

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

        self.matrix = matrix

        return self

    def REF(self): # m.ref "(1,2,3;4,5,6;7,8,9)"
        matrix = self.matrix     
       
        r = 0
        for i in range(len(matrix)): # Prochazim radky
            pivot = matrix[i][r]

            i_next = i + 1
            while pivot == 0 and i_next < len(matrix): # Pokud je na pivotu 0, prohodim aktualni a nasledujci radek
                matrix[i],matrix[i_next] = matrix[i_next],matrix[i_next]
                i_next += 1

            for j in range(len(matrix)): # Prochazim radky po aktualnim radkem
                ratio = matrix[j][r] / pivot
                for k in range(len(matrix[i])): # Prochazim sloupce
                    matrix[j][k] = matrix[j][k] - ratio * matrix[i][k] 
            r += 1

        return self

    def RREF(self): # m.rref "(1,2,3;4,5,6;7,8,9)"
        matrix = self.matrix
       
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

    def multiply_left(self):
        return self

    def multiply_right(self):
        return self

    def add(self):
        return self

    def subtract(self):
        return self

    def transpose(self):
        matrix = self.matrix
        
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
           
        self.matrix = new_matrix
        return self

    def inverse(self):
        return self

    def rank(self):
        return 0

    def clone(self):
        return Matrix(get_arr())
    


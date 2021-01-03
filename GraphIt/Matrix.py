import copy
import Matrix

class Matrix:
    def __init__(self, matrix = [], columns = 0, rows = 0):
        self.array = matrix

        if columns > 0 and rows > 0:
            for i in range(rows):
                row = []
                for j in range(columns):
                    row.append(0)
                self.array.append(row)

    @property
    def array(self):
       return self.__array

    @array.setter
    def array(self, value):
       self.__array = value
        
    def get_count_cols(self):
        return len(self.array[0]) if len(self.array) > 0 else 0

    def get_count_rows(self):
        return len(self.array)

    def load(self, input): # m.load "{1,2,3;4,5,6;7,8,9}"
        """
        Nacteni matice ze vstupu
        """
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
        """
        Uprava matice do REF
        """
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

            if r + 1 < len(matrix[i]):
                r += 1

        return self

    def RREF(self): # m.rref "(1,2,3;4,5,6;7,8,9)"
        """
        Uprava matice do RREF
        """
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
            
            if r + 1 < len(matrix[i]):
                r += 1

        return self

    def can_multiply(self, matrix: Matrix, dir = "l"):
        """
        Lze matice nasobit
        ---------------------------------------------------------
        Dir(ection)
        > dir = "l" ... nasobit zleva
        > dir = "r" ... nasobit zprava
        """
        if dir == "l":
            return self.get_count_rows() == matrix.get_count_cols()
        if dir == "r":
            return self.get_count_cols() == matrix.get_count_rows()

    def multiply_left(self, matrix: Matrix): # m.ml "(1,3;5,2;2,4)";"(1,1,3;3,2,4)"  , m.ml "(1,1,3;3,2,4)";"(1,3;5,2;2,4)"
        """
        Nasobeni matici zleva
        """

        if not self.can_multiply(matrix, "l"):
            raise Exception("Invalid matrix size")

        self.transpose()
        result = Matrix([], self.get_count_rows(), matrix.get_count_rows())

        for i in range(len(matrix.array)): # Radky leve matice
           for j in range(len(self.array)): # Sloupce prave matice
               val = 0
               for k in range(len(matrix.array[i])): # Sloupce leve matice
                   val += matrix.array[i][k] * self.array[j][k]
               result.array[i][j] = val

        self.transpose()

        self.array = result.array

        return self

    def multiply_right(self, matrix: Matrix): # [1,2;1,2]*[1;2]
        """
        Nasobeni matici zprava
        """
        temp = []
        temp.extend(self.array)
        self.array.clear()
        self.array.extend(matrix.array)
        matrix.array.clear()
        matrix.array.extend(temp)

        return self.multiply_left(matrix)

    def add(self, matrix: Matrix):
        """
        Secteni dvou matic
        """
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                self.array[i][j] += matrix.get_value(i, j)
        return self

    def substract(self, matrix: Matrix):
        """
        Odecteni dvou matic
        """
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                self.array[i][j] -= matrix.get_value(i, j)
        return self

    def get_value(self, row, column):
        """
        Hodnota konretniho prvku
        """
        if len(self.array) >= row:
            if len(self.array[row]) >= column:
                return self.array[row][column]
        return 0

    def multipy_const(self, const):
        """
        Vynasobeni matice konstantou
        """
        for i in range(self.array):
            for j in range(self.array[i]):
                self.array[i][j] *= const
        return self

    def transpose(self):
        """
        Transpozice
        """
        new_matrix = []

        for i in range(self.get_count_cols()):
            new_row = []
            for j in range(self.get_count_rows()):
                new_row.append(self.array[j][i])
            new_matrix.append(new_row)
           
        self.array = new_matrix
        return self

    def to_string(self):
        ret = ""
        for row in self.array:
            for cell in row:
                ret += str(cell) + "    "
            ret += "\n"
        ret = ret[:-1]

        return ret

    def clone(self):
        """
        Deepclone
        """
        return copy.deepcopy(self)
    


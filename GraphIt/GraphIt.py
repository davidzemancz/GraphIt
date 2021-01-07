from NumericalExpression import NumericalExpression
from Action import Action, ActionResult
from Matrix import Matrix
from Vertex import Vertex
from Edge import Edge
from Graph import Graph
import traceback

class Console:

    def __init__(self):
        self.matrix = Matrix([])
        self.graph = Graph()

    @property
    def matrix(self):
       return self.__matrix

    @matrix.setter
    def matrix(self, value):
       self.__matrix = value

    @property
    def graph(self):
       return self.__graph

    @graph.setter
    def graph(self, value):
       self.__graph = value

    @staticmethod
    def start(): 
        console = Console().run()
        return console

    def run(self):
        while True:
            # Nacteni vstupu
            input = self.get_input()

            # Validace vstupu
            if input == "" or input.isspace():
                continue
            elif not self.validate_input(input):
                print("Invalid input")
                continue

            # Urceni akce
            action = self.evaulate_input(input)

            # Vyhodnoceni akce
            result = self.perform_action(action)
            if result.is_error():
                print(result.get_error())
            elif result.get_stop():
                break

        return self

    def get_input(self): 
        return input("GraphIt.Command>").strip()

    def validate_input(self, input):
                       
        return True

    def evaulate_input(self, input):
        command = ""
        params = []
        flags = []

        # Pokud je na zacatku cislo → vyhodnoceni vyrazu
        if len(input) > 0 and ((ord(input[0]) > 47 and ord(input[0]) < 58) or ord(input[0]) == 40):
            params.clear()
            params.append(input.replace(" ",""))
            command = "nexp.infix"
        # Pokud na na zacatku slozena zavorka - matice
        elif len(input) > 0 and input[0] == "[":
            input = input.replace(" ","")

            lb = input.find("]")
            sign = input[lb + 1]
            if sign == "+":
                command = "matrix.add"
            elif sign == "-":
                command = "matrix.sub"
            elif sign == "*":
                command = "matrix.mlp"

            params.clear()
            params.append(input[:lb + 1])
            params.append(input[lb + 2:])


        # Vyraz s parametry
        else: 
            quotation_marks = False
            space = 0

            val = ""
            for i in range(len(input)):
                if quotation_marks:
                    if input[i] == "\"":
                        quotation_marks = False
                    else:
                        val = val + input[i]
                else:
                    if input[i] == "\"":
                        if val != "":
                            if space == 1:
                                params.append(val)
                            elif space == 2:
                                flags.append(val)

                        quotation_marks = True
                        val = ""
                    elif input[i] == ";":
                        if space == 1:
                            params.append(val)
                        elif space == 2:
                            flags.append(val)
                        val = ""
                    elif input[i] == " ":
                        if space == 0:
                            command = val
                        elif space == 1:
                            params.append(val)
                        elif space == 2:
                            flags.append(val)
                        space += 1
                        val = ""
                    else:
                        val = val + input[i]
    
            if val != "":
                if space == 0:
                    command = val
                elif space == 1:
                     params.append(val)
                elif space == 2:
                     flags.append(val)


        return Action(command, params, flags)

    def print_msg(self, msg):
        print("[ =========== MESSAGE =========== ] \n  " + msg + "\n[ =============================== ]")

    def perform_action(self, action):
        try:
            command = action.get_command()
            command_subs = command.split(".")
            params = action.get_params()
            flags = action.get_flags()

            if len(command) == 0:
                command_subs = [""] * 5

            # ====== STOP ======
            if command_subs[0] == "stop":
                return ActionResult(stop = True)
            # ====== TESTOVACI PRINT ======
            elif command_subs[0] == "print":
                for param in params:
                    print(param)
            # ====== NUMERICKE VYRAZY ======
            elif command_subs[0] == "nexp":
                if len(command_subs) > 1 and command_subs[1] == "i2p":
                    num_expression = NumericalExpression(params[0])
                    print(params[0], "->", num_expression.infix_to_postfix())
                elif len(command_subs) > 1 and command_subs[1] == "infix":
                    num_expression = NumericalExpression(params[0])
                    result = ""
                    result = num_expression.evaulate_infix()
                    print(params[0], "=", result)
            # ====== MATICE ======
            elif command_subs[0] == "matrix":
                if len(command_subs) > 1:
                    if command_subs[1] == "new":
                        self.matrix = Matrix([])
                        print(self.matrix.to_string())
                    elif command_subs[1] == "print":
                        print(self.matrix.to_string())
                    elif command_subs[1] == "load":
                        print(self.matrix.load(params[0]).to_string())
                    elif command_subs[1] == "tr":
                        print(self.matrix.transpose().to_string())
                    elif command_subs[1] == "mlp":
                        if len(command_subs) > 2 and command_subs[2] == "left":
                            matrix_2 = Matrix().load(params[0])
                            print(self.matrix.multiply_left(matrix_2).to_string())
                        elif len(command_subs) > 2 and command_subs[2] == "right":
                            matrix_2 = Matrix().load(params[0])
                            print(self.matrix.multiply_right(matrix_2).to_string())
                        else: # [1,2;1,2;1,2]*[1;2]
                            if len(params) > 1:
                                self.matrix = Matrix([])
                                self.matrix.load(params[0])
                                matrix_2 = Matrix().load(params[1])
                            else:
                                matrix_2 = Matrix().load(params[0])
                            print(self.matrix.multiply_right(matrix_2).to_string())
                    elif command_subs[1] == "add": # [2,2;2,2]+[2,2;2,2]
                        if len(params) > 1:
                            self.matrix = Matrix([])
                            self.matrix.load(params[0])
                            matrix_2 = Matrix().load(params[1])
                        else:
                            matrix_2 = Matrix().load(params[0])
                        print(self.matrix.add(matrix_2).to_string())
                    elif command_subs[1] == "sub":
                        if len(params) > 1:
                            self.matrix = Matrix([])
                            self.matrix.load(params[0])
                            matrix_2 = Matrix().load(params[1])
                        else:
                            matrix_2 = Matrix().load(params[0])
                        print(self.matrix.substract(matrix_2).to_string())
            # ====== GRAFIKY ======
            elif command_subs[0] == "graph":
                if len(command_subs) > 1:
                    if command_subs[1] == "new":
                        self.graph = Graph()
                        self.graph.print()
                    elif command_subs[1] == "print":
                        self.graph.print()
                    elif command_subs[1] == "import":
                        self.graph.import_file(params[0])
                        self.graph.print()
                    elif command_subs[1] == "export":
                        self.graph.export_file(params[0])
                        self.print_msg("Export successful")
                    elif command_subs[1] == "vertex":
                        if command_subs[2] == "set":
                            self.graph.set_vertex(Vertex(params[0], params[1] if len(params) > 1 else params[0]))
                            self.graph.print()
                        elif command_subs[2] == "remove":
                            self.graph.remove_vertex(Vertex(params[0]))
                            self.graph.print()
                    elif command_subs[1] == "edge":
                        if command_subs[2] == "set":
                            self.graph.set_edge(Edge(Vertex(params[0]), Vertex(params[1]), params[2] if len(params) > 2 else 1), "a")
                            self.graph.print()
                        elif command_subs[2] == "remove":
                            self.graph.remove_edge(Edge(Vertex(params[0]), Vertex(params[1])))
                            self.graph.print()
                    elif command_subs[1] == "findroute":
                        arr = self.graph.find_route(Vertex(params[0]), Vertex(params[1]))
                        for i in range(len(arr)):
                            print(arr[i][0], "-", arr[i][1])
                    elif command_subs[1] == "minspntree":
                        self.graph = self.graph.get_minSpanningTree()
                        self.graph.print()
                    elif command_subs[1] == "connected":
                        print(self.graph.is_connected())
            return ActionResult()
        except Exception as err:
            tr = traceback.format_exc()
            return ActionResult(error = ("[ =========== ERROR MESSAGE =========== ] \n" + tr + "[ ===================================== ]"))
            
    



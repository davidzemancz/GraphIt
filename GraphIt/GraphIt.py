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
       return self.__array

    @graph.setter
    def graph(self, value):
       self.__array = value

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

    def get_input(self): # Zatim jediny typ vstupu
        return input("GraphIt.Command>")

    def validate_input(self, input):
        command = ""

        arr = input.split(" ")
        if len(arr) >= 0:
            command = arr[0]

        return True

        valid_commands = [
            "stop", 
            "print", 
            # numericke vyrazy
            "nexp.eva",
            "nexp.i2p",
            # matice
            "m.load",
            "m.tr",
            "m.ref",
            "m.rref",
            "m.mpl",
            "m.mr",
            "m.new",
            # grafy
            "g.new",
            "g.load",
            ]

        return command in valid_commands

    def evaulate_input(self, input):
        command = ""
        params = []
        flags = []

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

        # Pokud je na zacatku cilo → vyhodnoceni vyrazu
        if len(command) > 0 and ((ord(command[0]) > 47 and ord(command[0]) < 58) or ord(command[0]) == 40):
            params.clear()
            params.append(command)
            command = ""


        return Action(command, params, flags)

    def perform_action(self, action):
        try:
            command = action.get_command()
            command_subs = command.split(".")
            params = action.get_params()
            flags = action.get_flags()

            if len(command) == 0:
                command_subs = [""] * 5

            # ====== STOP ======
            if command == "stop":
                return ActionResult(stop = True)
            # ====== TESTOVACI PRINT ======
            elif command == "print":
                for param in params:
                    print(param)
            # ====== NUMERICKE VYRAZY ======
            elif command == "":
                if command_subs[1] == "i2p":
                    num_expression = NumericalExpression(params[0])
                    print(params[0], "->", num_expression.infix_to_postfix())
                else:
                    num_expression = NumericalExpression(params[0])
                    result = ""
                    if len(flags) > 0:
                        if flags[0] == "postfix":
                            result = num_expression.evaulate_postfix()
                        elif flags[0] == "prefix":
                            raise Exception("Not supported flag")
                        elif flags[0] == "infix":
                            result = num_expression.evaulate_infix()
                    else:
                        result = num_expression.evaulate_infix()
                    print(params[0], "=", result)
            # ====== MATICE ======
            elif command_subs[0] == "matrix":
                matrix = self.matrix
                if command_subs[1] == "new":
                    matrix = Matrix([])
                elif command_subs[1] == "load":
                    print(matrix.load(params[0]).array)
                elif command_subs[1] == "tr":
                    print(matrix.load(params[0]).transpose().array)
                elif command_subs[1] == "ref":
                    print(matrix.load(params[0]).REF().array)
                elif command_subs[1] == "rref":
                    print(matrix.load(params[0]).RREF().array)
                elif command_subs[1] == "mlp":
                    if command_subs[2] == "left":
                        matrix.load(params[0])
                        matrix_2 = Matrix().load(params[1])
                        print(matrix.multiply_left(matrix_2).array)
                    elif command_subs[2] == "right":
                        matrix.load(params[0])
                        matrix_2 = Matrix().load(params[1])
                        print(matrix.multiply_right(matrix_2).array)
            # ====== GRAFIKY ======
            elif command_subs[0] == "graph":
                graph = self.graph
                if command_subs[1] == "new":
                    graph = Graph([])
                elif command_subs[1] == "load":
                    graph.load_fromFile(params[0]).print()
                elif command_subs[1] == "vertex":
                    if command_subs[2] == "add":
                        graph.add_vertex(Vertex(params[0], params[1] if len(params) > 1 else params[0]))
                        graph.print()
                elif command_subs[1] == "edge":
                    if command_subs[2] == "add":
                        graph.add_edge(Edge(Vertex(params[0]), Vertex(params[1]), params[2] if len(params) > 2 else 1), "a")
                        graph.print()
            return ActionResult()
        except Exception as err:
            tr = traceback.format_exc()
            return ActionResult(error = ("[ERROR] - " + tr))
            
    



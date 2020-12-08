from NumericalExpression import NumericalExpression
from Action import Action, ActionResult
from Matrix import Matrix
from Vertex import Vertex
from Edge import Edge
from Graph import Graph
import traceback

class Console:

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

        valid_commands = [
            "stop", 
            "print", 
            "nexp.eva",
            "nexp.i2p",
            "m.load",
            "m.tr",
            "m.ref",
            "m.rref",
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


        return Action(command, params, flags)

    def perform_action(self, action):
        try:
            command = action.get_command()
            command_subs = command.split(".")
            params = action.get_params()
            flags = action.get_flags()

            # ====== STOP ======
            if command == "stop":
                return ActionResult(stop = True)
            # ====== TESTOVACI PRINT ======
            elif command == "print":
                for param in params:
                    print(param)
            # ====== NUMERICKE VYRAZY ======
            elif command_subs[0] == "nexp":
                if command_subs[1] == "eva":
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
                elif command_subs[1] == "i2p":
                    num_expression = NumericalExpression(params[0])
                    print(params[0], "->", num_expression.infix_to_postfix())
            # ====== MATICE ======
            elif command_subs[0] == "m":
                matrix = Matrix()
                if command_subs[1] == "load":
                    print(matrix.load(params[0]).array)
                elif command_subs[1] == "tr":
                    print(matrix.load(params[0]).transpose().array)
                elif command_subs[1] == "ref":
                    print(matrix.load(params[0]).REF().array)
                elif command_subs[1] == "rref":
                    print(matrix.load(params[0]).RREF().array)
            # ====== GRAFIKY ======

            return ActionResult()
        except Exception as err:
            tr = traceback.format_exc()
            return ActionResult(error = ("[ERROR] - " + tr))
            
    



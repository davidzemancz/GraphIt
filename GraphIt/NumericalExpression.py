from Stack import Stack

class NumericalExpression:
    def __init__(self, data = ""):
        self.__data = data

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def evaulate_postfix(self):
        """
        Vyhodnoceni postfix vyrazu
        """
        data = self.get_data() + " "
        
        stack = Stack()
        val = ""
        for item in data:
            if item == " ":
                if self.is_operation(val):
                    num1 = stack.pop()
                    num2 = stack.pop()
                    assert num1 is not None and num2 is not None
                    result = self.perform_operation(num2, num1, val)
                    stack.push(result)
                else:
                    stack.push(float(val))
                val = ""
            else:
                val += item
        result = stack.pop()
        assert result is not None and stack.count() == 0
        return result

    def evaulate_infix(self):
        """
        Vyhodnoceni infixniho vyrazu
        """
        self.set_data(self.infix_to_postfix())
        return self.evaulate_postfix()

    def infix_to_postfix(self):
        """
        Prevod infixniho vyrazu na postfixni
        """
        data = self.get_data()
        infix_arr = []
        postfix_arr = []

        val = ""
        for item in data:
            if self.is_operation(item):
                if val != "":
                    infix_arr.append(float(val))
                infix_arr.append(item)
                val = ""
            elif item == "(":
                infix_arr.append(item)
            elif item == ")":
                if val != "": 
                    infix_arr.append(float(val))
                infix_arr.append(item)
                val = ""
            else:
                val += item
        
        if val != "":
           infix_arr.append(float(val))

        stack = Stack()
        for item in infix_arr:
            if self.is_operation(item):
                if self.get_operation_pritorty(item) < self.get_operation_pritorty(stack.first()):
                    for op in stack.to_list():
                        if op == "(":
                            continue
                        postfix_arr.append(op)
                    stack.clear()
                stack.push(item)
            elif item == "(":
                 stack.push(item)
            elif item == ")":
                while stack.first() != "(":
                    op = stack.pop()
                    postfix_arr.append(op)
            else:
               postfix_arr.append(item)

        for op in stack.to_list():
            if op == "(":
                continue
            postfix_arr.append(op)

        return " ".join(map(str, postfix_arr)) 

    def perform_operation(self, num1, num2, operation):
        """
        Provedeni aritmeticke operace
        """
        if operation == "+":
            return num1 + num2
        elif operation == "-":
            return num1 - num2
        elif operation == "*":
            return num1 * num2
        elif operation == "^":
            return num1 ** num2
        elif operation == "/":
            assert num2 != 0
            return num1 / num2

    def is_operation(self, val):
        """
        Je znak operace?
        """
        return val == "+" or val == "*" or val == "-" or val == "/" or val == "^"

    def get_operation_pritorty(self, operation):
        """
        Priorita operace
        """
        if operation == "+" or operation == "-":
            return 1
        elif operation == "*" or operation == "/":
            return 2
        elif operation == "^":
            return 3
        return 0

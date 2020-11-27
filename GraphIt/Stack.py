class StackElement:
    def __init__(self, value, next = None):
        self.value = value 
        self.next = next 

class Stack:
    def __init__(self):
        self.__set_count(0)
        self.__set_first(None)

    def __get_first(self):  # Ref to first item
        return self.__first

    def __set_first(self, first):
        self.__first = first

    def __set_count(self, val):
        self.__count = val
    
    def __count_increment(self): # Increment count of items, e.g. while adding new one
        self.__count =  self.__count + 1
        return self.__count

    def __count_decrement(self): # Decrement count of items, e.g. while removing one
        self.__count =  self.__count - 1
        return self.__count

    def push(self, value):
        element = StackElement(value, self.__get_first())
        self.__set_first(element)
        self.__count_increment()
        return self

    def pop(self):
        first = self.__get_first()
        if first is None:
            return None
        self.__set_first(first.next)
        self.__count_decrement()
        return first.value

    def count(self):  # Ref to first item
        return self.__count

    def clear(self):
        self.__set_first(None)

    def first(self):
        first = self.__get_first()
        if first is None:
            return None
        return first.value

    def to_list(self):
        list = [] 
        element = self.__get_first()
        while element is not None:
            list.append(element.value)
            element = element.next
        return list


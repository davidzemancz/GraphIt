import enum

class Heap:
    def __init__(self):
        self.arr = []

    def add(self, value):
        index = len(self.arr)
        self.arr.append(value)
        
        parent = (index - 1) // 2 

        while parent >= 0 and self.arr[index] < self.arr[parent]:
            self.arr[index], self.arr[parent] = self.arr[parent], self.arr[index]

            index = parent
            parent = (index - 1) // 2 

    def build(self, arr):
        l = len(arr)

        for i in range(l // 2, -1, -1):
            
            j = i
            child_left = 2 * i + 1
            child_right = 2 * i + 2

            while (child_left < l and arr[j] > arr[child_left]) or (child_right < l and arr[j] > arr[child_right]):
                if l > child_left and arr[j] > arr[child_left] and (l <= child_right or arr[child_left] < arr[child_right]):
                    arr[j], arr[child_left] = arr[child_left], arr[j]
                    j = child_left
                    child_left = j * 2 + 1
                    child_right = j * 2 + 2
                elif l > child_right and arr[j] > arr[child_right]:
                    arr[j], arr[child_right] = arr[child_right], arr[j]
                    j = child_right
                    child_left = j * 2 + 1
                    child_right = j * 2 + 2

        self.arr = arr

    def check(self):
        l = len(self.arr)
        for i in range(1, l):
            parent = (i - 1) // 2 
            if self.arr[i] < self.arr[parent]:
                return False

        return True

    def get_min(self):
        l = len(self.arr)

        if l <= 0:
            return None
        elif l == 1:
            return self.arr.pop()

        min = self.arr[0]
        self.arr[0] = self.arr.pop()
        l -= 1

        index = 0
        child_left = 1
        child_right = 2

        while (child_left < l and self.arr[index] > self.arr[child_left]) or (child_right < l and self.arr[index] > self.arr[child_right]):
            if self.arr[index] > self.arr[child_left] and (l <= child_right or self.arr[child_left] < self.arr[child_right]):
                self.arr[index], self.arr[child_left] = self.arr[child_left], self.arr[index]
                index = child_left
                child_left = index * 2 + 1
                child_right = index * 2 + 2
            elif self.arr[index] > self.arr[child_right]:
                self.arr[index], self.arr[child_right] = self.arr[child_right], self.arr[index]
                index = child_right
                child_left = index * 2 + 1
                child_right = index * 2 + 2
            else:
                break

        return min

    def sort(self):
        arr = []
        min = self.get_min()
        while min is not None:
            arr.append(min)
            min = self.get_min()

        return arr

    def print(self):
        print(self.arr)

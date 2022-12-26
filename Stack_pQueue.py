import numpy as np


class myStack():
    def __init__(self, max_capacity):
        self.max_capacity = max_capacity
        self.stack = [0]*max_capacity
        self.stack_pointer = -1
        self.pop_counter = 0
    
    # O(1), Door het gebruik van een stackPointer hoeven we niet te loopen door de "stack".
    def push(self, item):
        if self.isFull():
            return False
        self.stack_pointer += 1
        self.stack[self.stack_pointer] = item
        return True
    
    # O(1), Door het gebruik van een stackPointer hoeven we niet te loopen door de "stack".
    def pop(self):
        if not self.isEmpty():
            item = self.stack[self.stack_pointer]
            self.stack[self.stack_pointer] = 0
            self.stack_pointer -= 1
            self.pop_counter += 1
            return item
        return None
    
    # O(1), Door het gebruik van een stackPointer hoeven we niet te loopen door de "stack".
    def peek(self):
        if not self.isEmpty():
            return self.stack[self.stack_pointer]
        return None
        
    # O(1)
    def isEmpty(self):
        return (self.stack_pointer == -1)
    
    # O(1)
    def isFull(self):
        return (self.stack_pointer == self.max_capacity-1)
    
    # O(n), Om de max_capacity te vergroten moeten we ervoor zorgen dat er een niewe lijst wordt gemaakt
    # die 2x zo groot is. We slaan de huidige stack tijdelijk op, maken een nieuwe lijst van zeros
    # en kopiëren vervolgens de tijdelijke stack op de niewe, vergrote stack.
    def doubleCapacity(self):
        tmp_stack = self.stack
        tmp_max_capacity = self.max_capacity
        
        self.max_capacity *= 2
        self.stack = [0]*self.max_capacity
        for i in range(tmp_max_capacity):
            self.stack[i] = tmp_stack[i]
        
        return True
        
    def __str__(self):
        return self.stack.__str__()
    
    def __repr__(self):
        return self.__str__()

# Dit is representatie klasse. Puur om de __str__ en __repr__ te kunnen implementeren voor meer duidelijkheid in mijn queue
class task():
    def __init__(self, value = 0, priority = 0, n = 0):
        self.value = value
        self.prio = priority
        self.N = n
        
    def __str__(self):
        return '({}, {})'.format(self.value, self.prio)
    
    def __repr__(self):
        return self.__str__()
        
        
class pQueue:
    def __init__(self, max_capacity):
        self.max_capacity = max_capacity
        self.array = [task()]*max_capacity
        self.available_indexes = myStack(max_capacity)
        for i in range(max_capacity):
            self.available_indexes.push(i)
    
    # O(1)
    def queue(self, v, p):
        if self.available_indexes.isEmpty():    # no more available indexes on stack
            return False
        self.array[self.available_indexes.pop()] = task(v, p, self.available_indexes.pop_counter)
        return True
    
    # O(n)
    def dequeu(self):
        if self.available_indexes.isFull():
            return None
        
                    # idx, element      
        highest_prio = (0, None)
        
        for (i, elem) in enumerate(self.array):
            if elem.prio != 0:
                if highest_prio[1] == None:
                    highest_prio = (i, elem)
                
                elif elem.prio == highest_prio[0]:
                    if elem.N < highest_prio[1].N:
                        highest_prio = (i, elem)
                
                elif elem.prio > highest_prio[0]:
                    highest_prio = (i, elem)
         
        highest_prio_value = highest_prio[1].value
        self.array[highest_prio[0]] = task()
        self.available_indexes.push(highest_prio[0])
        return highest_prio_value
    
    # O(n)
    def contains(self, v):
        for i in self.array:
            if i.value == v:
                return True
        return False
    
    # O(n)
    def remove(self, e):
        for i in range(self.max_capacity):
            if self.array[i].value == e:
                self.array[i] = task()
                self.available_indexes.push(i)

    def __str__(self):
        return self.array.__str__()
    
    def __repr__(self):
        return self.__str__() 


prio = pQueue(10)











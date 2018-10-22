import logging
from random import randint


class Memory:
   
    def __init__(self):
        self.data = [randint(0, 1000) for x in range(4)]
    
   
    def write_back(self, location, data_to_be_writen):
        if (location <0) or (location > 3):
            print("Invalid location: ",location)
            print("Exiting !!!!")
            exit(1) 
        self.data[location] = data_to_be_writen

    def read_location(self, location):
        if (location <0) or (location > 3):
            print("Invalid location: ",location)
            print("Exiting !!!!")
            exit(1) 
             
        return self.__data[location] 
    
    def get_data(self):
        return self.data
    
    
    
import logging
from random import randint


class Memory:
    """
    This class simulates Memory. As the project specification requires only 1 block with 4 memory location.
    We are not writing any details to handle more than 4 memory location.  Each of the memory location is initiated with 
    random data  
    """

    def __init__(self):
        self.__data = [randint(0, 1000) for x in range(4)]
    
    
    """
    As the data is private variable. This method will be used for wrting "data_to_be_writen" to the "location" 
    """
    def write_back(self, location, data_to_be_writen):
        if (location <0) or (location > 3):
            print("Invalid location: ",location)
            print("Exiting !!!!")
            exit(1) 
        self.__data[location] = data_to_be_writen
        
    """
    As the data is private variable. This method will be used for reading what is in the "location" 
    """
    def read_location(self, location):
        if (location <0) or (location > 3):
            print("Invalid location: ",location)
            print("Exiting !!!!")
            exit(1) 
             
        return self.__data[location] 
    
    
    
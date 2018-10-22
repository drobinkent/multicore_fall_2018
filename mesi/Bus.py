import logging
from random import randint

class Bus:
    """
    Simulates an inter-core bus on a multi-processor chip.
    """

    def __init__(self, memory):
        self.memory = memory
        self.all_processors = []
        self.all_transactions = []
        self.data_block= None

    @property
    def status(self):
    
        all_processors_status = []
        for x in self.all_processors:
            all_processors_status.append(x.cache['state'])
        return all_processors_status

    def transaction(self, action):
     
        logging.debug(action)
        self.all_transactions.append(action)
        self.processor_snooping()
        return getattr(self, action[1])()

    def bus_rd(self):
        if self.data_block:
            cache_block = self.data_block
            self.data_block = None
            return 'S', cache_block
        else:
            return 'E', self.memory.data

    def bus_rd_x(self):
   
        if self.data_block:
            cache_block = self.data_block
            self.data_block = None
            return cache_block
        else:
            return self.memory.data

   
   

    def bus_upgr(self):
    
        return None

    def flush(self):
    

        self.memory.data = self.data_block
        return self.memory.data

    def flush_opt(self):

        self.memory.data = self.data_block
        return self.memory.data

    def processor_snooping(self):
        
        last_action = self.all_transactions[-1]
        for x in self.all_processors:
            x.snooper(last_action)

        return None
    
    

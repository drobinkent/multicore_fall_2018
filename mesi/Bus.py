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
        """
        Gets the current state of all of the processor's caches.
        :return: list of states for all processors
        """
        all_processors_status = []
        for x in self.all_processors:
            all_processors_status.append(x.cache['state'])
        return all_processors_status

    def transaction(self, action):
        """
        Performs the specified bus transaction and appends it to the history.
        :param action: transaction as [processor_number, action]
        :return: The result of the transaction.
        """
        logging.debug(action)
        self.all_transactions.append(action)
        self.processor_snooping()
        return getattr(self, action[1])()

    def bus_rd(self):
        """
        Snooped request that indicates there is a read request to a Cache block
        made by another processor.

        :return: block from memory or another cache
        """

        if self.data_block:
            cache_block = self.data_block
            self.data_block = None
            return 'S', cache_block
        else:
            return 'E', self.memory.data

    def bus_rd_x(self):
        """
        Snooped request that indicates there is a write request to a Cache block
        made by another processor which doesn't already have the block.

        :return: the block from another cache or memory.
        """

        if self.data_block:
            cache_block = self.data_block
            self.data_block = None
            return cache_block
        else:
            return self.memory.data

   
   

    def bus_upgr(self):
        """
        Snooped request that indicates that there is a write request to a Cache block
        made by another processor but that processor already has that Cache block
        resident in its Cache.

        :return: None
        """

        return None

    def flush(self):
        """
        Snooped request that indicates that an entire cache block is written back
        to the main memory by another processor.

        :return: The current values in memory.
        """

        self.memory.data = self.data_block
        return self.memory.data

    def flush_opt(self):
        """
        Snooped request that indicates that an entire cache block is posted on the bus
        in order to supply it to another processor (Cache to Cache transfers).

        :return: The current values in memory.
        """

        self.memory.data = self.data_block
        return self.memory.data

    def processor_snooping(self):
        """
        Has all processors perform their snooping and respond appropripyately.

        :return: None
        """
        last_action = self.all_transactions[-1]
        for x in self.all_processors:
            x.snooper(last_action)

        return None
    
    

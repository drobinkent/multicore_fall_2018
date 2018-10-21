import logging
from random import randint

class Processor:
   

    def __init__(self, processor_id, bus, memory):
        """
        Initializes a simulated processor and its cache.
        """

        logging.debug("Initializing processor--" + str(id))
        self.cache = {'state': 'I', 'values': [0, 0, 0, 0]}  #One block of cache memory for this processor
        self.processor_id = processor_id
        self.bus = bus
        self.bus.processors.append(self)
        self.memory = memory
        logging.debug("Cache contents of the processor are : ",self.cache)

    def simulate_processor_read(self, address):
        """
        Simulates reading of a cache block.

        :return: The cache
        """

        if self.cache['state'] is 'I':  # If we're in the invalid state
            # Issue BusRd to the bus
            # other Caches see BusRd and check if they have a non-invalid copy, inform sending cache
            # State transition to (S)Shared, if other Caches have non-invalid copy.
            # State transition to (E)Exclusive, if none (must ensure all others have reported).
            # If other Caches have copy, one of them sends value, else fetch from Main Memory
            self.cache['state'], self.cache['values'] = self.bus.transaction([self.number, 'bus_rd'])

        else:  # M, S, and E
            # We already have a valid copy of the information.
            # No bus transactions generated
            # State remains the same.
            # Read to the block is a Cache hit
            pass

        logging.info("Value: " + str(self.cache['values'][address]))
        return self.cache

    def pr_wr(self, address):
        """
        Writes to a cache block.

        :param address: The address in memory
        :return: The cache.
        """
        if self.cache['state'] is 'I':
            # Issue BusRdX signal on the bus
            # State transition to (M)Modified in the requestor Cache.
            # If other Caches have copy, they send value, otherwise fetch from Main Memory
            # If other Caches have copy, they see BusRdX signal and Invalidate their copies.
            # Write into Cache block modifies the value.
            self.cache['values'] = self.bus.transaction([self.number, 'bus_rd_x'])

        elif self.cache['state'] is 'S':
            self.bus.transaction([self.number, 'bus_upgr'])

        self.cache['state'] = 'M'

        self.cache['values'][address] = randint(0, 1000)

        return self.cache
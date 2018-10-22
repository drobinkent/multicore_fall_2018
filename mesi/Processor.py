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
        self.bus.all_processors.append(self)
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
            self.cache['state'], self.cache['values'] = self.bus.transaction([self.processor_id, 'bus_rd'])

        else:  # M, S, and E
            # We already have a valid copy of the information.
            # No bus transactions generated
            # State remains the same.
            # Read to the block is a Cache hit
            pass

        logging.info("Value: " + str(self.cache['values'][address]))
        return self.cache

    def simulate_processor_write(self, address):
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
            self.cache['values'] = self.bus.transaction([self.processor_id, 'bus_rd_x'])

        elif self.cache['state'] is 'S':
            self.bus.transaction([self.processor_id, 'bus_upgr'])

        self.cache['state'] = 'M'

        self.cache['values'][address] = randint(0, 1000)

        return self.cache
    
    
    

    def snooper(self, last_transaction):
        """
        Snoops on the bus for changes in the cache.

        :return: the states of the item in other caches.
        """
        logging.debug('P{} snooping'.format(self.processor_id))

        logging.debug('last_transaction: ' + str(last_transaction))

        if last_transaction[0] is not self.processor_id:
            # logging.debug("not issued by self.")

            # BusRd
            if last_transaction[1] is "bus_rd":
                if self.cache['state'] is 'E':
                    logging.debug('BusRd E->S')
                    # Transition to Shared (Since it implies a read taking place in other cache).
                    # Put FlushOpt on bus together with contents of block.

                    # logging.debug("Transitioning from E to S")
                    self.cache['state'] = 'S'
                    self.bus.data_block = self.cache['values']
                    self.bus.transaction([self.processor_id, 'flush_opt'])

                elif self.cache['state'] is 'S':
                    logging.debug('BusRd S->S')
                    # No State change (other cache performed read on this block, so still shared).
                    # May put FlushOpt on bus together with contents of block
                    # (design choice, which cache with Shared state does this).
                    self.bus.data_block = self.cache['values']
                    self.bus.transaction([self.processor_id, 'flush_opt'])

                elif self.cache['state'] is 'M':
                    # Transition to (S)Shared.
                    # Put FlushOpt on Bus with data. Received by sender of BusRd and Memory Controller,
                    # which writes to Main memory.
                    logging.debug('BusRd M->S')

                    self.cache['state'] = 'S'
                    self.bus.data_block = self.cache['values']
                    self.bus.transaction([self.processor_id, 'flush_opt'])

            # BusRdX
            elif last_transaction[1] is 'bus_rd_x':
                if self.cache['state'] is not 'I':
                    logging.debug("BusRdX has valid copy.")
                    logging.debug('state was: {}'.format(self.cache['state']))
                    # If we had a valid copy of the data (E,M,S)
                    # Transition to Invalid.
                    # Put FlushOpt on Bus, together with the data from now-invalidated block.
                    self.cache['state'] = 'I'

                    self.bus.data_block = self.cache['values']
                    self.bus.transaction([self.processor_id, 'flush_opt'])
            # BusUpgr
            elif last_transaction[1] is "bus_upgr":
                if self.cache['state'] is 'S':
                    logging.debug('BusUpgr S->I')
                    self.cache['state'] = 'I'

        return self.bus.status

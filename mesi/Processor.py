import logging
from random import randint

class Processor:
   

    def __init__(self, processor_id, bus, memory):
    
        logging.debug("Initializing processor cache --" + str(id))
        self.cache = {'state': 'I', 'values': [0, 0, 0, 0]}  #One block of cache memory for this processor
        self.processor_id = processor_id
        self.bus = bus
        self.bus.all_processors.append(self)
        self.memory = memory
        logging.debug("Cache contents of the processor are : ",self.cache)

    def simulate_processor_read(self, address):
        print("Processor-{} has issued a read operation.".format(self.processor_id))
        if self.cache['state'] is 'I':  # If we're in the invalid state
            print("Cache is in invalid state. Seiding read request over the bus")
            self.cache['state'], self.cache['values'] = self.bus.transaction([self.processor_id, 'bus_rd'])

        elif self.cache['state'] is 'M':  # M, S, and E
            print("Cache is in \"M\" state. Serving read request from cache")
        elif self.cache['state'] is 'E':  # M, S, and E
            print("Cache is in \"E\" state. Serving read request from cache")
        elif self.cache['state'] is 'S':  # M, S, and E
            print("Cache is in \"S\" state. Serving read request from cache")


        print("Value: " + str(self.cache['values'][address]))
        return self.cache

    def simulate_processor_write(self, address):
        print("Processor-{} has issued a write operation.".format(self.processor_id))

        if self.cache['state'] is 'I':
            self.cache['values'] = self.bus.transaction([self.processor_id, 'bus_rd_x'])
        elif self.cache['state'] is 'S':
            self.bus.transaction([self.processor_id, 'bus_upgr'])
        self.cache['state'] = 'M'
        self.cache['values'][address] = randint(0, 1000)
        return self.cache
    
    
    

    def snooper(self, last_transaction):
       
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

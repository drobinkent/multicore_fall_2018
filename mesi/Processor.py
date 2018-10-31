from random import randint



class Processor:
   

    def __init__(self, processor_id, bus, memory):
    
        print("Initializing processor cache --" + str(id))
        self.cache = {'state': 'I', 'values': [0, 0, 0, 0]}  #One block of cache memory for this processor
        self.processor_id = processor_id
        self.bus = bus
        self.bus.all_processors.append(self)
        self.memory = memory
        print("Cache contents of the processor are : ",self.cache)

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
       
        print('Processor--{} snooping'.format(self.processor_id))
        print('current instruction in the bus: ' + str(last_transaction))
        if last_transaction[0] is not self.processor_id:
           
            if last_transaction[1] is "bus_rd":
                print("Instruction type is Bus Read")
                if self.cache['state'] is 'E':
                    print("Inside Processor-",self.processor_id, "cache state is transitioning from \"E\" to \"S\"")
                    self.cache['state'] = 'S'
                    self.bus.data_block = self.cache['values']
                    self.bus.transaction([self.processor_id, 'flush_opt'])
                    print("flush_opt instruction issued for all other processors. ")

                elif self.cache['state'] is 'S':
                    print("Inside Processor-",self.processor_id, "cache state is transitioning from \"S\" to \"S\"")
                    self.bus.data_block = self.cache['values']
                    self.bus.transaction([self.processor_id, 'flush_opt'])
                    print("flush_opt instruction issued for all other processors. ")


                elif self.cache['state'] is 'M':
                    print("Inside Processor-",self.processor_id, "cache state is transitioning from \"M\" to \"S\"")
                    self.cache['state'] = 'S'
                    self.bus.data_block = self.cache['values']
                    self.bus.transaction([self.processor_id, 'flush_opt'])
                    print("flush_opt instruction issued for all other processors. ")

            # BusRdX
            elif last_transaction[1] is 'bus_rd_x':
                print("Instruction type is Bus Read_X")
                if self.cache['state'] is not 'I':
                    print("BusRdX has valid copy.")
                    print("Inside Processor-",self.processor_id, "cache state is transitioning from {} to \"I\"".format(self.cache['state']))
                    self.cache['state'] = 'I'
                    self.bus.data_block = self.cache['values']
                    self.bus.transaction([self.processor_id, 'flush_opt'])
                    print("flush_opt instruction issued for all other processors. ")

            # BusUpgr
            elif last_transaction[1] is "bus_upgr":
                print("Instruction type is Bus UPGR")
                if self.cache['state'] is 'S':
                    print('BusUpgr S->I')
                    self.cache['state'] = 'I'
        return self.bus.status

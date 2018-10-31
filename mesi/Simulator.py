import logging
from random import randint
import Memory as mem
import Bus as bus
import Processor as processor
from builtins import int



class Simulator:
    def __init__(self):
        self.memory = mem.Memory()
        self.bus = bus.Bus(self.memory)

        self.processors = {}
        for x in range(4):
            self.processors[x] = processor.Processor(x, self.bus, self.memory)

    def instruction(self, processor, r_w, address):
        """
        Performs the specified request in the cache.

        :param processor: numerical id o the processor
        :param r_w: 0 means processor  read and 1 means  write
        """

        if r_w is 0:
            print('P{}: PrRd addr {}'.format(processor, address))
            instruction = self.processors[processor].simulate_processor_read(address)
        else:
            print('P{}: PrWr addr {}'.format(processor, address))
            instruction = self.processors[processor].simulate_processor_write(address)
        print('P{}: Cache: {}'.format(processor, instruction))
        return instruction







if __name__ == "__main__":
    print("Illustrating MESI protcol test based on tests defined in wikipedia page: ")
    mesi_sim = Simulator()
    wikipedia_test_suite = [
        [0, 0],
        [0, 1],
        [2, 0],
        [2, 1],
        [0, 0],
        [2, 0],
        [1, 0]
    ]

    for n in range(len(wikipedia_test_suite)):
        print("----- {} th INSTRUCTION  -----".format(n+1))
        test_instruction = wikipedia_test_suite[n]
        mesi_sim.instruction(test_instruction[0], test_instruction[1], randint(0, 3))
        print("STATES of cache blocks after excetuting the instruction: " + str(mesi_sim.bus.status))
        print("Data in memory                                         : " + str(mesi_sim.memory.data))
        
    print("\n\n\n\n\n\n\n\n Doing a set of random tests. ---")
    n_as_string = input("How many radom tests you want to generate?")
    n = int(n_as_string)



    mesi_sim = Simulator()

    for x in range(n):
        print("----- {} th INSTRUCTION  -----".format(x+1))
        instruction = mesi_sim.instruction(randint(0, 3), randint(0, 1), randint(0, 3))
        print("STATES of cache blocks after excetuting the instruction: " + str(mesi_sim.bus.status))
        print("Data in memory                                         : " + str(mesi_sim.memory.data))

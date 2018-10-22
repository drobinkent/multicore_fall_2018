import logging
from random import randint
import Memory as mem
import Bus as bus
import Processor as processor



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

        :param processor: processor number (0 to 3)
        :param r_w: 0 for read 1 for write
        :param address: address to access (0 to 3)
        :return: The result of the specified operation.
        """

        if r_w is 0:
            print('P{}: PrRd addr {}'.format(processor, address))
            instruction = self.processors[processor].simulate_processor_read(address)
        else:
            print('P{}: PrWr addr {}'.format(processor, address))
            instruction = self.processors[processor].simulate_processor_write(address)
        print('P{}: Cache: {}'.format(processor, instruction))
        return instruction

    def random_test(self):
        instruction = self.instruction(randint(0, 3), randint(0, 1), randint(0, 3))
        return instruction







def random_test(n):
    """
    Performs the specified number of random tests on the MESI simulator.
    :param n: number of random instructions to perform.
    :return: None
    """
    mesi = Simulator()

    for x in range(n):
        print("----- INSTRUCTION #{} -----".format(x+1))
        mesi.random_test()
        print("STATES: " + str(mesi.bus.status))
        print("MEM:    " + str(mesi.memory.data))
    # print("BUS TRANSACTIONS:")
    # for transaction in mesi.bus.transactions:
    #     print(transaction)


def wikipedia_test():
    """
    Performs the operations outlined in "Illustration of MESI protocol operations" on the MESI protocol Wikipedia page.

    :return: None
    """
    mesi = Simulator()
    tests = [
        [0, 0],
        [0, 1],
        [2, 0],
        [2, 1],
        [0, 0],
        [2, 0],
        [1, 0]
    ]

    for n in range(len(tests)):
        print("----- INSTRUCTION #{} -----".format(n+1))
        t = tests[n]
        mesi.instruction(t[0], t[1], 0)
        print("STATES: " + str(mesi.bus.status))
        print("MEM:    " + str(mesi.memory.data))

    # Uncomment to see bus transactions
    # print("BUS TRANSACTIONS:")
    # for transaction in mesi.bus.transactions:
    #     print(transaction)


if __name__ == "__main__":
    random_test(10)

    # wikipedia_test()

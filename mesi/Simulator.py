import logging
from random import randint
import Memory as mem
import Bus as bus
import Processor as processor



class Simulator:
    """
    Main MESI simulator class. Can be seen as the chip that contains all of the Processors, Bus, and Memory.
    """

    def __init__(self):
        """
        Initializes bus, memory, and processors.
        """
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
        # logging.basicConfig(level=logging.DEBUG, format="%(message)s")

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
            logging.info('P{}: PrRd addr {}'.format(processor, address))
            instruction = self.processors[processor].simulate_processor_read(address)
        else:
            logging.info('P{}: PrWr addr {}'.format(processor, address))
            instruction = self.processors[processor].simulate_processor_write(address)

        logging.info('P{}: Cache: {}'.format(processor, instruction))
        return instruction

    def random_test(self):
        """
        Performs a random test on the MESI simulator.

        :return: The result of the instruction.
        """
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
        logging.info("----- INSTRUCTION #{} -----".format(x+1))
        mesi.random_test()
        logging.info("STATES: " + str(mesi.bus.status))
        logging.info("MEM:    " + str(mesi.memory.data))
    # logging.info("BUS TRANSACTIONS:")
    # for transaction in mesi.bus.transactions:
    #     logging.info(transaction)


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
        logging.info("----- INSTRUCTION #{} -----".format(n+1))
        t = tests[n]
        mesi.instruction(t[0], t[1], 0)
        logging.info("STATES: " + str(mesi.bus.status))
        logging.info("MEM:    " + str(mesi.memory.data))

    # Uncomment to see bus transactions
    # logging.info("BUS TRANSACTIONS:")
    # for transaction in mesi.bus.transactions:
    #     logging.info(transaction)


if __name__ == "__main__":
    random_test(10)

    # wikipedia_test()

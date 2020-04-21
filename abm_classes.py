import numpy as np


class Government:

    def __init__(self, id, resources_init, rate_init):
        self.id = id
        self.resources = resources_init
        self.rate = np.array([0.08, 0.1, 0.4])
        self.rate = rate_init

    def collect(self):
        self.resources += np.sum(np.multiply(self.allocation, self.rate))

    def spend(self):
        self.resources -= np.multiply(self.resources, self.allocation)



class Firm:

    def __init__(self, id, resources_init, allocation_init):
        self.id = id
        self.resources = resources_init
        self.allocation = allocation_init



    def display_id(self):
        print(str(self.id) + ' resources = ' + str(self.resources))



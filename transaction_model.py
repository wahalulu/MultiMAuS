import numpy as np

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

import parameters

from customer import Customer
from fraudster import Fraudster
from merchant import Merchant
from authenticator import Authenticator


class TransactionModel(Model):
    """A model with some number of agents."""
    def __init__(self, model_parameters):
        super().__init__()

        # random state to reproduce results
        self.random_state = np.random.RandomState(model_parameters["seed"])

        # random activation scheme for the customers
        self.schedule = RandomActivation(self, seed=model_parameters["seed"])

        # create the payment processing platform via which all transactions go
        self.authenticator = Authenticator(self, self.random_state, model_parameters["max authentication steps"])

        # create merchants
        self.merchants = [Merchant(i, self) for i in range(model_parameters["num merchants"])]

        # create customers
        for i in range(model_parameters["num customers"]):
            c = Customer(i, self, self.random_state)
            self.schedule.add(c)

        # create fraudsters
        for i in range(model_parameters["num fraudsters"]):
            f = Fraudster(i, self, self.random_state)
            self.schedule.add(f)


            # # Add the agent to a random grid cell
            # x = random.randrange(self.grid.width)
            # y = random.randrange(self.grid.height)
            # self.grid.place_agent(a, (x, y))

        # self.datacollector = DataCollector(
        #     model_reporters={"Gini": compute_gini},
        #     agent_reporters={"Wealth": lambda a: a.wealth})

        # initialise time of day
        self.timesteps_per_day = 24
        self.time = 0

        # initialise a data collector
        self.datacollector = DataCollector(
            model_reporters={"date": lambda m: m.time},
            agent_reporters={"Account ID": lambda c: c.unique_id,
                             "Merchant": lambda c: c.curr_merchant.unique_id,
                             "Currency": lambda c: c.currency,
                             "Amount": lambda c: c.curr_transaction_amount,
                             "target": lambda c: c.fraudster})

    def step(self):

        # this calls the step function of each agent in the schedule (customer, fraudster)
        self.schedule.step()

        # write new transactions to log
        self.datacollector.collect(self)

        # update time
        self.time = (self.time + 1) % self.timesteps_per_day

        # TODO: customer/fraudster migration

    def process_transaction(self, client, amount, merchant):
        authorise = self.authenticator.authorise_payment(client, amount, merchant)
        return authorise


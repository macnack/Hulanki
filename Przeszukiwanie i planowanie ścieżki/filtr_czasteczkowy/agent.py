# prob.py
# This is

import random
import numpy as np
import queue
import math

from gridutil import *


class Agent:
    def __init__(self, size, sigma_move, sigma_perc):
        self.size = size
        self.sigma_sq_move = sigma_move ** 2
        self.sigma_sq_perc = sigma_perc ** 2
        self.sigma_perc = sigma_perc
        # list of valid locations
        self.locations = [loc for loc in range(size)]
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.action_dir = -1

        self.t = 0
        self.n = 20
        # create an initial particle set as 1-D numpy array (self.p)
        # and initial weights as 1-D numpy array (self.w)
        # TODO PUT YOUR CODE HERE
        self.p = np.ones(self.n) / self.n
        self.w = np.ones(self.n)
        # ------------------

    def __call__(self):
        # if reached one of the ends then start moving in the opposite direction
        if self.t % 20 == 0:
            self.action_dir *= -1

        # move by one or two cells
        action = self.action_dir * np.random.choice([1, 2])

        # use information about requested action to update posterior
        # TODO PUT YOUR CODE HERE
        self.predict_posterior(action)
        # ------------------

        self.t += 1

        return action

    def predict_posterior(self, action):
        # predict posterior using requested action
        # TODO PUT YOUR CODE HERE
        for curr_x in range(np.size(self.p)):
            self.p[curr_x] += action + np.random.normal(0, self.sigma_sq_move)  # P[(curr_x + action) % np.size(P)]
        # ------------------
        # self.p = self.p / np.sum(self.p)
        # this function does not return anything
        return

    def calculate_weights(self, percept):
        # calculate weights using percept
        # TODO PUT YOUR CODE HERE
        for i in range(np.size(self.w)):
            self.w[i] = np.exp(- ((self.p[i] - percept) ** 2) / (2 * self.sigma_sq_perc))
        # ------------------
        self.w = self.w / self.w.sum()
        # this function does not return anything
        return

    def correct_posterior(self):
        # correct posterior using measurements
        # TODO PUT YOUR CODE HERE
        # konstruktor liczb losowych
        rng = np.random.default_rng()
        #zbior nowych czasteczek
        new_P = []
        # losowanie poczatkowego indeksu
        index = rng.integers(0, len(self.p))
        beta = 0.0
        mw = max(self.w)
        for i in range(np.size(self.p)):
            beta += np.random.uniform(0, 2.0 * mw)
            # iteracyjne szukanie polozenia
            if beta > self.w[index]:
                # odejmowanie wag
                beta -= self.w[index]
                index = (index-1) % len(self.p)
            # dodanie czasteczki
            new_P.append(self.p[index])
        self.p = new_P
        # ------------------

        # this function does not return anything
        return

    def get_particles(self):
        return self.p

    def get_weights(self):
        return self.w

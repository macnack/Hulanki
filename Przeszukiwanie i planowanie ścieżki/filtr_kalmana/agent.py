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
        # list of valid locations
        self.locations = [loc for loc in range(size)]
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.action_dir = -1

        self.t = 0
        # initial belief
        self.mu = 0.0
        self.sigma_sq = 1.0

    def __call__(self):
        # if reached one of the ends then start moving in the opposite direction
        if self.t % 20 == 0:
            self.action_dir *= -1

        # move by random distance in range [1, 2)
        action = self.action_dir * (1.0 + np.random.random_sample(1))
        self.predict_posterior(action)
        # use information about requested action to update posterior
        # TODO PUT YOUR CODE HERE

        # ------------------

        self.t += 1

        return action

    def predict_posterior(self, action):
        # predict posterior using requested action
        # TODO PUT YOUR CODE HERE
        self.mu += action
        self.sigma_sq += self.sigma_sq_move
        # ------------------

        return

    def correct_posterior(self, percept):
        # correct posterior using measurements
        # TODO PUT YOUR CODE HERE
        sigma_p = self.sigma_sq_perc
        sigma_t = self.sigma_sq
        u_t = self.mu
        y = percept - u_t
        K = sigma_t / (sigma_t + sigma_p)
        self.mu = u_t + K * y
        self.sigma_sq = (1 - K) * sigma_t
        pass
        # ------------------

    def get_posterior(self):
        return self.mu, math.sqrt(self.sigma_sq)

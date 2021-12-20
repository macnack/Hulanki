# prob.py
# This is

import random
import numpy as np
import queue
import math

from gridutil import *


class Agent:
    def __init__(self, size, walls, loc, dir, sigma_move, sigma_perc, dt):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir
        self.dt = dt
        self.action_dir = 1
        self.mu = np.array([[0],[0]])
        self.Sigma = np.array([[1, 0], [0, 10]])  # dlaczego nie [ [1,dt], [0 , 10] ]??
        self.t = 0
        # create matrices used in Kalman filter
        # TODO PUT YOUR CODE HERE
        self.F = np.array([[1, dt], [0, 1]])
        self.B = np.array([[0], [0]])
        self.Q = np.array([[1 / 4.0 * dt ** 4, 1 / 2.0 * dt ** 3], [1 / 2 * dt ** 3, dt ** 2]]) * sigma_move ** 2
        self.R = sigma_perc
        self.Sigma_move = sigma_move
        self.H = np.array([1, 0])
        # ------------------

    def __call__(self):
        # use information about requested action to update posterior
        # TODO PUT YOUR CODE HERE
        self.predict_posterior()
        # ------------------

        # this function does not return anything
        return

    def predict_posterior(self):
        # predict posterior
        # TODO PUT YOUR CODE HERE
        u_t = np.random.normal(0, self.Sigma_move, 1)
        mu = self.mu.copy()
        self.mu = self.F @ mu + self.B * u_t
        self.Sigma = self.F @ self.Sigma @ self.F.T + self.Q
        # -----------------
        # this function does not return anything
        return

    def correct_posterior(self, percept):
        # correct posterior using measurements
        # TODO PUT YOUR CODE HERE
        mu_estimate = self.mu.copy()
        y = percept - self.H @ self.mu
        K = np.array(self.Sigma @ self.H.T * (self.H @ self.Sigma @ self.H.T + self.R) ** -1)
        K = np.reshape(K, (2, 1))
        self.mu = mu_estimate + K * y
        self.Sigma = (np.eye(2) - K * self.H) @ self.Sigma
        # ------------------

        # this function does not return anything
        return

    def get_posterior(self):
        return self.mu, self.Sigma

# prob.py
# This is

import random
import numpy as np
import queue
import math

from gridutil import *


class Agent:
    def __init__(self, size, landmarks, sigma_move_fwd, sigma_move_turn, sigma_perc):
        self.size = size
        self.landmarks = landmarks
        self.sigma_move_fwd = sigma_move_fwd
        self.sigma_move_turn = sigma_move_turn
        self.sigma_perc = sigma_perc

        self.t = 0
        self.n = 500
        # create an initial particle set as 2-D numpy array with size (self.n, 3) (self.p)
        # and initial weights as 1-D numpy array (self.w)
        rng = np.random.default_rng()
        self.p = np.ones((self.n, 3))
        self.p[:, 0:2] = self.n * rng.random((self.n, 2))
        self.p[:, 2] = 2 * np.pi * rng.random(self.n)
        self.w = np.full(self.n, 1) / self.n
        # TODO PUT YOUR CODE HERE

        # ------------------

    def __call__(self):
        # turn by -pi/20.0 and move forward by 1
        action = (-math.pi / 20, 1.0)
        # no turn, only move forward by 1.0
        # action = (0.0, 1.0)

        # use information about requested action to update posterior
        # TODO PUT YOUR CODE HERE
        self.predict_posterior(action)
        # ------------------

        self.t += 1

        return action

    def predict_posterior(self, action):
        # predict posterior using requested action
        # TODO PUT YOUR CODE HERE
        for i in range(len(self.p)):
            self.p[i][2] = (self.p[i][2] + np.random.normal(action, self.sigma_move_turn)[0]) % (2 * np.pi)
            [x, y] = moveForward((self.p[i][0], self.p[i][1]), self.p[i][2], np.random.normal(1, self.sigma_move_fwd))
            self.p[i, 0] = x
            self.p[i, 1] = y
        # ------------------
        # this function does not return anything
        return

    def calculate_weights(self, percept):
        # calculate weights using percept
        # TODO PUT YOUR CODE HERE
        for i in range(len(self.w)):
            for z in range(len(self.landmarks)):
                dist = np.sqrt((self.p[i][0] - self.landmarks[z][0]) ** 2 + (self.p[i][1] - self.landmarks[z][1]) ** 2)
                self.w[i] *= np.exp(- ((dist - percept[z]) ** 2) / (2.0 * self.sigma_perc))
        # # ------------------
        self.w = self.w / self.w.sum()
        # this function does not return anything
        return

    def correct_posterior(self):
        # correct posterior using measurements
        # TODO PUT YOUR CODE HERE
        rng = np.random.default_rng()
        # zbior nowych czasteczek
        new_P_x = []
        new_P_y = []
        new_P_phi = []
        # losowanie poczatkowego indeksu
        index = rng.integers(0, len(self.p))
        beta = 0.0
        mw = max(self.w)
        for i in range(len(self.p)):
            beta += np.random.uniform(0, 2.0 * mw)
            # iteracyjne szukanie polozenia
            while beta > self.w[index]:
                # odejmowanie wag
                beta -= self.w[index]
                index = (index - 1) % len(self.p)
            # dodanie czasteczki
            new_P_x.append(self.p[index, 0])
            new_P_y.append(self.p[index, 1])
            new_P_phi.append(self.p[index, 2])

        # ------------------
        self.p[:, 0] = new_P_x
        self.p[:, 1] = new_P_y
        self.p[:, 2] = new_P_phi
        # this function does not return anything
        return

    def get_particles(self):
        return self.p

    def get_weights(self):
        return self.w

#!/usr/bin/env python

"""code template"""

import random
import numpy as np

from graphics import *
from gridutil import *
from agent import *
from env import *


def main():
    # comment to get different scenarios
    random.seed(13)
    np.random.seed(13)
    # rate of executing actions
    rate = 1
    # size of the environment
    env_size = 32
    start_loc = (16.0, float(env_size // 2))
    start_orient = math.pi / 2.0
    sigma_move_fwd = 0.2
    sigma_move_turn = 0.05
    sigma_perc = 1.0
    # map of the environment: 1 - wall, 0 - free
    map = np.zeros((env_size, env_size))
    # build the list of walls locations
    walls = []
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i, j] == 1:
                walls.append((j, env_size - i - 1))

    # list of valid locations
    locs = list({*locations(env_size)}.difference(walls))

    landmarks = [(10.0, 16.0), (22.0, 16.0)]
    # landmarks = [(10.0, 16.0), (22.0, 16.0), (18.0, 20.0)]

    # create the environment and viewer
    env = LocWorldEnv(env_size, walls, landmarks, start_loc, start_orient, sigma_move_fwd, sigma_move_turn, sigma_perc)
    view = LocView(env)

    # create the agent
    agent = Agent(env.size, landmarks, sigma_move_fwd, sigma_move_turn, sigma_perc)
    # list of errors
    errors = []
    t = 0
    while t != 40:
        print('\nstep %d' % t)

        print('performing action')
        # get agent's action and execute it
        action = agent()
        print('action (turn, fwd): (%.3f, %.3f)' % (action[0], action[1]))
        env.doAction(action)

        print('performing perception')
        percept = env.getPercept()
        print('percept: ', percept)
        print('true loc: (%.3f, %.3f), orient: %.3f' % (env.agentLoc[0], env.agentLoc[1], env.agentOrient))
        agent.calculate_weights(percept)
        w = agent.get_weights()

        p = agent.get_particles()
        view.update(env, p, w)
        update(rate)
        # uncomment to pause before action
        view.pause()

        agent.correct_posterior()

        p = agent.get_particles()
        view.update(env, p)
        update(rate)

        # compute error as square root of expected value of differences
        diff2 = np.square(env.agentLoc[0] - p[:, 0]) + np.square(env.agentLoc[1] - p[:, 1])
        cur_error = np.sqrt(diff2.mean())
        print('current error: %.3f' % cur_error)

        errors.append(cur_error)
        print('mean error: %.3f' % np.array(errors).mean())

        # uncomment to pause before action
        view.pause()

        t += 1

    # pause until mouse clicked
    view.pause()


if __name__ == '__main__':
    main()

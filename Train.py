import json
import time
import argparse
import numpy as np


import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)
from file_processing import *
from World import World
from Movement import Trajectory, Point
from random import randint, randrange, sample
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import model_from_json

parser = argparse.ArgumentParser()
parser.add_argument('--load', help='Loads pre-existing weights for training',
                    action='store_true')
args = parser.parse_args()

class Train:
    def __init__(self, params, load):
        self.params  = params
        self.memory  = deque(maxlen=2500)
        self.epsilon = self.params['epsilon']

        if(load): self.model   = self.loadModel()
        else:     self.model   = self.build()
        
    # Build the model
    def build(self) -> 'model':
        model = Sequential()
        model.add(Dense(self.params['layer_size'], 
                        input_shape=((self.params['state_space'],)), 
                        activation='relu'))
        model.add(Dense(self.params['layer_size'], activation='relu'))
        model.add(Dense(self.params['layer_size'], activation='relu'))
        model.add(Dense(self.params['action_space'], activation='softmax'))
        model.compile(loss='mse', optimizer=Adam(lr=self.params['learning_rate']))

        return model
        
    # Remember state transition
    def remember(self, 
                 state: list, 
                 action: int, 
                 reward: int, 
                 nextState: list, 
                 alive: bool) -> None:
                 
        self.memory.append((state, action, reward, nextState, alive))

    # Performs snake movement from memory
    def action(self, state) -> int:
        if np.random.rand() <= self.epsilon:
            return randrange(self.params['action_space'])
        actions = self.model.predict(state)
        return np.argmax(actions[0])

    # Predicts the best action during gameplay
    def playAction(self, state) -> int:
        actions = self.model.predict(state)
        return np.argmax(actions[0])

    # Refactor
    def replay(self) -> None:

        if len(self.memory) < self.params['batch_size']:
            return

        minibatch   = sample(self.memory, self.params['batch_size'])
        states      = np.array([i[0] for i in minibatch])
        actions     = np.array([i[1] for i in minibatch])
        rewards     = np.array([i[2] for i in minibatch])
        nextState   = np.array([i[3] for i in minibatch])
        dones       = np.array([i[4] for i in minibatch])
        states      = np.squeeze(states)
        nextState   = np.squeeze(nextState)
        targets     = rewards + self.params['gamma']*(np.amax(self.model.predict_on_batch(nextState), axis=1))*(1-dones)

        targetsFull = self.model.predict_on_batch(states)
        ind = np.array([i for i in range(self.params['batch_size'])])
        targetsFull[[ind], [actions]] = targets

        self.model.fit(states, targetsFull, epochs=1, verbose=0)
        if self.epsilon > self.params['epsilon_min']:
            self.epsilon -= self.epsilon * self.params['epsilon_decay']

    def saveModel(self) -> None:
        jsonModel = self.model.to_json()
        with open("weights/model.json", "w") as json_file:
            json_file.write(jsonModel)
        self.model.save_weights("weights/model.h5")

    def loadModel(self) -> 'model':
        weights = open('weights/model.json', 'r')
        jsonModel = weights.read()
        weights.close()
        loaded_model = model_from_json(jsonModel)
        loaded_model.load_weights("weights/model.h5")
        loaded_model.compile(loss='mse', optimizer=Adam(lr=self.params['learning_rate']))
        print("Loaded model from disk")

        return loaded_model

# Placeholder for the training movement
def randomAIMovement() -> 'Trajectory':
    movementList = list(Trajectory)[:4]
    randomTrajec = randrange(0, len(movementList))
    return list(movementList)[randomTrajec]

# Train the AI
def train(load: bool) -> [int]:
    rewardSums  = []
    scoreSample = []
    config      = loadGameConfig()
    params      = loadParams()
    worldSize   = config["square_number"]
    debug       = config["debug"]
    binary      = config["binary"]
    agent       = Train(params, load)

    for e in range(params['episodes']):
        score = 0
        env   = World(worldSize, debug, binary, True)
        state = np.reshape(env.stateSpace, (1, params['state_space']))
        start = time.time()
        
        for i in range(params['max_steps']):
            action    = agent.action(state)
            nextState, reward, alive = env.step(action)
            score    += reward
            nextState = np.reshape(nextState, (1, len(nextState)))
            agent.remember(state, action, reward, nextState, alive)
            state = nextState
            
            if params['batch_size'] > 1: agent.replay()

            # If the snake is dead, initiate a new episode
            if not alive:
                break

        if(0 == (e % params['save_interval'])):
            print(f"\nSaving model: [{e}/{params['episodes']}] -> {((time.time() - start)/5):.2f} avg time/episode")
            print(f"Sample  Mean: <{np.mean(scoreSample):.2f}>: {scoreSample}")
            print(f"Total   Mean: <{np.mean(rewardSums):.2f}> [{len(rewardSums)}]")
            agent.saveModel()
            scoreSample = []

        scoreSample.append(score)
        rewardSums.append(score)

    print(f"Best Score: {max(rewardSums)}")
    return rewardSums

if __name__ == '__main__':
    rewards = train(args.load)
    
    # Could be used for plotting
    #print(rewards)
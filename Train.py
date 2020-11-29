import json
import numpy as np

from World import World
from Movement import Trajectory, Point
from random import randint, randrange, sample
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import model_from_json

class Train:
    def __init__(self, params, load):
        self.params = params
        self.memory = deque(maxlen=2500)

        if(load):
            self.model = self.loadModel()
        else:
            self.model  = self.build()
        

    
    # Build the model
    def build(self):
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
    def remember(self, state, action, reward, nextState, alive):
        #print(f"\nRemembering: {action}, {reward}, {alive}")
        #print(f"State: {state}")
        #print(f"Next State: {nextState}")
        self.memory.append((state, action, reward, nextState, alive))

    # Performs snake movement from memory
    def action(self, state):
        if np.random.rand() <= self.params['epsilon']:
            return randrange(self.params['action_space'])
        actions = self.model.predict(state)
        return np.argmax(actions[0])

    # Refactor
    def replay(self):

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
        #states      = np.squeeze(states).astype('float32')
        #nextState   = np.squeeze(nextState).astype('float32')
        targets     = rewards + self.params['gamma']*(np.amax(self.model.predict_on_batch(nextState), axis=1))*(1-dones)

        targetsFull = self.model.predict_on_batch(states)
        ind = np.array([i for i in range(self.params['batch_size'])])
        targetsFull[[ind], [actions]] = targets

        self.model.fit(states, targetsFull, epochs=1, verbose=0)
        if self.params['epsilon'] > self.params['epsilon_min']:
            self.params['epsilon'] *= self.params['epsilon_decay']

    def saveModel(self):
        jsonModel = self.model.to_json()
        with open("weights/model.json", "w") as json_file:
            json_file.write(jsonModel)
        self.model.save_weights("weights/model.h5")

    def loadModel(self):
        weights = open('weights/model.json', 'r')
        jsonModel = weights.read()
        weights.close()
        loaded_model = model_from_json(jsonModel)
        loaded_model.load_weights("model.h5")
        loaded_model.compile(loss='mse', optimizer=Adam(lr=self.params['learning_rate']))
        return loaded_model
        print("Loaded model from disk")

# Load Game configurations
def loadGameConfig():
    with open('config.json') as json_file:
        config = json.load(json_file)
    return config

# Load network parameter config
def loadParams():
    with open('params.json') as json_file:
        params = json.load(json_file)
    return params

# Placeholder for the training movement
def randomAIMovement():
    movementList = list(Trajectory)[:4]
    randomTrajec = randrange(0, len(movementList))
    return list(movementList)[randomTrajec]

# Train the AI
def train(load):
    rewardSums = []
    episodes = 1
    config   = loadGameConfig()
    params   = loadParams()

    worldSize = config["square_number"]
    debug     = config["debug"]
    terminal  = config["terminal_mode"]
    agent     = Train(params, load)

    for e in range(params['episodes']):
        score = 0
        env   = World(worldSize, debug, terminal)
        state = np.reshape(env.stateSpace, (1, params['state_space']))
        
        for i in range(params['max_steps']):
            action    = agent.action(state)
            prevState = state
            nextState, reward, alive = env.step(action)
            score    += reward
            nextState = np.reshape(nextState, (1, len(nextState)))
            #print(len(state[0]), state)
            agent.remember(state, action, reward, nextState, alive)
            state = nextState
            
            if params['batch_size'] > 1: agent.replay()

            # If the snake is dead, initiate a new episode
            if not alive:
                break

        if(0 == (e % params['save_interval'])):
            print(f"Saving model: [{e}/{params['episodes']}]")
            agent.saveModel()

        rewardSums.append(score)
    return rewardSums

if __name__ == '__main__':
    loadModel = True
    rewards = train(loadModel)
    print(rewards)

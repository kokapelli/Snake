import json

#from keras import Sequential
#from keras.layers import Dense
#from keras.optimizers import Adam

class Train:
    def __init__(self, env, params):
        self.model = self.build()

    # Build the model
    def build(self):
        pass

    # Train the AI
    def train(self):
        pass

    # Remember state transition
    def remember(self, state, action, reward, next_state, done):
        pass
if __name__ == '__main__':
    with open('params.json') as json_file:
        params = json.load(json_file)

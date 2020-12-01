import json

# Load Game configurations
def loadGameConfig() -> dict:
    with open('configurations/config.json') as json_file:
        config = json.load(json_file)
    return config

# Load network parameter config
def loadParams() -> dict:
    with open('configurations/params.json') as json_file:
        params = json.load(json_file)
    return params
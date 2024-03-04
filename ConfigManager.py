import yaml

# Dict containing cached config from program start
# Any changes made to config during program runtime will not be reflected in this
config = None

# Should only be called ONCE at the start of the program
def load_config():
    global config
    with open("config.yml", 'r') as stream:
        try:
           config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def write_config():
    global config
    with open("config.yml", 'w') as stream:
        try:
           yaml.safe_dump(config, stream)
        except yaml.YAMLError as exc:
            print(exc)

# Call as many times as necessary, loads the cached config
def get_config():
    return config

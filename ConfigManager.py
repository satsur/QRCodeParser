import yaml

def load_config():
    with open("example.yaml") as stream:
        try:
            print(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)
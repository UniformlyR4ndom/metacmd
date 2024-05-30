import json

def readConfig(path) -> dict[str, str]:
    content = '{}'
    with open(path, 'r') as configFile:
        config = json.load(configFile)
    return config


def getarg(args, i) -> str | None:
    return args[i] if i < len(args) else None

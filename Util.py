import json

def readConfig(path) -> dict[str, str]:
    content = '{}'
    with open(path, 'r') as configFile:
        config = json.load(configFile)
    return config


def getarg(args, i) -> str | None:
    return args[i] if i < len(args) else None


def isHexString(string : str) -> bool:
    string = string.lower()
    return  all([c in '0123456789abcdef' for c in string])


def isNtHash(hashCandidate : str) -> bool:
    h = hashCandidate.strip()
    return len(h) == 32 and isHexString(h)

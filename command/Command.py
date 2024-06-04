class Command:
    def __init__(self, name : str, config : dict[str, str], tags : list[str]):
        self.name = name
        self.config = config
        self.tags = tags

    def matchesTrigger(self, trigger : str) -> bool:
        raise NotImplemented("Needs to be implemented by each command")

    def getHelp(self) -> str:
        raise NotImplemented("Needs to be implemented by each command")

    def genCommands(self, trigger : str, args : list[str]) -> list[str]:
        raise NotImplemented("Needs to be implemented by each command")

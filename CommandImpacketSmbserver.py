from Command import Command
from Util import getarg

class CommandImpacketSmbserver(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)
        conf = config['commands']['impacket-smbserver']
        self.defaultUserName = conf['defaultUsername']
        self.defaultPassword = conf['defaultPassword']
        self.defaultShareName = conf['defaultSharename']
        self.defaultSharePath = conf['defaultSharepath']


    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        nmapTriggers = ['impacket-smbserver', 'smbserver']
        return any(word in triggerLower for word in nmapTriggers)


    def getHelp(self) -> str:
        return 'impacket-smbserver'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        commands = []
        commands.append(f'impacket-smbserver -smb2support -username {self.defaultUserName} -password {self.defaultPassword} {self.defaultShareName} {self.defaultSharePath}')
        return commands

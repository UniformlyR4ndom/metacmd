
from command.Command import Command
from Util import getarg

class CommandHydra(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)

    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['hydra']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'hydra <help|ftp|rdp|snmp|ssh|telnet> <args>'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        def getExtendedHelp():
            commonArgs = '<ip> <user-spec> <pw-spec> [<port>]'
            helpLines = []
            for proto in ['ftp', 'rdp', 'ssh', 'telnet']:
                helpLines.append(f'hydra {proto} {commonArgs}')
            
            helpLines.append('hydra snmp <community-spec> [<port>]')
            return sorted(helpLines)

        def _genCommandGeneric(host, proto, userSpec, pwSpec, port, threads=''):
            commands = []
            commands.append('# Attack single user')
            commands.append(f"hydra -l '{userSpec}' -P {pwSpec} -s {port} {threads}{host} {proto}")
            commands.append('')
            commands.append('# Spray single password')
            commands.append(f"hydra -L {userSpec} -p '{pwSpec}' -s {port} {threads}{host} {proto}")
            commands.append('')
            commands.append('# Attack multiple users')
            commands.append(f'hydra -L {userSpec} -P {pwSpec} -s {port} -u {threads}{host} {proto}')
            return commands

        if len(args) < 1:
            return getExtendedHelp()

        if 'help' in args[0]:
            return getExtendedHelp()

        proto = args[0]

        if len(args) < 3:
            return getExtendedHelp()

        host = args[1]
        userSpec = args[2]

        if proto == 'snmp':
            pwSpec = args[2]
            port = (' -s ' + getarg(args, 3)) if getarg(args, 3) else ' -s 161'
            commands = []
            commands.append('# Bruteforce community strings ()')
            commands.append(f'hydra -P {pwSpec}{port} {host} snmp')
            return commands


        if len(args) < 4:
            return [self.getHelp()]

        pwSpec = args[3]
        port = getarg(args, 4)

        if proto == 'ftp':
            return _genCommandGeneric(host, 'ftp', userSpec, pwSpec, port or 21)

        if proto == 'rdp':
            return _genCommandGeneric(host, 'rdp', userSpec, pwSpec, port or 3389)

        if proto == 'ssh':
            return _genCommandGeneric(host, 'ssh', userSpec, pwSpec, port or 22, threads='-t 4 ')

        if proto == 'telnet':
            return _genCommandGeneric(host, 'telnet', userSpec, pwSpec, port or 23)

        return getExtendedHelp()
        

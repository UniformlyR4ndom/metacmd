from Command import Command
from Util import getarg

class CommandSnmpwalk(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)
        snmpwalkConfig = config['commands']['snmpwalk']
        self.defaultVersion = snmpwalkConfig['defaultVersion']


    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['snmpwalk', 'snmpbulkwalk']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'snmpwalk <ip> <ommunity-string> [<version>]'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        if len(args) < 2:
            return [self.getHelp()]

        targetHost = args[0]
        communityString = args[1]
        version = getarg(args, 2) or self.defaultVersion
        logfile = f'smnpinfo-v{version}-{targetHost}.log'

        commands = []
        commands.append('# Using snmpwalk (potentially slow)')
        commands.append(f'snmpwalk -c {communityString} -v{version} -Oa {targetHost} | tee {logfile}')
        commands.append('')
        commands.append('# Using snmpbulkwalk (can be faster)')
        commands.append(f'snmpbulkwalk -c {communityString} -v{version} -Oa {targetHost} | tee {logfile}')
        commands.append('')
        commands.append('# Misc')
        commands.append('## SNMP versions')
        commands.append('try different SNMP versions (1 or 2c or 3)')
        commands.append('## Ouput hex strings raw instead of translaing to ASCII')
        commands.append('omit flag -Oa (which translates hex strings to ASCII)')
        commands.append('')
        commands.append('# Postprocessing')
        commands.append('## Extract strings')
        commands.append(f'grep \'STRING\' {logfile}')

        return commands

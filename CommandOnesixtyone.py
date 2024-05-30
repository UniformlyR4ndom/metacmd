from Command import Command
import os

class CommandOnesixtyone(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)

        seclistBase = config['wordlists']['seclistsBase']
        onesixtyoneConfig = config['commands']['onesixtyone']
        defaultLists = []
        if 'defaultLists' in onesixtyoneConfig:
            for l in onesixtyoneConfig['defaultLists']:
                if 'pathAbs' in l:
                    path = l['pathAbs']
                    defaultLists.append(path)
                elif 'seclistsPathRel' in l:
                    path = os.path.join(seclistBase, l['seclistsPathRel'])
                    defaultLists.append(path)
        self.defaultLists = defaultLists


    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['onesixtyone', '161']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'onesixtyone <ip> [<community-string-list>]'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        if len(args) < 1:
            return [self.getHelp()]

        targetHost = args[0]
        lists = [args[1]] if len(args) >= 2 else self.defaultLists

        commands = []
        for path in lists:
            commands.append(f'onesixtyone -c {path} {targetHost} -o onesixtyone-{targetHost}.log')

        commands.append('')
        commands.append('# Misc')
        commands.append('To attack list of IPs pass -i <ip-list> instead of single IP')

        return commands

from command.Command import Command
from Util import getarg

class CommandJohn(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)
        self.defaultWordlist = config['wordlists']['rockyou']


    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['john']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'john <hash-file> [<wordlist>]'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        if len(args) < 1:
            return [self.getHelp()]

        hashFile = args[0]
        wordlist = getarg(args, 1) or self.defaultWordlist

        commands = []
        commands.append('# Basic usage')
        commands.append('## Cracking')
        commands.append(f'john --wordlist={wordlist} {hashFile}')
        commands.append('## List formats')
        commands.append('john --list=formats')
        commands.append('')
        commands.append('# Custom hash formats')
        commands.append('## Involving constants (dot used for concatenation)')
        commands.append(f'john --format=dynamic=\'md5($c1.$p),c1=myConstant1337\' --wordlist={wordlist} {hashFile}')
        commands.append('## Involving seed (hash format: <hash>$<seed>')
        commands.append(f'john --format=dynamic=\'md5($s.$p)\' --wordlist={wordlist} {hashFile}')

        return commands

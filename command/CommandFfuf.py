import os

from command.Command import Command
from Util import getarg

class CommandFfuf(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)
        ffufConfig = config['commands']['ffuf']
        seclistBase = config['wordlists']['seclistsBase']
        defaultLists = []
        if 'defaultLists' in ffufConfig:
            for l in ffufConfig['defaultLists']:
                if 'pathAbs' in l:
                    path = l['pathAbs']
                    tag = l['tag'] if 'tag' in l else ''
                    flags = l['flags'] if 'flags' in l else []
                    defaultLists.append((path, tag, flags))
                elif 'seclistsPathRel' in l:
                    path = os.path.join(seclistBase, l['seclistsPathRel'])
                    tag = l['tag'] if 'tag' in l else ''
                    flags = l['flags'] if 'flags' in l else []
                    defaultLists.append((path, tag, flags))
        self.defaultLists = defaultLists


    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        ffufTriggers = ['ffuf', 'fuzz']
        return any(word in triggerLower for word in ffufTriggers)


    def getHelp(self) -> str:
        return 'ffuf <url> [<wordlist>] [<naming-tag>]'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        if len(args) < 1:
            return [self.getHelp()]

        url = args[0]
        optWordlist = getarg(args, 1)
        optTag = getarg(args, 2) or ''
        optFlags = args[3:]

        if optWordlist:
            wordlists = [(optWordlist, optTag, optFlags)]
        else:
            wordlists = self.defaultLists
        
        commands = []
        for wl, tag, flags in wordlists:
            flagsStr = ' ' + ' '.join(flags) if flags else ''
            if not 'FUZZ' in url:
                if not url.endswith('/'):
                    url += '/'
                fuzzURL = f'{url}FUZZ'
            else:
                fuzzURL = url

            urlFriendly = fuzzURL.replace('://', '-').replace('/', '-').replace(':', '-')
            tag = '-' + tag if tag else ''
            commands.append(f'ffuf -u {fuzzURL} -w {wl}{flagsStr} -mc all -fc 404 -of html -o {urlFriendly}{tag}.html')

        return commands

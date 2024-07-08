from command.Command import Command
from Util import getarg

class CommandIptables(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)


    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['iptables']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'iptables'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        exampleRange = '10.10.11.0/24'
        exampleInterface = 'eth0'
        exampleRedirectDstOrig = '10.10.4.8'
        exampleRedirectDstPortOrig = '443'
        exampleRedirectDstMod = '102.168.5.9'
        exampleRedirectDstPortMod = '8443'

        commands = []

        commands.append(f'# Policies (default rules)')
        commands.append(f'## Drop all incoming traffic by default')
        commands.append(f'iptables -P INPUT DROP')
        commands.append(f'## Allow all outgoing traffic by default')
        commands.append(f'iptables -P OUTPUT ACCEPT')
        commands.append('')

        commands.append('# Drop traffic')
        commands.append(f'## Drop all incoming traffic from {exampleRange} (across all interfaces or specify incoming interface with -i)')
        commands.append(f'iptables -A INPUT -i {exampleInterface} -j DROP')
        commands.append(f'iptables -A INPUT -s {exampleRange} -j DROP')
        commands.append(f'iptables -A INPUT -i {exampleInterface} -s {exampleRange} -j DROP')
        commands.append(f'## Drop all outgoing traffic to {exampleRange} (acrsss all interfaces or specify outgoing interface with -o)')
        commands.append(f'iptables -A OUTPUT -i {exampleInterface} DROP')
        commands.append(f'iptables -A OUTPUT -d {exampleRange} -j DROP')
        commands.append(f'iptables -A OUTPUT -o {exampleInterface} -d {exampleRange} -j DROP')
        commands.append('')

        commands.append('# Allow traffic (analogous to drop)')
        commands.append(f'## Allow all incoming traffic from {exampleRange} (across all interfaces or specify incoming interface with -i)')
        commands.append(f'iptables -A INPUT -i {exampleInterface} -j ACCEPT')
        commands.append(f'iptables -A INPUT -s {exampleRange} -j ACCEPT')
        commands.append(f'iptables -A INPUT -i {exampleInterface} -s {exampleRange} -j ACCEPT')
        commands.append(f'## Allow all outgoing traffic to {exampleRange} (acrsss all interfaces or specify outgoing interface with -o)')
        commands.append(f'iptables -A OUTPUT -i {exampleInterface} ACCEPT')
        commands.append(f'iptables -A OUTPUT -d {exampleRange} -j ACCEPT')
        commands.append(f'iptables -A OUTPUT -o {exampleInterface} -d {exampleRange} -j ACCEPT')
        commands.append('')

        commands.append('# Redirect traffic')
        commands.append(f'iptables -t nat -A PREROUTING -p tcp -d {exampleRedirectDstOrig} --dport {exampleRedirectDstPortOrig} -j DNAT --to-destination {exampleRedirectDstMod}:{exampleRedirectDstPortMod}')

        return commands


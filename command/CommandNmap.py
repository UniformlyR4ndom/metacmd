import os

from command.Command import Command
from Util import getarg

class CommandNmap(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)
        conf = config['commands']['nmap']
        self.defaultScanTcp = conf['tcp']['defaultScan']
        self.defaultPortSpecTcp = conf['tcp']['defaultPortSpec']
        self.defaultFlagsTcp = conf['tcp']['defaultFlags']
        self.defaultScanUdp = conf['udp']['defaultScan']
        self.defaultPortSpecUdp = conf['udp']['defaultPortSpec']
        self.defaultFlagsUdp = conf['udp']['defaultFlags']


    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['nmap', 'portscan']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'nmap <target> [<port-spec>]'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        def _genPortTag(scan, portSpec):
            scanTag = scan[1:] if scan.startswith('-') else scan
            if portSpec == '-p-':
                portSpec = 'full'
            elif '--top-ports' in portSpec:
                portSpec = f'top{portSpec.split(" ", 2)[1]}'
            else:
                portSpec = portSpec.replace(' ', '').replace('-p', '')
            return f'{scanTag}-{portSpec}'

        if len(args) < 1:
            return [self.getHelp()]

        target = args[0]
        targetPrefix = '-iL ' if os.path.isfile(target) else ''

        portspecTcp = portspecUdp = getarg(args, 1)
        portspecTcp = f'-p {portspecTcp}' if portspecTcp else self.defaultPortSpecTcp
        portspecUdp = f'-p {portspecUdp}' if portspecUdp else self.defaultPortSpecUdp

        porttagTcp = _genPortTag(self.defaultScanTcp, portspecTcp)
        porttagUdp = _genPortTag(self.defaultScanUdp, portspecUdp)

        flagsTcp = ' ' + ' '.join(self.defaultFlagsTcp) if self.defaultFlagsTcp else ''
        flagsUdp = ' ' + ' '.join(self.defaultFlagsUdp) if self.defaultFlagsUdp else ''

        targetTag = target.replace('/', '-').replace(':', '-')
        portsTCPLanSmall = '21,22,80,88,443,445,8080,1433,2049'
        portsTCPLanBig = '21,22,23,25,80,88,443,445,1099,1311,1433,1521,2049,2381,2483,3300,3306,3389,5000,5432,5500,5555,5800,8080,8081,8443,8089,9443'

        commands = []
        commands.append('# TCP')
        commands.append(f'sudo nmap {self.defaultScanTcp}{flagsTcp} {portspecTcp} -oA tcp-{porttagTcp}-{targetTag} {targetPrefix}{target}')
        commands.append('## Useful ports for internal scans (LAN)')
        commands.append(f'sudo nmap {self.defaultScanTcp}{flagsTcp} -p {portsTCPLanSmall} -oA tcp-lanports-small-{targetTag} {targetPrefix}{target}')
        commands.append(f'sudo nmap {self.defaultScanTcp}{flagsTcp} -p {portsTCPLanBig} -oA tcp-lanports-big-{targetTag} {targetPrefix}{target}')
        commands.append('')
        commands.append('# UDP')
        commands.append(f'sudo nmap {self.defaultScanUdp}{flagsUdp} {portspecUdp} -oA udp-{porttagUdp}-{targetTag} {targetPrefix}{target}')
        commands.append('## Useful ports for internal scans (LAN)')
        commands.append(f'sudo nmap {self.defaultScanUdp}{flagsUdp} -p 53,161,636 -oA udp-lanports-{targetTag} {targetPrefix}{target}')
        commands.append('')
        commands.append('# Post-processing')
        commands.append('## Get all open ports')
        commands.append("awk '/Host/ && /open/' <nmap_output.gnmap> | grep -o 'Ports:.*$' | grep -o '\\s[0-9]*/open' | sort -nu | tr -d '/ open' | sed -z 's/\\n/,/g;s/,$//g' ")
        commands.append('## Convert to html (using xsltproc)')
        commands.append('xsltproc <nmap_output.xml> -o <nmap_output.html>')
        return commands


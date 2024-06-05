#!/usr/bin/env python3
import os
import sys
import pathlib

from Util import readConfig
from command.Command import Command
from command.CommandChisel import CommandChisel
from command.CommandFfuf import CommandFfuf
from command.CommandHydra import CommandHydra
from command.CommandImpacketGetNPUsers import CommandImpacketGetNPUsers
from command.CommandImpacketGetUserSPNs import CommandImpacketGetUserSPNs
from command.CommandImpacketLookupsid import CommandImpacketLookupsid
from command.CommandImpacketSmbserver import CommandImpacketSmbserver
from command.CommandJohn import CommandJohn
from command.CommandLigolong import CommandLigolong
from command.CommandNmap import CommandNmap
from command.CommandNxcMssql import CommandNxcMssql
from command.CommandNxcSmb import CommandNxcSmb
from command.CommandOnesixtyone import CommandOnesixtyone
from command.CommandStabilizeShell import CommandStabilizeShell
from command.CommandSnmpwalk import CommandSnmpwalk


BASE_PATH = pathlib.Path(__file__).parent.resolve() 
CONFIG_NAME = 'config.json'


def gencmdImpacketSmbserver() -> list[str]:
    return ['impacket-smbserver -smb2support -username p -password p share share']


def main():
    configPath = os.path.join(BASE_PATH, CONFIG_NAME)
    config = readConfig(configPath)

    commands : list[Command] = []
    commands.append(CommandChisel('chisel', config, ['chisel', 'forward', 'socks']))
    commands.append(CommandFfuf('ffuf', config, ['ffuf', 'fuzz', 'web', 'enum', 'directory', 'brute']))
    commands.append(CommandHydra('hydra', config, ['hydra', 'bruteforce']))
    commands.append(CommandImpacketGetNPUsers('impacket-getnpusers', config, ['impacket-getnpusers', 'getnpusers', 'npusers', 'asreproast', 'roast']))
    commands.append(CommandImpacketGetUserSPNs('impacket-getuserspns', config, ['impacket-getuserspns', 'getuserspns', 'userspns', 'uspns', 'kerberoast', 'roast']))
    commands.append(CommandImpacketLookupsid('impacket-lookupsid', config, ['impacket-lookupsid', 'lookupsid', 'sid']))
    commands.append(CommandImpacketSmbserver('impacket-smbserver', config, ['impacket-smbserver', 'smbserver']))
    commands.append(CommandJohn('john', config, ['john', 'crack', 'pass', 'brute']))
    commands.append(CommandLigolong('ligolong', config, ['ligolo', 'pivot']))
    commands.append(CommandNmap('nmap', config, ['nmap', 'portscan']))
    commands.append(CommandNxcMssql('nxc-mssql', config, ['nxc', 'netexec', 'nxc-mssql', 'cme', 'crackmapexec', 'cme-mssql']))
    commands.append(CommandNxcSmb('nxc-smb', config, ['nxc', 'netexec', 'nxc-smb', 'cme', 'crackmapexec', 'cme-smb']))
    commands.append(CommandOnesixtyone('onesixtyone', config, ['onesixtyone', '161', 'snmp', 'bruteforce']))
    commands.append(CommandSnmpwalk('snmpwalk', config, ['snmpwalk', 'snmpbulkwalk', 'snmp']))
    commands.append(CommandStabilizeShell('stabilize-shell', config, ['stabilize-shell', 'upgrade-shell']))

    first = sys.argv[1].lower()
    if any(first == s for s in ['l', 'list', 'h', 'help']):
        lines = []
        for cmd in commands:
            lines.append(cmd.getHelp())
        print('\n'.join(sorted(lines)))
        return 

    if any(first == s for s in ['s', 'search']):
        if len(sys.argv) < 3:
            print(f'Usage: {sys.argv[0]} search <searchtern>')
            return
        searchterm = sys.argv[2]
        for cmd in commands:
            if any((searchterm in tag) or (tag in searchterm) for tag in cmd.tags):
                print(cmd.getHelp())
        return

    matchingCommands = [cmd for cmd in commands if cmd.matchesTrigger(first)]
    if not matchingCommands:
        print(f'{first} matches no known command. List supported commands with python3 {sys.argv[0]} l')
        return

    if len(matchingCommands) > 1:
        print(f'{first} matches multiple commands. Please be more specific.')
        print('\n'.join([cmd.getHelp() for cmd in matchingCommands]))
        return

    print('\n'.join(matchingCommands[0].genCommands(first, sys.argv[2:])))

if __name__ == "__main__":
    main()

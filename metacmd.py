#!/usr/bin/env python3
import os
import sys
import pathlib

from Util import readConfig
from Command import Command
from CommandFfuf import CommandFfuf
from CommandImpacketGetNPUsers import CommandImpacketGetNPUsers
from CommandImpacketGetUserSPNs import CommandImpacketGetUserSPNs
from CommandImpacketSmbserver import CommandImpacketSmbserver
from CommandLigolong import CommandLigolong
from CommandNmap import CommandNmap
from CommandChisel import CommandChisel
from CommandStabilizeShell import CommandStabilizeShell
from CommandOnesixtyone import CommandOnesixtyone


BASE_PATH = pathlib.Path(__file__).parent.resolve() 
CONFIG_NAME = 'config.json'


def gencmdImpacketSmbserver() -> list[str]:
    return ['impacket-smbserver -smb2support -username p -password p share share']



def main():
    configPath = os.path.join(BASE_PATH, CONFIG_NAME)
    config = readConfig(configPath)

    commands : list[Command] = []
    commands.append(CommandFfuf('ffuf', config, ['ffuf', 'fuzz', 'web', 'enum', 'directory', 'brute']))
    commands.append(CommandNmap('nmap', config, ['nmap', 'portscan']))
    commands.append(CommandLigolong('ligolong', config, ['ligolo', 'pivot']))
    commands.append(CommandImpacketGetNPUsers('impacket-getnpusers', config, ['impacket-getnpusers', 'getnpusers', 'npusers', 'asreproast', 'roast']))
    commands.append(CommandImpacketGetUserSPNs('impacket-getuserspns', config, ['impacket-getuserspns', 'getuserspns', 'userspns', 'uspns', 'kerberoast', 'roast']))
    commands.append(CommandImpacketSmbserver('impacket-smbserver', config, ['impacket-smbserver', 'smbserver']))
    commands.append(CommandChisel('chisel', config, ['chisel', 'forward', 'socks']))
    commands.append(CommandStabilizeShell('stabilize-shell', config, ['stabilize-shell', 'upgrade-shell']))
    commands.append(CommandOnesixtyone('onesixtyone', config, ['onesixtyone', '161', 'snmp', 'bruteforce']))

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

    for cmd in commands:
        if cmd.matchesTrigger(first):
            print('\n'.join(cmd.genCommands(first, sys.argv[2:])))
            break
    

if __name__ == "__main__":
    main()

import platform
import socket
import psutil


def size(byte):

    symbol = ['', 'K', 'M', 'G', 'T', 'P', 'E']

    for i in symbol:

        if byte < 1024:
            return f'{round(byte)} {i}B'

        byte /= 1024


def check():

    result = f'{socket.gethostname()} - {platform.uname().system + ' ' + platform.uname().release}'

    return result


def storage():
    pass


def info():

    details = f'''
+----------------+
|Platform Details|
+----------------+

Host Name            : {socket.gethostname()}
OS                   : {platform.uname().system}
Release              : {platform.uname().system + ' ' + platform.uname().release}
Version              : {platform.uname().version}
Machine Architecture : {platform.uname().machine}

+----------------+
|Hardware Details|
+----------------+

CPU          : {platform.uname().processor}
RAM          : {size(psutil.virtual_memory().total)}
Disk Space   : {size(psutil.disk_usage('C://').total)}
'''

    return details

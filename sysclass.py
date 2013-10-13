import socket
import string
import sys

newgame = "Good stuff, let's start a game. Signups are now open"
game = 0

def parsecommand(dataarg):
    privdata = dataarg
    privsplit = dataarg.split()
    userinfo = privsplit[0]
    messagetype = privsplit[1]
    messagelocation = privsplit[2]
    command = privsplit[3]
    if len(privsplit) > 4:
        parameters = privsplit[4]
    else:
        parameters = ""

    if command.find (b'!#commandtest') != -1:
        if userinfo.find (b'Palmar.users.quakenet.org') != -1 or userinfo.find (b'palamrg') != -1:
            print(userinfo)
            print(messagetype)
            print(messagelocation)
            print(command)
            print(parameters)
        else:
            print("you're not the boss of me nigga")

    elif command.find (b'!#startgame') != -1:
        irc.send(bytes("PRIVMSG %s %s\r\n" % (messagelocation, newgame), "UTF-8" ))
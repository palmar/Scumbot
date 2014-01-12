import socket
import string
import sys
from mafiaplayer import mafiaplayer
import random

#Define Bot Parameters

network = 'irc.quakenet.org'
port = 6667

nick = "Scumbot"
ident = "Scumbot"
realname = "Scumbot"
password = "none"
channel = "<#insertchannelhere>"
owner = "Palmar"


#defining game messages

newgame = "Good stuff, let's start a game. Signups are now open type !#in to join"
gameinprogress = "Sorry there is already a game in progress"
testjoinmessage = "whatup"
gamesstartingmessage = "The game is either full, or you have already signed up."
gamenotfullmessage = "The game is not full you cannot start it"
youarealreadysignedinmessage = "Sorry, but you have already signed up for this game"
gamestartingmessage2 = "The game has now started, Good Luck!"
nightvoteerror = "You cannot vote during the night!"
lynchmessage = "Someone has been lynched hahahahahhaa"
notplayingerror = "Dude you're not even in the game"
gameovermafiawins = "The game is now over, the mafia has won!"
gameovertownwins = "The game is now over, the town has won!"

#defining game variables

game = 0
gamefinished = 0
mafiacount = 0
towniecount = 0
playercount = 0
maxplayers = 3
gamefull = 0
daystatus = 0
day = 0
night = 0
playerlist = []
objectplayerlist = []

#make irc connection

def connectToIrc(network, port, ident, realname):
    irc = socket.socket ( )
    irc.connect ((network, port))

    dataonconnect = irc.recv ( 4096 )
    if dataonconnect.find (b'PING' ) != -1:
        irc.send ( b'PONG ' + dataonconnect.split() [ 1 ] + b'\r\n' )

    irc.send(bytes("NICK %s\r\n" % nick, "UTF-8" ))
    irc.send(bytes("User %s %s bla :%s\r\n" % (ident, network, realname), "UTF-8" ))

    return irc

class ircMessage:
    def __init__ (self, message):
        try:
            self.parsemessage(message)
        except:
            pass
    def parsemessage(self, message):
        split = message.split()
        userinfo = split[0]
        messagetype = split[1]

        tostringuserinfo = userinfo.decode()
        setattr(self, 'userinfo', tostringuserinfo)
        tempusername = tostringuserinfo.split("!")
        part1username = tempusername[0]
        temp2username = part1username.split(":")
        if len(temp2username) > 1:
            actualusername = temp2username[1]
            setattr(self, 'username', actualusername)
    
        if len(split) > 2:
            messagelocation = split[2]
            strmessagelocation = messagelocation.decode()
            setattr(self, 'messagelocation', strmessagelocation)
        if len(split) > 3:
            command = split[3]
            tempstrcommand = command.decode()
            strcommand = tempstrcommand[1:]
            setattr(self, 'command', strcommand)
        if len(split) > 4:
            parameters = split[4]
            strparameters = parameters.decode()
            setattr(self, 'parameter', strparameters)

#run part

irc = connectToIrc(network, port, ident, realname)

while True: 

    data = irc.recv ( 4096 )
    message = ircMessage(data)

    # Here begins the command section. PING response is mandatory for IRC

    if data.find ( b'PING' ) != -1:
        irc.send ( b'PONG ' + data.split() [ 1 ] + b'\r\n' )

    # A few management  commands. This is only for the administrator of the bot
    ##TODO: change the admin from hard-code to use a list.
    if not hasattr(message, 'command'):
        pass
    
    elif message.command == "!#commandtest":
        if message.username == owner:
            print(message.username)
            if hasattr(message, 'command'):
                print(message.command)
            print(message.messagelocation)
            if hasattr(message, 'parameter'):
                print(message.parameter)
        else:
            print("you're not the boss of me")
  
  #Owner call fixed, but still somewhat vulnerable. Need to use hostname too.
    elif message.command == "!#join":
        if message.username == owner:
            irc.send(bytes("JOIN %s\r\n" % (message.parameter), "UTF-8" ))
            channel = message.parameter
   
    elif message.command == "!#forceclose":
        if message.username == owner:
            break
    
    #this is where the magic happens
    elif message.command == "!#startgame":
        if message.username == owner:

            if game == 0:
                irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, newgame), "UTF-8" ))
                try:
                    maxplayers = int(message.parameter)
                    gamestart = "" + message.username + " has started a game with " + str(maxplayers) + " spots."
                    irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, gamestart), "UTF-8" ))
                    game = 1
                except:
                    pass
                channel = message.messagelocation
            else: 
                irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, gameinprogress), "UTF-8"))

    elif message.command == "!#forcegameend":
        game = 0
        playerlist = []
        playercount = 0
        day = 0
        night = 0

    elif message.command == "!#in":
        if len(playerlist) < maxplayers and game == 1 and message.username not in playerlist:     
            playerlist.append(message.username)
            playerspecificmessage = message.username + " has joined the game"
            irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, playerspecificmessage), "UTF-8"))
            playercount = len(playerlist)    
        
            if len(playerlist) == maxplayers:
                randomizedlist = list(playerlist)
                currentplayerlist = list(playerlist)
                random.shuffle(randomizedlist, random.random)
                irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, gamestartingmessage2), "UTF-8"))
            
                objectplayerlist = []
                n = 0

                for item in randomizedlist:
                    item = mafiaplayer();
                    item.setplayername(randomizedlist[n])
                    objectplayerlist.append(item)
                    n = n+1
                    if n <= len(randomizedlist)/3:
                        item.setmafia()

                daystatus = 1
                day = 1

                for item1 in objectplayerlist:
                    irc.send(bytes("PRIVMSG %s :%s\r\n" % (item1.getname(), item1.tostring()), "UTF-8"))
        else:
            irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, gamesstartingmessage), "UTF-8"))
            
    
    elif message.command == "!#listplayers":
        if day == 0:
            irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, playerlist), "UTF-8"))
        else:
            returnlist = []
            for item in objectplayerlist:
                returnlist.append(item.getname())
                random.shuffle(returnlist, random.random)
            irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, returnlist), "UTF-8"))


    elif message.command == "!#vote":
        if message.parameter not in playerlist:
            irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, notplayingerror), "UTF-8"))
        elif daystatus == 0:
            irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, nightvoteerror), "UTF-8"))
        else:
            testtext2 = "" + message.username + " has voted for: " + message.parameter
            
            for item in objectplayerlist:
                if item.getname() == message.username:
                    item.setvotes(message.parameter)
                    irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, testtext2), "UTF-8"))

            votecount = 0

            for item in objectplayerlist:
                item.resetvote()

            for item in objectplayerlist:
                if item.votes == message.parameter:
                   votecount = votecount + 1

            for item in objectplayerlist:
                if item.getname() == message.parameter:
                    item.votecount(votecount)

            for item in objectplayerlist:
                if item.getname() == message.parameter:
                    infovotecounttext2 = "" + item.getname() + " now has " + str(item.lynchvotes) + " votes against him"
                    irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, infovotecounttext2), "UTF-8"))

            for item in objectplayerlist:
                if item.lynchvotes > len(objectplayerlist)/2:
                    lynchmessage2 = "" + item.name + " has been lynched. He was " + item.alignment
                    irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, lynchmessage2), "UTF-8"))
                    item.kill()
                    daystatus = 0
                    night = night + 1
                    objectplayerlist[:] = [itemj for itemj in objectplayerlist if itemj.status == "Alive"]

                    mafiacount = 0
                    playercount = 0
                    for item2 in objectplayerlist:
                        playercount = len(objectplayerlist)
                        if item2.alignment == "Mafia":
                            mafiacount = mafiacount + 1

                    if mafiacount >= (playercount/2):
                        irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, gameovermafiawins), "UTF-8"))
                    elif mafiacount == 0:
                        irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, gameovertownwins), "UTF-8"))
                    else:
                        nightmessage = "It is now night: " + str(night) + ". Please send in your night actions."
                        irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, nightmessage), "UTF-8"))

    elif message.command == "!#nightkill":
        if message.messagelocation == nick:                
            for item in objectplayerlist:
                if item.name == message.username:
                    if item.alignment == "Mafia":
                        for item2 in objectplayerlist:
                            if item2.name == message.parameter:
                                item2.kill()
                                daystatus = 1
                                day = day + 1
                                objectplayerlist[:] = [itemj for itemj in objectplayerlist if itemj.status == "Alive"]

                                lynchmessage3 = "" + item2.name + " has been murdered in the night. He was " + item2.alignment
                                irc.send(bytes("PRIVMSG %s :%s\r\n" % (channel, lynchmessage3), "UTF-8"))

                                mafiacount = 0
                                playercount = 0

                                for item3 in objectplayerlist:
                                    playercount = len(objectplayerlist)
                                    if item3.alignment == "Mafia":
                                        mafiacount = mafiacount + 1

                                if mafiacount >= (playercount/2):
                                    irc.send(bytes("PRIVMSG %s :%s\r\n" % (channel, gameovermafiawins), "UTF-8"))
                                elif mafiacount == 0:
                                    irc.send(bytes("PRIVMSG %s :%s\r\n" % (channel, gameovertownwins), "UTF-8"))
                                else:
                                    daymessage = "It is now day: " + str(day) + " Good Luck! " #+ len(objectplayerlist) + " players alive it takes " + str(math.ceil(len(objectplayerlist/2))) + " votes to lynch." 
                                    irc.send(bytes("PRIVMSG %s :%s\r\n" % (channel, daymessage), "UTF-8"))
                    else:
                        yourenotmafiamessage = "you're not even part of the Mafia"
                        if item.getname() == message.username:
                            irc.send(bytes("PRIVMSG %s :%s\r\n" % (item.getname(), yourenotmafiamessage), "UTF-8"))
        else:
            killsonlyinpmerror = "nightkills should only be sent using PM"
            irc.send(bytes("PRIVMSG %s :%s\r\n" % (message.messagelocation, killsonlyinpmerror), "UTF-8"))
    print(data)
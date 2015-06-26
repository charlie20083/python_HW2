# telnet program example
from getpass import getpass 
import socket, select, string, sys
 
def prompt() :
    sys.stdout.write('\r> ')
    sys.stdout.flush()
 
#main function
if __name__ == "__main__":
     
    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port'
        sys.exit()

    logincount=0
    nonlogin=1
    userid=0
    islistuser=0

    while (nonlogin):
        account=raw_input("User account :")
        password=getpass()

        if account=='John' :
            if password=='12345678':
                 print "Welcome, John"
                 nonlogin=0
                 userid=1
        elif account=='Mary' :
            if password=='87654321':
                 print "Welcome, Mary"
                 nonlogin=0
                 userid=2
        elif account=='ccy99u' :
            if password=='edde4969' :
                 print "Welcome, ccy99u"
                 nonlogin=0
                 userid=3

     
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()

    s.send(str(userid) + " online")
     
#   print 'Connected to remote host. Start sending messages\n'

    prompt()

    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
#                   print data[2:10]
#                   print data
                    if data[3:9]=='online':
#                       print 'isonline'

			if data[1]=='1':
                            print '\rJohn is online now'
                        elif data[1]=='2':
                            print '\rMary is online now'
                        elif data[1]=='3':
                            print '\rccy99u is online now'
                    elif data[3:10]=='offline':
#                       print 'isonline'

                        if data[1]=='1':
                            print '\rJohn is offline now'
                        elif data[1]=='2':
                            print '\rMary is offline now'
                        elif data[1]=='3':
                            print '\rccy99u is offline now'
                    elif data[2]==str(userid):
                        if data[1]==str(1):
                            print '\rJohn : ' + data[3:]
                        elif data[1]==str(2):
                            print '\rMary : ' + data[3:]
                        elif data[1]==str(3):
                            print '\rccy99u : ' + data[3:]
                    elif data[2]=='0':
                        if data[1]==str(1):
                            print '\rJohn : ' + data[3:] + ' (broadcast)'
                        elif data[1]==str(2):
                            print '\rMary : ' + data[3:] + ' (broadcast)'
                        elif data[1]==str(3):
                            print '\rccy99u : ' + data[3:] + ' (broadcast)'
                    elif data[1:9]=='userlist':
                    #   s.send('listuser')
                        if islistuser:
                            userresult = '\rCurrent online user : '
                            if int(data[9]):
                                userresult = userresult + 'John '
                            if int(data[10]):
                                userresult = userresult + 'Mary '
                            if int(data[11]):
                                userresult = userresult + 'ccy99u'
                            islistuser=0                        
                            print userresult

                    prompt()
             
            #user entered a message
            else :
                command = raw_input()
                
                smsg=''
                
                if command[0:8]=='listuser':
                    smsg='listuser'
                    islistuser=1
                elif command[0:9]=='Broadcast':
                    target=0
                    smsg=str(userid) + '0' + command[10:]
                elif command[0:4]=='Talk':
                    if command[5:9]=='John':
                        target=1
                        smsg=str(userid) + str(target) + command[10:]
                    elif command[5:9]=='Mary':
                        target=2
                        smsg=str(userid) + str(target) + command[10:]
                    elif command[5:11]=='ccy99u':
                        target=3
                        smsg=str(userid) + str(target) + command[12:]
                elif command[0:4]=="exit":
                    s.send(str(userid) + " offline")
                    s.close()
                    sys.exit()

                s.send(smsg)
#                tempdata=sock.recv(4096)
#                print tempdata
                prompt();


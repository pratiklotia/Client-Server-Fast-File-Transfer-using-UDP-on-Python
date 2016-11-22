'''
Created on Sep 17, 2016

@author: prati
'''
import socket
import time
import os
import sys


def checkArg():
    """this works omly if executed from command prompt window, it is not designed to work on
    eclipse platform, since by default, len(sys.argv)=1 & therefore the below condition will
    always be displayed as true"""
    if len(sys.argv) != 2:
        print(
            "ERROR. Wrong number of arguments passed. System will exit. Next time please supply 1 argument!")
        sys.exit()
    else:
        print("1 Argument exists. We can proceed further")


def checkPort():
    if int(sys.argv[1]) <= 5000:
        print(
            "Port number invalid. Port number should be greater than 5000. Next time enter valid port.")
        sys.exit()
    else:
        print("Port number accepted!")


def ServerList():
    print("Sending Acknowledgment of command.")
    msg = "Valid List command. Let's go ahead "
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Message Sent to Server.")

    print("In Server, List function")

    F = os.listdir(
        path="C:/Users/prati/workspace/Data Communications Assignment 1/FinalServer")
    """this path will work on system where server program was made.
    Pls change this path to the directory you have stored the server.py file
    """

    Lists = []
    for file in F:
        Lists.append(file)
    ListsStr = str(Lists)
    ListsEn = ListsStr.encode('utf-8')
    s.sendto(ListsEn, clientAddr)
    print("List sent from Server")


def ServerExit():

    print(
        "System will gracefully exit! Not sending any message to Client. Closing my socket!")
    s.close()  # closing socket
    sys.exit()


def ServerGet(g):
    print("Sending Acknowledgment of command.")
    msg = "Valid Get command. Let's go ahead "
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Message Sent to Client.")

    print("In Server, Get function")

    if os.path.isfile(g):
        msg = "File exists. Let's go ahead "
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)
        print("Message about file existence sent.")

        c = 0
        sizeS = os.stat(g)
        sizeSS = sizeS.st_size  # number of packets
        print("File size in bytes:" + str(sizeSS))
        NumS = int(sizeSS / 4096)
        NumS = NumS + 1
        tillSS = str(NumS)
        tillSSS = tillSS.encode('utf8')
        s.sendto(tillSSS, clientAddr)

        check = int(NumS)
        GetRunS = open(g, "rb")
        while check != 0:
            RunS = GetRunS.read(4096)
            s.sendto(RunS, clientAddr)
            c += 1
            check -= 1
            print("Packet number:" + str(c))
            print("Data sending in process:")
        GetRunS.close()
        print("Sent from Server - Get function")

    else:
        msg = "Error: File does not exist in Server directory."
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)
        print("Message Sent.")


def ServerPut():
    print("Sending Acknowledgment of command.")
    msg = "Valid Put command. Let's go ahead "
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Message Sent to Client.")

    print("In Server, Put function")
    if t2[0] == "put":

        BigSAgain = open(t2[1], "wb")
        d = 0
        print("Receiving packets will start now if file exists.")
        #print("Timeout is 15 seconds so please wait for timeout at the end.")
        try:
            Count, countaddress = s.recvfrom(4096)  # number of packet
        except ConnectionResetError:
            print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()

        tillI = Count.decode('utf8')
        tillI = int(tillI)

        #tillI = 100
        #tillI = tillI - 2
        # s.settimeout(2)
        while tillI != 0:
            ServerData, serverAddr = s.recvfrom(4096)
            # s.settimeout(2)

            #BigS = open("tmp.txt", "wb")
            dataS = BigSAgain.write(ServerData)
            #BigS2 = open("tmp.txt", "r")
            #Add = BigS2.read()
            # print(Add)
            #Big = Big + Add
            # BigS2.close()
            #dataF = tmp.write(ServerData)
            # Big.append(ServerData)
            d += 1
            tillI = tillI - 1
            print("Received packet number:" + str(d))

            # tmp.close()

        #Bigstr = ''.join(map(str, Big))
        BigSAgain.close()
        print("New file closed. Check contents in your directory.")
        #Bigstr = str(Big)
        # print(Big)

        #BigSAgain = open(t2[1], "w")
        # BigSAgain.write(Big)
        # BigSAgain.close()


def ServerElse():
    msg = "Error: You asked for: " + \
        t2[0] + " which is not understood by the server."
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Message Sent.")


host = ""
checkArg()
try:
    port = int(sys.argv[1])
except ValueError:
    print("Error. Exiting. Please enter a valid port number.")
    sys.exit()
except IndexError:
    print("Error. Exiting. Please enter a valid port number next time.")
    sys.exit()
checkPort()

#port = 6000
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Server socket initialized")
    s.bind((host, port))
    print("Successful binding. Waiting for Client now.")
    # s.setblocking(0)
    # s.settimeout(15)
except socket.error:
    print("Failed to create socket")
    sys.exit()

# time.sleep(1)
while True:
    try:
        data, clientAddr = s.recvfrom(4096)
    except ConnectionResetError:
        print(
            "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
        sys.exit()
    text = data.decode('utf8')
    t2 = text.split()
    #print("data print: " + t2[0] + t2[1] + t2[2])
    if t2[0] == "get":
        print("Go to get func")
        ServerGet(t2[1])
    elif t2[0] == "put":
        print("Go to put func")
        ServerPut()
    elif t2[0] == "list":
        print("Go to List func")
        ServerList()
    elif t2[0] == "exit":
        print("Go to Exit function")
        ServerExit()
    else:
        ServerElse()

print("Program will end now. ")
quit()

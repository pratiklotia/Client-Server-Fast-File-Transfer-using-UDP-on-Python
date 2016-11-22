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
    if len(sys.argv) != 3:
        print(
            "ERROR. Wrong number of arguments passed. System will exit. Next time please supply 2 arguments!")
        sys.exit()
    else:
        print("2 Arguments exist. We can proceed further")


def checkPort():
    if int(sys.argv[2]) <= 5000:
        print(
            "Port number invalid. Port number should be greater than 5000 else it will not match with Server port. Next time enter valid port.")
        sys.exit()
    else:
        print("Port number accepted!")

checkArg()
try:
    socket.gethostbyname(sys.argv[1])
except socket.error:
    print("Invalid host name. Exiting. Next time enter in proper format.")
    sys.exit()

host = sys.argv[1]
try:
    port = int(sys.argv[2])
except ValueError:
    print("Error. Exiting. Please enter a valid port number.")
    sys.exit()
except IndexError:
    print("Error. Exiting. Please enter a valid port number next time.")
    sys.exit()

checkPort()

#host = "127.0.0.1"
#port = 6000
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Client socket initialized")
    s.setblocking(0)
    s.settimeout(15)
except socket.error:
    print("Failed to create socket")
    sys.exit()
# time.sleep(1)  # gives times for server to reach at same stage

"""
Functions like below can be created and called. However, for simplicity, we just put everything in main.
def ClientGet(a):
    ClientData, clientAddr = s.recvfrom(51200)
    text = ClientData.decode('utf8')
    print(text)

    ClientData, clientAddr = s.recvfrom(8192)
    text = ClientData.decode('utf8')
    print("hey" + text)

    if len(text) < 30:
        Data, Recv = s.recvfrom(8192)
        NewFileOpen = open(a, "wb")
        NewFileOpen.write(Data)
        NewFileOpen.close()
        print("Received File")
        
        
"""

while True:
    command = input(
        "Please enter a command: \n1. get [file_name]\n2. put [file_name]\n3. list\n4. exit\n ")

    """o get [file_name]
    o put [file_name]
    o list
    o exit"""
    CommClient = command.encode('utf-8')
    try:
        s.sendto(CommClient, (host, port))
    except ConnectionResetError:
        print(
            "Error. Port numbers are not matching. Exiting. Next time please enter same port numbers.")
        sys.exit()
    #text1 = CommClient.decode('utf-8')
    #t3 = text1.split()
    CL = command.split()
    print(
        "We shall proceed, but you may want to check Server command prompt for messages, if any.")
    # starting operations
    if CL[0] == "get":
        print("Checking for acknowledgement")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)
        print("Inside Client Get")

        try:
            ClientData2, clientAddr2 = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()

        text2 = ClientData2.decode('utf8')
        print(text2)

        if len(text2) < 30:
            if CL[0] == "get":
                BigC = open("Received-" + CL[1], "wb")
                d = 0
                try:
                    # number of paclets
                    CountC, countaddress = s.recvfrom(4096)
                except ConnectionResetError:
                    print(
                        "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
                    sys.exit()
                except:
                    print("Timeout or some other error")
                    sys.exit()

                tillC = CountC.decode('utf8')
                tillCC = int(tillC)
                print("Receiving packets will start now if file exists.")
                # print(
                #   "Timeout is 15 seconds so please wait for timeout at the end.")
                while tillCC != 0:
                    ClientBData, clientbAddr = s.recvfrom(4096)
                    dataS = BigC.write(ClientBData)
                    d += 1
                    print("Received packet number:" + str(d))
                    tillCC = tillCC - 1

                BigC.close()
                print(
                    "New Received file closed. Check contents in your directory.")

    elif CL[0] == "put":
        print("Checking for acknowledgement")
        try:
            ClientData, clientAddr = s.recvfrom(4096)
        except ConnectionResetError:
            print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)
        print("We shall start sending data.")

        if text == "Valid Put command. Let's go ahead ":
            if os.path.isfile(CL[1]):

                c = 0
                #Length = len(CL1[1])

                size = os.stat(CL[1])
                sizeS = size.st_size  # number of packets
                #sizeS = sizeS[:-1]
                print("File size in bytes: " + str(sizeS))
                Num = int(sizeS / 4096)
                Num = Num + 1
                print("Number of packets to be sent: " + str(Num))
                till = str(Num)
                tillC = till.encode('utf8')
                s.sendto(tillC, clientAddr)
                tillIC = int(Num)
                GetRun = open(CL[1], "rb")

                while tillIC != 0:

                    #Run = GetRun.read(1024)
                    Run = GetRun.read(4096)
                    # print(str(Run))
                    #CLC = CL[1].encode('utf-8')
                    # GetRun.close()
                    #propMsg = b"put" + b"|||" + CLC + b"|||" + Run
                    s.sendto(Run, clientAddr)
                    c += 1
                    tillIC -= 1
                    print("Packet number:" + str(c))
                    print("Data sending in process:")

                GetRun.close()

                print("Sent from Client - Put function")
            else:
                print("File does not exist.")
        else:
            print("Invalid.")

    elif CL[0] == "list":
        print("Checking for acknowledgement")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)

        if text == "Valid List command. Let's go ahead ":
            ClientDataL, clientAddrL = s.recvfrom(4096)
            text2 = ClientDataL.decode('utf8')
            print(text2)
        else:
            print("Error. Invalid.")

    elif CL[0] == "exit":
        print(
            "Server will exit if you have entered port number correctly, but you will not receive Server's message here.")

    else:
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Error. Port numbers not matching. Exiting. Next time enter same port numbers.")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)

print("Program will end now. ")  # though, this won't get executed.
quit()

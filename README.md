Author: Pratik Lotia

Python programs executable in v3.1 and higher versions (done on v3.4)

Usage (on 2 separate command prompt windows):
client.py "Host-address" "Port-number"
server.py "Port-number"

To check locally - enter Host address as 127.0.0.1

Note:
1. For sending and receiving chunks of data as form of packets, they are encoded
in binary format (read as binary or write as binary).
For simple text message, they are encoded in 'utf8' format
Separate encoding is not needed.
2. Buffer size for sending data in packets in 4096 KB.
3. Please remember to change the list path according to your directory. (If doing copy+paste, replace '\' by '/')
4. Number of packets sent and received are recorded so as to know if there is any packet loss. (UDP is prone to packet loss)
Ideally, since client and server both exist on same system here, there should be minimal or zero packet loss.

Files chosen to be sent & received (find inside zip file)
1. Foo1.txt (text file - 3KB)
2. Foo2.jpg (image file - 33KB)
3. Foo3.jpg (gif file - 56KB)
3. Foo4.mp3 (music file - 2350KB)


Both python files require valid number of command line arguments (CLA)
to be passed while executing them in Command Prompt (cmd). (use different cmd for server and client)
(pls change the directory in command prompt to the location where to you have stored the client and server files respectively.
The format is:
1. For Client: (in path where file is saved) client.py Hostname PortNumber
2. For Server: (in path where file is saved) server.py PortNumber 

PortNumber>5000 to be used.

Failure to enter proper type and number of arguments will result in error
and program will exit.
Also, failure to enter same port number on both sides will result in error
and program will exit.

Any data smaller than 64KB can be sent directly as one file. Since assignment asks us
to send data above 2-5KB in chunks, we set buffer size of 4KB to create chunks of that size.

The program is designed in such a way that all types of files (txt, jpg, gif, mp3, mp4) including large file can be 
sent to and received from.

Explanation is divided into multiple parts as follows:
1. Client file
2. Server file

Functions are included in the programs and they shall be explained
when they 'called' by the main program and not as we traverse
the Client and Server files.

1. Client file:

Program imports various libraries such as
socket (for creating socket)
time (for adding delay if required anywhere) #not used
os (for path finding and searching files in directory)
sys (for exiting program midway via sys.exit()) 

The checkArg() is called to check number of arguments and if 
it is invalid it will exit the program. 
The try and except alogorithm checks validity of hostname.

First CLA is assigned to host.

Try and except checks validity of port number (in terms of type)

checkPort() checks validity of port number (in terms of value)

Try and except checks validity of UDP socket created. 

#not used (Sleep gives time for 'server' to create socket and bind by that time.)

Main program starts and takes command input from user which is 
encoded and sent to server.

The command input value is split to address and call them separately.


If command is get, it will get acknowledgment from server about correctness of command.

It next receives message about validity of file existence at server.

If the message is short it understands that file exists and opens 
the file required by user.

Depending on number of packets to be received, it receives and adds data in chunks.


If command is put, it will get acknowledgment from server about correctness of command.
If file exists, it checks size and divides it in buffer size of 4096.
It will send data in number of chunks, depending on size, till it reads full data.
Delimiter was used initially, while sending small files but for larger files it isn't needed.


If command is list, it will receive the contents of list from server and
print it.

If command is exit, the server will close socket & exit gracefully.
Client won't recieve any confirmation message from server.

If command is not identified, it will let us know.







2. Server file:

Program imports various libraries such as
socket (for creating socket)
time (for adding delay if required anywhere)
os (for path finding and searching files in directory)
sys (for exiting program midway via sys.exit()) 

Host is blank and therefore can connect to any hostname of client.

The checkArg() is called to check number of arguments and if 
it is invalid it will exit the program. 

Try and except checks validity of port number (in terms of type)

checkPort() checks validity of port number (in terms of value)

Try and except checks validity of UDP socket created.

Sleep gives time for 'client' to create socket by that time.

Main program starts and recives command from client and split for identification purpose.

If command is get, it sends ACK to client, sends file in chunks if is exists. The same logic used in Put at
Client side is used here.

If command is put, it sends ACK to client, receives files in chunks. Same logic used
in Get part of Client is user here.

If command is list, it goes in its directory and adds name of each file and sends it.
Note: the path will have to be changed according to the system in which the server.py file is run.
to client

If command is exit, socket is closed and program is gracefully exited.

If command is unidentified, it will notfy accordingly.




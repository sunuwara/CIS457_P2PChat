import socket
import threading
import sys

BUFFER = 4096
ENCODING = 'UTF-8'

""" Runs the Server """
class Server:

    def __init__(self, myHost, myPort):
        self.host = myHost
        self.port = myPort
        self.run()

    def run(self):
        print(f"Server started at ({self.host}:{self.port})")
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind((self.host, self.port))

        serverSocket.listen(1)
        print ("Listening for connections...")

        (clientSocket, clientAddress) = serverSocket.accept()
        print(f"Connected to ({str(clientAddress[0])}:{int(clientAddress[1])})")

        receiveThread = threading.Thread(target=receive, args=(clientSocket, str(clientAddress[0]), int(clientAddress[1])))
        receiveThread.setDaemon(True)
        receiveThread.start()

        while True:
            send(clientSocket)

""" Runs the Client """
class Client:

    def __init__(self, otherHost, otherPort):
        self.host = otherHost
        self.port = otherPort
        self.run()

    def run(self):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Establishing connection...")

        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        clientSocket.connect((self.host, self.port))
        print(f"Connected to ({self.host}:{self.port})")

        sendThread = threading.Thread(target=send, args=(clientSocket,))
        sendThread.setDaemon(True)
        sendThread.start()

        while True:
            receive(clientSocket, self.host, self.port)

""" Sends the message through the socket """
def send(socket):
    while True:
        try:
            sendMsg = input("")
            socket.send(sendMsg.encode(ENCODING))
        except KeyboardInterrupt:
            sys.exit(0)

""" Receives the message on socket and prints it out """
def receive(socket, host, port):
    while True:
        receiveMsg = socket.recv(BUFFER)
        print(f"Friend: {receiveMsg.decode(ENCODING)}")

        if not receiveMsg:
            print(f"({host}:{port}) has disconnected")
            socket.close()
            break

""" Start program """
if __name__ == '__main__':

    # determine if arguments to run program were correct
    if(len(sys.argv) < 3):
        print("Use Command: python p2pChat.py $myhostname $myportnumber\n")
        sys.exit(0)

    # save this client hostname and port number
    myHost = sys.argv[1]
    myPort = int(sys.argv[2])

    # Establish connection or wait for someone
    print(f"Welcome ({myHost} : {myPort})!")
    print("Waiting to establish connection...")

    # Prompt whether to act as a server or a client
    otherHost = input("Enter 'wait' or the Hostname to connect to: ")

    # if 'wait' was entered then act as server and wait for connections
    if (otherHost.lower() == 'wait'):
        try:
            server = Server(myHost, myPort)
        except KeyboardInterrupt:
            print("Unable to start as server!")
            sys.exit(0)

    # otherwise run as client and connect to server acting client
    else:
        try:
            otherPort = int(input("Enter the Port Number to connect to: "))
            client = Client(otherHost, otherPort)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print("Connection Failed!")

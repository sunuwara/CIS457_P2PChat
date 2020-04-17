import socket
import threading
import sys
import time

BUFFER = 4096
ENCODING = 'UTF-8'

class Server:

    def __init__(self, myHost, myPort):
        self.host = myHost
        self.port = myPort
        self.run()

    def receive(self, socket, address):
        while True:
            receiveMsg = socket.recv(BUFFER)
            print(f"({str(address[0])}:{int(address[1])}): {receiveMsg.decode(ENCODING)}")

            if not receiveMsg:
                print(f"({str(address[0])}:{int(address[1])}) has disconnected")
                socket.close()
                break

    def run(self):
        print(f"Server started at ({self.host}:{self.port})")
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind((self.host, self.port))

        serverSocket.listen(1)
        print ("Listening for connections...")

        (clientSocket, clientAddress) = serverSocket.accept()
        print(f"Connected to ({str(clientAddress[0])}:{int(clientAddress[1])})")

        receiveThread = threading.Thread(target=self.receive, args=(clientSocket, clientAddress))
        receiveThread.setDaemon(True)
        receiveThread.start()

        while True:
            try:
                sendMsg = input("")
                clientSocket.send(sendMsg.encode(ENCODING))
            except KeyboardInterrupt:
                sys.exit(0)

class Client:

    def __init__(self, otherHost, otherPort):
        self.host = otherHost
        self.port = otherPort

        self.run()

    def send(self, socket):
        while True:
            try:
                sendMsg = input(" ")
                socket.send(sendMsg.encode(ENCODING))
            except KeyboardInterrupt:
                sys.exit(0)

    def run(self):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Establishing connection with ({self.host}:{self.port})...")

        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        clientSocket.connect((self.host, self.port))
        print(f"Connected to ({self.host}:{self.port})")

        sendThread = threading.Thread(target=self.send, args=(clientSocket,))
        sendThread.setDaemon(True)
        sendThread.start()

        while True:
            receiveMsg = clientSocket.recv(BUFFER)
            print(f"({self.host}:{self.port}): {receiveMsg.decode(ENCODING)}")

            if not receiveMsg:
                print(f"({self.host}:{self.port}) has disconnected")
                clientSocket.close()
                break

def prompt() :
	sys.stdout.write('You: ')
	sys.stdout.flush()

""" Start program """
if __name__ == '__main__':

    # determine if arguments to run program were correct
    if(len(sys.argv) < 3):
        print("Use Command: python daemon.py $myhostname $myportnumber\n")
        sys.exit(0)

    # save this client hostname and port number
    myHost = sys.argv[1]
    myPort = int(sys.argv[2])

    # Establish connection or wait for someone
    print(f"({myHost} : {myPort}) Waiting to establish connection...")

    otherHost = input("Hostname to connect to (or enter 'Wait'): ")

    if (otherHost.lower() == 'wait'):
        try:
            server = Server(myHost, myPort)
        except KeyboardInterrupt:
            sys.exit(0)

    else:
        try:
            otherPort = int(input("Port Number to connect to: "))

            client = Client(otherHost, otherPort)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print("Connection Failed!")

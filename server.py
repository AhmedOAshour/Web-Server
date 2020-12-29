# import socket module
from socket import *
from datetime import *

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
serverHost = "localhost"  # initialize host
serverPort = 8484  # initialize port
serverSocket.bind((serverHost, serverPort))  # bind to host in this case localhost (127.0.0.1) and port
serverSocket.listen(1)  # max 1 queued request

while True:
    # Establish the connection
    print("Ready to serve...\n")
    connectionSocket, addr = serverSocket.accept()  # Awaiting connection. accept returns tuple (socket, address/port)
    try:
        message = connectionSocket.recv(4096)  # max 4096 bytes
        print(message.decode("utf-8"))
        if not message:  # to avoid server crash
            continue
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        # Send one HTTP header line into socket
        requestTime = datetime.now().strftime("%Y-%m-%d %H:%M")
        responseHeader = "HTTP/1.1 200 OK"  # response header
        header = {  # create headers
            "Date": requestTime,  # date header
            "Content-Length": len(outputdata.encode("utf-8")),  # content length header
            "Content-Type": "text/html; charset=utf-8",  # content type header
        }
        httpHeader = "\r\n".join(f"{head}:{header[head]}" for head in header)
        responseMessage = f"{responseHeader}\r\n{httpHeader}\r\n\r\n"
        connectionSocket.send(responseMessage.encode("utf-8"))  # use encode to typecast from string to bytes utf-8
        print(responseMessage)

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode("utf-8"))  # send page byte by byte
        connectionSocket.close()
    except IOError:
        #   Send response message for file not found
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html><html><body><h1>404 Not Found<h1></body></html>") # response header + error html page
        print("HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html><html><body><h1>404 Not Found<h1></body></html>")
        # Close client socket
        connectionSocket.close()
serverSocket.close()

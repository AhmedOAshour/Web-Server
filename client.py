from socket import *

serverHost = "localhost"   # initialize host
serverPort = 8484  # initialize port
filename = ""  # initialize file name

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverHost, serverPort))  # connect to server
header = {
    "first_header": f"GET /{filename} HTTP/1.1",  # request header
    "Host": f"{serverHost}:{serverPort}",  # host header
    "Accept": "text/html",  # accept header
    "Accept-Language": "en-us",  # language header
}
httpHeader = "\r\n".join(f"{head}:{header[head]}" for head in header)
requestMessage = f"{httpHeader}\r\n\r\n"
clientSocket.send(requestMessage.encode("utf-8"))  # send request
print("request:\n", requestMessage)

result = ""
responseMessage = clientSocket.recv(4096)
while responseMessage:
    result += responseMessage.decode("utf-8")
    responseMessage = clientSocket.recv(4096)

clientSocket.close()
print("response: ", result)

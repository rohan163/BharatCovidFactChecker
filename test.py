import sys
import datetime
import socket

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = "%s" % (sys.argv[1])  # take input

    
    client_socket.send(message.encode())  # send message
    data = client_socket.recv(1024).decode()  # receive response

    if (data == "True"):
        sent="According To The Fact Checker The News Is:"
        sent2=""
    else :
        sent="According To The Fact Checker The News Is:"
        sent2=". We Wont Recommend You Sharing This News Further. But We Would Still Request You To Cross Check The News From An Authentic News Channel."
    
    print(sent + data + sent2)  # show in terminal

        

    #client_socket.close()  # close the connection
    

if __name__ == '__main__':
    client_program()

#output="%s" % (sys.argv[1])
#print(output)
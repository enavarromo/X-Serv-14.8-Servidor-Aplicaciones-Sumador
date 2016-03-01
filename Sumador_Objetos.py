#!/usr/bin/python
import socket
import random

# -------------- Port Set Up --------------
G_host = socket.gethostname()
G_port = 1234

class webApp:

    def parse(self, request):
        return None

    def process(self, parsedRequest):
        return ("200 OK", "<html><body><h1>It works!</h1></body></html>")

    def __init__(self, hostname, port):

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        while True:
            print ('Waiting for connections')
            (recvSocket, address) = mySocket.accept()
            print ('HTTP request received (going to parse and process):')
            request = recvSocket.recv(2048)
            print (request)
            parsedRequest = self.parse(request)
            (returnCode, htmlAnswer) = self.process(parsedRequest)
            print ('Answering back...')
            recvSocket.send("HTTP/1.1 " + returnCode + " \r\n\r\n"
                            + htmlAnswer + "\r\n")
            recvSocket.close()


class sumaApp(webApp):

    def parse(self, request):
        try:
            numero = int(request.split()[1][1:]);
            valido = True
        except ValueError:
            numero = 0
            valido = False
        return numero, valido

    def process(self, parsedRequest):
        numero, valido = parsedRequest
        if not valido:
            return('200 OK', '<html><body><h1>Solo numeros</h1></body></html>')
        if self.primero:
            self.guardado = numero
            self.primero = False
            return('200 OK', '<html><body><h1>Dame otro numero</h1></body></html>')
        else:
            resultado = self.guardado + numero
            self.primero = True
        return('200 OK', '<html><body><h1>Resultado: '+str(resultado) + '</h1></body></html>')

    def __init__(self, hostname, port):
        self.primero = True
        webApp.__init__(self,hostname, port)    # sintaxis valida en python


class divApp(sumaApp):

    def process(self, parsedRequest):
        numero, valido = parsedRequest
        if not valido:
            return('200 OK', '<html><body><h1>Solo numeros</h1></body></html>')
        if self.primero:
            self.guardado = numero
            self.primero = False
            return('200 OK', '<html><body><h1>Dame otro numero</h1></body></html>')
        else:
            if numero != 0:
                resultado = self.guardado / numero
                self.primero = True
                return('200 OK', '<html><body><h1>Resultado: '+
                        str(resultado) + '</h1></body></html>')
            else:
                return('200 OK', '<html><body><h1>No introducir 0'+
                        '</h1></body></html>')

if __name__ == "__main__":
    testWebApp = sumaApp(G_host, G_port)
    
    
    
    
    



"""
super(sumaApp, self).__init__(hostname, port) # Mala sintaxis en python 3
"""
    
    

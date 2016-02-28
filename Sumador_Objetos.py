# -*- coding: utf-8 -*-
#!/usr/bin/python
import socket
import random

"""
No se si se tragara esto, estando aqui, puede estar mal ubicado o faltarle
self. y demas...:
"""
# -------------- Port Set Up --------------
G_host = socket.gethostname()
G_port = 1234


class Utils():
    def Parse(self, Rx):
        self.Rx = Rx
        print self.Rx
        self.Rx = self.Rx.split()[1][1:]
        print "trozo: " + self.Rx
        return self.Rx

    def Process(self, ParsedRx):
        return int(ParsedRx)

class WebAdder():
    def __init__(self, hostname, port):
        """Initialize the web application."""
        # -------------- State Variable --------------
        self.Estado = 'Sumando1'
        self.host = hostname
        self.port = port
        # Create a TCP objet socket and bind it to a port
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mySocket.bind((self.host, self.port))  # '192.168.1.132', 'localhost'
        self.mySocket.listen(5) # 5 TPC Cons cap
        self.Utilities = Utils()

    def run(self):
        # -------------- Main Loop --------------
        try:
            print('Server running...\n')
            while True:
                (recvSocket, address) = self.mySocket.accept()
                self.RxParsed = self.Utilities.Parse(recvSocket.recv(1024))

                """
                Todo esto hay que ver donde lo meto; 
                Que dejo aquí y que distribuyo a process()
                La variable de Estado me monta un pollo fino...
                """
                if self.Estado == 'Sumando1':    # -------- Estado 1 --------
                    self.Sumando1 = self.Utilities.Process(self.RxParsed)
                    recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
                    "<html><body><h1>Sumador:</h1>" +
                    "<p>Primer sumando: " + str(self.Sumando1) + "</p>" +
                    "<h4>Introduzca segundo sumando</h4>"+
                    "</body></html>\r\n")
                    self.Estado = 'Sumando2'
                elif self.Estado == 'Sumando2':  # -------- Estado 2 --------
                    self.Sumando2 = self.Utilities.Process(self.RxParsed)
                    recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
                    "<html><body><h1>Sumador:</h1>" +
                    "<p>Primer sumando: " + str(self.Sumando1) + "</p>" +
                    "<p>Segundo sumando: " + str(self.Sumando2) + "</p>" +
                    str(self.Sumando1)+" + "+str(self.Sumando2)+" = "+
                    str((self.Sumando1+self.Sumando2)) +
                    "</body></html>\r\n")
                    self.Estado = 'Sumando1'
                else:
                    self.Estado = 'Sumando1'
                    
                recvSocket.close()
                """
                Hasta aqui esta la duda del process()
                """

        except KeyboardInterrupt:
            self.mySocket.close()
            print("\nExiting Ok")

if __name__ == "__main__":
    MyAPP = WebAdder(G_host, G_port)
    MyAPP.run()
    print('Server Closed')









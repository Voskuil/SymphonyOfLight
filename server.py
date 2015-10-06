import SocketServer
import lumiversepython as L
import time

rig = L.Rig("/home/teacher/Lumiverse/PBridge.rig.json")

rig.init()
rig.run()

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        self.doBridgeThings()
        self.request.sendall("Got it")
        
    def doBridgeThings(self):
        [on,panel,intenStr] = self.data.split("*")
        (a,b,c) = self.mapColor(int(panel))
        inten = int(intenStr)/120.0
        '''
        for x in xrange(57):
            if ((int(panel) == x) and int(on)):
                print "HERLJ:LKSJDF:LKJE:KL"
                rig.select("$panel=%d"%int(panel)).setColorRGBRaw("color",a,b,c,inten)
            else:
                rig.select("$panel=%d"%int(panel)).setColorRGBRaw("color",0,0,0)

        '''
        if (int(on)):
            print "goooood"
            rig.select("$panel=%d"%int(panel)).setColorRGBRaw("color",a,b,c,inten)
        else:
            rig.select("$panel=%d"%int(panel)).setColorRGBRaw("color",0,0,0)
        print "Recieved: ",self.data
        #print "a=%f, b=%f, c=%f"%(a,b,c)
        #print "inten=%f"%inten
        

    def mapColor(self,x):
        a,b,c = 0,0,0
        if (x<13):
            a = 0
            c = 1
            b = (12-x)/12.0
        elif (x<25):
            b = 0
            c = 1
            a = (x-12)/12.0
        elif (x<37):
            a = 1
            b = 0
            c = (12-(x-24))/12.0
        elif (x<49):
            a = 1
            c = 0
            b = (x-36)/12.0
        else:
            b = 1
            c = 0
            a = (12-(x-48))/12.0
        return (b,a,c)


if __name__ == "__main__":
    HOST, PORT = '', 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


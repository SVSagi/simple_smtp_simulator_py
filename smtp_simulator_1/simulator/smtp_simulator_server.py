'''
Created on Nov 27, 2014

@author: Sarraju
'''

import smtpd, threading, asyncore, time, socket

class SMTPSimulationServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        f = open(time.strftime('%d-%m-%Y_%H%M%S')+'.eml','a+b')
        print data
        f.write(data)
        f.close()
        

class ServerManager(object):
    
    smtp = None
    
    def start(self):
        if not self.canStartServer():
            print 'Cannot start Server.'
            #return
        
        self.smtp = SMTPSimulationServer(('', 25), None)
        self.thread =  threading.Thread(target=asyncore.loop,kwargs = {'timeout':1} )
        self.thread.start()
        print 'Done'     

    def stop(self):
        if self.smtp!=None and self.smtp.accepting:
            self.smtp.close()
            self.thread.join()
            print 'Stopped'
        
    def canStartServer(self):
        return self.isPortOpen()
    
    def isPortOpen(self):
        try:
            s = socket.socket()
            result = s.connect(('', 25))
            print 'Result '+result
            #s.shutdown(2)
            return True
        except socket.error, e:
            print socket.error
            print '========'
            print e
            return False        


    
    
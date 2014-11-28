'''
Created on Nov 27, 2014

@author: Sarraju
'''

import smtpd, threading, asyncore, socket, os
from datetime import datetime

last_eml = ""

class SMTPSimulationServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        self.thread =  threading.Thread(self.storeEmail(data))
        self.thread.start()
        
    def storeEmail(self, data):
        #print 'Email: '+data
        try:
            file_name = self.getFileName()+'.eml'
            f = open('emails/'+file_name,'a+b')
            f.write(data)
            f.close()
            global last_eml
            last_eml = file_name
        except Exception as e:
            print 'log it'+e
        
    def getFileName(self):
        
        fileid = 'FILENAME_GENERATION_ERROR'
        
        try:
            fileid = datetime.now().strftime('%d%m%Y%H%M%S%f')
            
            c = 0
            while os.path.exists('emails/'+fileid+'.eml') and c != 100:
                fileid = str(int(fileid) + 1)
                c += 1
            
            if c==100:
                return 'FILENAME_GENERATION_ERROR'
       
        except Exception as e:
            print e
            return 'FILENAME_GENERATION_ERROR'

        return fileid
        

class ServerManager(object):
    
    smtp = None
    
    def start(self):
        '''
        if not self.canStartServer():
            print 'Cannot start Server.'
            #return
        '''
        self.smtp = SMTPSimulationServer(('', 25), None)
        self.thread =  threading.Thread(target=asyncore.loop,kwargs = {'timeout':1} )
        self.thread.start()
        print 'Started'     

    def stop(self):
        if self.smtp!=None and self.smtp.accepting:
            self.smtp.close()
            self.thread.join()
            print 'Stopped'
        
    def canStartServer(self):
        return self.isPortOpen()
    
    def isPortOpen(self):
        result = None
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


    
    
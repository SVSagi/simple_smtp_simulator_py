'''
Created on Nov 27, 2014

@author: Sarraju
'''

import smtpd, threading, asyncore, time

class SMTPSimulationServer(smtpd.SMTPServer):
    emails = []
    def process_message(self, peer, mailfrom, rcpttos, data):
        f = open(time.strftime('%d-%m-%Y_%H%M%S')+'.eml','a+b')
        f.write(data)
        

class ServerProcess(object):
    def start(self):
        self.smtp = SMTPSimulationServer(('', 25), None)
        self.thread =  threading.Thread(target=asyncore.loop,kwargs = {'timeout':1} )
        self.thread.start()
        print 'Started'     

    def stop(self):
        self.smtp.close()
        self.thread.join()
        print 'Stopped'

    def count(self):
        return len(self.smtp.emails)        

    def get(self):
        return self.smtp.emails
    
    
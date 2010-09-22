#!/usr/bin/python

import  os
import  signal
import  socket

host = 'mx.darkzone.un'
host = 'nonesuch.host.here'
host = 'localhost'
host = '192.168.0.13'
port = 80

class   Bp( object ):
    def __init__( self, host = 'localhost' ):
        self.host           = host
        self.currently_up   = False
        self.previously_up  = False
        self.up_interval    = 60
        self.down_interval  = 30
        self.seconds        = self.down_interval
        self.connectTimeout = self.down_interval - 1
        return

    def handler( self, signum, frame ):
        raise IOError, 'Host %d not responding.' % self.host

    def poll( self ):
        try:
            self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            signal.signal( signal.SIGALRM, self.handler )
            signal.alarm( self.connectTimeout )
            try:
                self.sock.connect( self.host, self.port )
                signal.alarm( 0 )
                self.sock.close()
                self.currently_up = True
                self.seconds = self.up_interval
            except IOError, e:
                self.currently_up = False
                self.seconds      = self.down_interval
            if( not self.currently_up and self.previously_up ):
                self.osd.display(
                    'HOST %s IS NOT RESPONDING!' % self.host
                )

if __name__ == '__main__':
    clinger = Bp( host )
    clinger.poll()

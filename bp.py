#!/usr/bin/python

import  os
from    urllib2 import  *

host = 'http://mx.darkzone.un/index.html'
host = 'http://nonesuch.host.here/index.html'
host = 'http://localhost/index.html'
host = 'http://192.168.0.13/index.html'

class   Bp( object ):
    def __init__( self, url = host ):
        self.url           = url
        self.currently_up  = False
        self.up_interval   = 60
        self.down_interval = 30
        self.seconds       = self.down_interval
        return

    def poll( self ):
        try:
            u = urlopen( self.url, timeout=20 )
            print u.info()
            u.close()
            self.currently_up = True
            self.seconds = self.up_interval
        except (HTTPError, URLError), e:
            print '**** BOGUS ****'
            self.currently_up = False
            self.seconds = self.down_interval

if __name__ == '__main__':
    clinger = Bp( host )
    clinger.poll()

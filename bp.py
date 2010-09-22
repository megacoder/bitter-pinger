#!/usr/bin/python

import  os
import  pyosd
import  signal
import  socket
import  sys

host = 'mx.darkzone.un'
host = 'nonesuch.host.here'
host = 'localhost'
host = '192.168.0.13'

class   BitterPinger( object ):

    def __init__( self, host = 'localhost', port = 80 ):
        super(BitterPinger, self).__init__()
        self.host           = host
        self.port           = port
        self.currently_up   = False
        self.previously_up  = False
        self.up_interval    = 60
        self.down_interval  = 30
        self.seconds        = self.down_interval
        self.connectTimeout = self.down_interval - 1
        self.osd            = pyosd.osd(
            font='-*-helvetica-*-r-*-*-*-*-*-*-*-182-*-*',
            colour = "firebrick",
            timeout = self.seconds - 1,
            pos = pyosd.POS_TOP,
            align = pyosd.ALIGN_CENTER,
            offset = 0,
            hoffset = 0,
            shadow = 2,
            lines = 2
        )
        return

    def __del__( self ):
        self.osd.wait_until_no_display()
        return

    def handler( self, signum, frame ):
        raise IOError, 'Host %d not responding.' % self.host

    def poll( self ):
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        signal.signal( signal.SIGALRM, self.handler )
        signal.alarm( self.connectTimeout )
        try:
            self.sock.connect( (self.host, self.port) )
            signal.alarm( 0 )
            self.sock.close()
            self.currently_up = True
            self.seconds = self.up_interval
        except IOError, e:
            self.currently_up = False
            self.seconds      = self.down_interval
        if not self.currently_up:
            self.osd.set_timeout( self.seconds - 1 )
            self.osd.scroll( 1 )
            msg = 'Host %s is not responding!' % self.host
            self.osd.display(
                msg,
                type = pyosd.TYPE_STRING,
                line = self.osd.get_number_lines() - 1
            )
            print >>sys.stderr, msg
        elif self.currently_up and not self.previously_up:
            self.osd.set_timeout( self.seconds - 1 )
            self.osd.scroll( 1 )
            msg = 'Host %s responding.' % self.host
            self.osd.display(
                'Host %s responding.' % self.host,
                type = pyosd.TYPE_STRING,
                line = self.osd.get_number_lines() - 1
            )
            print >>sys.stderr, msg
        return

if __name__ == '__main__':
    clinger = BitterPinger( host )
    clinger.poll()

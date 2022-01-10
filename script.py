import xbmc
import time
import serial

class XBMCPlayer( xbmc.Player ):

    def __init__( self, *args ):
        pass

    def onPlayBackStarted( self ):
        # Will be called when xbmc starts playing a file
        xbmc.log( "LED Status: Playback Stopped, LED ON" )
        ser.write("set mode 2\r")
        ser.write("set step 1\r")
        ser.write("set rgb 0 0 0\r")
        xmbc.sleep(12)
        ser.write("set atx off\r")

    def onPlayBackEnded( self ):
        # Will be called when xbmc stops playing a file
        xbmc.log( "LED Status: Playback Stopped, LED OFF" )
        ser.write("set atx on\r")
        ser.write("set mode 1\r")
        ser.write("set step 4\r")
        ser.write("set rgb 255 255 255\r")

    def onPlayBackStopped( self ):
        # Will be called when user stops xbmc playing a file
        xbmc.log( "LED Status: Playback Stopped, LED OFF" )
        ser.write("set atx on\r")
        ser.write("set mode 1\r")
        ser.write("set step 4\r")
        ser.write("set rgb 255 255 255\r")

    def onPlayBackPaused( self ):
        # Will be called when user Pauses xbmc playing a file
        xbmc.log( "LED Status: Playback Paused, LED ON BUT STILL" )
        ser.write("set atx on\r")
        ser.write("set mode 1\r")
        ser.write("set step 2\r")
        ser.write("set rgb 100 100 100\r")

    def onPlayBackResumed( self ):
        # Will be called when user stops xbmc playing a file
        xbmc.log( "LED Status: Playback Resumed, LED ON" )
        ser.write("set mode 0\r")
        ser.write("set rgb 0 0 0\r")
        xmbc.sleep(10)
        ser.write("set atx off\r")

player = XBMCPlayer()
xbmc.log("Started Lightcontroller")
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.write("set rgb 255 0 0\n\r")
xbmc.sleep(10)
ser.write("set rgb 255 255 255\n\r")
time.sleep(10)
while(not xbmc.abortRequested):
    xbmc.sleep(100)

ser.close()
xbmc.log( "LED Status: Script Stopped" )

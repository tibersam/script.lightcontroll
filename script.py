import xbmc
from lightcontroller import LightController

class XBMCPlayer( xbmc.Player ):

    def __init__( self, *args ):
        self.lightcontroller = LightController()
        self.started_playback = False
        xbmc.log("Initialised LightController", level=xbmc.LOGINFO)
        pass

    def onAVStarted( self ):
        # Will be called when xbmc starts playing a file
        if not self.isPlayingVideo():
            return
        self.started_playback = True
        xbmc.log( "LightControll: LED Status: Playback Started, LED ON", level=xbmc.LOGINFO)
        self.lightcontroller.abortprevious()
        if self.lightcontroller.atx:
            self.lightcontroller.mode = 2
            self.lightcontroller.step = 1
            self.lightcontroller.set_rgb( 0, 0, 0)
            self.lightcontroller.set_rgb_limit( 2, 2, 2, 30, 30)
            self.lightcontroller.set_lights( False, delay=20)

    def onPlayBackEnded( self ):
        # Will be called when xbmc stops playing a file
        if self.started_playback is False:
            return
        self.started_playback = False
        xbmc.log( "LightControll: LED Status: Playback Stopped, LED OFF", level=xbmc.LOGINFO )
        self.lightcontroller.abortprevious()
        if not self.lightcontroller.atx:
            self.lightcontroller.set_lights(True)
        self.lightcontroller.mode = 1
        self.lightcontroller.step = 4
        self.lightcontroller.set_rgb( 100, 100, 100)
        self.lightcontroller.set_rgb( 255, 255, 255, delay=30)

    def onPlayBackStopped( self ):
        # Will be called when user stops xbmc playing a file
        if self.started_playback is False:
            return
        self.started_playback = False
        xbmc.log( "LightControll: LED Status: Playback Stopped, LED OFF", level=xbmc.LOGINFO )
        self.lightcontroller.abortprevious()
        if not self.lightcontroller.atx:
            self.lightcontroller.set_lights(True)
        self.lightcontroller.mode = 1
        self.lightcontroller.step = 4
        self.lightcontroller.set_rgb( 255, 255, 255)

    def onPlayBackPaused( self ):
        # Will be called when user Pauses xbmc playing a file
        if self.started_playback is False:
            return
        xbmc.log( "LightControll: LED Status: Playback Paused, LED ON BUT STILL", level=xbmc.LOGINFO )
        self.lightcontroller.abortprevious()
        if not self.lightcontroller.atx:
            self.lightcontroller.set_lights(True)
        self.lightcontroller.mode = 1
        self.lightcontroller.step = 2
        self.lightcontroller.set_rgb( 100, 100, 100)

    def onPlayBackResumed( self ):
        # Will be called when user stops xbmc playing a file
        if self.started_playback is False:
            return
        xbmc.log( "LightControll: LED Status: Playback Resumed, LED ON" )
        self.lightcontroller.abortprevious()
        if self.lightcontroller.atx:
            self.lightcontroller.mode = 0
            self.lightcontroller.set_rgb( 10, 10, 10)
            self.lightcontroller.set_lights( False, delay=5)

player = XBMCPlayer()
xbmc.log("Started Lightcontroller", level=xbmc.LOGINFO)
monitor = xbmc.Monitor()
while(not monitor.abortRequested()):
    monitor.waitForAbort(60)

del player
xbmc.sleep(10)
xbmc.log( "LightControll: LED Status: Script Stopped", level=xbmc.LOGINFO)

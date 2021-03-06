import xbmc
import xbmcaddon
from lightcontroller import LightController
import time

class XBMCPlayer( xbmc.Player ):

    def __init__( self, *args ):
        self.lightcontroller = LightController()
        self.started_playback = False
        self.last_executed = time.time() - 20
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
            if(time.time() - self.last_executed > 10):
                self.lightcontroller.set_rgb_limit( 50, 50, 50, 120, 95, mode=2, delay=4)
                self.lightcontroller.set_rgb_limit( 50, 50, 50, 350, 87, mode=1)
                self.lightcontroller.set_rgb_limit( 50, 50, 50, 0 , 10, mode=1)
                self.lightcontroller.set_lights( False, delay=20)
            else:
                self.lightcontroller.set_lights( False)
            self.lightcontroller.mode = 1
            self.last_executed = time.time()

    def onPlayBackEnded( self ):
        # Will be called when xbmc stops playing a file
        if self.started_playback is False:
            return
        self.started_playback = False
        xbmc.log( "LightControll: LED Status: Playback Stopped, LED OFF", level=xbmc.LOGINFO )
        self.lightcontroller.abortprevious()
        self.lightcontroller.mode = 0
        if not self.lightcontroller.atx:
            self.lightcontroller.set_lights(True)
        self.lightcontroller.set_rgb( 0, 0, 0)
        self.lightcontroller.mode = 1
        self.lightcontroller.step = 4
        self.lightcontroller.set_rgb( 50, 50, 50)
        self.lightcontroller.set_rgb( 255, 255, 255, delay=30)
        self.last_executed = time.time()

    def onPlayBackStopped( self ):
        # Will be called when user stops xbmc playing a file
        if self.started_playback is False:
            return
        self.started_playback = False
        xbmc.log( "LightControll: LED Status: Playback Stopped, LED OFF", level=xbmc.LOGINFO )
        self.lightcontroller.abortprevious()
        self.lightcontroller.mode = 0
        if not self.lightcontroller.atx:
            self.lightcontroller.set_lights(True)
        self.lightcontroller.set_rgb( 0, 0, 0)
        self.lightcontroller.mode = 1
        self.lightcontroller.step = 2
        self.lightcontroller.set_rgb( 255, 255, 255)
        self.last_executed = time.time()

    def onPlayBackPaused( self ):
        # Will be called when user Pauses xbmc playing a file
        if self.started_playback is False:
            return
        xbmc.log( "LightControll: LED Status: Playback Paused, LED ON BUT STILL", level=xbmc.LOGINFO )
        self.lightcontroller.abortprevious()
        if not self.lightcontroller.atx:
            self.lightcontroller.set_lights(True)
        self.lightcontroller.set_rgb( 0, 0, 0)
        self.lightcontroller.mode = 1
        self.lightcontroller.step = 2
        self.lightcontroller.set_rgb_limit( 50, 50, 50, 60, 155, mode=1)
        self.lightcontroller.set_rgb_limit( 50, 50, 50, 0 , 60, mode=2)
        self.lightcontroller.set_rgb_limit( 50, 50, 50, 350, 87, mode=1, delay=1)
        self.lightcontroller.step = 4
        self.lightcontroller.set_rgb( 150, 150, 150, delay=20)
        self.last_executed = time.time()

    def onPlayBackResumed( self ):
        # Will be called when user stops xbmc playing a file
        if self.started_playback is False:
            return
        xbmc.log( "LightControll: LED Status: Playback Resumed, LED ON" )
        self.lightcontroller.abortprevious()
        if self.lightcontroller.atx:
            self.lightcontroller.mode = 0
            self.lightcontroller.set_rgb( 20, 20, 20)
            self.lightcontroller.set_lights( False, delay=5)
            self.lightcontroller.mode=1
            self.last_executed = time.time()

def show_notification(msg, icon, title='Lightcontroller', displaytime=3000):
    xbmc.executebuiltin(f'Notification({title}, {msg}, {displaytime}, {icon})')
    
def script():
    player = XBMCPlayer()
    addon = xbmcaddon.Addon()
    icon = addon.getAddonInfo('icon')
    show_notification( "Started script succesfully :) Now running", icon)
    xbmc.log("Started Lightcontroller", level=xbmc.LOGINFO)
    monitor = xbmc.Monitor()
    while((not monitor.abortRequested()) and player.lightcontroller.backgroundthreadalive()):
        monitor.waitForAbort(60)
    xbmc.log("LightController ",level=xbmc.LOGINFO)
    del player
    del monitor
    show_notification( "Stopped script succesfully :)", icon)
    del icon
    del addon
    xbmc.sleep(10)
    xbmc.log( "LightControll: LED Status: Script Stopped", level=xbmc.LOGINFO)

if __name__ == '__main__':
    script()

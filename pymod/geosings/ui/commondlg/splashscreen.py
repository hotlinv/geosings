#----------------------------------------------------------------------
# Name:        wxPython.lib.splashscreen
# Purpose:     A simple frame that can display a bitmap and closes itself
#              after a specified timeout or a mouse click.
#
# Author:      Mike Fletcher, Robin Dunn
#
# Created:     19-Nov-1999
# RCS-ID:      $Id: splashscreen.py,v 1.6 2004/05/02 02:41:24 RD Exp $
# Copyright:   (c) 1999 by Total Control Software
# Licence:     wxWindows license
#----------------------------------------------------------------------
# 12/11/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o 2.5 compatability update.
# o Untested.
#

"""
A Splash Screen implemented in Python.

NOTE: Now that wxWindows has a wxSplashScrren class and it is wrapped
in wxPython this class is deprecated.  See the docs for more details.
"""

import  warnings
import  wx

warningmsg = r"""\

#####################################################\
# THIS MODULE IS NOW DEPRECATED                      |
#                                                    |
# The core wx library now contains an implementation |
# of the 'real' wx.SpashScreen.                      |
#####################################################/

"""

#warnings.warn(warningmsg, DeprecationWarning, stacklevel=2)


#----------------------------------------------------------------------

class SplashScreen(wx.Frame):
    def __init__(self, parent, ID=-1, title="SplashScreen",
                 style=wx.SIMPLE_BORDER|wx.STAY_ON_TOP|
                 wx.FRAME_SHAPED|wx.FRAME_NO_TASKBAR,
                 duration=1500, bitmapfile="geosings.png",
                 callback = None):
        '''
        parent, ID, title, style -- see wx.Frame
        duration -- milliseconds to display the splash screen
        bitmapfile -- absolute or relative pathname to image file
        callback -- if specified, is called when timer completes, callback is
                    responsible for closing the splash screen
        '''
        ### Loading bitmap
        if type(bitmapfile)==str or \
            type(bitmapfile)==unicode:
            self.bitmap = bmp = wx.Image(bitmapfile, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        else:
            self.bitmap = bmp = bitmapfile

        ### Determine size of bitmap to size window...
        size = (bmp.GetWidth(), bmp.GetHeight())
        #self.hasShape = False



        # size of screen
        width = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_X)
        height = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_Y)
        pos = ((width-size[0])/2, (height-size[1])/2)

        # check for overflow...
        if pos[0] < 0:
            size = (wx.SystemSettings_GetSystemMetric(wx.SYS_SCREEN_X), size[1])
        if pos[1] < 0:
            size = (size[0], wx.SystemSettings_GetSystemMetric(wx.SYS_SCREEN_Y))

        wx.Frame.__init__(self, parent, ID, title, pos, size, style)

        if wx.Platform == "__WXGTK__":
            # wxGTK requires that the window be created before you can
            # set its shape, so delay the call to SetWindowShape until
            # this event.
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)
        else:
            # On wxMSW and wxMac the window has already been created, so go for it.
            self.SetWindowShape()

        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseClick)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBG)

        self.Show(True)


        class SplashTimer(wx.Timer):
            def __init__(self, targetFunction):
                self.Notify = targetFunction
                wx.Timer.__init__(self)

        if callback is None:
            callback = self.OnSplashExitDefault

        self.timer = SplashTimer(callback)
        self.timer.Start(duration, 1) # one-shot only

    def SetWindowShape(self, evt=None):
        r = wx.RegionFromBitmap(self.bitmap)
        self.hasShape = self.SetShape(r)
        

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap, 0,0, False)

    def OnEraseBG(self, event):
        pass

    def OnSplashExitDefault(self, event=None):
        self.Close(True)

    def OnCloseWindow(self, event=None):
        self.Show(False)
        try:
            self.timer.Stop()
            del self.timer
        except:
            pass
        self.Destroy()

    def OnMouseClick(self, event):
        self.timer.Notify()

#----------------------------------------------------------------------


if __name__ == "__main__":
    class DemoApp(wx.App):
        def OnInit(self):
            wx.InitAllImageHandlers()
            #self.frame = wx.Frame(None,-1,"a")
            self.splash = SplashScreen(None,
                    bitmapfile="../image/toucan.png",
                    callback=None)
            self.splash.Show(True)
            self.SetTopWindow(self.splash)
            return True
        def OnSplashExit(self, event=None):
            print "Yay! Application callback worked!"
            self.splash.Close(True)
            del self.splash
            ### Build working windows here...
    def test(sceneGraph=None):
        app = DemoApp(0)
        app.MainLoop()
    test()

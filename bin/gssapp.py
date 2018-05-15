
import wx,Image
from geosings.ui.core.MainImage import GetSplashBitmap

from geosings.ui.commondlg.splashscreen import SplashScreen

class MySplashScreen(SplashScreen):
    def __init__(self):
        bmp = GetSplashBitmap()
        SplashScreen.__init__(self, None, bitmapfile = bmp,
                                 style=wx.FRAME_SHAPED|wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                 duration=2000, callback=None, ID=-1)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.FutureCall(10, self.ShowMain)

    def OnClose(self, evt=None):
        # Make sure the default handler runs too so this window gets
        # destroyed
        #print "SplashScreen Close"
        if evt is not None:
            evt.Skip()
        self.Hide()
        
        # if the timer is still running then go ahead and show the
        # main frame now
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()


    def ShowMain(self):
        from geosings.ui.PyMainFrame import MainFrame
        from geosings.core.system.DefConf import GSSHOME,DOCHOME,BINHOME
        print "$HOME =",GSSHOME,'; $DOCHOME =',DOCHOME,
        print "; $BINHOME =", BINHOME
        mainframe = MainFrame(None, -1, "")
        mainframe.Show()
        if self.fc.IsRunning():
            self.Raise()
        self.Close(True)
        

class MyApp(wx.App):
    def OnInit(self):
        """
        Create and show the splash screen.  It will then create and show
        the main frame when it is time to do so.
        """

        #wx.SystemOptions.SetOptionInt("mac.window-plain-transition", 1)

        # For debugging
        #self.SetAssertMode(wx.PYAPP_ASSERT_DIALOG)

        # Normally when using a SplashScreen you would create it, show
        # it and then continue on with the applicaiton's
        # initialization, finally creating and showing the main
        # application window(s).  In this case we have nothing else to
        # do so we'll delay showing the main frame until later (see
        # ShowMain above) so the users can see the SplashScreen effect.        
        splash = MySplashScreen()
        splash.Show()

        import os
        from geosings.core.system.DefConf import GSSHOME
        p = os.path.join(GSSHOME,'pymod','geosings',"core",'CherryWebSite.py')
        if os.name=='nt':
            print os.system("start "+p)
        else:
            execstr = "xterm -e python %s &" % p
            print execstr
            print os.system(execstr)

        return True



#---------------------------------------------------------------------------

import sys
if __name__=="__main__":
    if len(sys.argv)==1:
        # run main application
        app = MyApp(False)
        app.MainLoop()
    elif sys.argv[1].lower()=="tools" or \
            sys.argv[1].lower()=="lin":
        # run tools
        from geosings.core.system.DefConf import GSSHOME,DOCHOME,BINHOME
        print "$HOME =",GSSHOME,'; $DOCHOME =',DOCHOME,
        print "; $BINHOME =", BINHOME
        from geosings.tools.gsstoolsapp import run
        run()
